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


bruker_login_manager = LoginManager()
bruker_login_manager.login_view = 'bruker_login'
bruker_login_manager.init_app(app)

admin_login_manager = LoginManager()
admin_login_manager.login_view = 'admin_login'
admin_login_manager.init_app(app)


@admin_login_manager.user_loader
def load_admin(admin_id):
    with Database() as database:
        admin = Admin( *database.get_admin(admin_id)[0] )
    return admin


@bruker_login_manager.user_loader
def load_bruker(bruker_id):
    with Database() as database:
        bruker = Bruker( *database.get_bruker(bruker_id)[0] )
    return bruker


@admin_login_manager.user_loader
def load_admin(admin_id):
    with Database() as database:
        admin = Admin( *database.get_admin(admin_id)[0] )
    return admin


@bruker_login_manager.user_loader
def load_bruker(bruker_id):
    with Database() as database:
        bruker = Bruker( *database.get_bruker(bruker_id)[0] )
    return bruker


@app.route("/")
def start():
    return render_template("startside.html")


@app.route("/adminlogin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        admin_id = request.form.get("admin_id")
        admin = load_admin(admin_id)
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
        bruker = load_bruker(bruker_id)
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