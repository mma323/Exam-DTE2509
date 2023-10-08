class Admin:
    def __init__(self, admin_id, fornavn, etternavn, password_hash) -> None:
        self.admin_id = admin_id
        self.fornavn = fornavn
        self.etternavn = etternavn
        self.password_hash = password_hash

    def is_active(self):
        return True

    def get_id(self):
        return self.admin_id

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
