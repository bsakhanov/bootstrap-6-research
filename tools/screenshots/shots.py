#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""shots.py — снимает экраны демо-сайта Bootstrap 6 в настоящем Chromium 153 через Playwright.

Запуск: python3 tools/screenshots/shots.py http://127.0.0.1:8077 skrinshoty/img
Требуется бинарник Chromium (переменная CHROMIUM) и python-пакет playwright ≥ 1.56.
Десктоп — 1440×900 при масштабе 2×, телефон — 390×844 при 2×; тёмная схема включается
эмуляцией prefers-color-scheme, как это сделал бы пользователь в системе.
"""
import os, sys, time, pathlib
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8077'
OUT = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else 'skrinshoty/img')
OUT.mkdir(parents=True, exist_ok=True)
CHROMIUM = os.environ.get('CHROMIUM', '/home/claude/chromium/chromium')
ARGS = ['--no-sandbox', '--no-zygote', '--disable-gpu', '--disable-dev-shm-usage',
        '--use-gl=angle', '--use-angle=swiftshader', '--in-process-gpu', '--font-render-hinting=none']
DESK = {'width': 1440, 'height': 900}
MOB = {'width': 390, 'height': 844}

PAGES = [('glavnaya', 'index'), ('rubrika', 'rubrika'), ('statya', 'statya'), ('komponenty', 'komponenty'),
         ('formy', 'formy'), ('tokeny', 'tokeny'), ('redakciya', 'redakciya')]


def settle(pg, ms=700):
    pg.wait_for_load_state('networkidle')
    pg.evaluate('document.fonts.ready')
    pg.wait_for_timeout(ms)


def shot(pg, name, full=True, clip=None):
    path = OUT / f'{name}.png'
    if full and clip is None:
        # липкие шапка и боковые колонки должны стоять на своих местах, а не там, где остановилась прокрутка
        pg.evaluate('window.scrollTo(0, 0)'); pg.wait_for_timeout(250)
    pg.screenshot(path=str(path), full_page=full, clip=clip)
    print('ok', path.name, f'{path.stat().st_size // 1024} KB', flush=True)


def element_shot(pg, selector, name, pad=16):
    el = pg.locator(selector).first
    el.scroll_into_view_if_needed()
    pg.wait_for_timeout(300)
    # clip задаётся в координатах страницы, а bounding_box — в координатах окна: добавляем прокрутку
    box = el.evaluate('e => { const r = e.getBoundingClientRect(); return {x: r.x + scrollX, y: r.y + scrollY, width: r.width, height: r.height} }')
    clip = {'x': max(box['x'] - pad, 0), 'y': max(box['y'] - pad, 0), 'width': box['width'] + 2 * pad, 'height': box['height'] + 2 * pad}
    pg.evaluate('window.scrollTo(0, 0)'); pg.wait_for_timeout(250)  # липкая шапка — на своём месте
    pg.screenshot(path=str(OUT / f'{name}.png'), full_page=True, clip=clip)
    print('ok', f'{name}.png', f'{(OUT / f"{name}.png").stat().st_size // 1024} KB', flush=True)


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROMIUM, headless=True, args=ARGS)

        # --- десктоп, светлая схема, полные страницы --------------------------------------
        ctx = browser.new_context(viewport=DESK, device_scale_factor=2, locale='ru-RU', color_scheme='light')
        pg = ctx.new_page()
        for i, (name, file) in enumerate(PAGES, 1):
            pg.goto(f'{BASE}/{file}.html'); settle(pg)
            shot(pg, f'{i:02d}-{name}')

        # элементы крупным планом
        pg.goto(f'{BASE}/komponenty.html'); settle(pg)
        element_shot(pg, '#c-buttons', 'e01-knopki')
        element_shot(pg, '#c-badges', 'e02-znachki-chipy')
        element_shot(pg, '#c-nav', 'e03-navigaciya-stepper')
        element_shot(pg, '#c-avatars', 'e04-avatary-kartochki')
        pg.goto(f'{BASE}/tokeny.html'); settle(pg)
        element_shot(pg, '#palette', 'e05-palitra')
        element_shot(pg, '#h-layers', 'e06-sloi-zagolovok', pad=0)
        element_shot(pg, 'ol.list-unstyled', 'e06-sloi')
        pg.goto(f'{BASE}/index.html'); settle(pg)
        element_shot(pg, 'header.sticky-top', 'e07-navbar-desktop', pad=0)
        element_shot(pg, '.sp-hero', 'e08-geroi', pad=0)

        # --- интерактивные состояния (видимая область) ---------------------------------
        pg.goto(f'{BASE}/statya.html'); settle(pg)
        pg.click('[data-bs-target="#shareDialog"]'); pg.wait_for_timeout(700)
        shot(pg, '11-statya-dialog', full=False)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(400)

        pg.goto(f'{BASE}/komponenty.html'); settle(pg)
        pg.click('[data-bs-target="#dlgDark"]'); pg.wait_for_timeout(700)
        shot(pg, '12-komponenty-dialog-dark', full=False)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(400)
        pg.locator('#c-menus').scroll_into_view_if_needed(); pg.wait_for_timeout(300)
        pg.locator('#c-menus button[data-bs-toggle="menu"]').first.click(); pg.wait_for_timeout(500)
        sub = pg.locator('#c-menus .submenu > button').first
        try:
            sub.hover(); pg.wait_for_timeout(600)
        except Exception as e:
            print('submenu hover:', e)
        shot(pg, '13-komponenty-menu', full=False)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
        pg.click('[data-bs-target="#drwStart"]'); pg.wait_for_timeout(800)
        shot(pg, '14-komponenty-drawer', full=False)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(400)
        pg.locator('#c-alerts').scroll_into_view_if_needed(); pg.wait_for_timeout(200)
        pg.click('text=Показать тост'); pg.wait_for_timeout(300)
        pg.click('text=Тост с темой success'); pg.wait_for_timeout(300)
        pg.click('text=Тост об ошибке'); pg.wait_for_timeout(600)
        shot(pg, '20-komponenty-tosty', full=False)
        pg.wait_for_timeout(4500)

        pg.goto(f'{BASE}/rubrika.html'); settle(pg)
        pg.click('[data-bs-toggle="combobox"]'); pg.wait_for_timeout(500)
        shot(pg, '15-rubrika-combobox', full=False)
        pg.click('.menu-item[data-bs-value="read"]'); pg.wait_for_timeout(300)
        print('combobox value:', pg.evaluate("document.querySelector('.combobox-value').textContent"))

        pg.goto(f'{BASE}/formy.html'); settle(pg)
        pg.click('#fBirth'); pg.wait_for_timeout(800)
        shot(pg, '16-formy-datepicker', full=False)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
        pg.locator('#fPass').fill('Polosa-6!'); pg.wait_for_timeout(300)
        pg.locator('#fTopics').fill('дизайн'); pg.keyboard.press('Enter'); pg.wait_for_timeout(300)
        pg.locator('#fOtp').fill('482913'); pg.wait_for_timeout(300)
        pg.click('button[type="submit"]'); pg.wait_for_timeout(900)
        shot(pg, '17-formy-validaciya')

        pg.goto(f'{BASE}/tokeny.html'); settle(pg)
        pg.select_option('#tkHue', 'teal'); pg.locator('#tkRadius').fill('1.25'); pg.locator('#tkSpacer').fill('1.25')
        pg.locator('#tkRadius').dispatch_event('input'); pg.locator('#tkSpacer').dispatch_event('input'); pg.locator('#tkHue').dispatch_event('input')
        pg.wait_for_timeout(500)
        element_shot(pg, '[data-sp-playground]', '18-tokeny-perestroika')

        pg.goto(f'{BASE}/index.html'); settle(pg)
        pg.locator('#cqRange').fill('45'); pg.locator('#cqRange').dispatch_event('input'); pg.wait_for_timeout(500)
        element_shot(pg, '#h-cq', '19-glavnaya-cq-zagolovok', pad=0)
        element_shot(pg, '#cqBox', '19-glavnaya-cq-uzkaya')

        pg.goto(f'{BASE}/komponenty.html'); settle(pg)
        pg.locator('#c-carousel').scroll_into_view_if_needed(); pg.wait_for_timeout(300)
        pg.locator('[data-bs-target="#carouselThree"][data-bs-slide="next"]').click(); pg.wait_for_timeout(900)
        element_shot(pg, '#c-carousel', 'e09-karusel')
        ctx.close()

        # --- десктоп, тёмная схема --------------------------------------------------------
        ctx = browser.new_context(viewport=DESK, device_scale_factor=2, locale='ru-RU', color_scheme='dark')
        pg = ctx.new_page()
        pg.goto(f'{BASE}/index.html'); settle(pg); shot(pg, '08-glavnaya-tyomnaya')
        pg.goto(f'{BASE}/redakciya.html'); settle(pg); shot(pg, '09-redakciya-tyomnaya')
        pg.goto(f'{BASE}/komponenty.html'); settle(pg); shot(pg, '10-komponenty-tyomnaya', full=False)
        pg.goto(f'{BASE}/tokeny.html'); settle(pg); element_shot(pg, '#h-semantic', 'e10-temy-tyomnaya-zagolovok', pad=0); element_shot(pg, '#h-semantic + p + .row', 'e10-temy-tyomnaya')
        ctx.close()

        # --- телефон -----------------------------------------------------------------------
        ctx = browser.new_context(viewport=MOB, device_scale_factor=2, locale='ru-RU', color_scheme='light', is_mobile=True, has_touch=True)
        pg = ctx.new_page()
        for i, (name, file) in enumerate(PAGES, 21):
            pg.goto(f'{BASE}/{file}.html'); settle(pg)
            shot(pg, f'{i:02d}-m-{name}')
        pg.goto(f'{BASE}/index.html'); settle(pg)
        pg.click('.navbar-toggler'); pg.wait_for_timeout(800)
        shot(pg, '28-m-menu-drawer', full=False)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
        pg.goto(f'{BASE}/rubrika.html'); settle(pg)
        pg.click('[data-bs-target="#filterDrawer"]'); pg.wait_for_timeout(800)
        shot(pg, '29-m-rubrika-filtry', full=False)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
        pg.goto(f'{BASE}/redakciya.html'); settle(pg)
        pg.click('[data-bs-target="#adminSide"]'); pg.wait_for_timeout(800)
        shot(pg, '30-m-redakciya-razdely', full=False)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
        pg.goto(f'{BASE}/komponenty.html'); settle(pg)
        pg.click('[data-bs-target="#dlgSlide"]'); pg.wait_for_timeout(800)
        shot(pg, '32-m-dialog-snizu', full=False)
        ctx.close()
        ctx = browser.new_context(viewport=MOB, device_scale_factor=2, locale='ru-RU', color_scheme='dark', is_mobile=True, has_touch=True)
        pg = ctx.new_page()
        pg.goto(f'{BASE}/index.html'); settle(pg); shot(pg, '31-m-glavnaya-tyomnaya', full=False)
        pg.goto(f'{BASE}/statya.html'); settle(pg); shot(pg, '33-m-statya-tyomnaya', full=False)
        ctx.close()
        browser.close()


if __name__ == '__main__':
    t = time.time()
    run()
    print(f'done in {time.time() - t:.0f}s')
