#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_demo.py — собирает демонстрационный сайт «Шестая полоса» на Bootstrap 6.0.0-alpha.1.

Каждая страница лежит фрагментом в tools/demo/pages/<имя>.html: первая строка — заголовок,
вторая — описание, дальше содержимое <main>. Сборщик оборачивает фрагмент общим каркасом:
шапка на .navbar с drawer-меню, переключатель цветовой схемы, спрайт иконок, подвал.
Bootstrap подключён локально (demo/assets/bootstrap), чтобы сайт открывался без сети.
"""
import datetime, html, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
PAGES = ROOT / 'tools/demo/pages'
OUT = ROOT / 'demo'
VERSION = '1.0.3'
STAMP = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')

NAV = [('index', 'Главная'), ('rubrika', 'Рубрика'), ('statya', 'Статья'),
       ('komponenty', 'Компоненты'), ('formy', 'Формы'), ('tokeny', 'Токены'), ('redakciya', 'Редакция')]

ICONS = """<svg xmlns="http://www.w3.org/2000/svg" class="d-none" aria-hidden="true">
<symbol id="i-search" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="10.5" cy="10.5" r="7"/><path d="M21 21l-5-5"/></symbol>
<symbol id="i-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></symbol>
<symbol id="i-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></symbol>
<symbol id="i-half" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 0 1 0 18z" fill="currentColor"/></symbol>
<symbol id="i-chevron-right" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 3 5 5-5 5"/></symbol>
<symbol id="i-chevron-down" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m3 6 5 5 5-5"/></symbol>
<symbol id="i-arrow-right" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 8h12M9 3l5 5-5 5"/></symbol>
<symbol id="i-check" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m2 8 4 4 8-8"/></symbol>
<symbol id="i-x" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 4l8 8M12 4l-8 8"/></symbol>
<symbol id="i-plus" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M8 3v10M3 8h10"/></symbol>
<symbol id="i-dots" viewBox="0 0 16 16" fill="currentColor"><circle cx="3" cy="8" r="1.6"/><circle cx="8" cy="8" r="1.6"/><circle cx="13" cy="8" r="1.6"/></symbol>
<symbol id="i-person" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></symbol>
<symbol id="i-calendar" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></symbol>
<symbol id="i-share" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m8.6 13.5 6.8 4M15.4 6.5l-6.8 4"/></symbol>
<symbol id="i-bell" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9a6 6 0 0 1 12 0c0 7 3 8 3 8H3s3-1 3-8M10 21a2 2 0 0 0 4 0"/></symbol>
<symbol id="i-mail" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></symbol>
<symbol id="i-pencil" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20h4l10.5-10.5a2.1 2.1 0 0 0-3-3L5 17z"/></symbol>
<symbol id="i-trash" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3"/></symbol>
<symbol id="i-filter" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 5h18l-7 8v6l-4-2v-4z"/></symbol>
<symbol id="i-lock" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></symbol>
<symbol id="i-clock" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></symbol>
<symbol id="i-layers" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="m12 3 9 5-9 5-9-5zM3 13l9 5 9-5M3 17l9 5 9-5"/></symbol>
<symbol id="i-menu" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></symbol>
</svg>"""


def navbar(active):
    items = ''.join(
        f'<li class="nav-item"><a class="nav-link{" active" if key == active else ""}"'
        f'{" aria-current=\"page\"" if key == active else ""} href="{key}.html">{label}</a></li>'
        for key, label in NAV)
    return f"""<header class="sticky-top">
<nav class="navbar md:navbar-expand bg-1 border-bottom border-subtle" aria-label="Главное меню">
  <div class="container">
    <a class="navbar-brand fw-semibold d-flex align-items-center" href="index.html"><span class="sp-mark" aria-hidden="true">B</span>Bootstrap 6<span class="badge badge-subtle theme-primary ms-2">демо</span></a>
    <button class="btn-icon navbar-toggler" type="button" data-bs-toggle="drawer" data-bs-target="#navDrawer" aria-controls="navDrawer" aria-expanded="false" aria-label="Открыть меню">
      <span class="navbar-toggler-icon" aria-hidden="true"></span>
    </button>
    <dialog class="drawer drawer-end" tabindex="-1" id="navDrawer" aria-labelledby="navDrawerLabel">
      <div class="drawer-header">
        <h5 class="drawer-title" id="navDrawerLabel">Меню</h5>
        <button type="button" class="btn-close" data-bs-dismiss="drawer" aria-label="Закрыть"></button>
      </div>
      <div class="drawer-body">
        <ul class="nav navbar-nav me-auto">{items}</ul>
        <div class="d-flex align-items-center gap-3 mt-5 md:mt-0">
          <div class="position-relative">
            <button class="btn-icon btn-subtle theme-secondary" type="button" data-bs-toggle="menu" aria-expanded="false" aria-label="Цветовая схема" id="themeToggle">
              <svg class="sp-icon" width="18" height="18"><use href="#i-half"/></svg>
            </button>
            <div class="menu">
              <button class="menu-item" type="button" data-sp-theme="light"><svg class="sp-icon me-2" width="16" height="16"><use href="#i-sun"/></svg>Светлая</button>
              <button class="menu-item" type="button" data-sp-theme="dark"><svg class="sp-icon me-2" width="16" height="16"><use href="#i-moon"/></svg>Тёмная</button>
              <button class="menu-item active" type="button" data-sp-theme="auto"><svg class="sp-icon me-2" width="16" height="16"><use href="#i-half"/></svg>Как в системе</button>
            </div>
          </div>
          <a class="btn-solid theme-primary btn-sm" href="formy.html">Подписаться</a>
        </div>
      </div>
    </dialog>
  </div>
