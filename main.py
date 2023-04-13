from flask import (
    Flask, render_template, request, redirect, url_for
)
from flask_login import (
    LoginManager, login_required, login_user, logout_user, current_user
)
from Database import Database
from Admin import Admin
from Bruker import Bruker
import os


app = Flask(__name__,
    static_folder='static',
    template_folder='templates')


app.secret_key = os.urandom(24)


login_manager = LoginManager(app)
login_manager.login_view = "start" #Ønsket side ved login_required
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    with Database() as database:
        admin = database.get_admin(id)
        #Vil kun finnes i admintabellen hvis admin_ er prefiks
        if admin:
            return Admin(*admin[0]) #Indeks fordi databasen bruker fetchall()
        bruker = database.get_bruker(id)
        #Vil kun finnes i brukertabellen hvis bruker_ er prefiks
        if bruker:
            return Bruker(*bruker[0]) #Indeks fordi databasen bruker fetchall()
    return None


@app.route("/")
def start():
    return render_template("startside.html")


@app.route("/adminlogin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        #Legger til admin_ foran id for å skille mellom bruker og admin
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
        #Legger til bruker_ foran id for å skille mellom bruker og admin
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
    

@app.route("/brukerregistrering", methods=["GET", "POST"])
def bruker_register():
    if request.method == "POST":
        bruker_id = "bruker_" + request.form.get("bruker_id")
        with Database() as database:
            database.insert(
                f"INSERT INTO Bruker (idBruker) VALUES ('{bruker_id}')"
            )
        return redirect(url_for('bruker_login'))
    
    return render_template("brukerregistrering.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('start'))


@app.route("/quizzer", methods=["GET", "POST"])
@login_required
def quiz_oversikt():
    with Database() as database:
        quizzer = database.get_quizzer()
        quizzer.reverse() #Reverserer for å få nyeste øverst
        sporsmal_liste = database.get_sporsmal()
        
        for quiz in quizzer:
            for sporsmal in sporsmal_liste:
                if quiz.id_quiz == sporsmal.id_quiz:
                    quiz.sporsmal.append(sporsmal)

        svar_liste = database.get_svar()
        for svar in svar_liste:
            for sporsmal in sporsmal_liste:
                if (
                    (svar.id_sporsmal == sporsmal.id_sporsmal) and 
                    (svar.id_quiz == sporsmal.id_quiz)
                ):  
                    sporsmal.svar.append(svar)  
    return render_template("quizzer.html", quizzes=quizzer)


@app.route("/quiz/create", methods=["GET", "POST"])
@login_required
def quiz_create():
    if request.method == "POST":
        quiz_navn = request.form.get("quiz_navn")
        with Database() as database:
            database.insert(
                f"INSERT INTO Quiz (navn) VALUES ('{quiz_navn}')"
            )
        return redirect(url_for('quiz_oversikt'))


@app.route("/quiz/delete", methods=["GET", "POST"])
@login_required
def quiz_delete():
    if request.method == "POST":
        quiz_id = request.form.get("quiz")
        with Database() as database:
            database.insert(
                f"DELETE FROM Quiz WHERE idQuiz = '{quiz_id}'"
            )
            database.insert(
                f"DELETE FROM Sporsmal WHERE idQuiz = '{quiz_id}'"
            )
            database.insert(
                f"DELETE FROM Svar WHERE idQuiz = '{quiz_id}'"
            )
        return redirect(url_for('quiz_oversikt'))


@app.route("/quiz/sporsmal/create", methods=["GET", "POST"])
@login_required
def sporsmal_create():
    if request.method == "POST":
        quiz_id = request.form.get("quiz_id")
        sporsmal_id = request.form.get("sporsmal_nummer")
        sporsmal_tekst = request.form.get("sporsmal_tekst")
        with Database() as database:
            
            database.insert(
                f"""
                INSERT INTO Sporsmal (Quiz_idQuiz, idSporsmal, Tekst, Tema_idTema) 
                VALUES ('{quiz_id}', '{sporsmal_id}', '{sporsmal_tekst}', '1') 
                """
            )
            svar = ["svar1", "svar2", "svar3", "svar4"]
            svar_riktig = request.form.get("riktig_svar")
            for index, svar in enumerate(svar):
                database.insert(
                    f"""
                    INSERT INTO Svar (Sporsmal_Quiz_idQuiz, Sporsmal_idSporsmal, idSvar, Tekst, isRiktig) 
                    VALUES ('{quiz_id}', '{sporsmal_id}', '{index+1}', '{request.form.get(svar)}', '{1 if svar_riktig == (index) else 0}') 
                    """
                )

        return redirect(url_for('quiz_oversikt'))


if __name__ == "__main__":
    app.run(debug=True)