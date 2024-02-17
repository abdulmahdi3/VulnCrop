var words = ['VulnCrop', 'Pentesting Tool', 'Vulnerability Scanner'],
  part,
  i = 0,
  offset = 0,
  len = words.length,
  forwards = true,
  skip_count = 0,
  skip_delay = 30,
  speed = 60;
var wordflick = function () {
  setInterval(function () {
    if (forwards) {
      if (offset >= words[i].length) {
        ++skip_count;
        if (skip_count == skip_delay) {
          forwards = false;
          skip_count = 0;
        }
      }
    } else {
      if (offset == 0) {
        forwards = true;
        i++;
        offset = 0;
        if (i >= len) {
          i = 0;
        }
      }
    }
    part = words[i].substr(0, offset);
    if (skip_count == 0) {
      if (forwards) {
        offset++;
      } else {
        offset--;
      }
    }
    $('.word').text(part);
  }, speed);
};
$(document).ready(function () {
  wordflick();
});

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
