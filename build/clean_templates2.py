#!/usr/bin/env python3
"""Second pass: remove leftover empty labels and junk fragments."""
import re, glob, os

LABELS = ['Battery', 'Power output', 'Rated range', 'Charging', 'Electric motor',
          'Combustion engine', 'Transmission', 'Drive layout', 'Production',
          'Also sold as', 'Shares its underpinnings with']

JUNK_ITEMS = {'peak', '30 min maximum', 'maximum', 'up to', 'n/a', 'na', '-', '–'}

def tidy(text):
    # drop junk list items left over from templates
    for j in JUNK_ITEMS:
        text = re.sub(r'(?<=[,:]\s)' + re.escape(j) + r'(?=\s*[,.;])', '', text, flags=re.I)
        text = re.sub(r'(?<=:\s)' + re.escape(j) + r'(?=\s*[,.;])', '', text, flags=re.I)
    # remove a label that is immediately followed by another label (no value)
    lab = '|'.join(re.escape(l) for l in LABELS)
    for _ in range(6):
        new = re.sub(r'\b(' + lab + r')\s*:\s*(?=(' + lab + r')\s*:)', '', text)
        if new == text:
            break
        text = new
    # remove a label with no value before sentence end
    text = re.sub(r'\b(' + lab + r')\s*:\s*(?=[.;]|$)', '', text)
    # collapse punctuation debris
    text = re.sub(r'\s*,\s*(?=[,.;])', '', text)
    text = re.sub(r'\.\s*\.', '.', text)
    text = re.sub(r'\s+([,.;:])', r'\1', text)
    text = re.sub(r'\(\s*\)', '', text)
    text = re.sub(r':\s*:', ':', text)
    text = re.sub(r'\s{2,}', ' ', text)
    text = re.sub(r'\s+\.', '.', text)
    text = re.sub(r'\.\s*,', '.', text)
    return text.strip()

def process(path):
    with open(path, encoding='utf-8') as f:
        html = f.read()
    before = html
    def fix_para(m):
        return m.group(1) + tidy(m.group(2)) + m.group(3)
    html = re.sub(r'(<p>)(.*?)(</p>)', fix_para, html, flags=re.S)
    if html != before:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        return 1
    return 0

if __name__ == '__main__':
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    files = sorted(glob.glob(os.path.join(root, 'cars', '*.html')))
    changed = sum(process(p) for p in files)
    print(f'pass2 cleaned {changed} files')
    # report remaining suspicious patterns
    bad = 0
    for p in files:
        with open(p, encoding='utf-8') as f:
            t = f.read()
        if re.search(r'\b(Battery|Power output|Rated range|Charging)\s*:\s*(?=[.;]|$)', t) or '{{' in t:
            bad += 1
    print(f'files with leftover empty labels: {bad}')
