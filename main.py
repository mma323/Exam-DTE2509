from flask import (
    Flask, render_template, request, redirect, url_for, session
)
from flask_login import (
    LoginManager, login_required, login_user, logout_user, current_user
)
from flask_wtf.csrf import CSRFProtect
from werkzeug.routing import BaseConverter
from werkzeug.security import generate_password_hash, check_password_hash
from Database import Database
from Admin import Admin
from Bruker import Bruker
import os
from functools import wraps


app = Flask(__name__,
            static_folder='static',
            template_folder='templates')


app.secret_key = os.urandom(24)
app.config['SECRET_KEY'] = app.secret_key

csrf = CSRFProtect(app)

login_manager = LoginManager(app)
login_manager.login_view = "start"  # Ønsket side ved login_required
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    with Database() as database:
        admin = database.get_admin(id)
        # Vil kun finnes i admintabellen hvis admin_ er prefiks
        if admin:
            return Admin(*admin[0])  # Indeks fordi databasen bruker fetchall()
        bruker = database.get_bruker(id)
        # Vil kun finnes i brukertabellen hvis bruker_ er prefiks
        if bruker:
            # Indeks fordi databasen bruker fetchall()
            return Bruker(*bruker[0])
    return None


# Annoterer for å hindre at innlogget bruker kan gå til admin-sider,
# i tillegg til login_required
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if isinstance(current_user, Admin):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('admin_login'))
    return wrapper


# Annoterer for å hindre at innlogget admin kan gå til bruker-sider,
# i tillegg til login_required
def bruker_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if isinstance(current_user, Bruker):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('bruker_login'))
    return wrapper


@app.route("/")
def start():
    return render_template("startside.html")


