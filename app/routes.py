from app import app, db
from app.forms import InputForm, GridForm, SubmitForm
from flask import render_template, flash, redirect, url_for, request, session
from app.solver import solve
from app.models import Puzzles
from  sqlalchemy.sql.expression import func, select

@app.route('/solution', methods=['GET', 'POST'])
def solution():
    return render_template(
        'display.html',
        puzzle=session['solved_puzzle'],
        title_name = 'Solved Puzzle',
        sudoku_name = 'Solved Sudoku',
        button_text = 'Go home',
        redirect_link = url_for('index'))

@app.route('/custom', methods=['GET', 'POST'])
def custom():
    form_grid = GridForm()

    if form_grid.submit.data and form_grid.validate_on_submit():
        puzzle = ''
        for i in form_grid.square:
            if len(i.data) < 1:
                new = '.'
            else:
                if int(i.data) < 1 or int(i.data) > 9:
                    session['solved_puzzle'] = None
                    return redirect(url_for('solution'))
                new = i.data
            puzzle = puzzle + new
        session['solved_puzzle'] = solve(puzzle)
        return redirect(url_for('solution'))

    return render_template('custom.html', form_grid=form_grid)

@app.route('/random', methods=['GET', 'POST'])
def random():
    query = db.session.query(Puzzles)
    current_data = query.order_by(func.random()).first()
    current_puzzle = current_data.puzzle
    current_difficulty = current_data.difficulty
    session['solved_puzzle'] = solve(current_puzzle)
    return render_template(
        'display.html',
        puzzle=current_puzzle,
        title_name = 'Random Puzzle',
        sudoku_name = 'Random Sudoku',
        button_text = 'Solve',
        redirect_link = url_for('solution'))

@app.route('/browse', methods=['GET', 'POST'])
def browse():
    form = SubmitForm()
    puzzles = db.session.query(Puzzles).all()
    if 'action' in request.form:
        session['solved_puzzle'] = solve(request.form['action'])
        return redirect(url_for('solution'))
    return render_template(
        'browse.html',
        puzzles=[(i.puzzle, i.difficulty) for i in puzzles], form=form)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


