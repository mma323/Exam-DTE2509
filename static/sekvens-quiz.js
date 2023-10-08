var currentSporsmal = 1;
var totalSporsmal = {{ quiz.get_antall_sporsmal() }};
var sporsmalContainer = document.getElementsByClassName('sporsmal-container')[0];
var sporsmalList = sporsmalContainer.getElementsByClassName('sporsmal');
var gaVidereButton = document.getElementById('ga-videre');
var leverButton = document.getElementById('lever');
var quizForm = document.getElementById('quiz-form');

function visNesteSporsmal() {
    if (currentSporsmal < totalSporsmal) {
        sporsmalList[currentSporsmal - 1].style.display = 'none';
        currentSporsmal++;
        sporsmalList[currentSporsmal - 1].style.display = 'block';
    }

    if (currentSporsmal === totalSporsmal) {
        gaVidereButton.style.display = 'none';
        leverButton.style.display = 'block';
    }
}

// Skjul alle spørsmål bortsett fra det første
for (var i = 1; i < totalSporsmal; i++) {
    sporsmalList[i].style.display = 'none';
}

gaVidereButton.addEventListener('click', visNesteSporsmal);