from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class LoginForm(FlaskForm):
    """
    Form for user login.
    Requires email and password fields to be filled.
    """
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

class TransferForm(FlaskForm):
    """
    Form for transferring funds between accounts.
    Requires valid account IDs and an amount within the allowed range.
    """
    from_account = StringField("From Account", validators=[DataRequired()])
    to_account = StringField("To Account", validators=[DataRequired()])
    amount = IntegerField(
        "Amount",
        validators=[
            DataRequired(),
            NumberRange(min=1, max=1000, message="Transfer amount must be between 1 and 1000.")
        ]
    )
