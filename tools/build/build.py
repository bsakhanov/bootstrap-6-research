#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build.py — собирает исследование-доклад о Bootstrap 6 из Markdown-исходника.

Что делает:
1. ссылки вида [@key] нумерует по первому упоминанию и строит «Список использованных источников»;
2. Markdown → HTML (python-markdown: tables, attr_list);
3. <div class="chart" data-chart="…"> превращает в <canvas> с данными для Chart.js (вшит в файл);
4. <div class="diagram" data-diagram="…"> заменяет рисованной SVG-схемой;
5. режет документ на главы по h2, нумерует их, строит оглавление и боковую рейку;
6. пишет doklad/bootstrap-6-research.html и пронумерованный исходник doklad/bootstrap-6-research.md.
Стиль наследует докладу о Joomla 6: бумага, акцент, прогресс-бар, липкое оглавление.
"""
import html, json, pathlib, re, sys
import markdown

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / 'tools/build/doklad-bootstrap-6.md'
OUT_HTML = ROOT / 'doklad/bootstrap-6-research.html'
OUT_MD = ROOT / 'doklad/bootstrap-6-research.md'
CHARTJS = (ROOT / 'tools/build/chart.umd.js').read_text(encoding='utf-8')
CANONICAL = 'https://bsakhanov.github.io/bootstrap-6-research/doklad/bootstrap-6-research.html'

D = 'https://getbootstrap.com/docs/6.0'
G = 'https://github.com/twbs/bootstrap'
SOURCES = {
    'blog': f'Otto M. Bootstrap 6 Alpha // Bootstrap Blog, 8 октября 2026. URL: https://blog.getbootstrap.com/2026/10/08/bootstrap-6-alpha/',
    'migration': f'Migration // Bootstrap 6 documentation. URL: {D}/guides/migration/',
    'approach': f'Approach // Bootstrap 6 documentation. URL: {D}/getting-started/approach/',
    'browsers': f'Browsers & devices // Bootstrap 6 documentation. URL: {D}/getting-started/browsers-devices/',
    'install': f'Install // Bootstrap 6 documentation. URL: {D}/getting-started/install/',
    'npm6': 'bootstrap 6.0.0-alpha.1 // npm. URL: https://www.npmjs.com/package/bootstrap/v/6.0.0-alpha.1',
    'npm5': 'bootstrap 5.3.8 // npm. URL: https://www.npmjs.com/package/bootstrap/v/5.3.8',
    'repo': f'twbs/bootstrap, ветка main, коммит 7771f16 от 8 октября 2026 // GitHub. URL: {G}',
    'config': f'scss/_config.scss, ветка main // GitHub, twbs/bootstrap. URL: {G}/blob/main/scss/_config.scss',
    'colors': f'scss/_colors.scss, ветка main // GitHub, twbs/bootstrap. URL: {G}/blob/main/scss/_colors.scss',
    'theme': f'scss/_theme.scss, ветка main // GitHub, twbs/bootstrap. URL: {G}/blob/main/scss/_theme.scss',
    'root': f'scss/_root.scss, ветка main // GitHub, twbs/bootstrap. URL: {G}/blob/main/scss/_root.scss',
    'combobox-ts': f'js/src/combobox.ts, ветка main // GitHub, twbs/bootstrap. URL: {G}/blob/main/js/src/combobox.ts',
    'data-ts': f'js/src/dom/data.ts, ветка main // GitHub, twbs/bootstrap. URL: {G}/blob/main/js/src/dom/data.ts',
    'skills': f'skills/ — навыки для агентов, ветка main // GitHub, twbs/bootstrap. URL: {G}/tree/main/skills',
    'agents': f'AGENTS.md, ветка main // GitHub, twbs/bootstrap. URL: {G}/blob/main/AGENTS.md',
    'ai': f'Using Bootstrap with AI // Bootstrap 6 documentation. URL: {D}/getting-started/ai/',
    'llms': 'llms.txt // getbootstrap.com. URL: https://getbootstrap.com/llms.txt',
    'llmstxt': 'The /llms.txt file // llmstxt.org : сайт. URL: https://llmstxt.org/',
    'colormodes': f'Color modes // Bootstrap 6 documentation. URL: {D}/customize/color-modes/',
    'cq': f'Container queries // Bootstrap 6 documentation. URL: {D}/utilities/container-queries/',
    'dialog': f'Dialog // Bootstrap 6 documentation. URL: {D}/components/dialog/',
    'drawer': f'Drawer // Bootstrap 6 documentation. URL: {D}/components/drawer/',
    'navbar': f'Navbar // Bootstrap 6 documentation. URL: {D}/components/navbar/',
    'accordion': f'Accordion // Bootstrap 6 documentation. URL: {D}/components/accordion/',
    'carousel': f'Carousel // Bootstrap 6 documentation. URL: {D}/components/carousel/',
    'menu': f'Menu // Bootstrap 6 documentation. URL: {D}/components/menu/',
    'stepper': f'Stepper // Bootstrap 6 documentation. URL: {D}/components/stepper/',
    'avatar': f'Avatar // Bootstrap 6 documentation. URL: {D}/components/avatar/',
    'navoverflow': f'Nav overflow // Bootstrap 6 documentation. URL: {D}/components/nav-overflow/',
    'prose': f'Prose // Bootstrap 6 documentation. URL: {D}/content/prose/',
    'hoverlift': f'Hover lift // Bootstrap 6 documentation. URL: {D}/helpers/hover-lift/',
    'shadows': f'Shadows // Bootstrap 6 documentation. URL: {D}/utilities/shadows/',
    'field': f'Field // Bootstrap 6 documentation. URL: {D}/forms/field/',
    'validation': f'Validation // Bootstrap 6 documentation. URL: {D}/forms/validation/',
    'combobox': f'Combobox // Bootstrap 6 documentation. URL: {D}/forms/combobox/',
    'chips': f'Chips // Bootstrap 6 documentation. URL: {D}/forms/chips/',
    'otp': f'OTP input // Bootstrap 6 documentation. URL: {D}/forms/otp-input/',
    'strength': f'Password strength // Bootstrap 6 documentation. URL: {D}/forms/password-strength/',
    'range': f'Range // Bootstrap 6 documentation. URL: {D}/forms/range/',
    'datepicker': f'Datepicker // Bootstrap 6 documentation. URL: {D}/forms/datepicker/',
    'floating': 'Floating UI : сайт. URL: https://floating-ui.com/',
    'vcp': 'Vanilla Calendar Pro : сайт. URL: https://vanilla-calendar.pro/',
    'postcss-prefix': 'twbs/postcss-prefix-custom-properties // GitHub. URL: https://github.com/twbs/postcss-prefix-custom-properties',
    'rolldown': 'Rolldown : сайт. URL: https://rolldown.rs/',
    'vitest': 'Browser Mode // Vitest : документация. URL: https://vitest.dev/guide/browser/',
    'astro': 'Astro : сайт. URL: https://astro.build/',
    'pagefind': 'Pagefind : сайт. URL: https://pagefind.app/',
    'tailwind': 'Responsive design // Tailwind CSS : документация. URL: https://tailwindcss.com/docs/responsive-design',
    'htmldialog': 'The dialog element // HTML Living Standard, WHATWG. URL: https://html.spec.whatwg.org/multipage/interactive-elements.html#the-dialog-element',
    'mdn-interp': 'interpolate-size // MDN Web Docs. URL: https://developer.mozilla.org/en-US/docs/Web/CSS/interpolate-size',
    'wcag222': 'Success Criterion 2.2.2 Pause, Stop, Hide // WCAG 2.1, W3C. URL: https://www.w3.org/TR/WCAG21/#pause-stop-hide',
    'wcag1413': 'Understanding Success Criterion 1.4.13: Content on Hover or Focus // W3C WAI. URL: https://www.w3.org/WAI/WCAG21/Understanding/content-on-hover-or-focus.html',
    'discussions': 'v6 feedback // GitHub Discussions, twbs. URL: https://github.com/orgs/twbs/discussions/categories/v6-feedback',
    'joomla-report': 'Саханов Б. Joomla 6 для новостной редакции : исследование-доклад, редакция 1.1, 8 октября 2026. URL: https://bsakhanov.github.io/joomla-6-newsroom-research/',
    'joomla-package': 'package.json, ветка 6.1-dev // GitHub, joomla/joomla-cms. URL: https://github.com/joomla/joomla-cms/blob/6.1-dev/package.json',
    'chromium': 'Sparticuz/chromium, релиз v153.0.0 // GitHub. URL: https://github.com/Sparticuz/chromium/releases/tag/v153.0.0',
    'playwright': 'Playwright for Python : документация. URL: https://playwright.dev/python/',
}

src = SRC.read_text(encoding='utf-8')
meta = dict(re.findall(r'<!--\s*(\w+):\s*(.*?)\s*-->', src))
src = re.sub(r'<!--\s*\w+:.*?-->\n?', '', src)

# --- 1. нумерация источников по первому упоминанию -------------------------------------------
order = []
def cite(m):
    key = m.group(1)
    if key not in SOURCES:
        sys.exit(f'нет источника с ключом {key}')
    if key not in order:
        order.append(key)
    return f'[{order.index(key) + 1}]'
src = re.sub(r'\[@([a-z0-9-]+)\]', cite, src)
unused = sorted(set(SOURCES) - set(order))
sources_html = '<ol class="sources">' + ''.join(f'<li id="src-{i + 1}">{html.escape(SOURCES[k])}</li>' for i, k in enumerate(order)) + '</ol>'
sources_md = '\n'.join(f'{i + 1}. {SOURCES[k]}' for i, k in enumerate(order))
src = src.replace('[[sources]]', sources_html)
OUT_MD.parent.mkdir(exist_ok=True)
OUT_MD.write_text(
    f"<!-- title: {meta['title']} -->\n<!-- subtitle: {meta['subtitle']} -->\n<!-- date: {meta['date']} -->\n\n"
    + src.replace(sources_html, sources_md), encoding='utf-8')

# --- 2. Markdown → HTML -----------------------------------------------------------------------
md = markdown.Markdown(extensions=['tables', 'attr_list', 'md_in_html'])
body = md.convert(src)
body = re.sub(r'(?<![\w"=/-])\[(\d{1,3})\](?!\()', lambda m: f'<a class="cite" href="#src-{m.group(1)}">{m.group(1)}</a>', body)

# --- 3. графики --------------------------------------------------------------------------------
def clamp_px(vw, lo, base, slope, hi):
    return max(lo, min(hi, base + slope * vw / 100))
widths = list(range(360, 1601, 40))
FS = [('lg', 18, 16, .625, 20), ('xl', 24, 17.6, .75, 28), ('2xl', 28, 20.8, 1, 32), ('3xl', 32, 24, 1.875, 40),
      ('4xl', 36, 28, 2.5, 48), ('5xl', 48, 32, 5, 64), ('6xl', 60, 40, 6.25, 80)]
PAL = ['#B54A24', '#33505E', '#A9743B', '#1E5B54', '#6B4C9A', '#8B3A62', '#2C7A6F']
CHARTS = {
    'functions': {'type': 'bar', 'height': 420, 'data': {
        'labels': ['color-mix()', ':where()', 'oklch()', ':has()', 'light-dark()', '@layer', '@container', '::backdrop', 'clamp()', '@starting-style', '@property', 'цвета #hex', 'rgba()'],
        'datasets': [{'label': 'Bootstrap 6.0.0-alpha.1', 'data': [312, 302, 262, 148, 83, 63, 36, 24, 22, 9, 8, 5, 10], 'backgroundColor': '#B54A24'},
                     {'label': 'Bootstrap 5.3.8', 'data': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 424, 137], 'backgroundColor': '#33505E'}]},
        'options': {'indexAxis': 'y', 'scales': {'x': {'title': {'display': True, 'text': 'вхождений в bootstrap.css'}}}}},
    'breakpoints': {'type': 'bar', 'height': 360, 'data': {
        'labels': ['sm', 'md', 'lg', 'xl', 'xxl → 2xl'],
        'datasets': [{'label': 'точка перелома v5, px', 'data': [576, 768, 992, 1200, 1400], 'backgroundColor': '#33505E'},
                     {'label': 'точка перелома v6, px', 'data': [576, 768, 1024, 1280, 1536], 'backgroundColor': '#B54A24'},
                     {'label': 'контейнер v5, px', 'data': [540, 720, 960, 1140, 1320], 'backgroundColor': '#9FB3BC'},
                     {'label': 'контейнер v6, px', 'data': [540, 720, 960, 1200, 1440], 'backgroundColor': '#E0A585'}]},
        'options': {'scales': {'y': {'beginAtZero': True, 'title': {'display': True, 'text': 'пиксели'}}}}},
    'spacers': {'type': 'bar', 'height': 340, 'data': {
        'labels': [str(i) for i in range(13)],
        'datasets': [{'label': 'v5, rem', 'data': [0, .25, .5, 1, 1.5, 3, None, None, None, None, None, None, None], 'backgroundColor': '#33505E'},
                     {'label': 'v6, rem', 'data': [0, .25, .375, .5, .75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 3], 'backgroundColor': '#B54A24'}]},
        'options': {'scales': {'x': {'title': {'display': True, 'text': 'ключ в классе (p-N, m-N, g-N)'}}, 'y': {'title': {'display': True, 'text': 'rem'}}}}},
    'fontsizes': {'type': 'line', 'height': 380, 'data': {
        'labels': widths,
        'datasets': [{'label': f'fs-{n}', 'data': [round(clamp_px(w, lo, b, s, hi), 1) for w in widths], 'borderColor': PAL[i], 'backgroundColor': PAL[i], 'pointRadius': 0, 'borderWidth': 2, 'tension': 0}
                     for i, (n, lo, b, s, hi) in enumerate(FS)]},
        'options': {'scales': {'x': {'title': {'display': True, 'text': 'ширина окна, px'}, 'ticks': {'maxTicksLimit': 9}}, 'y': {'title': {'display': True, 'text': 'размер шрифта, px'}}}}},
    'sizes': {'type': 'bar', 'height': 360, 'data': {
        'labels': ['CSS min', 'CSS min + gzip', 'JS bundle min', 'JS bundle + gzip', 'JS без зависимостей min', 'JS без зависимостей + gzip'],
        'datasets': [{'label': 'Bootstrap 5.3.8', 'data': [226, 30, 78, 23, 59, 16], 'backgroundColor': '#33505E'},
                     {'label': 'Bootstrap 6.0.0-alpha.1', 'data': [372, 50, 214, 58, 137, 34], 'backgroundColor': '#B54A24'}]},
        'options': {'scales': {'y': {'beginAtZero': True, 'title': {'display': True, 'text': 'килобайты'}}}}},
}
chart_n = [0]
def chart_fig(m):
    key, caption = m.group(1), m.group(2)
    chart_n[0] += 1
    h = CHARTS[key]['height']
    return (f'<figure class="chart"><div class="chart-box" style="height:{h}px"><canvas id="chart-{key}" role="img" aria-label="{html.escape(caption)}"></canvas></div>'
            f'<figcaption>{caption}</figcaption></figure>')
body = re.sub(r'<div class="chart" data-chart="([a-z]+)" data-caption="([^"]+)"></div>', chart_fig, body)

# --- 4. схемы (SVG) ----------------------------------------------------------------------------
INK, SOFT, LINE, ACC, STEEL, PAPER, WARM = '#171A1C', '#565D60', '#C7CABC', '#B54A24', '#33505E', '#FBFBF8', '#A9743B'
def box(x, y, w, h, title, sub='', fill=PAPER, stroke=LINE, tc=INK, mono=False, r=3):
    f = "font-family:'JetBrains Mono',ui-monospace,monospace;font-size:12.5px" if mono else "font-family:'Manrope',system-ui,sans-serif;font-size:13.5px;font-weight:600"
    t = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"/>'
    ty = y + h / 2 + (-3 if sub else 5)
    t += f'<text x="{x + w / 2}" y="{ty}" text-anchor="middle" fill="{tc}" style="{f}">{html.escape(title)}</text>'
    if sub:
        t += f'<text x="{x + w / 2}" y="{ty + 17}" text-anchor="middle" fill="{SOFT}" style="font-family:\'Manrope\',system-ui,sans-serif;font-size:12px">{html.escape(sub)}</text>'
    return t
def arrow(x1, y1, x2, y2, color=STEEL):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.5" marker-end="url(#arr)"/>'
def label(x, y, text, color=SOFT, anchor='middle', size=12, mono=False):
    f = "font-family:'JetBrains Mono',ui-monospace,monospace" if mono else "font-family:'Manrope',system-ui,sans-serif"
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{color}" style="{f};font-size:{size}px">{html.escape(text)}</text>'
DEFS = f'<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{STEEL}"/></marker></defs>'

def diagram_tokens():
    s = [f'<svg viewBox="0 0 1100 420" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Путь токена от карты Sass до компонента">{DEFS}']
    s.append(label(60, 30, 'до сборки · Sass', ACC, 'start', 12))
    s.append(label(640, 30, 'в браузере · CSS', ACC, 'start', 12))
    s.append(f'<line x1="600" y1="15" x2="600" y2="400" stroke="{LINE}" stroke-dasharray="4 5"/>')
    s.append(box(40, 60, 240, 70, '$root-tokens, $alert-tokens', 'карты токенов ядра', mono=True))
    s.append(box(40, 170, 240, 70, '@use "bootstrap" with (…)', 'карты проекта', mono=True))
    s.append(box(330, 110, 220, 76, 'defaults()', 'сливает карты, null удаляет ключ'))
    s.append(arrow(280, 95, 330, 138)); s.append(arrow(280, 205, 330, 160))
    s.append(box(330, 250, 220, 60, '@include tokens()', 'выводит переменные', mono=True))
    s.append(arrow(440, 186, 440, 250))
    s.append(box(330, 340, 220, 50, 'PostCSS: префикс bs-', '', mono=True))
    s.append(arrow(440, 310, 440, 340))
    s.append(box(640, 60, 200, 70, ':root, :host', '--bs-spacer, --bs-blue-500…', fill='#E9EEF0', mono=True))
    s.append(box(640, 170, 200, 70, '.theme-primary', '--bs-theme-bg: var(--bs-primary-bg)', fill='#F1E7D8', mono=True))
    s.append(box(640, 280, 200, 70, '.alert, .btn-solid', '--bs-alert-bg: var(--bs-theme-bg-subtle)', fill='#E4EDE9', mono=True))
    s.append(arrow(550, 365, 740, 365)); s.append(arrow(740, 365, 740, 350)); 
    s.append(arrow(740, 130, 740, 170)); s.append(arrow(740, 240, 740, 280))
    s.append(box(890, 60, 180, 70, 'правка в CSS', ':root { --bs-spacer: 1.5rem }', fill=PAPER, mono=True))
    s.append(box(890, 170, 180, 70, 'правка скриптом', 'el.style.setProperty(…)', fill=PAPER, mono=True))
    s.append(box(890, 280, 180, 70, 'data-bs-theme', 'light-dark() выбирает значение', fill=PAPER, mono=True))
    s.append(arrow(890, 95, 840, 95)); s.append(arrow(890, 205, 840, 205)); s.append(arrow(890, 315, 840, 315))
    s.append(label(740, 410, 'компонент читает токен темы, а не цвет', SOFT, 'middle', 12))
    s.append('</svg>'); return ''.join(s)

def diagram_layers():
    layers = [('colors', '208 цветовых токенов'), ('config', 'флаги и карты'), ('root', 'глобальные токены, color-scheme'), ('reboot', 'нормализация'),
              ('layout', 'контейнеры, сетка'), ('content', 'типографика, таблицы, prose'), ('forms', 'поля, флажки, комбобокс'), ('components', '25 компонентов'),
              ('custom', 'пусто — для стилей проекта'), ('helpers', 'hstack, hover-lift, visually-hidden'), ('utilities', 'верхний слой: всегда побеждает')]
    s = [f'<svg viewBox="0 0 1100 470" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Одиннадцать слоёв каскада">{DEFS}']
    y = 430
    for i, (name, sub) in enumerate(layers):
        w = 420 + i * 22; x = 80
        fill = '#F1E7D8' if name == 'custom' else ('#E9EEF0' if name == 'utilities' else PAPER)
        s.append(f'<rect x="{x}" y="{y - 34}" width="{w}" height="32" rx="3" fill="{fill}" stroke="{LINE}"/>')
        s.append(label(x + 14, y - 13, f'{i + 1:02d}  {name}', INK, 'start', 13, mono=True))
        s.append(label(x + w - 14, y - 13, sub, SOFT, 'end', 12))
        y -= 38
    s.append(f'<line x1="800" y1="40" x2="800" y2="420" stroke="{STEEL}" stroke-width="1.5" marker-end="url(#arr)" transform="rotate(180 800 230)"/>')
    s.append(label(820, 60, 'приоритет растёт', STEEL, 'start', 12))
    s.append(label(820, 80, 'снизу вверх', STEEL, 'start', 12))
    s.append(label(820, 130, 'правило слоя utilities', SOFT, 'start', 12)); s.append(label(820, 148, 'перекроет правило components,', SOFT, 'start', 12)); s.append(label(820, 166, 'как бы ни был длинен селектор', SOFT, 'start', 12))
    s.append(label(820, 220, 'стили демо-сайта Bootstrap 6', SOFT, 'start', 12)); s.append(label(820, 238, 'лежат в слое custom:', SOFT, 'start', 12)); s.append(label(820, 256, 'выше компонентов, ниже утилит', SOFT, 'start', 12))
    s.append(label(820, 310, 'AGENTS.md перечисляет ещё слой', SOFT, 'start', 12)); s.append(label(820, 328, 'theme — в коде его нет (Р-03)', SOFT, 'start', 12))
    s.append('</svg>'); return ''.join(s)

def diagram_components():
    rows = [('Modal', 'Dialog', '<dialog>, ::backdrop'), ('Offcanvas', 'Drawer', '<dialog>, свайп'), ('Dropdown', 'Menu', 'Floating UI, подменю'),
            ('Accordion + Collapse', 'Accordion', '<details name>, interpolate-size'), ('Carousel (float, JS)', 'Carousel', 'scroll-snap, несколько слайдов'),
            ('.btn-primary', 'btn-solid + theme-*', 'композиция формы и темы'), ('navbar-collapse', 'navbar + drawer', 'меню в ящике'),
            ('.form-check', 'check / radio / switch', 'маски, :has()'), ('.form-select', 'form-control', 'слияние'), ('Popper', 'Floating UI', 'зависимость')]
    news = ['Stepper', 'Avatar', 'Chip, Chip input', 'Combobox', 'OTP input', 'Password strength', 'Range (JS)', 'Datepicker', 'Nav overflow', 'Toggler', 'Form field', 'Form adorn', 'Prose', 'Hover lift']
    H = 70 + len(rows) * 36 + 120
    s = [f'<svg viewBox="0 0 1100 {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Соответствие компонентов пятой и шестой версий">{DEFS}']
    s.append(label(60, 30, 'пятая версия', ACC, 'start')); s.append(label(430, 30, 'шестая версия', ACC, 'start')); s.append(label(720, 30, 'на чём построено', ACC, 'start'))
    y = 50
    for a, b, c in rows:
        s.append(f'<rect x="60" y="{y}" width="300" height="28" rx="3" fill="{PAPER}" stroke="{LINE}"/>'); s.append(label(74, y + 19, a, INK, 'start', 13, True))
        s.append(arrow(360, y + 14, 420, y + 14))
        s.append(f'<rect x="430" y="{y}" width="260" height="28" rx="3" fill="#E4EDE9" stroke="{LINE}"/>'); s.append(label(444, y + 19, b, INK, 'start', 13, True))
        s.append(label(720, y + 19, c, SOFT, 'start', 12))
        y += 36
    y += 20
    s.append(label(60, y, 'новое в шестой версии', ACC, 'start')); y += 14
    x = 60
    for n in news:
        w = 26 + len(n) * 7.6
        if x + w > 1060: x = 60; y += 36
        s.append(f'<rect x="{x}" y="{y}" width="{w:.0f}" height="28" rx="14" fill="#F1E7D8" stroke="{LINE}"/>'); s.append(label(x + w / 2, y + 19, n, INK, 'middle', 12.5, True))
        x += w + 10
    s.append('</svg>'); return ''.join(s)

def diagram_site():
    pages = [('Главная', 'герой clamp(), Grid 8+4,', 'контейнерные запросы'), ('Рубрика', 'nav-overflow, комбобокс,', 'lg:drawer, скелеты'),
             ('Статья', 'prose, <dialog>,', '<details>, чипы'), ('Компоненты', 'кнопки форма×тема,', 'диалоги, меню, карусель'),
             ('Формы', 'form-field, комбобокс,', 'otp, strength, календарь'), ('Токены', 'палитра 16×13, темы,', 'перестройка, слои'),
             ('Редакция', 'колонка → ящик,', 'степпер, таблица')]
    s = [f'<svg viewBox="0 0 1100 330" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Карта демо-сайта">{DEFS}']
    s.append(box(430, 20, 240, 56, 'Демо-сайт Bootstrap 6', 'build_demo.py · каркас + 7 фрагментов', fill='#E9EEF0'))
    for i, (t, a, b) in enumerate(pages):
        x = 20 + i * 152; y = 150
        s.append(arrow(550, 76, x + 68, y))
        s.append(f'<rect x="{x}" y="{y}" width="136" height="110" rx="3" fill="{PAPER}" stroke="{LINE}"/>')
        s.append(label(x + 68, y + 24, t, INK, 'middle', 13.5)); s.append(f'<line x1="{x + 12}" y1="{y + 34}" x2="{x + 124}" y2="{y + 34}" stroke="{LINE}"/>')
        s.append(label(x + 68, y + 58, a, SOFT, 'middle', 10)); s.append(label(x + 68, y + 76, b, SOFT, 'middle', 10))
    s.append(label(550, 300, 'общее: навбар с md:navbar-expand и меню в ящике · переключатель схемы · site.css в @layer custom · 43 снимка в Chromium 153', SOFT, 'middle', 12))
    s.append('</svg>'); return ''.join(s)

DIAGRAMS = {'tokens': diagram_tokens, 'layers': diagram_layers, 'components': diagram_components, 'site': diagram_site}
def diagram_fig(m):
    key, caption = m.group(1), m.group(2)
    return f'<figure class="diagram">{DIAGRAMS[key]()}<figcaption>{caption}</figcaption></figure>'
body = re.sub(r'<div class="diagram" data-diagram="([a-z]+)" data-caption="([^"]+)"></div>', diagram_fig, body)

# --- 5. главы ---------------------------------------------------------------------------------
parts = re.split(r'(?=<h2 )', body)
sections = parts[1:]
apparatus = {'glossariy', 'reestry', 'ukazatel', 'istochniki'}
short = {'rezyume': 'резюме', 'anons': 'анонс', 'porog': 'порог', 'arhitektura': 'архитектура', 'cvet': 'цвет', 'setka': 'сетка',
         'komponenty': 'компоненты', 'formy': 'формы', 'javascript': 'javascript', 'agenty': 'агенты', 'sayt': 'сайт',
         'reshenija': 'решения', 'lovushki': 'ловушки', 'joomla': 'joomla', 'rekomendatsii': 'рекомендации',
         'glossariy': 'глоссарий', 'reestry': 'реестры', 'ukazatel': 'указатель', 'istochniki': 'источники'}
nav, rail, out = [], [], []
n = 0
for sec in sections:
    m = re.match(r'<h2 id="([^"]+)">(.*?)</h2>', sec, re.S)
    sid, title = m.group(1), m.group(2)
    rest = sec[m.end():]
    if sid in apparatus:
        eyebrow, num = 'служебный аппарат', ''
    else:
        n += 1; num = f'{n:02d}'; eyebrow = f'глава {num}'
    nav.append(f'<a href="#{sid}">{short.get(sid, title)}</a>')
    if num:
        rail.append(f'<a href="#{sid}" title="{html.escape(title)}">{num}</a>')
    cls = 'section apparatus' if sid in apparatus else 'section'
    out.append(f'<section id="{sid}" class="{cls}"><div class="wrap"><div class="section-head"><p class="eyebrow">{eyebrow}</p><h2>{title}</h2></div><div class="prose">{rest}</div></div></section>')

title, subtitle, date = meta['title'], meta['subtitle'], meta['date']

CSS = r"""
:root{--paper:#F3F4EF;--paper-raised:#FBFBF8;--ink:#171A1C;--ink-soft:#565D60;--ink-faint:#8B9190;--line:#DBDDD2;--line-strong:#C7CABC;--accent:#B54A24;--accent-ink:#7C3216;--steel:#33505E;--steel-soft:#DEE6E7;--serif:'Newsreader',Georgia,serif;--sans:'Manrope',system-ui,sans-serif;--mono:'JetBrains Mono',ui-monospace,monospace;--container:1120px;}
*,*::before,*::after{box-sizing:border-box}
html{background:var(--paper);scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased}
section[id]{scroll-margin-top:84px}
a{color:inherit}
.wrap{max-width:var(--container);margin:0 auto;padding:0 40px}
@media (max-width:720px){.wrap{padding:0 22px}}
.progress-track{position:fixed;top:0;left:0;width:100%;height:2px;background:var(--line);z-index:200}
.progress-fill{height:100%;width:0%;background:var(--accent)}
.topnav{position:sticky;top:2px;z-index:190;background:rgba(243,244,239,.92);backdrop-filter:blur(6px);border-bottom:1px solid var(--line)}
.topnav-inner{max-width:var(--container);margin:0 auto;padding:0 40px;display:flex;align-items:center;gap:28px;height:56px}
@media (max-width:720px){.topnav-inner{padding:0 22px;gap:18px}}
.topnav-mark{font-family:var(--mono);font-size:12px;letter-spacing:.03em;color:var(--ink);white-space:nowrap;text-decoration:none;font-weight:500}
.topnav-links{display:flex;gap:2px;overflow-x:auto;scrollbar-width:none}
.topnav-links::-webkit-scrollbar{display:none}
.topnav-links a{font-family:var(--mono);font-size:12px;white-space:nowrap;color:var(--ink-soft);text-decoration:none;padding:8px 10px;border-radius:2px;transition:color .15s,background-color .15s}
.topnav-links a:hover{color:var(--ink);background:var(--steel-soft)}
.topnav-links a.active{color:var(--accent-ink);font-weight:600}
.side-rail{position:fixed;right:22px;top:50%;transform:translateY(-50%);z-index:150;display:flex;flex-direction:column;gap:8px}
.side-rail a{font-family:var(--mono);font-size:10px;color:var(--ink-faint);text-decoration:none;width:24px;height:24px;display:flex;align-items:center;justify-content:center;border:1px solid transparent;border-radius:50%;transition:all .2s}
.side-rail a:hover{border-color:var(--line-strong);color:var(--ink)}
.side-rail a.active{color:var(--paper);background:var(--accent);border-color:var(--accent)}
@media (max-width:1240px){.side-rail{display:none}}
.hero-report{position:relative;overflow:hidden;padding:110px 0 80px}
.hero-report::before{content:"";position:absolute;inset:0;pointer-events:none;background-image:linear-gradient(rgba(23,26,28,.055) 1px,transparent 1px),linear-gradient(90deg,rgba(23,26,28,.055) 1px,transparent 1px);background-size:56px 56px;-webkit-mask-image:linear-gradient(to bottom,black,transparent 82%);mask-image:linear-gradient(to bottom,black,transparent 82%)}
.hero-inner{position:relative}
.eyebrow{font-family:var(--mono);font-size:12px;letter-spacing:.06em;color:var(--steel);margin:0 0 20px}
.hero-report h1{font-family:var(--serif);font-weight:500;font-size:clamp(2.4rem,5.6vw,4.4rem);line-height:1.04;letter-spacing:-.01em;margin:0 0 26px;max-width:16ch}
.hero-lead{font-size:19px;max-width:680px;margin:0 0 18px;line-height:1.6}
.hero-sub{font-size:15px;color:var(--ink-soft);max-width:640px;margin:0 0 36px}
.hero-links{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 36px}
.hero-links a{font-family:var(--mono);font-size:12px;text-decoration:none;color:var(--accent-ink);border:1px solid var(--line-strong);background:var(--paper-raised);padding:8px 12px;border-radius:2px}
.hero-links a:hover{border-color:var(--accent)}
.method-box{border:1px solid var(--line-strong);background:var(--paper-raised);padding:22px 26px;max-width:780px;border-radius:2px}
.method-box .eyebrow{margin-bottom:10px}
.method-box p{margin:0;font-size:14px;color:var(--ink-soft);line-height:1.65}
.section{padding:72px 0;border-top:1px solid var(--line)}
.section.apparatus{background:var(--paper-raised)}
.section-head{max-width:760px;margin-bottom:34px}
.section-head .eyebrow{margin-bottom:14px}
.section-head h2{font-family:var(--serif);font-weight:500;font-size:clamp(1.7rem,3.2vw,2.3rem);letter-spacing:-.01em;margin:0;line-height:1.15}
.prose > p,.prose > ol,.prose > ul,.prose > h3,.prose > dl{max-width:780px}
.prose p{margin:0 0 1.1em;font-size:16.5px;line-height:1.7}
.prose h3{font-family:var(--serif);font-weight:500;font-size:1.45rem;margin:2.2em 0 .7em;line-height:1.2}
.prose ol,.prose ul{padding-left:1.3em;margin:0 0 1.2em}
.prose li{margin:.35em 0;line-height:1.6}
.prose code{font-family:var(--mono);font-size:.86em;background:var(--steel-soft);padding:1px 5px;border-radius:2px;overflow-wrap:anywhere}
.prose strong{font-weight:700}
.prose table{border-collapse:collapse;width:100%;max-width:100%;margin:1.4em 0 1.8em;font-size:14.5px;display:block;overflow-x:auto}
.prose th,.prose td{text-align:left;vertical-align:top;padding:9px 12px;border-bottom:1px solid var(--line)}
.prose th{font-family:var(--mono);font-size:11.5px;letter-spacing:.04em;color:var(--steel);font-weight:600;border-bottom:1px solid var(--line-strong)}
.prose tr:hover td{background:rgba(222,230,231,.35)}
a.cite{font-family:var(--mono);font-size:.72em;color:var(--accent-ink);text-decoration:none;vertical-align:super;line-height:0;padding:0 1px}
a.cite:hover{text-decoration:underline}
figure.diagram,figure.chart,figure.shot{margin:2em 0 2.2em;padding:18px 14px 12px;border:1px solid var(--line);background:var(--paper-raised);border-radius:2px}
figure.diagram svg{width:100%;height:auto;display:block}
figure figcaption{font-size:13.5px;color:var(--ink-soft);margin:12px 6px 0;line-height:1.55}
.chart-box{position:relative;width:100%}
figure.shot img{display:block;width:100%;height:auto;border:1px solid var(--line)}
figure.shot a{display:block}
figure.shot.shot-tall a{max-height:640px;overflow:auto;border:1px solid var(--line)}
figure.shot.shot-tall img{border:0}
dl.glossary dt{font-weight:700;margin-top:1.1em}
dl.glossary dd{margin:.3em 0 0;color:var(--ink);font-size:15.5px;line-height:1.65}
ol.sources{font-size:14px;line-height:1.55;padding-left:2.2em;max-width:900px}
ol.sources li{margin:.45em 0;overflow-wrap:anywhere}
ol.sources li:target{background:var(--steel-soft);outline:2px solid var(--steel-soft)}
.closing{padding:60px 0 56px;border-top:1px solid var(--line)}
.closing-box{max-width:820px;padding:28px 32px;border:1px solid var(--line-strong);background:var(--paper-raised);border-radius:2px}
.closing-box p{margin:0 0 .6em;font-size:15px;line-height:1.7}
.closing-box p:last-child{margin:0;color:var(--ink-soft);font-size:13.5px}
@media print{.progress-track,.topnav,.side-rail{display:none}.section{padding:28px 0;page-break-inside:avoid}figure.shot.shot-tall a{max-height:none;overflow:visible}}
"""

JS = r"""
(function(){
  var fill=document.getElementById('progressFill');
  function up(){var h=document.documentElement;var s=h.scrollHeight-h.clientHeight;fill.style.width=(s>0?(h.scrollTop/s)*100:0)+'%';}
  document.addEventListener('scroll',up,{passive:true});up();
  var secs=[].slice.call(document.querySelectorAll('section[id]'));
  var links=[].slice.call(document.querySelectorAll('.topnav-links a, .side-rail a'));
  function setActive(id){links.forEach(function(a){a.classList.toggle('active',a.getAttribute('href')==='#'+id);});}
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){setActive(e.target.id);}});},{rootMargin:'-40% 0px -55% 0px',threshold:0});
    secs.forEach(function(s){io.observe(s);});
  }
  var CH=__CHARTS__;
  Chart.defaults.font.family="'Manrope',system-ui,sans-serif";Chart.defaults.color='#565D60';Chart.defaults.borderColor='#DBDDD2';
  Object.keys(CH).forEach(function(k){var c=document.getElementById('chart-'+k);if(!c)return;var cfg=CH[k];
    var opt=Object.assign({responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'bottom',labels:{boxWidth:12}},tooltip:{mode:'index',intersect:false}},interaction:{mode:'index',intersect:false}},cfg.options||{});
    new Chart(c,{type:cfg.type,data:cfg.data,options:opt});});
})();
"""
JS = JS.replace('__CHARTS__', json.dumps({k: {'type': v['type'], 'data': v['data'], 'options': v['options']} for k, v in CHARTS.items()}, ensure_ascii=False))

doc = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)} — {html.escape(subtitle)}</title>
<meta name="description" content="Исследование-доклад о Bootstrap 6.0.0-alpha.1: архитектура токенов и слоёв, цвет в oklch, сетка с префиксами и контейнерными запросами, компоненты на нативных элементах, формы, JavaScript на ESM, навыки для агентов — проверено на смоделированном новостном сайте на Bootstrap 6 с 43 снимками в Chromium 153.">
<meta name="author" content="Бейбит Саханов">
<link rel="canonical" href="{CANONICAL}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(subtitle)}. {html.escape(date)}.">
<meta property="og:type" content="article">
<meta property="og:url" content="{CANONICAL}">
<meta property="og:image" content="https://bsakhanov.github.io/bootstrap-6-research/skrinshoty/preview/e08-geroi.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Manrope:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="progress-track"><div class="progress-fill" id="progressFill"></div></div>
<nav class="topnav" aria-label="Оглавление"><div class="topnav-inner">
<a class="topnav-mark" href="#top">bootstrap 6 · смоделированный сайт</a>
<div class="topnav-links">{''.join(nav)}</div>
</div></nav>
<aside class="side-rail" aria-hidden="true">{''.join(rail)}</aside>
<header class="hero-report" id="top"><div class="wrap hero-inner">
<p class="eyebrow">исследование-доклад · {html.escape(date)}</p>
<h1>{html.escape(title)}</h1>
<p class="hero-lead">{html.escape(subtitle).capitalize()}: что шестое поколение переносит из препроцессора в браузер, чем это оплачено и как это выглядит на семи страницах вымышленного издания — демо-сайта Bootstrap 6.</p>
<p class="hero-sub">Автор — Бейбит Саханов, Астана. Факты сверены по анонсу, документации и исходному коду ветки main на 8–9 октября 2026 года; расхождения и белые пятна вынесены в реестры, а не спрятаны в тексте.</p>
<div class="hero-links"><a href="../demo/index.html">демо-сайт Bootstrap 6</a><a href="../skrinshoty/">сайт в скриншотах</a><a href="https://github.com/bsakhanov/bootstrap-6-research">репозиторий</a><a href="https://bsakhanov.github.io/joomla-6-newsroom-research/">предыдущий доклад: Joomla 6</a></div>
<div class="method-box"><p class="eyebrow">метод</p><p>Источники — анонс проекта, 141 файл документации, исходный код Sass и TypeScript ветки main, пакеты npm шестой альфы и версии 5.3.8. Статистика CSS посчитана по скомпилированным файлам скриптом из репозитория исследования. Утверждения о вёрстке проверены на смоделированном сайте из семи страниц в Chromium 153 через Playwright. Каждое утверждение несёт номер источника; список построен по первому упоминанию. Текст прошёл четыре прохода языкового прогона и вычитку Редколлегией.</p></div>
</div></header>
<main>
{''.join(out)}
</main>
<footer class="closing"><div class="wrap"><div class="closing-box">
<p>Доклад подготовлен как основание для решения о сроках и способе перехода на Bootstrap 6. Рекомендации главы пятнадцатой самодостаточны; главы о цвете, сетке и ловушках годятся как памятка верстальщику при миграции.</p>
<p>{html.escape(date)} · Бейбит Саханов · тексты и схемы — CC BY 4.0, демо-сайт и инструменты — MIT</p>
</div></div></footer>
<script>{CHARTJS}</script>
<script>{JS}</script>
</body>
</html>
"""
OUT_HTML.parent.mkdir(exist_ok=True)
OUT_HTML.write_text(doc, encoding='utf-8')
words = len(re.findall(r'\w+', re.sub(r'<[^>]+>', ' ', body)))
print(f'written {OUT_HTML.name}: {len(doc)} chars, {n} глав, {len(order)} источников, {chart_n[0]} графиков, ~{words} слов')
if unused:
    print('не использованы ключи:', ', '.join(unused))
