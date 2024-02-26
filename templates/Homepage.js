const cert = document.querySelector('.cert');
cert.addEventListener('click', () => {
  const input = cert.querySelector('input');
  input.checked = !input.checked;
});

const cert2 = document.querySelector('.cert2');
cert2.addEventListener('click', () => {
  const input2 = cert2.querySelector('input');
  input2.checked = !input2.checked;
});

const form = document.querySelector('form');
const authCheckbox = document.getElementById('auth');
const authorityAlert = document.querySelector('.authority-alert');

form.addEventListener('submit', e => {
  if (!authCheckbox.checked) {
    e.preventDefault();
    authorityAlert.style.display = 'block';
  }
});
