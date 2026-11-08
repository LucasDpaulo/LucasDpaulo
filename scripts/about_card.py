"""Gera assets/about.svg: cartão "Sobre mim" do README.

Para mudar um texto, edite as constantes abaixo e rode:
    python3 scripts/about_card.py
"""
from html import escape
from pathlib import Path

NAME = "Lucas De Paulo"
ROLE = "Software Developer | AI Engineer"
BACKGROUND = "Formação em Design"
FOCUS = ["Desenvolvimento full-stack", "Agentes de IA", "Next.js & Python"]
BUILDING = "Gnomon"
STUDYING = "IA na UFPE"
DESCRIPTION = [
    "Entusiasta de tecnologia e curioso pelo open source",
    "Resolvo problemas com soluções práticas e bem arquitetadas",
    "Atenção ao design em cada detalhe",
    "Movido por curiosidade e criatividade",
]
WELCOME = [
    "Fique à vontade para explorar meus repositórios.",
    "Nem tudo é público, mas o que está aberto fica à disposição.",
]

# Cores: as mesmas do README (fundo escuro + um verde de destaque)
BG, BORDER, PANEL = "#272833", "#3a3c4e", "#2f3140"
TEXT, MUTED, ACCENT = "#f8f8f2", "#9a9cab", "#A9DC76"

W, PAD = 760, 40
SANS = "'Segoe UI',Ubuntu,'Helvetica Neue',Arial,sans-serif"
MONO = "'DejaVu Sans Mono',Consolas,'Courier New',monospace"


def text_w(s, size):
    """Largura aproximada de um texto em fonte sem serifa."""
    return sum(0.33 if c in " .,'|il" else 0.62 if c.isupper() else 0.54 for c in s) * size


parts, delay = [], 0.0


def group(svg):
    """Bloco que aparece com um leve fade, um depois do outro."""
    global delay
    parts.append(f'<g class="in" style="animation-delay:{delay:.2f}s">{svg}</g>')
    delay += 0.18


def label(x, y, s):
    return f'<text x="{x}" y="{y}" fill="{ACCENT}" font-family="{MONO}" font-size="12" letter-spacing="2">{escape(s.upper())}</text>'


y = 64
# Cabeçalho: nome, cargo e formação
group(
    f'<text x="{PAD}" y="{y}" fill="{TEXT}" font-family="{SANS}" font-size="30" font-weight="700">{escape(NAME)}</text>'
    f'<text x="{PAD}" y="{y + 32}" fill="{MUTED}" font-family="{SANS}" font-size="17">{escape(ROLE)}</text>'
)
bw = text_w(BACKGROUND, 13) + 28
group(
    f'<rect x="{W - PAD - bw}" y="{y - 22}" width="{bw:.0f}" height="28" rx="14" fill="none" stroke="{ACCENT}"/>'
    f'<text x="{W - PAD - bw / 2}" y="{y - 3}" text-anchor="middle" fill="{ACCENT}" font-family="{SANS}" font-size="13">{escape(BACKGROUND)}</text>'
)
y += 62
parts.append(f'<path d="M{PAD} {y}H{W - PAD}" stroke="{BORDER}"/>')

# Foco: etiquetas
y += 38
chips, x = [label(PAD, y, "Foco")], PAD
for f in FOCUS:
    cw = text_w(f, 14) + 30
    chips.append(
        f'<rect x="{x}" y="{y + 14}" width="{cw:.0f}" height="32" rx="8" fill="{PANEL}" stroke="{BORDER}"/>'
        f'<text x="{x + cw / 2:.1f}" y="{y + 35}" text-anchor="middle" fill="{TEXT}" font-family="{SANS}" font-size="14">{escape(f)}</text>'
    )
    x += cw + 10
group("".join(chips))

# Construindo / Estudando
y += 100
half = (W - 2 * PAD - 16) / 2
cards = []
for i, (lab, val) in enumerate([("Construindo", BUILDING), ("Estudando", STUDYING)]):
    cx = PAD + i * (half + 16)
    cards.append(
        f'<rect x="{cx}" y="{y - 22}" width="{half:.0f}" height="66" rx="10" fill="{PANEL}" stroke="{BORDER}"/>'
        + label(cx + 20, y + 2, lab)
        + f'<text x="{cx + 20}" y="{y + 28}" fill="{TEXT}" font-family="{SANS}" font-size="18" font-weight="600">{escape(val)}</text>'
    )
group("".join(cards))

# Sobre mim
y += 88
lines = [label(PAD, y, "Sobre mim")]
for k, d in enumerate(DESCRIPTION):
    ly = y + 32 + k * 28
    lines.append(
        f'<circle cx="{PAD + 4}" cy="{ly - 5}" r="3" fill="{ACCENT}"/>'
        f'<text x="{PAD + 18}" y="{ly}" fill="{TEXT}" font-family="{SANS}" font-size="16">{escape(d)}</text>'
    )
group("".join(lines))

# Convite final
y += 32 + len(DESCRIPTION) * 28 + 14
bh = 26 + len(WELCOME) * 24
wl = [
    f'<rect x="{PAD}" y="{y}" width="{W - 2 * PAD}" height="{bh}" rx="10" fill="{PANEL}"/>'
    f'<rect x="{PAD}" y="{y}" width="4" height="{bh}" rx="2" fill="{ACCENT}"/>'
]
for k, t in enumerate(WELCOME):
    wl.append(f'<text x="{PAD + 22}" y="{y + 30 + k * 24}" fill="{MUTED}" font-family="{SANS}" font-size="15" font-style="italic">{escape(t)}</text>')
group("".join(wl))

H = y + bh + PAD
summary = f"{NAME}, {ROLE}. " + " ".join(d + "." for d in DESCRIPTION) + " " + " ".join(WELCOME)
svg = (
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">'
    f'<title id="t">{escape(NAME)} — {escape(ROLE)}</title><desc id="d">{escape(summary)}</desc>'
    "<style>.in{animation:in .7s ease both}"
    "@keyframes in{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}"
    "@media (prefers-reduced-motion:reduce){.in{animation:none}}</style>"
    f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="{BG}" stroke="{BORDER}"/>'
    + "".join(parts)
    + "</svg>\n"
)
out = Path(__file__).resolve().parent.parent / "assets" / "about.svg"
out.write_text(svg, encoding="utf-8")
print(f"{out} ({W}x{H})")
