class Quiz:
    def __init__(self, id_quiz, navn) -> None:
        self.id_quiz = id_quiz
        self.navn = navn
        self.sporsmal = []
    

    def get_antall_sporsmal(self):
        return len(self.sporsmal)
    
    
    #Til bruk i debugging   
    def __str__(self) -> str:
        return f"Quiz: {self.id_quiz} - {self.navn} - {self.sporsmal} - {self.get_antall_sporsmal()}"