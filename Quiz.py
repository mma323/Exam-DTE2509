class Quiz:
    def __init__(self, id_quiz, navn) -> None:
        self.id_quiz = id_quiz
        self.navn = navn
        self.sporsmal = []
        self.antall_sporsmal = len(self.sporsmal)