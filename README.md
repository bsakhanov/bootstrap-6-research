# Bootstrap 6 на смоделированном сайте

**Исследование-доклад о шестом поколении фреймворка — архитектура, вёрстка, дизайн — проверенное на вымышленном новостном сайте «Шестая полоса» и 43 снимках экрана**

*Редакция 1.0 · 9 октября 2026 · автор — Бейбит Саханов, Астана*

[English version below](#bootstrap-6-on-a-modelled-site)

---

## О чём это

Восьмого октября 2026 года вышел первый альфа-выпуск Bootstrap 6 — через пять лет после пятой версии. Доклад отвечает, чем он силён и годится ли уже сегодня для сайтов, которые живут годами. Как инженерная конструкция — силён: почти каждая переменная Sass стала переменной CSS и меняется в браузере без пересборки, цвета считает сама страница в пространстве oklch, тёмная схема приходит из `light-dark()`, модальные окна и аккордеоны работают на родных `<dialog>` и `<details>`, а каскад разложен по одиннадцати слоям. Как продукт для боевого сайта — пока альфа: интерфейсы могут измениться до беты, порог браузеров поднят до Chrome 130, Firefox 132 и Safari 18 без запасных путей, сжатый CSS потяжелел с 226 до 372 килобайт, а переименованы классы кнопок, окон, меню, сетки и утилит.

Чтобы судить по вёрстке, а не по анонсу, на альфе собран сайт из семи страниц — главная, рубрика, статья, витрина компонентов, формы, площадка токенов и редакционная панель — с единственным файлом собственных стилей, где нет ни одного цвета в hex: всё из токенов ядра. В самой альфе найдены расхождения, которые стоит знать до перехода: тени собраны на относительном цветовом синтаксисе, лежащем по политике проекта выше порога браузеров, а комбобокс при запуске пишет в консоль ошибку о втором экземпляре. Для редакций на Joomla — отдельная глава: ядро везёт Bootstrap пятой ветки, пробовать шестую стоит в дочернем шаблоне и на лонгридах.

## Состав

| папка | что внутри |
|---|---|
| `doklad/` | исследование-доклад: самодостаточный HTML (15 глав, 5 интерактивных графиков, 4 схемы, 58 источников, реестры расхождений и белых пятен, глоссарий) и его Markdown-исходник |
| `demo/` | демо-сайт «Шестая полоса» на Bootstrap 6.0.0-alpha.1 — 7 страниц, Bootstrap подключён локально, собственные стили в `@layer custom` только на токенах |
| `skrinshoty/` | «Сайт в скриншотах»: 43 экрана в Chromium 153 (десктоп 1440 px, телефон 390 px, тёмная схема, открытые состояния) с разбором; оригиналы PNG в масштабе 2× и превью JPEG |
| `redkollegiya/` | отчёт вычитки по методологии языкового прогона (Чуковский → Аграновский ∥ Слопотрон → Розенталь → Мильчин) |
| `tools/` | всё для воспроизведения: сборщик доклада с графиками и схемами, сборщик демо-сайта, снимщик экранов на Playwright, скрипт статистики CSS, обёртка типографа |
| `dist/` | архивы доклада и демо-сайта для скачивания |

## Как смотреть

GitHub Pages: [титульная](https://bsakhanov.github.io/bootstrap-6-research/) · [доклад](https://bsakhanov.github.io/bootstrap-6-research/doklad/bootstrap-6-research.html) · [демо-сайт](https://bsakhanov.github.io/bootstrap-6-research/demo/index.html) · [сайт в скриншотах](https://bsakhanov.github.io/bootstrap-6-research/skrinshoty/). Все HTML-файлы открываются и с диска; демо-сайту для скриптов нужен любой локальный веб-сервер (`python3 -m http.server`), потому что Bootstrap 6 подключается модулем `type="module"`.

Демо-сайт требует браузера не ниже порога Bootstrap 6: Chrome и Edge 130, Firefox 132, Safari 18.

## Метод

Факты взяты из анонса проекта, 141 файла документации, исходного кода Sass и TypeScript ветки `main` (коммит 7771f16 от 8 октября 2026) и пакетов npm шестой альфы и версии 5.3.8; все адреса открыты 8–9 октября 2026 года. Статистика CSS посчитана по скомпилированным файлам (`tools/stats/css_stats.py`). Каждое утверждение несёт номер источника; список построен по первому упоминанию. Расхождения источников (Р) и белые пятна (М) вынесены в реестры. Текст прошёл четыре прохода языкового прогона и вычитку Редколлегией; типографика поставлена детерминированным типографом Мильчина.

## Воспроизведение

```bash
# демо-сайт
npm i bootstrap@6.0.0-alpha.1 && cp node_modules/bootstrap/dist/css/bootstrap.min.css node_modules/bootstrap/dist/js/bootstrap.bundle.min.js demo/assets/bootstrap/
python3 tools/demo/build_demo.py && (cd demo && python3 -m http.server 8077)

# снимки экранов: нужен Chromium (CHROMIUM=/путь/к/chromium) и pip install playwright
CHROMIUM=/opt/chromium/chromium python3 tools/screenshots/shots.py http://127.0.0.1:8077 skrinshoty/img

# доклад и страница скриншотов (pip install markdown pillow; chart.umd.js — из пакета chart.js@4.4.7)
python3 tools/lang/milchin_run.py tools/build/doklad-bootstrap-6.md   # типографика
python3 tools/build/build.py && python3 tools/build/build_shots.py

# статистика CSS/JS для графиков
npm i bootstrap5@npm:bootstrap@5.3.8 && python3 tools/stats/css_stats.py node_modules
```

## Версии

- **1.0** — 9 октября 2026: первая редакция доклада, демо-сайта и разбора в скриншотах.

## Лицензия

Тексты, схемы и снимки — [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.ru); демо-сайт и инструменты — MIT (`tools/LICENSE`). Bootstrap — MIT, © The Bootstrap Authors; торговая марка Bootstrap® принадлежит им, исследование с проектом не связано.

---

# Bootstrap 6 on a Modelled Site

**A research report on the sixth generation of the framework — architecture, markup, design — tested on a fictional news site, "Page Six", and 43 screenshots**

*Edition 1.0 · 9 October 2026 · by Beibit Sakhanov, Astana*

## What this is

On 8 October 2026 the first alpha of Bootstrap 6 shipped, five years after v5. The report asks what the release is strong at and whether it is ready today for sites that live for years. As an engineering construction it is strong: nearly every Sass variable became a CSS custom property that changes in the browser without recompiling, colours are computed by the page itself in oklch, dark mode comes from `light-dark()`, modals and accordions run on native `<dialog>` and `<details>`, and the cascade is split into eleven layers. As a product for production it is still an alpha: APIs may change before beta, the browser floor rose to Chrome 130, Firefox 132 and Safari 18 with no fallbacks, minified CSS grew from 226 to 372 KB, and the classes of buttons, modals, menus, grid and utilities were renamed.

To judge by markup rather than by the announcement, a seven-page site was built on the alpha — home, category, article, component showcase, forms, token playground and a newsroom dashboard — with a single stylesheet of its own that contains no hex colour: everything comes from core tokens. The study also surfaced discrepancies inside the alpha worth knowing before migrating: shadows are built on relative colour syntax, which the project's own browser policy places above the floor, and the combobox logs a second-instance error on start-up. A separate chapter addresses Joomla newsrooms: the core ships Bootstrap 5, so v6 is best tried in a child template and on long-reads first.

## Contents

| folder | inside |
|---|---|
| `doklad/` | the research report: a self-contained HTML (15 chapters, 5 interactive charts, 4 diagrams, 58 sources, registers of discrepancies and gaps, glossary) and its Markdown source |
| `demo/` | the demo site "Page Six" on Bootstrap 6.0.0-alpha.1 — 7 pages, Bootstrap bundled locally, own styles in `@layer custom` built on tokens only |
| `skrinshoty/` | the screenshot walkthrough: 43 screens in Chromium 153 (desktop 1440 px, phone 390 px, dark scheme, open states) with analysis; 2× PNG originals and JPEG previews |
| `redkollegiya/` | the proofreading report produced with the author's editorial methodology |
| `tools/` | everything needed to reproduce: report builder with charts and diagrams, demo-site builder, Playwright screenshot runner, CSS statistics script, typographer wrapper |
| `dist/` | downloadable archives of the report and the demo site |

## How to view

GitHub Pages: [landing](https://bsakhanov.github.io/bootstrap-6-research/) · [report](https://bsakhanov.github.io/bootstrap-6-research/doklad/bootstrap-6-research.html) · [demo site](https://bsakhanov.github.io/bootstrap-6-research/demo/index.html) · [walkthrough](https://bsakhanov.github.io/bootstrap-6-research/skrinshoty/). All HTML files open from disk; the demo site needs any local web server for its scripts because Bootstrap 6 loads as an ES module. The texts are in Russian.

## Method

Facts come from the project announcement, 141 documentation files, the Sass and TypeScript sources of the `main` branch (commit 7771f16, 8 October 2026) and the npm packages of the alpha and of 5.3.8; every URL was opened on 8–9 October 2026. CSS statistics were computed on the compiled files (`tools/stats/css_stats.py`). Each claim carries a source number; the list is ordered by first mention. Source discrepancies (Р) and gaps (М) live in registers rather than being hidden in prose.

## Reproducing

See the commands above: install the alpha from npm, build the demo site, run the Playwright screenshot plan against a local Chromium, then build the report and the walkthrough.

## License

Texts, diagrams and screenshots — [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); demo site and tools — MIT (`tools/LICENSE`). Bootstrap is MIT-licensed by The Bootstrap Authors; Bootstrap® is their trademark, and this study is not affiliated with the project.
