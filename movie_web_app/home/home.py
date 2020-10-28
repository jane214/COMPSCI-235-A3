from flask import Blueprint, render_template

import movie_web_app.utilities.utilities as utilities


home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template(
        'home/home.html',
        selected_movies=utilities.get_selected_movies(),
        genre_urls=utilities.get_genres_and_urls()
    )
