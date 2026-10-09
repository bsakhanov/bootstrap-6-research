#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""css_stats.py — статистика скомпилированных файлов Bootstrap для доклада.
Запуск: npm i bootstrap@6.0.0-alpha.1 bootstrap5@npm:bootstrap@5.3.8 && python3 tools/stats/css_stats.py node_modules"""
import gzip, os, re, sys
base = sys.argv[1] if len(sys.argv) > 1 else 'node_modules'
FEATS = ['oklch(', 'light-dark(', 'color-mix(', '@container', '@layer', ':has(', '@property', ':where(', 'interpolate-size',
         'content-visibility', '@starting-style', 'allow-discrete', '::details-content', '::backdrop', 'scroll-snap', 'mask-image',
         'padding-inline', 'margin-block', '(width >=', 'min-width:', 'rgba(', 'clamp(', 'dvh', 'var(--bs-', 'oklch(from']
for pkg, label in (('bootstrap', 'v6.0.0-alpha.1'), ('bootstrap5', 'v5.3.8')):
    css = open(f'{base}/{pkg}/dist/css/bootstrap.css', encoding='utf-8').read()
    print(f'== {label}: {len(css) // 1024} KB raw, {len(gzip.compress(css.encode(), 9)) // 1024} KB gzip, {css.count(chr(10))} строк')
    for f in FEATS:
        print(f'  {f:20s} {css.count(f)}')
    print('  #hex-цветов', len(re.findall(r'#[0-9a-fA-F]{3,8}\b', css)))
    print('  объявлений --bs-*', len(re.findall(r'--bs-[a-z0-9-]+\s*:', css)))
    classes = set(re.findall(r'\.([a-zA-Z0-9_\\:-]+)', css))
    print('  классов', len(classes), '| с префиксом md\\:', len([c for c in classes if c.startswith('md\\:')]))
    for f in ('dist/css/bootstrap.min.css', 'dist/js/bootstrap.bundle.min.js', 'dist/js/bootstrap.min.js'):
        b = open(f'{base}/{pkg}/{f}', 'rb').read()
        print(f'  {f}: {len(b) // 1024} KB min, {len(gzip.compress(b, 9)) // 1024} KB gzip')
