#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""milchin_run.py — прогон типографа Мильчина (семья скилов beaverbeard, MIT) по Markdown-исходнику доклада.
HTML-теги, спаны кода, адреса и ключи ссылок прячутся за плейсхолдеры, чтобы типограф правил только прозу."""
import re, subprocess, sys, pathlib
src = pathlib.Path(sys.argv[1]); text = src.read_text(encoding='utf-8')
store = []
def hide(m):
    store.append(m.group(0)); return f'QQPH{len(store) - 1}QQ'
protected = re.sub(r'<code>.*?</code>|<dt>.*?</dt>|<[^>]+>|`[^`\n]*`|\[@[a-z0-9-]+\]|https?://\S+|^```.*?^```', hide, text, flags=re.S | re.M)
res = subprocess.run([sys.executable, str(src.parent.parent / 'lang/milchin.py'), '--report'], input=protected, capture_output=True, text=True)
fixed = re.sub(r'QQPH(\d+)QQ', lambda m: store[int(m.group(1))], res.stdout)
assert len(fixed) > len(text) * 0.9, 'типограф вернул пустой или усечённый текст'
src.write_text(fixed, encoding='utf-8')
print(res.stderr.strip())
