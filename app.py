from flask import Flask, request, make_response, redirect, render_template, g, abort
from flask_wtf.csrf import CSRFProtect
from genericforms import LoginForm, TransferForm

# Business logic for user authentication and account transactions
from bin.account_service import get_balance, do_transfer
from user_service import get_user_with_credentials, logged_in

app = Flask(__name__)

# Security configuration (⚠️ Use a secure secret in production)
app.config['SECRET_KEY'] = 'yoursupersecrettokenhere'
app.config['WTF_CSRF_ENABLED'] = True

# Apply CSRF protection to all forms
csrf = CSRFProtect(app)

@app.route("/", methods=["GET"])
def home():
    """
    Home route:
    - If not logged in, present the login form.
    - If logged in, redirect to dashboard.
    """
    if not logged_in():
        return render_template("login.html", form=LoginForm())
    return redirect("/dashboard")

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Login route:
    - GET: Display the login form.
    - POST: Validate credentials and issue auth token on success.
    """
    form = LoginForm()

    if request.method == "GET":
        return render_template("login.html", form=form)

    if not form.validate_on_submit():
        return render_template("login.html", form=form, error="Invalid submission")

    email = form.email.data
    password = form.password.data
    user = get_user_with_credentials(email, password)

    if not user:
        return render_template("login.html", form=form, error="Invalid credentials")

    # Issue JWT in cookie and redirect
    response = make_response(redirect("/dashboard"))
    response.set_cookie("auth_token", user["token"], httponly=True, secure=True, samesite='Strict')
    return response, 303

@app.route("/dashboard", methods=["GET"])
def dashboard():
    """
    Dashboard route:
    - Protected view showing user email.
    """
    if not logged_in():
        return render_template("login.html", form=LoginForm())
    return render_template("dashboard.html", email=g.user)

@app.route("/details", methods=["GET"])
def details():
    """
    Account details route:
    - Requires login.
    - Displays balance for a specific account.
    """
    if not logged_in():
        return render_template("login.html", form=LoginForm())

    account_number = request.args.get("account")
    balance = get_balance(account_number, g.user)

    return render_template(
        "details.html",
        user=g.user,
        account_number=account_number,
        balance=balance
    )

@app.route("/transfer", methods=["GET", "POST"])
def transfer():
    """
    Transfer route:
    - GET: Show the transfer form.
    - POST: Validate and process a money transfer.
    """
    form = TransferForm()

    if request.method == "GET":
        return render_template("transfer.html", form=form)

    if not logged_in():
        return render_template("login.html", form=LoginForm())

    if not form.validate_on_submit():
        return render_template("transfer.html", form=form, error="Invalid input or CSRF token missing", success="Transfer completed!")

    source = form.from_account.data
    target = form.to_account.data
    amount = form.amount.data

    available_balance = get_balance(source, g.user)

# User can only transfer from their own account
    if available_balance is None:
        return render_template("transfer.html", form=form, error="You can only transfer from your own account.")


    if amount > available_balance:
        abort(400, "Insufficient funds")

    if not do_transfer(source, target, amount):
        abort(400, "Transfer failed due to internal error")

    return render_template("transfer.html", form=TransferForm(), success="Transfer completed!")


@app.route("/logout", methods=["GET"])
def logout():
    """
    Logout route:
    - Clears the auth token and redirects to dashboard.
    """
    response = make_response(redirect("/dashboard"))
    response.delete_cookie("auth_token")
    return response, 303

if __name__ == "__main__":
    app.run(debug=True)
