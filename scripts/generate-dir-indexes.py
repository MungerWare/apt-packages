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
<div class="page">
<p style="margin:12px 0 4px"><a href="/">MungerWare APT Repository</a> / <span id="dirpath">{title}/</span></p>
<table>
<thead><tr><th>Name</th><th>Type</th><th>Size</th></tr></thead>
<tbody>
"""

PAGE_BOTTOM = """</tbody>
</table>
<hr>
<p class="copyright">
Copyright &copy; 2026 <a href="https://github.com/Munger">Tim Hosking</a>.
<a href="https://github.com/Munger/packages">Source</a> &mdash;
<a href="https://repos.mungerware.com/LICENCE.html">MIT License</a>
</p>
</div>
</body>
</html>
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


def main() -> None:
    root = "."
    for current, dirs, _files in os.walk(root):
        if current == root:
            continue  # root index.html is hand-crafted

        rel = os.path.relpath(current, root)
        # Skip hidden directories (e.g. .git) — not served
        if "/" in rel and any(p.startswith(".") for p in rel.split("/")):
            continue
        if rel.startswith("."):
            continue

        html = build_sub_page(current, rel)
        with open(os.path.join(current, "index.html"), "w") as f:
            f.write(html)


if __name__ == "__main__":
    main()
