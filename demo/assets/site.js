// Демо-сайт Bootstrap 6 — сценарии. ES-модуль: в Bootstrap 6 нет UMD-сборки и глобального
// объекта `bootstrap`, классы берутся явным импортом из той же сборки, что подключена в <head>.
import { Tooltip, Popover, Toast, Dialog } from './bootstrap/bootstrap.bundle.min.js'

const root = document.documentElement
const KEY = 'sp-theme'

// 1. Цветовая схема. Ядро ставит color-scheme: light dark и считает цвета через light-dark(),
//    поэтому «как в системе» — это просто отсутствие атрибута data-bs-theme.
function applyTheme(mode) {
  if (mode === 'auto') root.removeAttribute('data-bs-theme')
  else root.setAttribute('data-bs-theme', mode)
  document.querySelectorAll('[data-sp-theme]').forEach(b => b.classList.toggle('active', b.dataset.spTheme === mode))
  const icon = document.querySelector('#themeToggle use')
  if (icon) icon.setAttribute('href', mode === 'light' ? '#i-sun' : mode === 'dark' ? '#i-moon' : '#i-half')
  try { localStorage.setItem(KEY, mode) } catch { /* приватный режим */ }
}
let saved = 'auto'
try { saved = localStorage.getItem(KEY) || 'auto' } catch { /* ничего */ }
applyTheme(saved)
document.querySelectorAll('[data-sp-theme]').forEach(b => b.addEventListener('click', () => applyTheme(b.dataset.spTheme)))

// 2. Подсказки и поповеры: их по-прежнему нужно создать явно.
document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => Tooltip.getOrCreateInstance(el))
document.querySelectorAll('[data-bs-toggle="popover"]').forEach(el => Popover.getOrCreateInstance(el))

// 3. Тосты: одна функция на весь сайт. show() возвращает промис — ждать событий не нужно.
export function spToast(text, theme = 'primary') {
  const area = document.getElementById('toastArea')
  if (!area) return
  const el = document.createElement('div')
  el.className = 'toast'
  el.setAttribute('role', 'status')
  el.innerHTML = `<div class="toast-header"><span class="badge theme-${theme} me-2">6</span><strong class="me-auto">Bootstrap 6 демо</strong><small class="fg-2">сейчас</small><button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Закрыть"></button></div><div class="toast-body">${text}</div>`
  area.appendChild(el)
  el.addEventListener('hidden.bs.toast', () => el.remove())
  Toast.getOrCreateInstance(el, { delay: 4000 }).show()
}
window.spToast = spToast
document.querySelectorAll('[data-sp-toast]').forEach(b => b.addEventListener('click', e => {
  if (b.tagName === 'BUTTON' && b.type !== 'submit') e.preventDefault()
  spToast(b.dataset.spToast, b.dataset.spTheme || 'primary')
}))

// 4. Формы: валидация включается атрибутом data-bs-validate, а по успешной отправке — тост.
document.querySelectorAll('form[data-sp-demo]').forEach(f => f.addEventListener('submit', e => {
  e.preventDefault()
  if (f.checkValidity()) spToast(f.dataset.spDemo, 'success')
  else spToast('В форме есть ошибки — поля подсвечены после первого касания.', 'danger')
}))

// 5. Контейнерные запросы: ползунок меняет ширину рамки, а не окна.
const cqRange = document.getElementById('cqRange')
const cqBox = document.getElementById('cqBox')
if (cqRange && cqBox) {
  const out = document.getElementById('cqOut')
  const upd = () => { cqBox.style.inlineSize = cqRange.value + '%'; if (out) out.textContent = Math.round(cqBox.getBoundingClientRect().width) + ' px' }
  cqRange.addEventListener('input', upd); upd()
  new ResizeObserver(() => { if (out) out.textContent = Math.round(cqBox.getBoundingClientRect().width) + ' px' }).observe(cqBox)
}

