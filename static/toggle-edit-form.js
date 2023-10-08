function toggleEditForm(quizId, sporsmalId) {
  var form = document.getElementById('editForm' + sporsmalId);
  if (form.style.display === 'none') {
    form.style.display = 'block';
  } else {
    form.style.display = 'none';
  }
}
