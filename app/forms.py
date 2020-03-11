from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList, RadioField
from wtforms.validators import DataRequired, Length, NumberRange

class InputForm(FlaskForm):
    puzzle = StringField('Puzzle', validators=[DataRequired(), Length(min=81,max=81)])
    submit = SubmitField('Submit puzzle')

class GridForm(FlaskForm):
    square = FieldList(StringField('Squares'), min_entries=81, max_entries=81)
    submit = SubmitField('Submit puzzle')

class SubmitForm(FlaskForm):
    puzzle = RadioField('Puzzle')
    submit = SubmitField('Solve this puzzle')
