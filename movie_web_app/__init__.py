from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker
from sqlalchemy.pool import NullPool

from movie_web_app.adapters import Movie_repo, database_repository
# from movie_web_app.adapters.Movie_repo import MovieRepo, populate
from movie_web_app.adapters.orm import metadata, map_model_to_tables
# from movie_web_app.datafilereaders.movie_file_csv_reader import MovieFileCSVReader
import movie_web_app.adapters.repository as repo


def create_app(test_config=None):
    # Create the Flask app object.
    app = Flask(__name__)

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = "movie_web_app/datafilereaders"

    if test_config is not None:
        # Load test configuration, and overrride any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    if app.config['REPOSITORY'] == 'memory':
        # Create the MemoryRepository instance for a memory-based repository.
        repo.repo_instance = Movie_repo.MovieRepo()
        Movie_repo.populate(data_path, repo.repo_instance)

    elif app.config['REPOSITORY'] == 'database':
        # Configure database.
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']

        # We create a comparatively simple SQLite database, which is based on a single file (see .env for URI).
        # For example the file database could be located locally and relative to the application in covid-19.db,
        # leading to a URI of "sqlite:///covid-19.db".
        # Note that create_engine does not establish any actual DB connection directly!
        database_echo = app.config['SQLALCHEMY_ECHO']
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                        echo=database_echo)

        if app.config['TESTING'] == 'True' or len(database_engine.table_names()) == 0:
            print("REPOPULATING DATABASE")
            # For testing, or first-time use of the web application, reinitialise the database.
            clear_mappers()
            metadata.create_all(database_engine)  # Conditionally create database tables.
            for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
                database_engine.execute(table.delete())

            # Generate mappings that map domain model classes to the database tables.
            map_model_to_tables()
            datafile = 'Data1000Movies.csv'
            session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
            database_repository.populate_data(session_factory,  data_path, datafile)
            database_repository.populate_user(database_engine, data_path)

        else:
            # Solely generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

        # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
        repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)

    with app.app_context():
        # Register blueprints.
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .movie import movie_page
        app.register_blueprint(movie_page.movies_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from .utilities import utilities
        app.register_blueprint(utilities.utilities_blueprint)

        # Register a callback the makes sure that database sessions are associated with http requests
        # We reset the session inside the database repository before a new flask request is generated
        @app.before_request
        def before_flask_http_request_function():
            if isinstance(repo.repo_instance, database_repository.SqlAlchemyRepository):
                repo.repo_instance.reset_session()

        # Register a tear-down method that will be called after each request has been processed.
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            if isinstance(repo.repo_instance, database_repository.SqlAlchemyRepository):
                repo.repo_instance.close_session()
    return app
