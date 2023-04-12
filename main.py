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
def load_user(id):
    with Database() as database:
        admin = database.get_admin(id)
        if admin:
            return Admin(*admin[0]) #Indeks fordi databasen bruker fetchall()
        bruker = database.get_bruker(id)
        if bruker:
            return Bruker(*bruker[0]) #Indeks fordi databasen bruker fetchall()
    return None


@app.route("/")
def start():
    return render_template("startside.html")


@app.route("/adminlogin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        #Legger til admin_ foran id for å skille mellom bruker og admin i db
        admin_id = "admin_" + request.form.get("admin_id")
        print(admin_id)
        admin = load_user(admin_id)
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


@app.route("/adminregistrering", methods=["GET", "POST"])
def admin_register():
    if request.method == "POST":
        admin_id = "admin_" + request.form.get("admin_id")
        admin_fornavn = request.form.get("fornavn")
        admin_etternavn = request.form.get("etternavn")
        with Database() as database:
            database.insert(
                f"""
                INSERT INTO Admin (idAdmin, fornavn, etternavn) 
                VALUES ('{admin_id}', '{admin_fornavn}', '{admin_etternavn}')
                """
            )
        return redirect(url_for('admin_login'))
    
    return render_template("adminregistrering.html")


@app.route("/brukerlogin", methods=["GET", "POST"])
def bruker_login():
    if request.method == "POST":
        #Legger til bruker_ foran id for å skille mellom bruker og admin i db
        bruker_id = "bruker_" + request.form.get("bruker_id")
        bruker = load_user(bruker_id)
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