@app.route("/adminlogin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        # Legger til admin_ foran id for å skille mellom bruker og admin i db
        admin_id = "admin_" + request.form.get("admin_id")
        password = request.form.get("password")
        admin = load_user(admin_id)

        if admin is not None and check_password_hash(
            admin.password_hash, password
        ):
            login_user(admin)
            session["admin_fornavn"] = admin.fornavn
            session["admin_etternavn"] = admin.etternavn
            return redirect(url_for("admin_dashboard"))
        else:
            error_message = "Invalid admin ID or password."
            return render_template(
                "adminlogin.html", error_message=error_message
            )

    return render_template("adminlogin.html")


@app.route("/admindashboard")
@login_required
@admin_required
def admin_dashboard():
    if isinstance(current_user, Admin):
        return render_template(
            "admindashboard.html", 
            fornavn=session["admin_fornavn"], 
            etternavn=session["admin_etternavn"]
        )
    else:
        return redirect(url_for('admin_login'))


@app.route("/adminregistrering", methods=["GET", "POST"])
def admin_register():
    if request.method == "POST":
        admin_id = "admin_" + request.form.get("admin_id")
        admin_fornavn = request.form.get("fornavn")
        admin_etternavn = request.form.get("etternavn")
        password = request.form.get("password")
        password_repeat = request.form.get("password_repeat")

        if password == password_repeat:
            admin_password_hash = generate_password_hash(password)
            with Database() as database:
                database.insert_admin(
                    admin_id, 
                    admin_fornavn, 
                    admin_etternavn, 
                    admin_password_hash
                    )
            return redirect(url_for('admin_login'))
        else:
            error_message = "Passordene er ikke like."
            return render_template(
                "adminregistrering.html", error_message=error_message
            )

    return render_template("adminregistrering.html")


@app.route("/brukerlogin", methods=["GET", "POST"])
def bruker_login():
    if request.method == "POST":
        # Legger til bruker_ foran id for å skille mellom bruker og admin
        bruker_id = "bruker_" + request.form.get("bruker_id")
        bruker = load_user(bruker_id)
        if bruker is not None:
            login_user(bruker)
            return redirect(url_for("bruker_dashboard"))

    return render_template("brukerlogin.html")


@app.route("/brukerdashboard")
@login_required
@bruker_required
def bruker_dashboard():
    if isinstance(current_user, Bruker):
        with Database() as database:
            quizzer = database.get_quizzer()
        return render_template("brukerdashboard.html", quizzer=quizzer)
    else:
        return redirect(url_for('bruker_login'))


# For å kunne sende quiz-objektet som parameter i URL
class QuizConverter(BaseConverter):
    def to_python(self, value):
        with Database() as database:
            quiz = database.get_quiz(int(value))
            sporsmal_liste = database.get_sporsmal()
            svar_liste = database.get_svar()

            for sporsmal in sporsmal_liste:
                if quiz.id_quiz == sporsmal.id_quiz:
                    quiz.sporsmal.append(sporsmal)
                    for svar in svar_liste:
                        if sporsmal.id_sporsmal == svar.id_sporsmal:
                            sporsmal.svar.append(svar)
            return quiz

    def to_url(self, value):
        return str(value.id_quiz)


app.url_map.converters['Quiz'] = QuizConverter


@app.route("/quiz/<int:quiz_id>", methods=["GET", "POST"])
@login_required
@bruker_required
def quiz(quiz_id):
    with Database() as database:
        quiz = database.get_quiz(quiz_id)
        sporsmal_liste = database.get_sporsmal()
        svar_liste = database.get_svar()

        for sporsmal in sporsmal_liste:
            if quiz.id_quiz == sporsmal.id_quiz:
                sporsmal.svar = []
                for svar in svar_liste:
                    if (
                        sporsmal.id_sporsmal == svar.id_sporsmal
                        and quiz.id_quiz == svar.id_quiz
                    ):
                        sporsmal.svar.append(svar)
                quiz.sporsmal.append(sporsmal)

    if request.method == "POST":
        try:
            for sporsmal in quiz.sporsmal:

                with Database() as database:
                    bruker_has_svar = database.get_bruker_has_svar(
                        current_user.bruker_id, 
                        quiz.id_quiz, 
                        sporsmal.id_sporsmal
                    )
                    if sporsmal.sporsmalstype == 1:
                        valgt_svar_id = request.form.get(
                            f"sporsmal{sporsmal.id_sporsmal}")
                        if bruker_has_svar == 0:
                            database.insert_bruker_has_svar(
                                current_user.bruker_id, 
                                quiz.id_quiz, 
                                sporsmal.id_sporsmal, 
                                valgt_svar_id
                            )
                        else:
                            database.update_bruker_has_svar(
                                current_user.bruker_id, 
                                quiz.id_quiz, 
                                sporsmal.id_sporsmal, 
                                valgt_svar_id
                            )
                    if sporsmal.sporsmalstype == 2:
                        if bruker_has_svar == 0:
                            database.insert_svar(quiz.id_quiz, 
                                                sporsmal.id_sporsmal, 
                                                1, 
                                                request.form.get(
                                                     f"sporsmal{sporsmal.id_sporsmal}"
                                                )
                            )
                            database.insert_bruker_has_svar(
                                current_user.bruker_id, 
                                quiz.id_quiz, 
                                sporsmal.id_sporsmal, 
                                1
                            )
                        else:
                            database.update_bruker_has_svar(
                                current_user.bruker_id, 
                                quiz.id_quiz, 
                                sporsmal.id_sporsmal, 
                                1
                            )

            with Database() as database:
                bruker_has_quiz = database.get_bruker_has_quiz(
                    current_user.bruker_id, quiz.id_quiz)
                if bruker_has_quiz == 0:
                    database.insert_quiz_gjennomforing(
                        current_user.bruker_id, quiz.id_quiz)
            return redirect(url_for("quiz_result", quiz=quiz))
        except:
            print("Allerede gjennomført quiz")
            return redirect(url_for("bruker_dashboard", quiz=quiz))

    return render_template("quiz.html", quiz=quiz)


@app.route('/quiz_result/<Quiz:quiz>/')
@login_required
@bruker_required
def quiz_result(quiz):
    return render_template('quiz_result.html', quiz=quiz)


@app.route("/brukerregistrering", methods=["GET", "POST"])
def bruker_register():
    if request.method == "POST":
        bruker_id = "bruker_" + request.form.get("bruker_id")
        with Database() as database:
            database.insert_bruker(bruker_id)
        return redirect(url_for('bruker_login'))

    return render_template("brukerregistrering.html")


@app.route("/logout")
@login_required
def logout():
    if session.get("admin_fornavn"):
        session.pop("admin_fornavn", None)
    if session.get("admin_etternavn"):
        session.pop("admin_etternavn", None)

    logout_user()
    return redirect(url_for('start'))


@app.route("/quizzer", methods=["GET", "POST"])
@login_required
@admin_required
def quiz_oversikt():
    with Database() as database:
        quizzer = database.get_quizzer()
        quizzer.reverse()  # Reverserer for å få nyeste øverst
        sporsmal_liste = database.get_sporsmal()
        temaer = database.get_temaer()

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

    return render_template("quizzer.html", quizzes=quizzer, temaer=temaer)


@app.route("/quiz/create", methods=["GET", "POST"])
@login_required
@admin_required
def quiz_create():
    if request.method == "POST":
        quiz_navn = request.form.get("quiz_navn")
        with Database() as database:
            database.insert_quiz(quiz_navn)
        return redirect(url_for('quiz_oversikt'))


@app.route("/quiz/delete", methods=["GET", "POST"])
@login_required
@admin_required
def quiz_delete():
    if request.method == "POST":
        quiz_id = request.form.get("quiz")
        with Database() as database:
            database.delete_quiz(quiz_id)
        return redirect(url_for('quiz_oversikt'))


@app.route("/quiz/sporsmal/create", methods=["GET", "POST"])
@login_required
@admin_required
def sporsmal_create():
    if request.method == "POST":
        quiz_id = request.form.get("quiz_id")
        sporsmal_id = request.form.get("sporsmal_nummer")
        sporsmal_tekst = request.form.get("sporsmal_tekst")
        tema_id = request.form.get("sporsmal_tema")
        sporsmal_type = request.form.get("sporsmal_type")
        with Database() as database:
            if sporsmal_type == "flervalg":
                database.insert_sporsmal(
                    quiz_id, 
                    sporsmal_id, 
                    sporsmal_tekst, 
                    tema_id, 
                    sporsmal_type
                )
                svar = ["svar1", "svar2", "svar3", "svar4"]
                for index, svar in enumerate(svar):
                    database.insert_svar(
                        quiz_id, sporsmal_id, index+1, request.form.get(svar)
                    )
            if sporsmal_type == "essay":
                database.insert_sporsmal(
                    quiz_id, 
                    sporsmal_id, 
                    sporsmal_tekst, 
                    tema_id, 
                    sporsmal_type
                )

        return redirect(url_for('quiz_oversikt'))


@app.route("/quiz/sporsmal/edit/<sporsmal_id>", methods=["GET", "POST"])
@login_required
@admin_required
def sporsmal_edit(sporsmal_id):
    if request.method == "POST":
        quiz_id = request.form.get("quiz_id")
        sporsmal_tekst = request.form.get("sporsmal_tekst")
        sporsmal_tema = request.form.get("sporsmal_tema")
        with Database() as database:
            database.update_sporsmal(
                quiz_id, sporsmal_id, sporsmal_tekst, sporsmal_tema)
            svar_id_list = request.form.getlist("svar_id")
            svar_tekst_list = request.form.getlist("svar_tekst")

            for index, svar_id in enumerate(svar_id_list):
                svar_tekst = svar_tekst_list[index]
                database.update_svar(quiz_id, sporsmal_id, svar_id, svar_tekst)

        return redirect(url_for('quiz_oversikt'))


@app.route(
        "/quiz/sporsmal/delete/<quiz_id>/<sporsmal_id>", 
        methods=["GET", "POST"]
)
@login_required
@admin_required
def sporsmal_delete(quiz_id, sporsmal_id):
    with Database() as database:
        database.delete_svar(sporsmal_id)
        database.delete_sporsmal(quiz_id, sporsmal_id)

    return redirect(url_for('quiz_oversikt'))


@app.route("/tema/create", methods=["GET", "POST"])
@login_required
@admin_required
def tema_create():
    if request.method == "POST":
        tema_navn = request.form.get("tema_navn")
        with Database() as database:
            database.insert_tema(tema_navn)
        return redirect(url_for('quiz_oversikt'))


@app.route("/brukersvar", methods=["GET", "POST"])
@login_required
@admin_required
def bruker_svar():
    with Database() as database:
        quiz_gjennomforinger = database.get_quiz_gjennomforinger()
    return render_template(
        "brukersvar.html", quiz_gjennomforinger=quiz_gjennomforinger
    )


@app.route("/quizgjennomgang/<bruker_id>/<quiz_id>", methods=["GET", "POST"])
@login_required
@admin_required
def quiz_gjennomgang(bruker_id, quiz_id):
    with Database() as database:
        quiz = database.get_quiz(quiz_id)
        sporsmal_liste = database.get_sporsmal()
        svar_liste = database.get_svar()
        bruker_svar_dictionary = {}
        bruker_quiz_relasjon = database.get_bruker_quiz_relasjon(
            bruker_id, quiz_id)

        for sporsmal in sporsmal_liste:
            if int(sporsmal.id_quiz) == int(quiz_id):
                quiz.sporsmal.append(sporsmal)
                bruker_svar = database.get_bruker_svar_to_sporsmal(
                    bruker_id, quiz_id, sporsmal.id_sporsmal)
                bruker_svar_dictionary[sporsmal.id_sporsmal] = bruker_svar
            for svar in svar_liste:
                if (
                    (svar.id_sporsmal == sporsmal.id_sporsmal) and
                    (svar.id_quiz == sporsmal.id_quiz)
                ):
                    sporsmal.svar.append(svar)

    if request.method == "POST":
        with Database() as database:
            database.kommenter_quiz(
                quiz_id, bruker_id, request.form.get("kommentar_quiz"))
            for sporsmal in quiz.sporsmal:
                riktig = request.form.get(f"riktig{sporsmal.id_sporsmal}")

                if riktig == "riktig":
                    database.evaluer_svar(
                        bruker_id, quiz_id, sporsmal.id_sporsmal, 1)
                if riktig == "ikke-riktig":
                    database.evaluer_svar(
                        bruker_id, quiz_id, sporsmal.id_sporsmal, 0)
                kommentar = request.form.get(
                    f"kommentar{sporsmal.id_sporsmal}")
                database.kommenter_sporsmal(
                    bruker_id, quiz_id, sporsmal.id_sporsmal, kommentar)

        return redirect(url_for('bruker_svar'))

    return render_template(
        "quizgjennomgang.html", 
        quiz=quiz, 
        bruker_svar_dictionary=bruker_svar_dictionary, 
        bruker_id=bruker_id, 
        bruker_quiz_relasjon=bruker_quiz_relasjon
    )


@app.route(
        "/quizgjennomgang/delete/<bruker_id>/<quiz_id>", 
        methods=["GET", "POST"]
)
@login_required
@admin_required
def quiz_gjennomgang_delete(bruker_id, quiz_id):
    with Database() as database:
        database.delete_bruker_quiz_relasjon(bruker_id, quiz_id)
    return redirect(url_for('bruker_svar'))


@app.route(
        "/quizgjennomgang/delete/<bruker_id>/<quiz_id>/<sporsmal_id>", 
        methods=["GET", "POST"]
)
@login_required
@admin_required
def delete_bruker_svar_to_sporsmal(bruker_id, quiz_id, sporsmal_id):
    with Database() as database:
        database.delete_bruker_svar_to_sporsmal(
            bruker_id, quiz_id, sporsmal_id)
    return redirect(
        url_for('quiz_gjennomgang', bruker_id=bruker_id, quiz_id=quiz_id)
        )


if __name__ == "__main__":
    app.run(debug=True)