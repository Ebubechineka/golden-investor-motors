#!/usr/bin/env python3
"""Third pass: drop labels whose value is only a parenthetical or junk."""
import re, glob, os

LABELS = ['Battery', 'Power output', 'Rated range', 'Charging', 'Electric motor',
          'Combustion engine', 'Transmission', 'Drive layout', 'Production',
          'Also sold as', 'Shares its underpinnings with']
LAB = '|'.join(re.escape(l) for l in LABELS)

def tidy(text):
    # label followed by only parenthetical(s) then sentence end -> drop whole clause
    text = re.sub(r'\b(' + LAB + r')\s*:\s*(?:\([^()]*\)\s*[,;]?\s*)+(?=[.;]|$)', '', text)
    # label followed by parentheticals then another label -> drop
    text = re.sub(r'\b(' + LAB + r')\s*:\s*(?:\([^()]*\)\s*[,;]?\s*)+(?=(' + LAB + r')\s*:)', '', text)
    # label with empty value
    text = re.sub(r'\b(' + LAB + r')\s*:\s*(?=[.;]|$)', '', text)
    # "peak (001 FR)" style leftovers
    text = re.sub(r',?\s*peak\s*\([^()]*\)', '', text, flags=re.I)
    text = re.sub(r',?\s*peak\b', '', text, flags=re.I)
    # collapse debris
    text = re.sub(r'\s*,\s*(?=[,.;])', '', text)
    text = re.sub(r'\.\s*\.', '.', text)
    text = re.sub(r'\s+([,.;:])', r'\1', text)
    text = re.sub(r'\(\s*\)', '', text)
    text = re.sub(r':\s*:', ':', text)
    text = re.sub(r'\s{2,}', ' ', text)
    text = re.sub(r'\s+\.', '.', text)
    text = re.sub(r'\.\s*,', '.', text)
    text = re.sub(r';\s*\.', '.', text)
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
    print(f'pass3 cleaned {changed} files')
    bad = []
    for p in files:
        with open(p, encoding='utf-8') as f:
            t = f.read()
        if re.search(r'\b(' + LAB + r')\s*:\s*(?=[.;]|$)', t) or '{{' in t or re.search(r'\bpeak\b', t):
            bad.append(p)
    print(f'files with leftovers: {len(bad)}')
    for b in bad[:5]:
        print(' ', b)
