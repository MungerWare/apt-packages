(function() {
  var repo = 'Munger/packages';
  var el = document.getElementById('list');
  var hd = document.getElementById('dirpath');
  var pt = document.getElementById('pagetitle');

  function fmt(b) {
    if (b < 1024) return b + ' B';
    if (b < 1048576) return (b / 1024).toFixed(1) + ' KB';
    return (b / 1048576).toFixed(1) + ' MB';
  }

  function load(dir) {
    var path = dir.replace(/^\/|\/$/g, '') || '';
    el.innerHTML = '<tr><td colspan="3" class="status">Loading…</td></tr>';
    var parts = path.split('/').filter(Boolean);
    var label = parts.length ? parts.join('/') + '/' : '(root)';
    if (hd) hd.textContent = label;
    if (pt) pt.textContent = label + ' — Munger APT Repository';

    fetch('https://api.github.com/repos/' + repo + '/contents' + (path ? '/' + path : '') + '?ref=gh-pages')
      .then(function(r) { if (!r.ok) throw new Error(); return r.json(); })
      .then(function(items) {
        var html = '';
        if (path) {
          var sl = path.lastIndexOf('/');
          // Determine what the parent link should be
          if (sl === -1) {
            // Top level — ".." goes to repo root /
            html += '<tr><td><a href="/">..</a></td><td>dir</td><td></td></tr>';
          } else {
            var up = path.substring(0, sl);
            html += '<tr><td><a href="#" class="d" data-d="' + up + '">..</a></td><td>dir</td><td></td></tr>';
          }
        }
        for (var i = 0; i < items.length; i++) {
          var item = items[i];
          if (item.name === 'index.html' || item.name === '404.html') continue;
          if (item.type === 'dir') {
            html += '<tr><td><a href="#" class="d" data-d="' + (path ? path + '/' : '') + item.name + '">' + item.name + '/</a></td><td>dir</td><td></td></tr>';
          } else {
            html += '<tr><td><a href="' + (path ? path + '/' : '') + item.name + '">' + item.name + '</a></td><td>file</td><td>' + fmt(item.size) + '</td></tr>';
          }
        }
        el.innerHTML = html;
        history.replaceState({d: path}, '', path ? '/' + path + '/' : '/');
      })
      .catch(function(err) {
        el.innerHTML = '<tr><td colspan="3" class="status">Failed to load directory</td></tr>';
        console.error('lister fetch error:', err);
      });
  }

  el.addEventListener('click', function(e) {
    var link = e.target.closest('.d');
    if (!link) return;
    e.preventDefault();
    load(link.getAttribute('data-d'));
  });

  window.addEventListener('popstate', function(e) {
    if (e.state && e.state.d !== undefined) load(e.state.d);
  });

  // Read initial directory from hash (set by 404.html for subdirectory direct links),
  // or from the URL pathname
  var initial = location.hash ? location.hash.substring(1) : location.pathname.replace(/\/$/, '') || '';
  load(initial);
})();
