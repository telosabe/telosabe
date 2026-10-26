# -*- coding: utf-8 -*-
"""Сборка сайта Telo.Sabe: python3 _build/build.py (из корня репозитория).
Создаёт index.html (RU), es/index.html, en/index.html и sitemap.xml."""
import json, os, html
from urllib.parse import quote
from content import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ARROW = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" aria-hidden="true"><path d="M4 12h16M14 6l6 6-6 6"/></svg>'
ARROW_L = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" aria-hidden="true"><path d="M20 12H4M10 6l-6 6 6 6"/></svg>'
DIAG = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8"/></svg>'
STAR = '<svg width="10" height="10" viewBox="0 0 24 24" aria-hidden="true" class="star"><path d="M12 1C13 9 15 11 23 12C15 13 13 15 12 23C11 15 9 13 1 12C9 11 11 9 12 1Z" fill="currentColor"/></svg>'
CLOSE = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>'
WA_ICON = '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3.6 20.4l1.2-4.1A8.6 8.6 0 1 1 8 19.3z"/><path d="M9.1 8.2c.2-.4.6-.5.9-.3l.9 1.6c.1.3 0 .6-.2.8l-.6.6c.6 1.3 1.6 2.3 2.9 2.9l.6-.6c.2-.2.5-.3.8-.2l1.6.9c.3.2.4.6.2.9-.5.9-1.4 1.4-2.4 1.1-2.6-.7-4.7-2.8-5.4-5.4-.2-.9.2-1.8.7-2.3z"/></svg>'
PLUS = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" aria-hidden="true"><path class="v" d="M12 5v14"/><path d="M5 12h14"/></svg>'


def wa(text=None):
    return f'https://wa.me/{PHONE}' + (f'?text={quote(text)}' if text else '')


def notch(width, inner):
    """Вырез в правом нижнем углу карточки с кнопкой внутри."""
    return (f'<div class="cut" style="width:{width}px">{inner}</div>'
            f'<div class="inv inv-t"></div><div class="inv" style="right:{width}px;bottom:0"></div>')


def pill(href, label, width):
    return notch(width + 24, f'<a class="pill" href="{href}" style="width:{width}px">{label} {ARROW}</a>')


