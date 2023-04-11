import mysql.connector

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
    

    def get_admin(self, admin_id):
        admin = self.query(
            f"SELECT * FROM Admin WHERE idAdmin = {admin_id}"
        )
        return admin
    

    def get_bruker(self, bruker_id):
        bruker = self.query(
            f"SELECT * FROM Bruker WHERE idBruker = {bruker_id}"
        )
        return bruker