import mysql.connector
from Quiz import Quiz
from Sporsmal import Sporsmal
from Svar import Svar

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
        admin = self.query(
            f"SELECT * FROM Admin WHERE idAdmin = '{admin_id}'"
        )
        return admin
        

    def get_bruker(self, bruker_id):
        bruker = self.query(
            f"SELECT * FROM Bruker WHERE idBruker = '{bruker_id}'"
        )
        return bruker
    

    def get_quizzer(self):
        quizzer = self.query(
            f"SELECT * FROM Quiz"
        )
        quizzer = [Quiz(*quiz) for quiz in quizzer]

        return quizzer
    

    def get_quiz(self, quiz_id):
        quiz = self.query(
            f"SELECT * FROM Quiz WHERE idQuiz = {quiz_id}"
        )
        quiz = Quiz(*quiz[0])
        return quiz


    def get_sporsmal(self):
        sporsmal = self.query(
            f"SELECT * FROM Sporsmal"
        )
        sporsmal = [Sporsmal(*sporsmal) for sporsmal in sporsmal]

        return sporsmal
    

    def get_svar(self):
        svar = self.query(
            f"SELECT * FROM Svar"
        )
        svar = [Svar(*svar) for svar in svar]
        return svar