// 6. Токены вживую. Радиусы и отступы в ядре — шкалы от одного базового значения,
//    поэтому один ползунок двигает всю шкалу; оттенок primary собирается из ступеней другого цвета.
const RADII = [0, .25, .375, .5, .75, 1, 1.25, 1.5, 1.75, 2]
const SPACERS = [0, .25, .375, .5, .75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 3]
function setPrimaryHue(el, hue) {
  const h = hue
  const map = {
    '--bs-primary-base': `var(--bs-${h}-500)`,
    '--bs-primary-bg': `var(--bs-${h}-500)`,
    '--bs-primary-fg': `light-dark(var(--bs-${h}-600), var(--bs-${h}-400))`,
    '--bs-primary-fg-emphasis': `light-dark(var(--bs-${h}-800), var(--bs-${h}-200))`,
    '--bs-primary-bg-subtle': `light-dark(var(--bs-${h}-100), var(--bs-${h}-900))`,
    '--bs-primary-bg-muted': `light-dark(var(--bs-${h}-200), var(--bs-${h}-800))`,
    '--bs-primary-border': `light-dark(var(--bs-${h}-300), var(--bs-${h}-600))`,
    '--bs-primary-focus-ring': `light-dark(color-mix(in oklch, var(--bs-${h}-500) 50%, var(--bs-bg-body)), color-mix(in oklch, var(--bs-${h}-500) 75%, var(--bs-bg-body)))`,
    '--bs-primary-contrast': ['yellow', 'amber', 'lime'].includes(h) ? 'var(--bs-gray-900)' : 'var(--bs-white)',
    '--bs-link-color': `light-dark(var(--bs-${h}-500), var(--bs-${h}-400))`
  }
  Object.entries(map).forEach(([k, v]) => el.style.setProperty(k, v))
  return map
}
document.querySelectorAll('[data-sp-playground]').forEach(pg => {
  const target = pg.querySelector('[data-sp-target]')
  const code = pg.querySelector('[data-sp-code]')
  const state = { radius: .5, spacer: 1, hue: 'blue', scheme: 'auto' }
  const render = () => {
    const lines = []
    RADII.forEach((k, i) => { const v = (state.radius * k).toFixed(4).replace(/\.?0+$/, ''); target.style.setProperty(`--bs-radius-${i}`, v + 'rem') })
    target.style.setProperty('--bs-spacer', state.spacer + 'rem')
    SPACERS.forEach((k, i) => { const v = (state.spacer * k).toFixed(4).replace(/\.?0+$/, ''); target.style.setProperty(`--bs-spacer-${i}`, v + 'rem') })
    const hueMap = setPrimaryHue(target, state.hue)
    if (state.scheme === 'auto') target.removeAttribute('data-bs-theme'); else target.setAttribute('data-bs-theme', state.scheme)
    lines.push(`.my-brand {`)
    lines.push(`  --bs-radius-5: ${state.radius}rem;      /* базовый шаг шкалы радиусов */`)
    lines.push(`  --bs-spacer: ${state.spacer}rem;        /* базовый шаг шкалы отступов */`)
    lines.push(`  --bs-primary-base: ${hueMap['--bs-primary-base']};`)
    lines.push(`  --bs-primary-bg-subtle: ${hueMap['--bs-primary-bg-subtle']};`)
    lines.push(`  --bs-primary-fg: ${hueMap['--bs-primary-fg']};`)
    lines.push(`  --bs-primary-border: ${hueMap['--bs-primary-border']};`)
    lines.push(`}`)
    if (code) code.textContent = lines.join('\n')
    pg.querySelectorAll('[data-sp-out]').forEach(o => { o.textContent = state[o.dataset.spOut] + (o.dataset.spUnit || '') })
  }
  pg.querySelectorAll('[data-sp-token]').forEach(inp => inp.addEventListener('input', () => { state[inp.dataset.spToken] = inp.type === 'range' ? parseFloat(inp.value) : inp.value; render() }))
  pg.querySelectorAll('[data-sp-scheme]').forEach(b => b.addEventListener('click', () => { state.scheme = b.dataset.spScheme; pg.querySelectorAll('[data-sp-scheme]').forEach(x => x.classList.toggle('active', x === b)); render() }))
  render()
})

// 7. Палитра: 16 оттенков × 13 ступеней читаются прямо из токенов :root.
const palette = document.getElementById('palette')
if (palette) {
  const hues = ['blue', 'indigo', 'violet', 'purple', 'pink', 'red', 'orange', 'amber', 'yellow', 'lime', 'green', 'teal', 'cyan', 'brown', 'gray', 'pewter']
  const stops = ['025', '050', '100', '200', '300', '400', '500', '600', '700', '800', '900', '950', '975']
  let html = '<div class="sp-palette-head d-grid gap-1 mb-2" style="grid-template-columns: 5rem repeat(13, 1fr)"><span></span>' + stops.map(s => `<span class="fs-xs fg-3 text-center font-monospace">${s}</span>`).join('') + '</div>'
  hues.forEach(h => {
    html += `<div class="d-grid gap-1 mb-1" style="grid-template-columns: 5rem repeat(13, 1fr)"><span class="fs-sm fg-2 font-monospace align-self-center">${h}</span>` +
      stops.map(s => `<span class="sp-swatch" style="background: var(--bs-${h}-${s})" title="--bs-${h}-${s}"></span>`).join('') + '</div>'
  })
  palette.innerHTML = html
}

// 8. Шкала шрифтов: показать вычисленный размер в пикселях рядом с классом.
document.querySelectorAll('[data-sp-fs]').forEach(el => {
  const out = el.querySelector('code')
  const sample = el.querySelector('[class*="fs-"]')
  if (out && sample) out.textContent = getComputedStyle(sample).fontSize + ' · ' + getComputedStyle(sample).lineHeight
})

// 9. Копирование ссылки из диалога «Поделиться».
document.querySelectorAll('[data-sp-copy]').forEach(b => b.addEventListener('click', async () => {
  const src = document.querySelector(b.dataset.spCopy)
  try { await navigator.clipboard.writeText(src.value); spToast('Ссылка скопирована.', 'success') } catch { spToast('Буфер обмена недоступен в этом окружении.', 'warning') }
  const dlg = b.closest('dialog'); if (dlg) await Dialog.getOrCreateInstance(dlg).hide()
}))
