import mysql.connector
from Quiz import Quiz
from Sporsmal import Sporsmal
from Svar import Svar
from Tema import Tema
from BrukerHasSvar import BrukerHasSvar
from BrukerHasQuiz import BrukerHasQuiz


class Database:
    def __init__(self) -> None:
        dbconfig = {'host': '127.0.0.1',
                    'user': 'user',
                    'password': 'test',
                    'database': 'myDb', }
        self.configuration = dbconfig


    def __enter__(self) -> 'cursor':
        self.conn = mysql.connector.connect(**self.configuration)
        self.cursor = self.conn.cursor()
        return self


    def __exit__(self, exc_type, exc_val, exc_trace) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


    def query(self, sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result


    def insert(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()


    def get_admin(self, admin_id):
        sql = "SELECT * FROM Admin WHERE idAdmin = %s"
        values = (admin_id,)
        self.cursor.execute(sql, values)
        admin = self.cursor.fetchall()
        return admin


    def get_bruker(self, bruker_id):
        sql = "SELECT * FROM Bruker WHERE idBruker = %s"
        values = (bruker_id,)
        self.cursor.execute(sql, values)
        bruker = self.cursor.fetchall()
        return bruker


    def get_quizzer(self):
        sql = "SELECT * FROM Quiz"
        self.cursor.execute(sql)
        quizzer = self.cursor.fetchall()
        quizzer = [Quiz(*quiz) for quiz in quizzer]
        return quizzer


    def get_quiz(self, quiz_id):
        sql = "SELECT * FROM Quiz WHERE idQuiz = %s"
        values = (quiz_id,)
        self.cursor.execute(sql, values)
        quiz = self.cursor.fetchall()
        quiz = Quiz(*quiz[0])
        return quiz


    def get_sporsmal(self):
        sql = "SELECT * FROM Sporsmal"
        self.cursor.execute(sql)
        sporsmal = self.cursor.fetchall()
        sporsmal = [Sporsmal(*sporsmal) for sporsmal in sporsmal]
        return sporsmal


    def get_svar(self):
        sql = "SELECT * FROM Svar"
        self.cursor.execute(sql)
        svar = self.cursor.fetchall()
        svar = [Svar(*svar) for svar in svar]
        return svar


    def insert_admin(
            self, 
            admin_id, 
            admin_fornavn, 
            admin_etternavn, 
            password_hash
    ):
        sql = """
            INSERT INTO Admin (idAdmin, fornavn, etternavn, Passordhash) 
            VALUES (%s, %s, %s, %s)
        """
        values = (admin_id, admin_fornavn, admin_etternavn, password_hash)
        self.cursor.execute(sql, values)


    def get_bruker_has_svar(self, bruker_id, quiz_id, sporsmal_id):
        sql = """
            SELECT count(*) FROM Bruker_has_Svar
            WHERE Bruker_idBruker = %s 
            AND Svar_Sporsmal_Quiz_idQuiz = %s
            AND Svar_Sporsmal_idSporsmal = %s
        """
        values = (bruker_id, quiz_id, sporsmal_id)
        self.cursor.execute(sql, values)
        result = self.cursor.fetchall()
        return result[0][0]


    def insert_bruker_has_svar(self, bruker_id, quiz_id, sporsmal_id, svar_id):
        sql = """
                INSERT INTO Bruker_has_Svar (
                Bruker_idBruker, 
                Svar_Sporsmal_Quiz_idQuiz, 
                Svar_Sporsmal_idSporsmal,
                Svar_idSvar
                )
                VALUES (%s, %s, %s, %s)
        """
        values = (bruker_id, quiz_id, sporsmal_id, svar_id)
        self.cursor.execute(sql, values)


    def update_bruker_has_svar(self, bruker_id, quiz_id, sporsmal_id, svar_id):
        sql = """
            UPDATE Bruker_has_Svar
            SET Svar_idSvar = %s
            WHERE Bruker_idBruker = %s 
            AND Svar_Sporsmal_Quiz_idQuiz = %s
            AND Svar_Sporsmal_idSporsmal = %s
        """
        values = (svar_id, bruker_id, quiz_id, sporsmal_id)
        self.cursor.execute(sql, values)


    def insert_bruker(self, bruker_id):
        sql = """
            INSERT INTO Bruker (idBruker) 
            VALUES (%s)
        """
        values = (bruker_id,)
        self.cursor.execute(sql, values)


    def insert_quiz(self, quiz_navn):
        sql = """
            INSERT INTO Quiz (navn)
            VALUES (%s)
        """
        values = (quiz_navn,)
        self.cursor.execute(sql, values)


    def delete_quiz(self, quiz_id):
        sql = """
            DELETE FROM Quiz
            WHERE idQuiz = %s
        """
        values = (quiz_id,)
        self.cursor.execute(sql, values)


    def insert_sporsmal(
            self, quiz_id, sporsmal_id, sporsmal_tekst, id_tema, sporsmalstype
    ):
        if sporsmalstype == "flervalg":
            sql = """
                INSERT INTO Sporsmal (
                Quiz_idQuiz, 
                idSporsmal, 
                tekst, 
                Tema_idTema, 
                Sporsmalstype_idSporsmalstype
                )
                VALUES (%s, %s, %s, %s, 1)
            """
            values = (quiz_id, sporsmal_id, sporsmal_tekst, id_tema)
            self.cursor.execute(sql, values)
        if sporsmalstype == "essay":
            sql = """
                INSERT INTO Sporsmal (
                Quiz_idQuiz, 
                idSporsmal, 
                tekst, 
                Tema_idTema, 
                Sporsmalstype_idSporsmalstype
                )
                VALUES (%s, %s, %s, %s, 2)
            """
            values = (quiz_id, sporsmal_id, sporsmal_tekst, id_tema)
            self.cursor.execute(sql, values)


    def insert_svar(self, quiz_id, sporsmal_id, svar_id, svar_tekst):
        sql = """
            INSERT INTO Svar (
            Sporsmal_Quiz_idQuiz, Sporsmal_idSporsmal, idSvar, Tekst
            )
            VALUES (%s, %s, %s, %s)
        """
        values = (quiz_id, sporsmal_id, svar_id, svar_tekst)
        self.cursor.execute(sql, values)


    def update_sporsmal(self, quiz_id, sporsmal_id, sporsmal_tekst, id_tema):
        sql = """
            UPDATE Sporsmal
            SET tekst = %s, Tema_idTema = %s
            WHERE Quiz_idQuiz = %s
            AND idSporsmal = %s
        """
        values = (sporsmal_tekst, id_tema, quiz_id, sporsmal_id)
        self.cursor.execute(sql, values)


    def update_svar(self, quiz_id, sporsmal_id, svar_id, svar_tekst):
        sql = """
            UPDATE Svar
            SET Tekst = %s
            WHERE Sporsmal_Quiz_idQuiz = %s
            AND Sporsmal_idSporsmal = %s
            AND idSvar = %s
        """
        values = (svar_tekst, quiz_id, sporsmal_id, svar_id)
        self.cursor.execute(sql, values)


    def delete_svar(self, sporsmal_id):
        sql = """
            DELETE FROM Svar
            WHERE Sporsmal_idSporsmal = %s
        """
        values = (sporsmal_id,)
        self.cursor.execute(sql, values)


    def delete_sporsmal(self, quiz_id, sporsmal_id):
        sql = """
            DELETE FROM Sporsmal
            WHERE idSporsmal = %s
            AND Quiz_idQuiz = %s
        """
        values = (sporsmal_id, quiz_id)
        self.cursor.execute(sql, values)


    def get_bruker_svar(self):
        sql = """
            SELECT 
            Bruker_has_Svar.Bruker_idBruker, 
            Quiz.navn, 
            Sporsmal.Tekst, 
            Svar.Tekst
            FROM Bruker_has_Svar, Quiz, Sporsmal, Svar
            WHERE Bruker_has_Svar.Svar_Sporsmal_Quiz_idQuiz = Quiz.idQuiz
            AND Bruker_has_Svar.Svar_Sporsmal_idSporsmal = Sporsmal.idSporsmal
            AND Bruker_has_Svar.Svar_idSvar = Svar.idSvar
            ORDER BY Sporsmal.Tekst;
        """
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result


    def insert_tema(self, navn):
        sql = """
            INSERT INTO Tema (navn)
            VALUES (%s)
        """
        values = (navn,)
        self.cursor.execute(sql, values)


    def get_temaer(self):
        sql = """
            SELECT * FROM Tema
        """
        self.cursor.execute(sql)
        temaer = self.cursor.fetchall()
        temaer = [Tema(*tema) for tema in temaer]
        return temaer


    def insert_quiz_gjennomforing(self, bruker_id, quiz_id):
        sql = """
            INSERT INTO  Bruker_has_Quiz(Bruker_idBruker, Quiz_idQuiz)
            VALUES (%s, %s)
        """
        values = (bruker_id, quiz_id)
        self.cursor.execute(sql, values)


    def get_bruker_has_quiz(self, bruker_id, quiz_id):
        sql = """
            SELECT count(*) FROM Bruker_has_Quiz
            WHERE Bruker_idBruker = %s
            AND Quiz_idQuiz = %s
        """
        values = (bruker_id, quiz_id)
        self.cursor.execute(sql, values)
        result = self.cursor.fetchone()
        return result[0]


    def get_quiz_gjennomforinger(self):
        sql = """
            SELECT * FROM Bruker_has_Quiz
        """
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result


    def get_bruker_svar_to_sporsmal(self, bruker_id, quiz_id, sporsmal_id):
        sql = """
            SELECT 
            Bruker_has_Svar.Svar_Sporsmal_Quiz_idQuiz,
            Bruker_has_Svar.Svar_Sporsmal_idSporsmal,
            Bruker_has_Svar.Svar_idSvar,
            Bruker_has_Svar.Bruker_idBruker,
            isRiktig,
            Kommentar
            FROM Bruker_has_Svar
            WHERE Bruker_has_Svar.Bruker_idBruker = %s
            AND Bruker_has_Svar.Svar_Sporsmal_Quiz_idQuiz = %s
            AND Bruker_has_Svar.Svar_Sporsmal_idSporsmal = %s
        """
        values = (bruker_id, quiz_id, sporsmal_id)
        self.cursor.execute(sql, values)
        bruker_svar = self.cursor.fetchone()
        if bruker_svar:
            bruker_svar = BrukerHasSvar(*bruker_svar)
        return bruker_svar


    def evaluer_svar(self, id_bruker, id_quiz, id_sporsmal, is_riktig):
        sql = """
            UPDATE Bruker_has_Svar
            SET isRiktig = %s
            WHERE Bruker_idBruker = %s
            AND Svar_Sporsmal_Quiz_idQuiz = %s
            AND Svar_Sporsmal_idSporsmal = %s
        """
        values = (is_riktig, id_bruker, id_quiz, id_sporsmal)
        self.cursor.execute(sql, values)


    def kommenter_sporsmal(self, id_bruker, id_quiz, id_sporsmal, kommentar):
        sql = """
            UPDATE Bruker_has_Svar
            SET Kommentar = %s
            WHERE Bruker_idBruker = %s
            AND Svar_Sporsmal_Quiz_idQuiz = %s
            AND Svar_Sporsmal_idSporsmal = %s
        """
        values = (kommentar, id_bruker, id_quiz, id_sporsmal)
        self.cursor.execute(sql, values)


    def get_bruker_quiz_relasjon(self, id_bruker, id_quiz):
        sql = """
            SELECT * FROM Bruker_has_Quiz
            WHERE Bruker_idBruker = %s
            AND Quiz_idQuiz = %s
        """
        values = (id_bruker, id_quiz)
        self.cursor.execute(sql, values)
        relasjon = self.cursor.fetchone()
        relasjon = BrukerHasQuiz(*relasjon)
        return relasjon


    def kommenter_quiz(self, id_quiz, id_bruker, kommentar):
        sql = """
            UPDATE Bruker_has_Quiz
            SET Kommentar = %s
            WHERE Bruker_idBruker = %s
            AND Quiz_idQuiz = %s
        """
        values = (kommentar, id_bruker, id_quiz)
        self.cursor.execute(sql, values)


    def delete_bruker_quiz_relasjon(self, id_bruker, id_quiz):
        print("delete_bruker_quiz_relasjon")
        sql = """
            DELETE FROM Bruker_has_Svar
            WHERE Bruker_idBruker = %s
            AND Svar_Sporsmal_Quiz_idQuiz = %s
        """
        values = (id_bruker, id_quiz)
        self.cursor.execute(sql, values)
        sql = """
            DELETE FROM Bruker_has_Quiz
            WHERE Bruker_idBruker = %s
            AND Quiz_idQuiz = %s
        """
        values = (id_bruker, id_quiz)
        self.cursor.execute(sql, values)


    def get_sporsmal_object(self, id_quiz, id_sporsmal):
        sql = """
            SELECT * FROM Sporsmal
            WHERE Quiz_idQuiz = %s
            AND idSporsmal = %s
        """
        values = (id_quiz, id_sporsmal)
        self.cursor.execute(sql, values)
        sporsmal = self.cursor.fetchone()
        sporsmal = Sporsmal(*sporsmal)
        return sporsmal


    def delete_bruker_svar_to_sporsmal(self, id_bruker, id_quiz, id_sporsmal):
        sporsmal = self.get_sporsmal_object(id_quiz, id_sporsmal)
        sporsmal_type = sporsmal.sporsmalstype

        if sporsmal_type == 2:
            sql = """
                DELETE FROM Svar
                WHERE Sporsmal_Quiz_idQuiz = %s
                AND Sporsmal_idSporsmal = %s
            """
            values = (id_quiz, id_sporsmal)
            self.cursor.execute(sql, values)
        sql = """
            DELETE FROM Bruker_has_Svar
            WHERE Bruker_idBruker = %s
            AND Svar_Sporsmal_Quiz_idQuiz = %s
            AND Svar_Sporsmal_idSporsmal = %s
        """
        values = (id_bruker, id_quiz, id_sporsmal)
        self.cursor.execute(sql, values)
