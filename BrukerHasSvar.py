class BrukerHasSvar:
    def __init__(self, id_quiz, id_sporsmal, id_svar, id_bruker, is_riktig=None, kommentar=None):
        self.id_bruker = id_bruker
        self.id_quiz = id_quiz
        self.id_sporsmal = id_sporsmal
        self.id_svar = id_svar
        self.is_riktig = is_riktig
        self.kommentar = kommentar
