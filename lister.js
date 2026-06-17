(async () => {
  const repo = 'Munger/packages';
  const path = location.pathname.replace(/\/$/, '') || '';
  const list = document.getElementById('list');

  try {
    const res = await fetch(`https://api.github.com/repos/${repo}/contents${path}?ref=gh-pages`);
    if (!res.ok) { list.innerHTML = '<tr><td colspan="3">Error loading directory</td></tr>'; return; }
    const items = await res.json();
    let html = '';

    if (path.includes('/')) {
      const parent = path.substring(0, path.lastIndexOf('/')) || '';
      html += `<tr><td><a href="${parent}/">..</a></td><td>dir</td><td></td></tr>`;
    }

    for (const item of items) {
      const url = item.type === 'dir' ? `${path}/${item.name}/` : `${path}/${item.name}`;
      const size = item.type === 'file' ? (item.size < 1024 ? item.size + ' B' : item.size < 1048576 ? (item.size/1024).toFixed(1) + ' KB' : (item.size/1048576).toFixed(1) + ' MB') : '';
      html += `<tr><td><a href="${url}">${item.name}</a></td><td>${item.type === 'dir' ? 'dir' : 'file'}</td><td>${size}</td></tr>`;
    }
    list.innerHTML = html;
  } catch (e) {
    list.innerHTML = '<tr><td colspan="3">Failed to load</td></tr>';
  }
})();
