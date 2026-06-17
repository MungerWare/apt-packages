#!/usr/bin/env python3
"""Generate static index.html for every directory under dists/."""

import os
import stat as stat_module


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


def suite_entry(name: str) -> str:
    return (
        f'<tr><td><a href="{name}/">{name}/</a></td>'
        f"<td>directory</td><td>-</td></tr>"
    )


def file_entry(name: str, size: str) -> str:
    return (
        f'<tr><td><a href="{name}">{name}</a></td>'
        f"<td>file</td><td>{size}</td></tr>"
    )


ROOT_TEMPLATE_TOP = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title id="pagetitle">dists/ — MungerWare APT Repository</title>
<link rel="stylesheet" href="https://repos.mungerware.com/style.css?v=2">
</head>
<body>
<div class="banner"><a href="https://github.com/Munger"><img src="https://repos.mungerware.com/logo.png" alt="MungerWare"></a></div>
<div class="sub"><a href="/">MungerWare APT Repository</a> / <span id="dirpath">dists/</span></div>
<div class="page">
<table>
<thead><tr><th>Name</th><th>Type</th><th>Size</th></tr></thead>
<tbody>
"""

ROOT_TEMPLATE_BOTTOM = """</tbody>
</table>
<hr>
<p class="copyright">
Copyright &copy; 2026 <a href="https://github.com/Munger">Tim Hosking</a>.
<a href="https://github.com/Munger/packages">Source</a>
</p>
</div>
<script src="https://repos.mungerware.com/lister.js?v=2"></script>
</body>
</html>
"""

SUB_TEMPLATE_TOP = """<!DOCTYPE html>
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

SUB_TEMPLATE_BOTTOM = """</tbody>
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


def build_root_index(dists_dir: str) -> str:
    suites = sorted(
        d
        for d in os.listdir(dists_dir)
        if os.path.isdir(os.path.join(dists_dir, d))
    )
    parts = [ROOT_TEMPLATE_TOP]
    for s in suites:
        parts.append("        " + suite_entry(s))
    parts.append(ROOT_TEMPLATE_BOTTOM)
    return "\n".join(parts)


def build_sub_index(subdir: str, rel: str) -> str:
    top = SUB_TEMPLATE_TOP.format(title=rel)
    parts = [top]
    parts.append('        <tr><td><a href="../">../</a></td><td>directory</td><td>-</td></tr>')

    entries = sorted(os.listdir(subdir))
    subdirs = []
    files = []
    for e in entries:
        path = os.path.join(subdir, e)
        if os.path.isdir(path):
            subdirs.append(e)
        else:
            files.append(e)

    for d in subdirs:
        parts.append("        " + suite_entry(d))
    for f in files:
        parts.append("        " + file_entry(f, fmt_size(os.path.join(subdir, f))))

    parts.append(SUB_TEMPLATE_BOTTOM)
    return "\n".join(parts)


def main() -> None:
    dists_dir = "dists"
    if not os.path.isdir(dists_dir):
        return

    # Root dists/index.html
    root_html = build_root_index(dists_dir)
    with open(os.path.join(dists_dir, "index.html"), "w") as f:
        f.write(root_html)

    # Subdirectory indexes
    for root, dirs, _files in os.walk(dists_dir):
        if root == dists_dir:
            continue  # already handled
        rel = os.path.relpath(root, dists_dir)
        html = build_sub_index(root, rel)
        with open(os.path.join(root, "index.html"), "w") as f:
            f.write(html)


if __name__ == "__main__":
    main()
