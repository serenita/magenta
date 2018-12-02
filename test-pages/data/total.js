document.addEventListener('readystatechange', function() {
  if (document.readyState == 'complete') {
    document.getElementById('total').textContent = total;
    document.getElementById('result').textContent = total == 49253 ? 'Correct' : 'Wrong';
  }
});
