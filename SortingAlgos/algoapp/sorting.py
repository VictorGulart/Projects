from flask import render_template, redirect, url_for, flash, Blueprint

bp = Blueprint('sorting', __name__)


@bp.route('/bubblesort')
def bubblesort():
    return render_template('sorting/bubblesort.html')


@bp.route('/selectionsort')
def selectionsort():
    return render_template('sorting/selectionsort.html')