#!/usr/bin/env python3
"""Generate static index.html for every directory in the repo."""

import os


def fmt_size(path: str) -> str:
    try:
        sz = os.stat(path).st_size
        if sz < 1024:
            return f"{sz} B"
        if sz < 1024 * 1024:
            return f"{sz // 1024} KiB"
        return f"{sz // (1024 * 1024)} MiB"
    except OSError:
        return "-"


def dir_entry(name: str) -> str:
    return (
        f'<tr><td><a href="{name}/">{name}/</a></td>'
        f"<td>directory</td><td>-</td></tr>"
    )


def file_entry(name: str, size: str) -> str:
    return (
        f'<tr><td><a href="{name}">{name}</a></td>'
        f"<td>file</td><td>{size}</td></tr>"
    )


ROOT_PAGE_TOP = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MungerWare APT Repository</title>
<link rel="stylesheet" href="https://repos.mungerware.com/style.css?v=2">
</head>
<body>
<div class="banner"><a href="https://github.com/Munger"><img src="https://repos.mungerware.com/logo.png" alt="MungerWare"></a></div>
<div class="sub"><a href="https://repos.mungerware.com/">repos.mungerware.com</a> / APT</div>
<div class="page">
<table>
<thead><tr><th>Name</th><th>Type</th><th>Size</th></tr></thead>
<tbody>
"""

SUB_PAGE_TOP = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}/ — MungerWare APT Repository</title>
<link rel="stylesheet" href="https://repos.mungerware.com/style.css?v=2">
</head>
<body>
<div class="banner"><a href="https://github.com/Munger"><img src="https://repos.mungerware.com/logo.png" alt="MungerWare"></a></div>
<div class="sub"><a href="/">MungerWare APT Repository</a> / <span id="dirpath">{title}/</span></div>
<div class="page">
<table>
<thead><tr><th>Name</th><th>Type</th><th>Size</th></tr></thead>
<tbody>
"""

PAGE_BOTTOM = """</tbody>
</table>
<hr>
<p class="copyright">
Copyright &copy; 2026 <a href="https://github.com/Munger">Tim Hosking</a>.
<a href="https://github.com/Munger/packages">Source</a>
</p>
</div>
</body>
</html>
"""

ROOT_EXTRA = """
<div class="content">

<h2>Setup</h2>

<pre>curl -fsSL https://apt.mungerware.com/key.asc | sudo gpg --dearmor -o /usr/share/keyrings/munger.gpg
echo "deb [signed-by=/usr/share/keyrings/munger.gpg] https://apt.mungerware.com/ noble main" | sudo tee /etc/apt/sources.list.d/munger.list
sudo apt-get update
sudo apt-get install mirror-dedupe</pre>

<h2>Browse</h2>
<ul>
  <li><a href="pool/">pool/</a> &mdash; package files (.deb)</li>
  <li><a href="dists/">dists/</a> &mdash; APT metadata (Release, Packages)</li>
  <li><a href="key.asc">key.asc</a> &mdash; GPG public key</li>
</ul>

<p><a href="https://github.com/Munger/packages">Source repository</a></p>

</div>
"""


def build_sub_page(dirpath: str, rel: str) -> str:
    parts = [SUB_PAGE_TOP.format(title=rel)]
    parts.append(
        '        <tr><td><a href="../">../</a></td><td>directory</td><td>-</td></tr>'
    )
    entries = sorted(os.listdir(dirpath))
    for e in entries:
        if e == "index.html":
            continue
        path = os.path.join(dirpath, e)
        if os.path.isdir(path):
            parts.append("        " + dir_entry(e))
        else:
            parts.append("        " + file_entry(e, fmt_size(path)))
    parts.append(PAGE_BOTTOM)
    return "\n".join(parts)


def build_root_page(root: str) -> str:
    parts = [ROOT_PAGE_TOP]
    parts.append(
        '        <tr><td><a href="https://repos.mungerware.com/">../</a></td>'
        "<td>directory</td><td>-</td></tr>"
    )
    entries = sorted(os.listdir(root))
    for e in entries:
        if e == "index.html":
            continue
        path = os.path.join(root, e)
        if os.path.isdir(path):
            parts.append("        " + dir_entry(e))
        else:
            parts.append("        " + file_entry(e, fmt_size(path)))
    parts.append(PAGE_BOTTOM)
    html = "\n".join(parts)
    # Insert extra content (setup instructions) before the copyright line
    html = html.replace('<hr>\n<p class="copyright">', ROOT_EXTRA + '\n<hr>\n<p class="copyright">')
    return html


def main() -> None:
    root = "."
    for current, dirs, _files in os.walk(root):
        rel = os.path.relpath(current, root)
        # Skip hidden directories (e.g. .git) — not served
        if "/" in rel and any(p.startswith(".") for p in rel.split("/")):
            continue
        if rel.startswith("."):
            continue

        if current == root:
            html = build_root_page(current)
        else:
            html = build_sub_page(current, rel)
        with open(os.path.join(current, "index.html"), "w") as f:
            f.write(html)


if __name__ == "__main__":
    main()