</nav>
</header>"""


FOOTER = """<footer class="border-top border-subtle bg-1 mt-12">
  <div class="container py-9">
    <div class="row g-7">
      <div class="md:col-5">
        <p class="fw-semibold mb-2"><span class="sp-mark" aria-hidden="true">B</span>Bootstrap 6 демо</p>
        <p class="fg-2 fs-sm mb-3">Вымышленное сетевое издание, собранное для исследования «Bootstrap 6 на смоделированном сайте». Имена, тексты и цифры придуманы, кроме сведений о самом фреймворке.</p>
        <p class="fg-3 fs-xs mb-0">Bootstrap 6.0.0-alpha.1 · сборка демо {stamp} · редакция {version}</p>
      </div>
      <div class="sm:col-6 md:col-3 md:offset-1">
        <p class="sp-kicker mb-3">Разделы</p>
        <ul class="list-unstyled vstack gap-2 fs-sm">{links}</ul>
      </div>
      <div class="sm:col-6 md:col-3">
        <p class="sp-kicker mb-3">Исследование</p>
        <ul class="list-unstyled vstack gap-2 fs-sm">
          <li><a class="underline-30 hover:underline-100" href="../doklad/bootstrap-6-research.html">Доклад</a></li>
          <li><a class="underline-30 hover:underline-100" href="../skrinshoty/">Сайт в скриншотах</a></li>
          <li><a class="underline-30 hover:underline-100" href="https://github.com/bsakhanov/bootstrap-6-research">Репозиторий</a></li>
          <li><a class="underline-30 hover:underline-100" href="https://getbootstrap.com/docs/6.0/">Документация Bootstrap 6</a></li>
        </ul>
      </div>
    </div>
  </div>
</footer>
<div class="toast-container position-fixed bottom-0 end-0 p-5" id="toastArea" aria-live="polite" aria-atomic="true"></div>"""


def build():
    OUT.mkdir(exist_ok=True)
    built = []
    for key, label in NAV:
        src = (PAGES / f'{key}.html').read_text(encoding='utf-8')
        lines = src.split('\n')
        title, desc = lines[0].strip(), lines[1].strip()
        body = '\n'.join(lines[2:])
        links = ''.join(f'<li><a class="underline-30 hover:underline-100" href="{k}.html">{l}</a></li>' for k, l in NAV)
        page = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} — Bootstrap 6 демо</title>
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(title)} — Bootstrap 6 демо">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<link rel="canonical" href="https://webmarka.kz/research/bootstrap-6/demo/{"" if key == "index" else key + ".html"}">
<meta property="og:url" content="https://webmarka.kz/research/bootstrap-6/demo/{"" if key == "index" else key + ".html"}">
<!-- Bootstrap 6 демо · демонстрационный сайт исследования «Bootstrap 6 на смоделированном сайте» · сборка {STAMP} · редакция {VERSION} -->
<script>try{{var t=localStorage.getItem('sp-theme');if(t&&t!=='auto')document.documentElement.setAttribute('data-bs-theme',t)}}catch(e){{}}</script>
<link rel="stylesheet" href="assets/bootstrap/bootstrap.min.css">
<link rel="stylesheet" href="assets/site.css">
<script type="module" src="assets/bootstrap/bootstrap.bundle.min.js"></script>
<script type="module" src="assets/site.js"></script>
</head>
<body class="bg-body fg-body" data-sp-page="{key}">
{ICONS}
{navbar(key)}
{body}
{FOOTER.replace('{stamp}', STAMP).replace('{version}', VERSION).replace('{links}', links)}
</body>
</html>
"""
        (OUT / f'{key}.html').write_text(page, encoding='utf-8')
        built.append((key, len(page)))
    for k, n in built:
        print(f'{k}.html  {n} chars')


if __name__ == '__main__':
    build()
