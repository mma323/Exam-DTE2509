class Bruker:
    def __init__(self, bruker_id) -> None:
        self.bruker_id = bruker_id

#Disse funksjonene er nødvendige for å kunne bruke flask-login


    def is_active(self):
        return True
    

    def get_id(self):
        return self.bruker_id


    def is_anonymous(self):
        return True
    
    
    def is_authenticated(self):
        return True