#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_shots.py — страница «Сайт в скриншотах»: 46 экранов демо-сайта «Шестая полоса» с разбором.
Превью (JPEG 1200 px) лежат в skrinshoty/preview, оригиналы (PNG, масштаб 2×) — в skrinshoty/img."""
import html, pathlib
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
IMG = ROOT / 'skrinshoty/img'
PREV = ROOT / 'skrinshoty/preview'
OUT = ROOT / 'skrinshoty/index.html'

SECTIONS = [
    ('desktop', 'Страницы целиком: десктоп 1440 px', 'Семь страниц в светлой схеме при ширине окна 1440 пикселей. Снимки сделаны целиком, в масштабе 2×; длинные страницы прокручиваются внутри рамки.', [
        ('01-glavnaya', 'Главная', 'Герой на текучем заголовке <code>fs-5xl</code>: при 1440 пикселях он отрисован в 64 px, на телефоне сожмётся до 48 без единого медиазапроса. Правее — карточка <code>card-translucent</code> со степпером выпуска и стопкой аватаров. Ниже сетка CSS Grid «восемь плюс четыре»: большой материал и три горизонтальные карточки <code>card-row</code>, у каждой из которых ссылка растянута на всю карточку классом <code>stretched-link</code>. Дальше три карточки рубрик на flex-сетке <code>md:row-cols-3</code>, демонстрация контейнерных запросов, площадка токенов и форма подписки.'),
        ('02-rubrika', 'Рубрика «Технологии»', 'Строка подрубрик — компонент <code>nav-overflow</code>: девять пунктов не помещаются, и плагин убрал «Архив» в меню «Ещё», измерив ширину обёртки. Справа комбобокс сортировки — кнопка <code>combobox-toggle</code> с меню на Floating UI. Лента — горизонтальные карточки с мягкими значками <code>badge-subtle</code>, замыкает её скелет <code>placeholder-wave</code>. Боковая колонка — отзывчивый ящик <code>lg:drawer</code>, который при 1440 пикселях стоит обычным блоком.'),
        ('03-statya', 'Статья', 'Хлебные крошки с явными разделителями <code>breadcrumb-divider</code>, заголовок <code>fs-4xl</code>, строка автора с аватаром из инициалов. Тело статьи — класс <code>prose</code>: абзацы, цитата с подписью <code>blockquote-footer</code>, таблица, список получили оформление без единого класса на элементе. Ниже аккордеон вопросов на <code>&lt;details&gt;</code>, чипы меток, обсуждение и форма комментария. Правая колонка липкая: <code>lg:sticky-top</code>.'),
        ('04-komponenty', 'Витрина компонентов', 'Левая колонка — вертикальные таблетки <code>nav-pills flex-column</code>, прилипшие к верху. Матрица кнопок пять форм на восемь тем, значки трёх форм, чипы, четыре оповещения с темами, полоса хода и стопка полос, спиннеры, кнопки, открывающие диалоги и ящики, меню, вкладки, подчёркнутая и таблеточная навигация, два степпера, две карусели, аватары, три варианта карточек, список и таблица в обёртке <code>md:table-responsive</code>.'),
        ('05-formy', 'Формы', 'Регистрация читателя в три раздела. Поля разложены сеткой <code>form-field</code>; обёртки с иконками — <code>form-adorn</code>; плавающая подпись «Город»; комбобокс роли с поиском; поле с чипами; кнопки-переключатели формата рассылки; флажки и переключатели с описаниями; ползунок с подписью значения и делениями; измеритель пароля; код подтверждения в шесть ячеек; группа ввода с тенге. Справа памятка о новом и исчезнувшем и два серверных состояния <code>is-valid</code> и <code>is-invalid</code>.'),
        ('06-tokeny', 'Токены и темы', 'Живая настройка с тремя ползунками и выбором схемы, палитра из 208 ячеек, восемь семантических тем по четыре роли, нейтральные поверхности <code>bg-1</code>–<code>bg-4</code> и ступени текста, лестница из одиннадцати слоёв каскада, шесть теней, одиннадцать радиусов, шкала шрифтов с вычисленными размерами.'),
        ('07-redakciya', 'Редакционная панель', 'Контейнер на всю ширину. Слева колонка с профилем главреда, индикатором статуса и меню разделов — это отзывчивый ящик, которому для вертикальной раскладки понадобился <code>lg:flex-column</code>. Четыре карточки показателей, одна из них <code>card-subtle theme-danger</code>; степпер конвейера с подписями-значками на каждом шаге; таблица материалов с аватарами, значками стадий, чипами меток и меню действий; дедлайны, стопка полос корректуры и предупреждение.'),
    ]),
    ('dark', 'Тёмная схема', 'Тёмная схема включена эмуляцией системного предпочтения <code>prefers-color-scheme: dark</code>, а не атрибутом. В стилях сайта нет ни одного правила для тёмной темы: пары <code>light-dark()</code> в токенах ядра выбрали вторые значения сами.', [
        ('08-glavnaya-tyomnaya', 'Главная в тёмной схеме', 'Поверхности <code>bg-body</code> и <code>bg-1</code> стали почти чёрными, текст — светлым, мягкие значки и карточки с темами перешли на ступени 900 и 800 своих оттенков. Градиенты-заглушки тоже потемнели, потому что собраны из токенов <code>--bs-primary-bg-subtle</code> и соседних. Тени углубились токеном <code>--bs-shadow-strength</code>.'),
        ('09-redakciya-tyomnaya', 'Панель в тёмной схеме', 'Таблица, значки стадий, карточка с темой danger и стопка полос читаются так же, как в светлой. Это и есть смысл семантических ролей: компонент просит «мягкий фон темы», а не конкретный цвет.'),
        ('10-komponenty-tyomnaya', 'Витрина в тёмной схеме, первый экран', 'Матрица кнопок: сплошные формы сохранили цвет, контурные и текстовые перешли на светлые ступени <code>fg</code>, тема inverse стала светлой кнопкой с тёмным текстом — роль <code>contrast</code> перевернулась вместе со схемой.'),
        ('e10-temy-tyomnaya', 'Восемь тем в тёмной схеме', 'Те же восемь карточек, что на странице токенов в светлой схеме: роли contrast, subtle, muted и две ступени текста. Жёлтая и бирюзовая темы в роли contrast дают тёмный текст, остальные — белый; это задано в карте <code>$theme-colors</code> и не требует правок.'),
    ]),
    ('states', 'Открытые состояния', 'Снимки видимой области после действия пользователя: клик, наведение, ввод. Всё, что открыто, — настоящие компоненты в работе, а не нарисованные макеты.', [
        ('11-statya-dialog', 'Диалог «Поделиться»', 'Родной элемент <code>&lt;dialog&gt;</code>: подложка с размытием нарисована псевдоэлементом <code>::backdrop</code>, страница за ним инертна, фокус заперт браузером. Внутри группа ввода со ссылкой и кнопкой «Копировать», которая кладёт адрес в буфер и показывает тост. Полоса прокрутки страницы не исчезла и макет не прыгнул — заслуга <code>scrollbar-gutter: stable</code>.'),
        ('12-komponenty-dialog-dark', 'Тёмный диалог на светлой странице', 'Атрибут <code>data-bs-theme="dark"</code> стоит только на диалоге: внутри него все токены пересчитаны, снаружи страница светлая. Так можно темнить одно окно, одну карточку или одну колонку.'),
        ('13-komponenty-menu', 'Меню с подменю', 'Меню «Рубрики» с заголовком группы <code>menu-header</code>, разделителем и подменю «Спецпроекты», раскрытым по наведению. Обёртки <code>dropdown</code> нет: кнопка и меню — соседние элементы, позицию считает Floating UI. Рядом ещё два меню с направлением через <code>data-bs-placement</code>, поповер и подсказка.'),
        ('14-komponenty-drawer', 'Ящик слева', 'Тот же элемент <code>&lt;dialog&gt;</code>, что у диалога, но с геометрией <code>drawer-start</code>: отступ от края, скругление, тень, подложка. На сенсорном экране его можно смахнуть обратно — жест встроен в плагин.'),
        ('15-rubrika-combobox', 'Комбобокс сортировки', 'Меню из четырёх пунктов под кнопкой-переключателем; активный пункт подсвечен. После выбора пункта «Самые читаемые» значение переписалось в кнопку и в скрытое поле <code>sort</code>. В консоли при загрузке страницы ядро пишет ошибку о втором экземпляре — она разобрана в докладе и занесена в реестр М-01.'),
        ('16-formy-datepicker', 'Календарь', 'Плагин Datepicker на Vanilla Calendar Pro открылся по фокусу в поле «Дата рождения». Дни недели и месяц — на русском, язык взят из браузера. Календарь закрывается после выбора, по Escape и при уходе фокуса.'),
        ('17-formy-validaciya', 'Форма после отправки с ошибками', 'Нажата «Зарегистрироваться» при пустых имени, почте и согласии. Атрибут <code>data-bs-validate</code> включил стили <code>:user-invalid</code>: подсвечены только тронутые поля. Поле с чипами приняло метку «дизайн», измеритель оценил пароль как «Хороший» (подписи переведены атрибутом <code>data-bs-messages</code>), код разложился по ячейкам 3+3, тост внизу сообщил об ошибках.'),
        ('18-tokeny-perestroika', 'Площадка токенов после перестройки', 'Оттенок primary — teal, базовый радиус — 1,25 rem, шаг отступов — 1,25 rem. Навбар, карточка, три кнопки, значки, оповещение, поле, переключатель, полоса хода, степпер и аккордеон перестроились разом; слева — CSS, который даёт тот же результат на любом сайте. Пересборки Sass не было.'),
        ('19-glavnaya-cq-uzkaya', 'Контейнерный запрос: рамка сжата до 45 процентов', 'Окно браузера — 1440 пикселей, но обёртка <code>contains-inline</code> сжата ползунком, и группа карточек сложилась в столбик, а список внизу остался вертикальным, потому что его порог — 1024 пикселя ширины контейнера. Это невозможно сделать медиазапросом: он знает только ширину окна.'),
        ('20-komponenty-tosty', 'Три тоста', 'Три уведомления в контейнере <code>toast-container</code> в правом нижнем углу: обычное, с темой success и об ошибке. Появляются из <code>@starting-style</code>, исчезают через четыре секунды; метод <code>show()</code> вернул промис.'),
    ]),
    ('closeups', 'Крупные планы', 'Фрагменты страниц, снятые по границам элемента с небольшим полем.', [
        ('e01-knopki', 'Матрица кнопок', 'Пять форм — solid, outline, subtle, text, styled — на восемь тем. В пятой версии этот набор требовал шестнадцати классов вида <code>btn-outline-danger</code>; здесь любая ячейка — два класса. Ниже размеры от xs до lg, квадратная <code>btn-icon</code>, кнопка с подъёмом, отключённая, кнопка-ссылка, группа переключателей на <code>btn-check</code> и разделённая кнопка с меню.'),
        ('e02-znachki-chipy', 'Значки и чипы', 'Три ряда значков — сплошные, мягкие, контурные — по восемь тем. Значок в заголовке, счётчик «99+» поверх кнопки, чипы: простой, с картинкой, с темой, активный, с иконкой и удаляемый с крестиком.'),
        ('e03-navigaciya-stepper', 'Навигация и шаги', 'Вкладки на плагине Tab, подчёркнутая и таблеточная навигация, горизонтальный степпер пути материала по редакции с темой и значком на каждом шаге и вертикальный степпер по умолчанию.'),
        ('e04-avatary-kartochki', 'Аватары и карточки', 'Аватары пяти размеров из инициалов, мягкий вариант, индикаторы статуса online, busy и away, стопка с перекрытием. Три карточки: мягкая с темой accent, матовое стекло поверх градиента и горизонтальная.'),
        ('e05-palitra', 'Палитра 16 × 13', 'Двести восемь ячеек построены скриптом из переменных <code>--bs-{оттенок}-{ступень}</code>. Базовая ступень 500 записана в oklch, остальные — <code>color-mix()</code> с белым и чёрным в том же пространстве, поэтому строки выглядят равномерными по светлоте.'),
        ('e06-sloi', 'Одиннадцать слоёв каскада', 'Лестница из <code>_root.scss</code>: от colors до utilities. Слой custom подсвечен — в нём лежит <code>site.css</code> демо-сайта.'),
        ('e07-navbar-desktop', 'Навбар на десктопе', 'Класс <code>md:navbar-expand</code> разложил содержимое ящика в строку: ссылки слева, переключатель схемы и кнопка подписки справа. Ниже md тот же элемент станет ящиком — см. снимок 28.'),
        ('e08-geroi', 'Герой главной', 'Фон — два радиальных градиента на токенах <code>--bs-primary-bg-subtle</code> и <code>--bs-accent-bg-subtle</code>. Заголовок с <code>text-balance</code>, подзаголовок с <code>text-pretty</code>, две кнопки размера lg, пять чипов, карточка матового стекла.'),
        ('e09-karusel', 'Карусель после перелистывания', 'Три слайда в ряд заданы переменными <code>--bs-carousel-items: 3</code> и <code>--bs-carousel-items-gap: 1rem</code>; кнопка «вперёд» прокрутила ленту на один кадр. Лента — контейнер с привязкой прокрутки, поэтому колёсико и свайп работают без плагина. Ниже карусель с наложенными элементами управления и индикаторами в тёмной схеме.'),
    ]),
    ('mobile', 'Телефон 390 px', 'Экран телефона 390 на 844 пикселя при масштабе 2×, с эмуляцией сенсорного ввода. Страницы сняты целиком.', [
        ('21-m-glavnaya', 'Главная на телефоне', 'Заголовок героя сжался до 48 px той же функцией <code>clamp()</code>. Сетка CSS Grid разложилась в одну колонку — после того как к <code>md:g-col-8</code> и <code>md:g-col-4</code> добавлен базовый <code>g-col-12</code>; без него элемент занимал одну двенадцатую ширины. Группа карточек в демонстрации контейнерных запросов стоит столбиком, потому что обёртка уже 576 пикселей.'),
        ('22-m-rubrika', 'Рубрика на телефоне', 'Переполнение навигации убрало в меню «Ещё» почти все подрубрики. Боковой колонки нет: она стала ящиком, который открывает кнопка «Фильтры» (снимок 29). Изображения горизонтальных карточек сохранили ширину 14 rem.'),
        ('23-m-statya', 'Статья на телефоне', 'Колонка <code>prose</code> читается без горизонтальной прокрутки, таблица внутри неё переносит строки. Аккордеон, чипы и форма комментария легли в одну колонку.'),
        ('24-m-komponenty', 'Витрина на телефоне', 'Левое меню разделов скрыто классом <code>d-none lg:d-block</code>. Матрица кнопок переносится по строкам, таблица в обёртке <code>md:table-responsive</code> получила горизонтальную прокрутку, карусель показывает три узких кадра.'),
        ('25-m-formy', 'Формы на телефоне', 'Все поля сетки <code>grid</code> встали в одну колонку благодаря базовому <code>g-col-12</code>. Код подтверждения в шесть ячеек поместился в ширину, памятка из боковой колонки ушла вниз.'),
        ('26-m-tokeny', 'Токены на телефоне', 'Палитра прокручивается по горизонтали внутри своей обёртки <code>overflow-x-auto</code>, остальные блоки легли в колонку. Кнопки выбора схемы в группе ужались.'),
        ('27-m-redakciya', 'Панель на телефоне', 'Боковая колонка превратилась в кнопку «Разделы панели» (ящик — снимок 30). Карточки показателей встали по две в ряд благодаря <code>sm:row-cols-2</code>, степпер конвейера прокручивается внутри <code>stepper-overflow</code>, таблица — внутри <code>md:table-responsive</code>.'),
        ('28-m-menu-drawer', 'Меню сайта на телефоне', 'Ящик <code>drawer-end</code> с заголовком, кнопкой закрытия, семью ссылками, переключателем схемы и кнопкой подписки. Это тот же элемент <code>&lt;dialog&gt;</code>, что в навбаре на десктопе, — он лишь сменил раскладку.'),
        ('29-m-rubrika-filtry', 'Ящик фильтров рубрики', 'Отзывчивый ящик <code>lg:drawer</code> в раскрытом состоянии: список популярного, флажки, радиокнопки периода, переключатель подписки. Кнопка закрытия нашла свой ящик без <code>data-bs-target</code>.'),
        ('30-m-redakciya-razdely', 'Разделы панели в ящике', 'Левая колонка панели как ящик <code>drawer-start</code>: профиль, меню со счётчиками, пояснение. Заголовок ящика, скрытый на десктопе классом <code>lg:d-none</code>, здесь виден.'),
        ('31-m-glavnaya-tyomnaya', 'Главная на телефоне в тёмной схеме', 'Первый экран героя в тёмной схеме: градиенты, чипы, карточка матового стекла и кнопки перешли на тёмные ступени без правок.'),
        ('32-m-dialog-snizu', 'Диалог, выезжающий снизу', 'Класс <code>dialog-slide-up</code> на телефоне: окно поднялось от нижнего края, как системный лист действий. Разметка та же, что у обычного диалога.'),
        ('33-m-statya-tyomnaya', 'Статья на телефоне в тёмной схеме', 'Хлебные крошки, значок рубрики, заголовок и строка автора в тёмной схеме; кнопки «Поделиться» и закладки сохранили контраст.'),
    ]),
]

CSS = """
:root{--paper:#F3F4EF;--paper-raised:#FBFBF8;--ink:#171A1C;--ink-soft:#565D60;--ink-faint:#8B9190;--line:#DBDDD2;--line-strong:#C7CABC;--accent:#B54A24;--accent-ink:#7C3216;--steel:#33505E;--steel-soft:#DEE6E7;--serif:'Newsreader',Georgia,serif;--sans:'Manrope',system-ui,sans-serif;--mono:'JetBrains Mono',ui-monospace,monospace}
*,*::before,*::after{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:16px;line-height:1.6}
a{color:inherit}.wrap{max-width:1120px;margin:0 auto;padding:0 40px}@media (max-width:720px){.wrap{padding:0 22px}}
.topnav{position:sticky;top:0;z-index:50;background:rgba(243,244,239,.92);backdrop-filter:blur(6px);border-bottom:1px solid var(--line)}
.topnav-inner{max-width:1120px;margin:0 auto;padding:0 40px;display:flex;align-items:center;gap:24px;height:56px}
.topnav-mark{font-family:var(--mono);font-size:12px;text-decoration:none;white-space:nowrap;font-weight:500}
.topnav-links{display:flex;gap:2px;overflow-x:auto;scrollbar-width:none}.topnav-links a{font-family:var(--mono);font-size:12px;white-space:nowrap;color:var(--ink-soft);text-decoration:none;padding:8px 10px}
.topnav-links a:hover{color:var(--ink);background:var(--steel-soft)}
header.hero{padding:90px 0 50px}.eyebrow{font-family:var(--mono);font-size:12px;letter-spacing:.06em;color:var(--steel);margin:0 0 18px}
h1{font-family:var(--serif);font-weight:500;font-size:clamp(2.2rem,5vw,3.8rem);line-height:1.05;margin:0 0 22px;max-width:18ch}
.lead{font-size:18px;max-width:700px;margin:0 0 14px}.sub{font-size:15px;color:var(--ink-soft);max-width:680px;margin:0 0 28px}
.links a{font-family:var(--mono);font-size:12px;text-decoration:none;color:var(--accent-ink);border:1px solid var(--line-strong);background:var(--paper-raised);padding:8px 12px;border-radius:2px;margin:0 8px 8px 0;display:inline-block}
section{padding:56px 0;border-top:1px solid var(--line)}section[id]{scroll-margin-top:70px}
section h2{font-family:var(--serif);font-weight:500;font-size:clamp(1.6rem,3vw,2.2rem);margin:0 0 10px}
section > .wrap > p{max-width:780px;color:var(--ink-soft);margin:0 0 30px}
figure.shot{margin:0 0 44px;padding:16px 14px 12px;border:1px solid var(--line);background:var(--paper-raised);border-radius:2px}
figure.shot .shot-head{display:flex;justify-content:space-between;align-items:baseline;gap:14px;flex-wrap:wrap;margin:0 4px 12px}
figure.shot h3{font-family:var(--serif);font-weight:500;font-size:1.3rem;margin:0}
figure.shot .meta{font-family:var(--mono);font-size:11.5px;color:var(--ink-faint)}
figure.shot a.img{display:block;border:1px solid var(--line)}figure.shot.tall a.img{max-height:720px;overflow:auto}
figure.shot img{display:block;width:100%;height:auto}
figure.shot.mobile{max-width:560px}figure.shot.mobile.tall a.img{max-height:760px}
figure.shot figcaption{font-size:14.5px;line-height:1.6;margin:12px 4px 0;color:var(--ink)}
figure.shot figcaption code{font-family:var(--mono);font-size:.86em;background:var(--steel-soft);padding:1px 5px;border-radius:2px}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:24px}
footer{padding:50px 0 60px;border-top:1px solid var(--line);font-size:14px;color:var(--ink-soft)}
"""

def main():
    nav = ''.join(f'<a href="#{sid}">{t.split(":")[0].split(" 390")[0].lower()}</a>' for sid, t, _, _ in SECTIONS)
    parts = []
    total = 0
    for sid, title, intro, shots in SECTIONS:
        figs = []
        for name, t, text in shots:
            png = IMG / f'{name}.png'
            if not png.exists():
                print('нет снимка', name); continue
            w, h = Image.open(png).size
            total += 1
            mobile = name.startswith(('2', '3')) and '-m-' in name
            tall = h > 2400
            cls = 'shot' + (' tall' if tall else '') + (' mobile' if mobile else '')
            figs.append(f'<figure class="{cls}" id="{name}"><div class="shot-head"><h3>{t}</h3><span class="meta">{name}.png · {w}×{h} px · {png.stat().st_size // 1024} КБ</span></div>'
                        f'<a class="img" href="img/{name}.png"><img src="preview/{name}.jpg" alt="{html.escape(t)}" loading="lazy" width="{min(w, 1200) // 2 * 2}"></a><figcaption>{text}</figcaption></figure>')
        body = ''.join(figs)
        if sid == 'mobile':
            body = f'<div class="grid2">{body}</div>'
        parts.append(f'<section id="{sid}"><div class="wrap"><h2>{title}</h2><p>{intro}</p>{body}</div></section>')
    doc = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Сайт в скриншотах — Bootstrap 6 на смоделированном сайте</title>
<meta name="description" content="{total} снимков демо-сайта «Шестая полоса» на Bootstrap 6.0.0-alpha.1 в Chromium 153 с разбором: десктоп, телефон, тёмная схема, открытые диалоги, меню, календарь, комбобокс, перестроенные токены.">
<meta name="author" content="Бейбит Саханов">
<link rel="canonical" href="https://bsakhanov.github.io/bootstrap-6-research/skrinshoty/">
<meta property="og:title" content="Сайт в скриншотах — Bootstrap 6 на смоделированном сайте"><meta property="og:type" content="article">
<meta property="og:image" content="https://bsakhanov.github.io/bootstrap-6-research/skrinshoty/preview/e08-geroi.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Manrope:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<nav class="topnav"><div class="topnav-inner"><a class="topnav-mark" href="../">bootstrap 6 · сайт в скриншотах</a><div class="topnav-links">{nav}<a href="../doklad/bootstrap-6-research.html">доклад</a><a href="../demo/index.html">демо-сайт</a></div></div></nav>
<header class="hero"><div class="wrap">
<p class="eyebrow">приложение к исследованию · редакция 1.0 · 9 октября 2026</p>
<h1>«Шестая полоса» в скриншотах</h1>
<p class="lead">{total} экранов демо-сайта на Bootstrap 6.0.0-alpha.1, снятых в Chromium 153.0.8010.0 через Playwright 1.56 в масштабе 2×: семь страниц на десктопе и телефоне, тёмная схема, открытые состояния и крупные планы — с разбором того, что на каждом экране делает фреймворк.</p>
<p class="sub">Клик по снимку открывает оригинал PNG; на странице показаны превью JPEG шириной 1200 пикселей. Тёмная схема включена эмуляцией системного предпочтения, а не атрибутом. Автор — Бейбит Саханов, Астана.</p>
<div class="links"><a href="../demo/index.html">открыть демо-сайт</a><a href="../doklad/bootstrap-6-research.html">читать доклад</a><a href="https://github.com/bsakhanov/bootstrap-6-research">репозиторий</a></div>
</div></header>
<main>{''.join(parts)}</main>
<footer><div class="wrap">Снимки сделаны скриптом <code>tools/screenshots/shots.py</code>; воспроизведение описано в README репозитория. Тексты и снимки — CC BY 4.0, демо-сайт — MIT.</div></footer>
</body>
</html>
"""
    OUT.write_text(doc, encoding='utf-8')
    print('written', OUT.name, len(doc), 'chars,', total, 'snapshots')

if __name__ == '__main__':
    main()