def build(lang):
    t = C[lang]
    pre = '' if lang == 'ru' else '../'
    img = pre + 'assets/img/'
    out = []
    w = out.append

    # ---------- head
    alts = ''.join(f'<link rel="alternate" hreflang="{l}" href="{SITE}{PATHS[l]}">' for l in LANGS)
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t['faq']]}
    biz_ld = {"@context": "https://schema.org", "@type": "HealthAndBeautyBusiness", "name": "Telo.Sabe",
              "url": SITE + PATHS[lang], "image": SITE + "/assets/img/og.jpg", "telephone": PHONE_PRETTY,
              "areaServed": "Barcelona", "address": {"@type": "PostalAddress", "addressLocality": "Barcelona", "addressCountry": "ES"},
              "sameAs": [f"https://instagram.com/{INSTAGRAM}"]}
    w(f'''<!doctype html>
<html lang="{t['html_lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t['title']}</title>
<meta name="description" content="{html.escape(t['description'])}">
<link rel="canonical" href="{SITE}{PATHS[lang]}">
{alts}<link rel="alternate" hreflang="x-default" href="{SITE}/">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}{PATHS[lang]}">
<meta property="og:title" content="{html.escape(t['og_title'])}">
<meta property="og:description" content="{html.escape(t['og_description'])}">
<meta property="og:image" content="{SITE}/assets/img/og.jpg">
<meta property="og:locale" content="{t['og_locale']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#2C4535">
<link rel="icon" href="{pre}favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{pre}assets/css/fonts.css">
<link rel="stylesheet" href="{pre}assets/css/site.css">
<script type="application/ld+json">{json.dumps(biz_ld, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">{'Перейти к содержанию' if lang == 'ru' else 'Saltar al contenido' if lang == 'es' else 'Skip to content'}</a>
''')

    # ---------- header
    nav = ''.join(f'<a href="{h}">{n}</a>' for h, n in t['nav'])
    langs = []
    for i, l in enumerate(LANGS):
        if i: langs.append('<span aria-hidden="true" class="sep">/</span>')
        cur = ' aria-current="true"' if l == lang else ''
        langs.append(f'<a class="lng{" on" if l == lang else ""}" href="{pre}{PATHS[l].lstrip("/")}index.html" hreflang="{l}" lang="{l}"{cur}>{l.upper()}</a>')
    langs = ''.join(langs)
    w(f'''<header class="hdr">
<div class="cols wrapw" style="align-items:center">
<div class="hleft">
<a class="logo" href="#top">telo.sabe</a>
<nav class="nav" aria-label="{t['nav_label']}">{nav}</nav>
<button type="button" class="burger" aria-expanded="false" aria-controls="mmenu" aria-label="{t['menu_open']}" data-open="{t['menu_open']}" data-close="{t['menu_close']}"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" aria-hidden="true"><path d="M4 9h16M4 15h16"/></svg></button>
</div>
<div class="hright">
<div class="langs" role="group" aria-label="{t['lang_label']}">{langs}</div>
<a class="write" href="#contact">{t['header_btn']} {ARROW}</a>
</div>
</div>
<div class="mmenu" id="mmenu" hidden>
<nav aria-label="{t['nav_label']}">{''.join(f'<a href="{h}">{n}</a>' for h, n in t['nav_footer'])}</nav>
<div class="mlangs">{langs}</div>
</div>
</header>
<main id="main">
''')

    # ---------- hero
    cap = (f'<img class="place-img" src="{img}{t["hero_caption_img"]}" alt="{t["hero_caption_text"]}" width="600" height="158">'
           if t['hero_caption_img'] else f'<p class="place">{t["hero_caption_text"]}</p>')
    w(f'''<section id="top" class="sec" style="padding-top:8px;padding-bottom:40px">
<div class="cols wrapw" style="align-items:stretch">
<div class="card green hero-card">
<p class="eyebrow">{t['hero_eyebrow']}</p>
<h1 class="h1">{t['hero_h1']}</h1>
{pill(wa(t['wa_hello']), t['wa_btn'], 296)}
</div>
<div class="photo" style="aspect-ratio:3/4;background:#5E6B57">
<img src="{img}hero.jpg" alt="{t['hero_alt']}" width="1350" height="1800" style="object-position:center 55%" fetchpriority="high">
<div class="shade" aria-hidden="true"></div>
{cap}
</div>
</div>
</section>
''')

    # ---------- about
    W = t['about_title_w']
    w(f'''<section id="about" class="sec">
<div class="wrapw stack">
<div class="rule"><h2 class="big">{t['about_title']}</h2></div>
<div class="about-grid">
<div class="card cream about-card a-name">
<p class="hand-name">{t['about_name']}</p>
<p class="caps small muted">{t['about_qual']}</p>
</div>
<div class="card sage a-story"><p class="body">{t['about_lead']}</p><p class="body">{t['about_story']}</p></div>
<div class="photo a-photo" style="aspect-ratio:3/4;background:#C9D2BF">
<img src="{img}about.jpg" alt="{t['about_alt']}" width="1200" height="1600" loading="lazy" style="object-position:center 40%;transform:scale(1.45);transform-origin:56% 88%">
{notch(216, f'<a class="pill" href="#reviews" style="width:192px">{t["about_reviews"]} {ARROW}</a>')}
</div>
<div class="card green a-keys"><p class="body">{t['about_keys']}</p></div>
</div>
</div>
</section>
''')

    # ---------- services
    def card_inner(s):
        durs = ''.join(f'<span class="dur">{d}</span>' for d in s['durs'])
        kinds = (f'<p class="kinds"><span>{s["kinds_label"]}</span> {s["kinds"]}</p>' if s['kinds'] else '')
        extras = ''.join(f'<li>{STAR}{e}</li>' for e in s['extras'])
        return (f'<div class="svc-head"><p class="svc-name">{s["name"]}</p><div class="durs">{durs}</div></div>'
                f'<p class="svc-desc">{s["desc"]}</p>{kinds}'
                f'<div class="svc-extra"><p>{s["extra_title"]}</p><ul>{extras}</ul></div>')
    tabs, panels = [], []
    for i, s in enumerate(t['services']):
        sel = 'true' if i == 0 else 'false'
        tabs.append(f'''<div class="svc-item{' on' if i == 0 else ''}">
<button type="button" role="tab" class="tab" id="tab{i}" aria-selected="{sel}" aria-controls="panel{i}" data-i="{i}"><span class="big tabname">{s['name']}</span><span class="tabcirc" aria-hidden="true">{ARROW}</span></button>
<div class="mcard"><div class="card green svc-card">{card_inner(s)}{pill(wa(s['wa']), t['wa_btn'], 296)}</div></div>
</div>''')
        panels.append(f'<div class="svc-panel" id="panel{i}" role="tabpanel" aria-labelledby="tab{i}" data-wa="{html.escape(wa(s["wa"]))}"{"" if i == 0 else " hidden"}>{card_inner(s)}</div>')
    w(f'''<section id="services" class="sec">
<div class="wrapw">
<div class="rule" style="margin-bottom:8px"><h2 class="big">{t['services_label']}</h2></div>
<div class="svc-wrap">
<div role="tablist" aria-label="{t['services_label']}" class="svc-list">
{''.join(tabs)}
<p class="lead muted">{t['services_lead']}</p>
</div>
<div class="svc-dpanel"><div class="card green svc-card svc-stack">{''.join(panels)}{pill(wa(t['services'][0]['wa']), t['wa_btn'], 296).replace('class="pill"', 'class="pill svc-wa"')}</div></div>
</div>
</div>
</section>
''')

    # ---------- quote
    qcap = (f'<img class="place-img q" src="{img}{t["quote_caption_img"]}" alt="{t["quote_caption_text"]}" width="600" height="114">'
            if t['quote_caption_img'] else f'<p class="place">{t["quote_caption_text"]}</p>')
    w(f'''<section id="quote" class="sec" style="padding-top:40px">
<div class="wrapw">
<div class="quote-card">
<img src="{img}quote.jpg" alt="" width="2000" height="1500" loading="lazy">
<div class="dim" aria-hidden="true"></div>
{qcap}
<figure>
<blockquote class="q">{t['quote']}</blockquote>
<figcaption>{t['quote_author']}</figcaption>
</figure>
</div>
</div>
</section>
''')

    # ---------- experience
    groups = []
    for name, items, also in t['exp_groups']:
        rows = ''.join(f'<div class="row"><p>{a}</p><p class="sch">{b}</p><p class="yr">{c}</p></div>' for a, b, c in items)
        al = ''
        if also:
            al = f'<div class="also"><p class="caps small">{t["exp_also"]}</p>' + ''.join(f'<p>{a} · {b} · {c}</p>' for a, b, c in also) + '</div>'
        groups.append(f'<div class="grp"><div class="grp-h">{STAR}<h3>{name}</h3></div>{rows}{al}</div>')
    certs = []
    for n in range(1, CERTS + 1):
        alt = t['cert_alt'].format(n=n, total=CERTS)
        wdt = 180 if n in CERTS_PORTRAIT else 320
        certs.append(f'<button type="button" class="cert" data-full="{img}certs/c{n}.jpg" data-alt="{alt}" aria-label="{t["cert_open"].format(n=n, total=CERTS)}"><img src="{img}certs/c{n}-thumb.jpg" alt="{alt}" loading="lazy" width="{wdt}" height="240" style="width:{wdt}px"></button>')
    w(f'''<section id="experience" class="sec">
<div class="wrapw stack" style="gap:40px">
<div class="rule"><h2 class="big">{t['exp_title']}</h2></div>
<div class="exp-wrap">
<div class="stack" style="gap:28px">
<p class="h3 serif green-t">{t['exp_h']}</p>
<p class="body" style="font-size:17px">{t['exp_p']}</p>
</div>
<div class="stack" style="gap:36px">{''.join(groups)}</div>
</div>
<div class="stack" style="gap:20px">
<div class="certs-h"><p class="caps small">{t['certs_label']}</p>
<div style="display:flex;gap:10px"><button type="button" class="arr" data-dir="-1" aria-label="{t['certs_prev']}">{ARROW_L}</button><button type="button" class="arr" data-dir="1" aria-label="{t['certs_next']}">{ARROW}</button></div></div>
<div class="track" tabindex="0" aria-label="{t['certs_label']}">{''.join(certs)}</div>
</div>
</div>
</section>
''')

    # ---------- reviews
    revs = []
    for r in REVIEWS:
        note = ''
        if lang != 'ru' and r['orig'] != lang:
            note = t['review_translated'].format(orig=ORIG_NAMES[lang][r['orig']])
        revs.append({'t': r['t'][lang], 'from': t['review_from'].format(name=r['name'][lang]), 'note': note,
                     'shot': f'{img}reviews/review-{r["shot"]}.jpg'})
    w(f'''<section id="reviews" class="sec">
<div class="wrapw stack">
<div class="rule"><h2 class="big">{t['reviews_title']}</h2></div>
<div class="rev-grid">
<div class="rev-card" data-reviews='{html.escape(json.dumps(revs, ensure_ascii=False), quote=True)}' data-prefix="{'«' if lang != 'en' else '“'}" data-suffix="{'»' if lang != 'en' else '”'}" data-shot-alt="{t['review_shot_alt']}">
<figure aria-live="polite">
<blockquote class="q rev-text"></blockquote>
<p class="rev-meta"><button type="button" class="orig"><span class="rev-from"></span> {DIAG}</button><span class="rev-note"></span></p>
</figure>
{notch(244, f'<div class="pager"><button type="button" class="nav-b" data-dir="-1" aria-label="{t["review_prev"]}">{ARROW_L}</button><span class="pos"></span><button type="button" class="nav-b" data-dir="1" aria-label="{t["review_next"]}">{ARROW}</button></div>')}
</div>
<div class="card green thanks"><p class="hand">{t['reviews_thanks']}</p></div>
</div>
</div>
</section>
''')

    # ---------- philosophy
    w(f'''<section id="philosophy" class="sec">
<div class="wrapw stack">
<div class="rule"><p class="big" aria-hidden="true">{t['phil_title']}</p></div>
<div class="grid3">
<div class="card sage phil-card"><h2 class="h2 serif green-t" style="font-size:54px">{t['phil_h']}</h2><p class="body">{t['phil_p1']}</p></div>
<div class="photo" style="aspect-ratio:3/4;background:#98A06B">
<img src="{img}philosophy.jpg" alt="{t['phil_alt']}" width="960" height="1280" loading="lazy" style="object-position:center 60%">
<div class="shade" aria-hidden="true"></div>
<p class="place">{t['phil_caption']}</p>
</div>
<div class="stack" style="gap:24px">
<div class="card cream flexc"><p class="body">{t['phil_p2']}</p></div>
<div class="card green flexc has-notch" style="min-height:200px"><p class="body">{t['phil_p3']}</p>{notch(84, f'<a class="wa" href="{wa(t["wa_hello"])}" aria-label="{t["wa_btn"]}" title="{t["wa_btn"]}">{WA_ICON}</a>')}</div>
</div>
</div>
</div>
</section>
''')

    # ---------- faq
    items = []
    for i, (q, a) in enumerate(t['faq']):
        op = i == 0
        items.append(f'''<div class="fq{' open' if op else ''}"><h3><button type="button" class="qrow" aria-expanded="{'true' if op else 'false'}" aria-controls="a{i}" id="q{i}"><span class="qt">{q}</span><span class="circle" aria-hidden="true">{PLUS}</span></button></h3><div class="ans" id="a{i}" role="region" aria-labelledby="q{i}"{'' if op else ' hidden'}><p>{a}</p></div></div>''')
    w(f'''<section id="faq" class="sec">
<div class="wrapw stack" style="gap:40px">
<div class="rule"><h2 class="big">{t['faq_title']}</h2></div>
<div class="faq-wrap">
<div class="card green faq-side has-notch">
<p class="serif" style="font-size:34px;line-height:1.08">{t['faq_side_h']}</p>
<p class="body" style="color:#E6E2D2">{t['faq_side_p']}</p>
{notch(84, f'<a class="wa" href="{wa(t["wa_hello"])}" aria-label="{t["wa_btn"]}" title="{t["wa_btn"]}">{WA_ICON}</a>')}
</div>
<div class="faq-list">{''.join(items)}</div>
</div>
</div>
</section>
''')

    # ---------- contact
    tiles = [('cream', wa(), 'WhatsApp', PHONE_PRETTY), ('sage', f'https://instagram.com/{INSTAGRAM}', 'Instagram', '@' + INSTAGRAM)]
    if t['show_telegram']:
        tiles.append(('line', f'https://t.me/{TELEGRAM}', 'Telegram', '@' + TELEGRAM))
    tiles_html = ''.join(f'<a class="tile {c}" href="{h}" target="_blank" rel="noopener"><span class="circle" aria-hidden="true">{DIAG}</span><span class="caps small">{lbl}</span><span class="tile-v">{v}</span></a>' for c, h, lbl, v in tiles)
    w(f'''<section id="contact" class="sec" style="padding-bottom:64px">
<div class="wrapw stack">
<div class="rule"><h2 class="big">{t['contact_title']}</h2></div>
<div class="contact-grid">
<div class="card green contact-card">
<p class="h2c serif">{t['contact_h']}</p>
<p class="body" style="font-size:17px;color:#E6E2D2;max-width:520px">{t['contact_lead']}</p>
</div>
<div class="stack" style="gap:24px">{tiles_html}</div>
<div class="photo contact-ph">
<img src="{img}contact.jpg" alt="{t['contact_alt']}" width="1400" height="1867" loading="lazy" style="object-position:center 60%">
<div class="shade" aria-hidden="true"></div>
<p class="place">{t['contact_caption']}</p>
</div>
</div>
</div>
</section>
</main>
''')

    # ---------- footer
    fnav = ''.join(f'<a href="{h}">{n}</a>' for h, n in t['nav_footer'])
    w(f'''<footer class="ftr">
<div class="wrapw ftr-in">
<div class="foot">
<a class="logo" href="#top">telo.sabe</a>
<nav aria-label="{t['nav_footer_label']}" class="fnav">{fnav}</nav>
<div class="langs" role="group" aria-label="{t['lang_label']}">{langs}</div>
</div>
<div class="fbot">
<div class="fleft"><p>© 2026 Telo.Sabe</p>
<!-- TODO: когда будут готовы страницы Aviso legal / Политика конфиденциальности / Cookies — добавить сюда ссылки на них -->
</div>
<a class="b2b" href="#" data-u="{EMAIL_USER}" data-d="{EMAIL_DOMAIN}" data-s="{html.escape(t['b2b_subject'])}">{t['b2b']}</a>
</div>
</div>
</footer>

<div class="lb" id="lb" role="dialog" aria-modal="true" hidden>
<button type="button" class="lb-bg" data-close aria-label="{t['lb_close']}"></button>
<figure><img alt=""><figcaption></figcaption></figure>
<button type="button" class="lbn lb-prev" aria-label="{t['lb_prev']}">{ARROW_L}</button>
<button type="button" class="lbn lb-next" aria-label="{t['lb_next']}">{ARROW}</button>
<button type="button" class="lbn lb-x" data-close aria-label="{t['lb_close']}">{CLOSE}</button>
</div>
<a class="fab" href="{wa(t['wa_hello'])}" aria-label="{t['wa_btn']}" title="{t['wa_btn']}">{WA_ICON}</a>
<script src="{pre}assets/js/site.js" defer></script>
</body>
</html>
''')
    return ''.join(out)


