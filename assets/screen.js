/* Reopen the Record · big-screen slides: arrows / space / click to advance, F for full screen. */
(function () {
  var s = [].slice.call(document.querySelectorAll('.slide')), n = s.length, i = 0;
  var cnt = document.getElementById('count');
  function go(k, push) {
    k = Math.max(0, Math.min(n - 1, k)); s[i].hidden = true; i = k; s[i].hidden = false;
    cnt.textContent = (i + 1) + ' / ' + n;
    if (push !== false) history.replaceState(null, '', '#' + (i + 1));
  }
  function fs() {
    if (document.fullscreenElement) document.exitFullscreen();
    else if (document.documentElement.requestFullscreen) document.documentElement.requestFullscreen();
  }
  document.getElementById('prev').onclick = function () { go(i - 1); };
  document.getElementById('next').onclick = function () { go(i + 1); };
  document.getElementById('fs').onclick = fs;
  document.addEventListener('keydown', function (ev) {
    if (ev.altKey || ev.ctrlKey || ev.metaKey) return;
    var k = ev.key;
    if (k === 'ArrowRight' || k === 'ArrowDown' || k === ' ' || k === 'PageDown' || k === 'Enter') { ev.preventDefault(); go(i + 1); }
    else if (k === 'ArrowLeft' || k === 'ArrowUp' || k === 'PageUp' || k === 'Backspace') { ev.preventDefault(); go(i - 1); }
    else if (k === 'Home') go(0); else if (k === 'End') go(n - 1);
    else if (k === 'f' || k === 'F') fs();
  });
  document.getElementById('deck').addEventListener('click', function (ev) {
    if (ev.target.closest('a,button')) return; go(i + 1);
  });
  var h = parseInt(location.hash.slice(1), 10); if (h) go(h - 1, false);
})();
