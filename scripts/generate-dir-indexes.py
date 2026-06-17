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


FULL_PAGE_TOP = """<!DOCTYPE html>
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

FULL_PAGE_BOTTOM = """</tbody>
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

# Directories that should also include lister.js for dynamic browsing
LISTER_DIRS = {"dists"}


def build_page(dirpath: str, rel: str, *, include_lister: bool = False) -> str:
    top = FULL_PAGE_TOP.format(title=rel)
    parts = [top]

    # Parent link — every directory gets one back to its parent
    parts.append(
        '        <tr><td><a href="../">../</a></td><td>directory</td><td>-</td></tr>'
    )

    entries = sorted(os.listdir(dirpath))
    subdirs = []
    files = []
    for e in entries:
        if e == "index.html":
            continue
        path = os.path.join(dirpath, e)
        if os.path.isdir(path):
            subdirs.append(e)
        else:
            files.append(e)

    for d in subdirs:
        parts.append("        " + dir_entry(d))
    for f in files:
        parts.append("        " + file_entry(f, fmt_size(os.path.join(dirpath, f))))

    bottom = FULL_PAGE_BOTTOM
    if include_lister:
        bottom = bottom.replace(
            "</body>",
            '<script src="https://repos.mungerware.com/lister.js?v=2"></script>\n</body>',
        )
    parts.append(bottom)
    return "\n".join(parts)


def main() -> None:
    root = "."
    # Walk all directories, generate index.html for each.
    # root `.` is skipped — its index.html is hand-crafted.
    for current, dirs, _files in os.walk(root):
        if current == root:
            continue

        rel = os.path.relpath(current, root)
        # Skip hidden directories (e.g. .git) — not served
        if "/" in rel and any(p.startswith(".") for p in rel.split("/")):
            continue
        if rel.startswith("."):
            continue

        include_lister = rel in LISTER_DIRS
        html = build_page(current, rel, include_lister=include_lister)
        with open(os.path.join(current, "index.html"), "w") as f:
            f.write(html)


if __name__ == "__main__":
    main()
