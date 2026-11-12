#!/usr/bin/env python3
"""Strip raw wiki template syntax ({{ubl | ... }}) from car descriptions."""
import re, glob, os, sys

TEMPLATE_NAMES = {
    'ubl', 'unbulleted list', 'plainlist', 'flatlist', 'bulleted list',
    'nowrap', 'small', 'convert', 'cvt', 'lang', 'abbr', 'tooltip',
}

def render_template(inner):
    """Turn the inside of {{...}} into readable text."""
    parts = [p.strip() for p in inner.split('|')]
    if not parts:
        return ''
    name = parts[0].strip().lower()
    if name in TEMPLATE_NAMES:
        items = parts[1:]
    else:
        # unknown template: keep params that look like prose, drop the name
        items = parts[1:] if len(parts) > 1 else parts
    # drop empty and pure-punctuation items
    clean = []
    for it in items:
        it = it.strip()
        if not it:
            continue
        if re.fullmatch(r'[\s\-–—,;:./()]*', it):
            continue
        clean.append(it)
    return ', '.join(clean)

def strip_templates(text):
    # repeatedly resolve innermost {{ ... }} (no nested braces inside)
    for _ in range(12):
        new = re.sub(r'\{\{([^{}]*)\}\}', lambda m: render_template(m.group(1)), text)
        if new == text:
            break
        text = new
    # any leftover unbalanced braces
    text = text.replace('{{', '').replace('}}', '')
    return text

def tidy(text):
    # remove dangling label with no value: "Battery: ." / "Power output: , ." / "Rated range: ."
    text = re.sub(r'\b(Battery|Power output|Rated range|Charging|Electric motor|Combustion engine|Transmission|Drive layout|Production)\s*:\s*(?=[.;]|$)', '', text)
    # collapse ", ," and ", ." and " ,"
    text = re.sub(r'\s*,\s*(?=[,.;])', '', text)
    text = re.sub(r'\.\s*\.', '.', text)
    text = re.sub(r'\s+([,.;:])', r'\1', text)
    text = re.sub(r'\(\s*\)', '', text)
    text = re.sub(r'\s{2,}', ' ', text)
    # "up to." -> "up to X." is unknowable; drop the fragment
    text = re.sub(r'\bup to\s*\.', '', text)
    text = re.sub(r'\s+\.', '.', text)
    return text.strip()

def process(path):
    with open(path, encoding='utf-8') as f:
        html = f.read()
    if '{{' not in html:
        return 0
    before = html
    # only touch text inside <p> ... </p> blocks in the prose area
    def fix_para(m):
        return m.group(1) + tidy(strip_templates(m.group(2))) + m.group(3)
    html = re.sub(r'(<p>)(.*?)(</p>)', fix_para, html, flags=re.S)
    if html != before:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        return 1
    return 0

if __name__ == '__main__':
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    files = sorted(glob.glob(os.path.join(root, 'cars', '*.html')))
    files.append(os.path.join(root, 'admin', 'index.html'))
    changed = 0
    for p in files:
        changed += process(p)
    print(f'cleaned {changed} files')
    # verify
    left = 0
    for p in files:
        with open(p, encoding='utf-8') as f:
            if '{{' in f.read():
                left += 1
    print(f'files still containing {{{{: {left}')