if __name__ == '__main__':
    for l in LANGS:
        d = ROOT if l == 'ru' else os.path.join(ROOT, l)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(build(l))
    urls = ''.join(f'''  <url>
    <loc>{SITE}{PATHS[l]}</loc>
{''.join(f'    <xhtml:link rel="alternate" hreflang="{x}" href="{SITE}{PATHS[x]}"/>' + chr(10) for x in LANGS)}    <changefreq>monthly</changefreq>
    <priority>{'1.0' if l == 'ru' else '0.8'}</priority>
  </url>
''' for l in LANGS)
    with open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n{urls}</urlset>\n')
    t = C['ru']
    with open(os.path.join(ROOT, '404.html'), 'w', encoding='utf-8') as f:
        f.write(f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Страница не найдена — Telo.Sabe</title>
<meta name="robots" content="noindex">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/css/fonts.css">
<link rel="stylesheet" href="/assets/css/site.css">
</head>
<body>
<header class="hdr"><div class="wrapw"><a class="logo" href="/">telo.sabe</a></div></header>
<main class="sec">
<div class="wrapw stack">
<div class="rule"><h1 class="big">404</h1></div>
<div class="card green nf">
<p class="h2c serif">Такой страницы нет, <span class="it hl">но тело всё равно знает дорогу.</span></p>
<p class="body" style="color:#E6E2D2">Página no encontrada · Page not found</p>
<div class="nf-links"><a class="pill" href="/" style="width:auto;padding:0 28px">На главную {ARROW}</a><a class="pill" href="/es/" style="width:auto;padding:0 28px">ES {ARROW}</a><a class="pill" href="/en/" style="width:auto;padding:0 28px">EN {ARROW}</a></div>
</div>
</div>
</main>
</body>
</html>
''')
    print('ok')
