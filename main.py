from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required, login_user, current_user
from Database import Database
from Admin import Admin
from Bruker import Bruker
import os


app = Flask(__name__,
    static_folder='static',
    template_folder='templates')

app.secret_key = os.urandom(24)


login_manager = LoginManager(app)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id, user_type="admin"):
    with Database() as database:
        if user_type == "admin":
            admin = Admin( *database.get_admin(id)[0] )
            return admin
        elif user_type == "bruker":
            bruker = Bruker( *database.get_bruker(id)[0] )
            return bruker


@app.route("/")
def start():
    return render_template("startside.html")


@app.route("/adminlogin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        admin_id = request.form.get("admin_id")
        admin = load_user(admin_id, "admin")
        if admin is not None:
            login_user(admin)
            return redirect( url_for("admin_dashboard") )
        
    return render_template("adminlogin.html")


@app.route("/admindashboard")
@login_required
def admin_dashboard():
    if isinstance(current_user, Admin):
        return render_template("admindashboard.html")
    else:
        return redirect(url_for('admin_login'))


@app.route("/adminregistrering")
def admin_register():
    return render_template("adminregistrering.html")


@app.route("/brukerlogin", methods=["GET", "POST"])
def bruker_login():
    if request.method == "POST":
        bruker_id = request.form.get("bruker_id")
        bruker = load_user(bruker_id, "bruker")
        if bruker is not None:
            login_user(bruker)
            return redirect( url_for("bruker_dashboard") )

    return render_template("brukerlogin.html")


@app.route("/brukerdashboard")
@login_required
def bruker_dashboard():
    if isinstance(current_user, Bruker):
        return render_template("brukerdashboard.html")
    else:
        return redirect(url_for('bruker_login'))
    

@app.route("/brukerregistrering")
def bruker_register():
    return render_template("brukerregistrering.html")


if __name__ == "__main__":
    app.run(debug=True)