"""
9Pilla Brandbook v2.0 — PDF generator (modelo "grátis até regular")
"""
import os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import HexColor, Color, white, black
from reportlab.lib.units import mm, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from PIL import Image as PILImage

# ---- paths ----
ROOT = "/home/user/workspace/9pilla/brandbook"
FONTS = os.path.join(ROOT, "fonts")
ASSETS_LAND = "/home/user/workspace/9pilla/landing_v2/assets"
OUT = os.path.join(ROOT, "9Pilla_Brandbook.pdf")

# ---- fonts ----
pdfmetrics.registerFont(TTFont("DM", os.path.join(FONTS, "DMSans-Regular.ttf")))
pdfmetrics.registerFont(TTFont("DM-Md", os.path.join(FONTS, "DMSans-Medium.ttf")))
pdfmetrics.registerFont(TTFont("DM-Bd", os.path.join(FONTS, "DMSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DM-Bk", os.path.join(FONTS, "DMSans-Black.ttf")))

# ---- colors ----
MOSS = HexColor("#3D5240")
BONE = HexColor("#FAF7F1")
INK  = HexColor("#0A0A0A")
LINE = HexColor("#E7E2D8")
MUTED = HexColor("#7A7670")
WHITE = white

# ---- pagesize: landscape A4 ----
W, H = landscape(A4)  # 842 x 595

# ---- helpers ----
def draw_bg(c, color=BONE):
    c.setFillColor(color)
    c.rect(0, 0, W, H, fill=1, stroke=0)

def page_chrome(c, page_num, total, section):
    """Top brand mark + footer with page number."""
    # top-left brand
    c.setFont("DM-Bd", 9)
    c.setFillColor(MOSS)
    c.drawString(28, H - 24, "9PILLA   ·   BRAND GUIDE   ·   v2.0")
    # section
    c.setFont("DM", 8.5)
    c.setFillColor(MUTED)
    c.drawRightString(W - 28, H - 24, section.upper())
    # top hairline
    c.setStrokeColor(LINE)
    c.setLineWidth(0.5)
    c.line(28, H - 30, W - 28, H - 30)
    # footer
    c.setStrokeColor(LINE)
    c.line(28, 24, W - 28, 24)
    c.setFillColor(MUTED)
    c.setFont("DM", 8)
    c.drawString(28, 12, "9Pilla — Liberdade. Em primeira pessoa.")
    c.drawRightString(W - 28, 12, f"{page_num:02d} / {total:02d}")

def section_eyebrow(c, x, y, text, color=MOSS):
    c.setFillColor(color)
    c.setFont("DM-Bd", 8.5)
    # letter-spacing simulated by drawing each char
    spacing = 2.2
    cx = x
    for ch in text.upper():
        c.drawString(cx, y, ch)
        cx += c.stringWidth(ch, "DM-Bd", 8.5) + spacing

def big_title(c, x, y, text, size=44, color=INK, font="DM-Bk"):
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawString(x, y, text)

def body_text(c, x, y, text, size=10, color=INK, font="DM", width=None, leading=None):
    c.setFillColor(color)
    c.setFont(font, size)
    if leading is None:
        leading = size * 1.45
    if width is None:
        c.drawString(x, y, text)
        return y - leading
    # wrap
    words = text.split()
    line = ""
    cur_y = y
    for w in words:
        test = (line + " " + w).strip()
        if c.stringWidth(test, font, size) <= width:
            line = test
        else:
            c.drawString(x, cur_y, line)
            cur_y -= leading
            line = w
    if line:
        c.drawString(x, cur_y, line)
        cur_y -= leading
    return cur_y

def page_number_label(c, num, total):
    c.setFillColor(MOSS)
    c.setFont("DM-Bd", 9)
    c.drawString(28, 36, f"PG {num:02d}")

# =====================================================
# PAGES
# =====================================================

TOTAL = 16
c = canvas.Canvas(OUT, pagesize=landscape(A4))
c.setTitle("9Pilla — Brand Guide v2.0")
c.setAuthor("Perplexity Computer")
c.setSubject("Identidade visual, voz e direção de marca da 9Pilla")

# -------- PAGE 1: COVER --------
draw_bg(c, MOSS)
# huge "9" mark
c.setFillColor(BONE)
c.setFont("DM-Bk", 360)
c.drawString(40, 90, "9")
# wordmark
c.setFillColor(BONE)
c.setFont("DM-Bk", 64)
c.drawString(W - 360, H - 200, "9Pilla.")
# eyebrow
c.setFillColor(BONE)
c.setFont("DM-Bd", 11)
spacing = 3
cx = W - 360
for ch in "BRAND GUIDE · V2.0".upper():
    c.drawString(cx, H - 230, ch)
    cx += c.stringWidth(ch, "DM-Bd", 11) + spacing
# tagline
c.setFillColor(BONE)
c.setFont("DM-Md", 22)
c.drawString(W - 360, H - 320, "Liberdade.")
c.drawString(W - 360, H - 350, "Em primeira pessoa.")
# meta footer
c.setFillColor(BONE)
c.setFont("DM", 9)
c.drawString(W - 360, 60, "Documento oficial · 16 de maio de 2026")
c.drawString(W - 360, 46, "9pilla.com   ·   @9pilla.link")
# hairline top
c.setStrokeColor(BONE)
c.setLineWidth(0.8)
c.line(28, H - 30, W - 28, H - 30)
c.setFont("DM-Bd", 9)
c.setFillColor(BONE)
c.drawString(28, H - 24, "9PILLA · BRAND GUIDE")
c.drawRightString(W - 28, H - 24, "CAPA")
c.showPage()

# -------- PAGE 2: SUMÁRIO --------
draw_bg(c)
page_chrome(c, 2, TOTAL, "Sumário")
section_eyebrow(c, 60, H - 80, "Sumário")
big_title(c, 60, H - 150, "O que tem aqui.", 44)

items = [
    ("01", "O que é a 9Pilla"),
    ("02", "Manifesto + Tagline"),
    ("03", "Tom de voz"),
    ("04", "Posicionamento"),
    ("05", "Roadmap público"),
    ("06", "Logo + uso"),
    ("07", "Paleta de cores"),
    ("08", "Tipografia"),
    ("09", "Fotografia"),
    ("10", "Raquel · protagonista"),
    ("11", "CVM · Blindagem"),
    ("12", "Canais e conteúdo"),
    ("13", "Turma (grátis até regular)"),
    ("14", "Don'ts definitivos"),
]
y = H - 220
col_x = [60, 430]
for i, (n, t) in enumerate(items):
    col = i % 2
    if i > 0 and col == 0:
        y -= 28
    x = col_x[col]
    c.setFillColor(MOSS)
    c.setFont("DM-Bd", 14)
    c.drawString(x, y, n)
    c.setFillColor(INK)
    c.setFont("DM-Md", 14)
    c.drawString(x + 40, y, t)
    # hairline
    c.setStrokeColor(LINE)
    c.line(x, y - 6, x + 330, y - 6)
c.showPage()

# -------- PAGE 3: O QUE É --------
draw_bg(c)
page_chrome(c, 3, TOTAL, "01 · O que é a 9Pilla")
section_eyebrow(c, 60, H - 80, "01 · A marca")
big_title(c, 60, H - 150, "A 9Pilla é um", 36)
big_title(c, 60, H - 200, "diário público.", 36, MOSS)

cy = body_text(c, 60, H - 250,
    "Todo dia útil, às 09:09, o Morning Call abre o pregão pela voz de quem opera o próprio dinheiro. PETR4, VALE3, BOVA11. Em primeira pessoa. Carteira aberta.",
    size=13, width=480, leading=22)

# Two columns: É / Não é
col_y = H - 380
col1_x = 60
col2_x = 440
c.setFillColor(MOSS); c.setFont("DM-Bd", 11); c.drawString(col1_x, col_y, "É")
c.setFillColor(MUTED); c.setFont("DM-Bd", 11); c.drawString(col2_x, col_y, "NÃO É")
c.setStrokeColor(LINE); c.line(col1_x, col_y - 8, col1_x + 330, col_y - 8)
c.line(col2_x, col_y - 8, col2_x + 330, col_y - 8)

e_items = [
    "Diário em primeira pessoa",
    "Carteira aberta · operação por operação",
    "Relato sob CVM 20/2021",
    "Liberdade como projeto de vida",
]
n_items = [
    "Call, sinal ou recomendação",
    "Curso de 12 módulos promissor",
    "Coach, guru ou fórmula secreta",
    "Promessa de ficar rico em 30 dias",
]
yy = col_y - 24
for a, b in zip(e_items, n_items):
    c.setFillColor(INK); c.setFont("DM", 11)
    c.drawString(col1_x, yy, "—  " + a)
    c.setFillColor(INK); c.setFont("DM", 11)
    c.drawString(col2_x, yy, "—  " + b)
    yy -= 22
c.showPage()

# -------- PAGE 4: MANIFESTO + TAGLINE --------
draw_bg(c, INK)
# top chrome custom
c.setFont("DM-Bd", 9); c.setFillColor(BONE)
c.drawString(28, H - 24, "9PILLA · BRAND GUIDE · v2.0")
c.setFont("DM", 8.5); c.setFillColor(HexColor("#8a8782"))
c.drawRightString(W - 28, H - 24, "02 · MANIFESTO")
c.setStrokeColor(HexColor("#2a2a28")); c.setLineWidth(0.5)
c.line(28, H - 30, W - 28, H - 30); c.line(28, 24, W - 28, 24)
c.setFillColor(HexColor("#8a8782")); c.setFont("DM", 8)
c.drawString(28, 12, "9Pilla — Liberdade. Em primeira pessoa.")
c.drawRightString(W - 28, 12, "04 / 16")

# eyebrow
c.setFillColor(BONE); c.setFont("DM-Bd", 8.5)
spacing = 2.2; cx = 60
for ch in "MANIFESTO":
    c.drawString(cx, H - 80, ch); cx += c.stringWidth(ch, "DM-Bd", 8.5) + spacing

# big quote
c.setFillColor(BONE)
c.setFont("DM-Bk", 48)
c.drawString(60, H - 160, "Eu penso em")
c.drawString(60, H - 210, "liberdade.")
# moss dot
c.setFillColor(MOSS); c.setFont("DM-Bk", 48)
c.drawString(60 + c.stringWidth("liberdade", "DM-Bk", 48) + 4, H - 210, ".")

# body
manifesto = [
    "Não quero esperar 10, 20, 30 anos pra viver a vida que eu",
    "sonho. Quero dar passos largos. Por isso opções — com risco",
    "calculado e posição dimensionada, sempre.",
    "",
    "Comecei com R$ 400. Hoje opero PETR4, VALE3 e BOVA11",
    "com regra escrita antes de cada operação e o diário aberto",
    "pra qualquer um conferir.",
    "",
    "Não vendo sinal. Não vendo curso. Não prometo virada de chave.",
    "Eu mostro o caminho como ele é — vencendo e perdendo, sem maquiar.",
]
c.setFillColor(BONE); c.setFont("DM", 13)
yy = H - 280
for line in manifesto:
    c.drawString(60, yy, line); yy -= 22

# tagline big right
c.setFillColor(MOSS); c.setFont("DM-Bk", 28)
c.drawString(60, 80, "O simples sempre vence.")
c.showPage()

# -------- PAGE 5: TOM DE VOZ --------
draw_bg(c)
page_chrome(c, 5, TOTAL, "03 · Tom de voz")
section_eyebrow(c, 60, H - 80, "03 · Voz")
big_title(c, 60, H - 150, "Como a 9Pilla fala.", 36)

cy = body_text(c, 60, H - 200,
    "Simples, direta, honesta. Inspiração: Buffett — clareza, frugalidade verbal, honestidade radical. Sem jargão de quem quer impressionar. Sem o tom messiânico de coach. Sem firula corporativa.",
    size=12, width=720, leading=20)

# table
col_y = cy - 30
c.setFillColor(MOSS); c.setFont("DM-Bd", 10); c.drawString(60, col_y, "USE")
c.setFillColor(MUTED); c.setFont("DM-Bd", 10); c.drawString(420, col_y, "NÃO USE")
c.setStrokeColor(LINE); c.line(60, col_y - 6, 60 + 330, col_y - 6)
c.line(420, col_y - 6, 420 + 330, col_y - 6)

rows = [
    ("Opero, operei, operando", "Aposto, apostar, aposta"),
    ("Risco calculado, posição dimensionada", "Tiro certo, trade infalível"),
    ("Relato pessoal, diário", "Sinal, call paga, recomendação"),
    ("Capital próprio, posição própria", "Robô, fórmula secreta, método"),
    ("Em primeira pessoa", "Trader, coach, mentor"),
    ("Estudei, aprendi, tô estudando", "Sou expert, domino o mercado"),
]
yy = col_y - 24
for a, b in rows:
    c.setFillColor(INK); c.setFont("DM", 10.5)
    c.drawString(60, yy, "+  " + a)
    c.setFillColor(INK); c.setFont("DM", 10.5)
    c.drawString(420, yy, "–  " + b)
    yy -= 20

# rule blocks
yy -= 14
c.setFillColor(MOSS); c.setFont("DM-Bd", 10); c.drawString(60, yy, 'REGRA DE OURO')
yy -= 16
c.setFillColor(INK); c.setFont("DM-Md", 13)
c.drawString(60, yy, '"9Pilla" sempre com P maiúsculo. Nunca "9pilla", "9PILLA" ou "9 Pilla".')
c.showPage()

# -------- PAGE 6: POSICIONAMENTO --------
draw_bg(c)
page_chrome(c, 6, TOTAL, "04 · Posicionamento")
section_eyebrow(c, 60, H - 80, "04 · Posicionamento")
big_title(c, 60, H - 150, "Pra quem é.", 36)
big_title(c, 60, H - 200, "E pra que serve.", 36, MOSS)

# Three columns
col_w = 230
gutter = 30
x0 = 60
y0 = H - 270
cols = [
    ("CATEGORIA",
     "Diário público de operações em opções na bolsa brasileira. Não é educação, não é assessoria. É reality financeiro autoral."),
    ("PARA QUEM",
     "Mulheres 25-45 que querem ACELERAR a liberdade financeira e estão cansadas de coach, curso e promessa fácil. Querem ver, com os próprios olhos, alguém operando de verdade."),
    ("DIFERENCIAL",
     "Em primeira pessoa, carteira aberta, todo dia útil às 09:09. CVM-blindada. Trajetória pública: CNPI até dez/2026 e Cert. de Assessora até mar/2027 — em estudo aberto."),
]
for i, (title, body) in enumerate(cols):
    x = x0 + i * (col_w + gutter)
    c.setFillColor(MOSS); c.setFont("DM-Bd", 10); c.drawString(x, y0, title)
    c.setStrokeColor(MOSS); c.setLineWidth(1.2); c.line(x, y0 - 6, x + 28, y0 - 6)
    body_text(c, x, y0 - 24, body, size=11, width=col_w, leading=17)

# closing slogan
c.setFillColor(MOSS); c.setFont("DM-Bk", 18)
c.drawString(60, 80,
    "A 9Pilla é o diário público de quem opera o próprio dinheiro")
c.drawString(60, 56, "em opções — em primeira pessoa, todo dia útil às 09:09.")
c.showPage()

# -------- PAGE 7: ROADMAP --------
draw_bg(c)
page_chrome(c, 7, TOTAL, "05 · Roadmap")
section_eyebrow(c, 60, H - 80, "05 · Roadmap público")
big_title(c, 60, H - 150, "Onde a 9Pilla está.", 32)
big_title(c, 60, H - 195, "E onde ela vai.", 32, MOSS)

# Horizontal timeline
tx = 60; ty = H - 320
tw = W - 120
# line
c.setStrokeColor(LINE); c.setLineWidth(2)
c.line(tx + 30, ty, tx + tw - 30, ty)
steps = [
    ("HOJE · mai/2026", "Diário público", "Opero o próprio capital. Mostro tudo. Turma gratuita no WhatsApp.", True),
    ("até dez/2026", "CNPI em estudo", "Analista de Valores Mobiliários. Estudando agora.", False),
    ("até mar/2027", "Cert. Assessora", "Credencial pra Turma virar produto regular.", False),
]
n = len(steps)
for i, (when, what, desc, now) in enumerate(steps):
    sx = tx + 30 + i * ((tw - 60) / (n - 1))
    # dot
    if now:
        c.setFillColor(MOSS); c.circle(sx, ty, 10, fill=1, stroke=0)
        c.setFillColor(BONE); c.circle(sx, ty, 5, fill=1, stroke=0)
    else:
        c.setFillColor(MOSS); c.circle(sx, ty, 7, fill=1, stroke=0)
    # text below
    c.setFillColor(MOSS); c.setFont("DM-Bd", 9)
    c.drawCentredString(sx, ty - 26, when.upper())
    c.setFillColor(INK); c.setFont("DM-Bk", 13)
    c.drawCentredString(sx, ty - 50, what.upper())
    # desc wrap
    c.setFillColor(MUTED); c.setFont("DM", 9.5)
    words = desc.split()
    line = ""; lines = []
    for w in words:
        test = (line + " " + w).strip()
        if c.stringWidth(test, "DM", 9.5) <= 170:
            line = test
        else:
            lines.append(line); line = w
    if line: lines.append(line)
    yyy = ty - 70
    for l in lines:
        c.drawCentredString(sx, yyy, l); yyy -= 13

c.showPage()

# -------- PAGE 8: LOGO --------
draw_bg(c)
page_chrome(c, 8, TOTAL, "06 · Logo")
section_eyebrow(c, 60, H - 80, "06 · Logo")
big_title(c, 60, H - 150, "Marca.", 44)

# Logo over bone (large)
logo_moss = os.path.join(ASSETS_LAND, "logo_moss.png")
logo_bege = os.path.join(ASSETS_LAND, "logo_bege.png")
logo_preto = os.path.join(ASSETS_LAND, "logo_preto.png")
logo_verde = os.path.join(ASSETS_LAND, "logo_verde.png")

# big mark on bone box
c.setFillColor(BONE); c.setStrokeColor(LINE); c.setLineWidth(1)
c.roundRect(60, H - 380, 360, 200, 12, fill=1, stroke=1)
c.drawImage(logo_moss, 60 + 30, H - 380 + 60, width=300, height=80, mask='auto', preserveAspectRatio=True)
c.setFillColor(MUTED); c.setFont("DM-Bd", 9)
c.drawString(60, H - 400, "LOGO MOSS  ·  SOBRE BONE")

# small boxes — 3 variantes
boxes = [
    (BONE, INK, logo_preto, "PRETO sobre BONE"),
    (INK, BONE, logo_bege, "BEGE sobre INK"),
    (MOSS, BONE, logo_bege, "BEGE sobre MOSS"),
]
bx0 = 450
by0 = H - 280
bw, bh = 100, 100
for i, (bg, fg, path, label) in enumerate(boxes):
    x = bx0 + i * (bw + 16)
    c.setFillColor(bg); c.setStrokeColor(LINE)
    c.roundRect(x, by0, bw, bh, 8, fill=1, stroke=1)
    c.drawImage(path, x + 10, by0 + 30, width=80, height=40, mask='auto', preserveAspectRatio=True)
    c.setFillColor(MUTED); c.setFont("DM-Bd", 7)
    c.drawString(x, by0 - 14, label)

# rules
ry = H - 440
c.setFillColor(MOSS); c.setFont("DM-Bd", 10); c.drawString(60, ry, "REGRAS")
c.setStrokeColor(MOSS); c.setLineWidth(1.2); c.line(60, ry - 6, 60 + 28, ry - 6)
rules = [
    "Área de proteção = altura do '9' em todos os lados",
    "Tamanho mínimo: 24px digital · 8mm impresso",
    "Não distorcer, não inclinar, não trocar o tipo",
    "Não escurecer e não clarear o Moss",
    "Versão preferida sempre Moss sobre Bone",
]
yy = ry - 26
for r in rules:
    c.setFillColor(INK); c.setFont("DM", 10.5)
    c.drawString(60, yy, "—  " + r); yy -= 18

c.showPage()

# -------- PAGE 9: PALETA --------
draw_bg(c)
page_chrome(c, 9, TOTAL, "07 · Paleta")
section_eyebrow(c, 60, H - 80, "07 · Paleta")
big_title(c, 60, H - 150, "Três cores.", 36)
big_title(c, 60, H - 195, "Só.", 36, MOSS)

# main 3 swatches
swatches = [
    (MOSS, "MOSS", "#3D5240", "61 · 82 · 64", "Cor principal da marca."),
    (BONE, "BONE", "#FAF7F1", "250 · 247 · 241", "Fundo claro · off-white."),
    (INK, "INK", "#0A0A0A", "10 · 10 · 10", "Tinta · texto principal."),
]
sw_w = 230; sw_h = 200
sx = 60
sy = H - 410
for i, (col, name, hexv, rgb, desc) in enumerate(swatches):
    x = sx + i * (sw_w + 16)
    c.setFillColor(col); c.rect(x, sy, sw_w, sw_h, fill=1, stroke=0)
    # label inside
    label_color = INK if col == BONE else BONE
    c.setFillColor(label_color); c.setFont("DM-Bk", 28)
    c.drawString(x + 16, sy + sw_h - 40, name)
    c.setFillColor(label_color); c.setFont("DM-Bd", 9)
    c.drawString(x + 16, sy + 24, hexv)
    c.drawString(x + 16, sy + 12, rgb)
    # under label
    c.setFillColor(INK); c.setFont("DM-Md", 10.5)
    c.drawString(x, sy - 16, desc)

# Secondary
sy2 = sy - 80
c.setFillColor(MOSS); c.setFont("DM-Bd", 9); c.drawString(60, sy2, "SECUNDÁRIAS · USAR COM PARCIMÔNIA")
c.setStrokeColor(LINE); c.line(60, sy2 - 6, 60 + 220, sy2 - 6)
sub = [
    (HexColor("#E7E2D8"), "Line", "#E7E2D8"),
    (HexColor("#7A7670"), "Muted", "#7A7670"),
]
for i, (col, n, hx) in enumerate(sub):
    x = 60 + i * 160
    c.setFillColor(col); c.rect(x, sy2 - 50, 30, 30, fill=1, stroke=0)
    c.setFillColor(INK); c.setFont("DM-Bd", 10); c.drawString(x + 40, sy2 - 30, n)
    c.setFillColor(MUTED); c.setFont("DM", 9); c.drawString(x + 40, sy2 - 44, hx)

c.showPage()

# -------- PAGE 10: TIPOGRAFIA --------
draw_bg(c)
page_chrome(c, 10, TOTAL, "08 · Tipografia")
section_eyebrow(c, 60, H - 80, "08 · Tipografia")
big_title(c, 60, H - 150, "DM Sans.", 44)

# scale
y = H - 220
c.setFillColor(INK); c.setFont("DM-Bk", 64); c.drawString(60, y, "Hero 64")
y -= 70
c.setFillColor(INK); c.setFont("DM-Bk", 40); c.drawString(60, y, "Title 40")
y -= 50
c.setFillColor(INK); c.setFont("DM-Bd", 24); c.drawString(60, y, "Heading 24")
y -= 36
c.setFillColor(INK); c.setFont("DM-Md", 16); c.drawString(60, y, "Subheading 16")
y -= 26
c.setFillColor(INK); c.setFont("DM", 13); c.drawString(60, y, "Body 13 — leitura confortável e neutra.")
y -= 20
c.setFillColor(MUTED); c.setFont("DM", 10); c.drawString(60, y, "CAPTION · LABEL · 10")

# right column rules
rx = 480
ry = H - 220
c.setFillColor(MOSS); c.setFont("DM-Bd", 10); c.drawString(rx, ry, "REGRAS")
c.setStrokeColor(MOSS); c.setLineWidth(1.2); c.line(rx, ry - 6, rx + 28, ry - 6)
rules = [
    "Display: DM Sans Black (900)",
    "Body: DM Sans Regular (400)",
    "Eyebrow: DM Sans Bold (700) CAPS",
    "Letter-spacing alto só em eyebrows",
    "Floor: 12px digital · 9pt impresso",
    "Numerais: sempre tabular-nums",
    "Wordmark serif aparece SÓ no logo",
]
yy = ry - 24
for r in rules:
    c.setFillColor(INK); c.setFont("DM", 11)
    c.drawString(rx, yy, "—  " + r); yy -= 18

c.showPage()

# -------- PAGE 11: FOTOGRAFIA --------
draw_bg(c)
page_chrome(c, 11, TOTAL, "09 · Fotografia")
section_eyebrow(c, 60, H - 80, "09 · Fotografia")
big_title(c, 60, H - 150, "Editorial. Terrosa.", 32)
big_title(c, 60, H - 195, "Carteira aberta.", 32, MOSS)

# Photo grid
photos = [
    ("hero_liberdade.jpg", "Liberdade"),
    ("horizonte.jpg", "Caminho"),
    ("sonho_quiosque.jpg", "Sonho · Bahia"),
    ("caderno.jpg", "Disciplina"),
]
px = 60; py = H - 410
pw = 180; ph = 130
for i, (fn, label) in enumerate(photos):
    x = px + i * (pw + 14)
    path = os.path.join(ASSETS_LAND, "img", fn)
    try:
        c.drawImage(path, x, py, width=pw, height=ph, mask='auto', preserveAspectRatio=True)
    except Exception:
        c.setFillColor(LINE); c.rect(x, py, pw, ph, fill=1, stroke=0)
    c.setFillColor(MUTED); c.setFont("DM-Bd", 8.5)
    c.drawString(x, py - 12, label.upper())

# rules
rules_y = py - 50
c.setFillColor(MOSS); c.setFont("DM-Bd", 10); c.drawString(60, rules_y, "DIREÇÃO")
c.setStrokeColor(MOSS); c.setLineWidth(1.2); c.line(60, rules_y - 6, 60 + 28, rules_y - 6)
rules = [
    "Cor neutra · contraste suave · sombras quentes",
    "Mulher de costas, varanda, mar, horizonte",
    "Mesa real · laptop · monitor · caderno · café",
    "Quiosque · prancha · areia (sonho Bahia)",
    "Foto pessoal da Raquel > foto editorial sempre",
]
yy = rules_y - 26
for r in rules:
    c.setFillColor(INK); c.setFont("DM", 10.5)
    c.drawString(60, yy, "—  " + r); yy -= 16

c.showPage()

# -------- PAGE 12: RAQUEL --------
draw_bg(c)
page_chrome(c, 12, TOTAL, "10 · Raquel")
section_eyebrow(c, 60, H - 80, "10 · A protagonista")
big_title(c, 60, H - 150, "Raquel.", 44)
big_title(c, 60, H - 200, "Em primeira pessoa.", 32, MOSS)

# Two columns
cx1, cx2 = 60, 440
cy = H - 260

c.setFillColor(MOSS); c.setFont("DM-Bd", 10); c.drawString(cx1, cy, "TRAJETÓRIA")
c.setStrokeColor(MOSS); c.setLineWidth(1.2); c.line(cx1, cy - 6, cx1 + 28, cy - 6)
body_text(c, cx1, cy - 26,
    "Empreendedora há 13+ anos no Mercado do Bairro. Graduanda em Administração com ênfase em Análise de Dados. Certificada Google em Análise de Dados. Passagens pela área financeira de algumas empresas.",
    size=11, width=340, leading=17)

# Right column: B7 + meta
c.setFillColor(MOSS); c.setFont("DM-Bd", 10); c.drawString(cx2, cy, "FORMAÇÃO ATUAL · B7 BUSINESS SCHOOL")
c.setStrokeColor(MOSS); c.setLineWidth(1.2); c.line(cx2, cy - 6, cx2 + 28, cy - 6)
body_text(c, cx2, cy - 26,
    "Dupla titulação em curso: MBA em Investments & Asset Allocation e MBA em Relationship Manager. Ambos reconhecidos pelo MEC.",
    size=11, width=340, leading=17)

# Bottom strip: capital + meta
sy = 80
c.setFillColor(MOSS); c.rect(60, sy, W - 120, 80, fill=1, stroke=0)
c.setFillColor(BONE); c.setFont("DM-Bd", 9); c.drawString(80, sy + 58, "OPERANDO DESDE FEV/2026")
c.setFillColor(BONE); c.setFont("DM-Bk", 22); c.drawString(80, sy + 26, "Comecei com R$ 400.")
c.setFillColor(BONE); c.setFont("DM", 11)
c.drawString(420, sy + 36, "Meta pública: 1.000 PETR4 até dezembro de 2026.")
c.drawString(420, sy + 18, "Carteira aberta. Todo dia útil às 09:09.")
c.showPage()

# -------- PAGE 13: CVM --------
draw_bg(c)
page_chrome(c, 13, TOTAL, "11 · CVM")
section_eyebrow(c, 60, H - 80, "11 · CVM · Blindagem regulatória")
big_title(c, 60, H - 150, "Relato pessoal.", 36)
big_title(c, 60, H - 195, "Nunca recomendação.", 36, MOSS)

body_text(c, 60, H - 240,
    "Todas as comunicações públicas da 9Pilla devem respeitar a Resolução CVM nº 20/2021. O conteúdo é diário pessoal de operação própria — nunca sinal, nunca call, nunca recomendação.",
    size=12, width=720, leading=20)

# 3 rules cards
cards = [
    ("FALAR NO PASSADO", "Operei. Comprei. Saí. Fechei. Nunca: compre, venda, faça."),
    ("SEM PROMESSA", "Nada de 'rentabilidade garantida', 'lucro certo', 'fórmula infalível'."),
    ("DISCLAIMER SEMPRE", "Conteúdo informativo. Não constitui recomendação. Resultados passados não garantem futuros."),
]
cy = H - 360
cw = 230; gutter = 18
for i, (t, d) in enumerate(cards):
    x = 60 + i * (cw + gutter)
    c.setStrokeColor(MOSS); c.setLineWidth(1.2)
    c.roundRect(x, cy - 130, cw, 130, 12, fill=0, stroke=1)
    c.setFillColor(MOSS); c.setFont("DM-Bd", 9.5)
    c.drawString(x + 16, cy - 26, t)
    body_text(c, x + 16, cy - 50, d, size=11, width=cw - 32, leading=16, color=INK)

c.showPage()

# -------- PAGE 14: CANAIS --------
draw_bg(c)
page_chrome(c, 14, TOTAL, "12 · Canais")
section_eyebrow(c, 60, H - 80, "12 · Canais e conteúdo")
big_title(c, 60, H - 150, "Pulverizar.", 36)
big_title(c, 60, H - 195, "Por etapas.", 36, MOSS)

phases = [
    ("AGORA", "Q2 · 2026", [
        "Instagram @9pilla.link (foco total)",
        "Morning Call WhatsApp (seg-sex 09:09)",
        "Site 9pilla.com + Turma grátis",
    ]),
    ("EXPANDIR", "Q3-Q4 · 2026", [
        "TikTok (conteúdo nativo)",
        "YouTube Shorts (cortes verticais)",
    ]),
    ("APROFUNDAR", "2027+", [
        "YouTube long-form",
        "Podcast no Spotify",
    ]),
]
px = 60; py = H - 220
pw = 240; gut = 20
card_h = 190
for i, (label, when, items) in enumerate(phases):
    x = px + i * (pw + gut)
    # Card body with thin border
    c.setStrokeColor(LINE); c.setLineWidth(1.0)
    c.roundRect(x, py - card_h, pw, card_h, 10, fill=0, stroke=1)
    # Top header strip
    c.setFillColor(MOSS)
    p = c.beginPath()
    p.moveTo(x, py); p.lineTo(x + pw, py); p.lineTo(x + pw, py - 36); p.lineTo(x, py - 36); p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.setFillColor(BONE); c.setFont("DM-Bd", 11); c.drawString(x + 16, py - 22, label)
    c.setFillColor(BONE); c.setFont("DM", 9); c.drawRightString(x + pw - 16, py - 22, when)
    yy = py - 60
    for it in items:
        c.setFillColor(INK); c.setFont("DM", 11)
        c.drawString(x + 16, yy, "—  " + it); yy -= 20
c.showPage()

# -------- PAGE 15: PRODUTO --------
draw_bg(c)
page_chrome(c, 15, TOTAL, "13 · Turma")
section_eyebrow(c, 60, H - 80, "13 · Turma 9Pilla")
big_title(c, 60, H - 150, "Grátis.", 44)
big_title(c, 60, H - 200, "Até ficar regular.", 32, MOSS)

# Big card — grátis
c.setFillColor(MOSS); c.roundRect(60, H - 420, 340, 180, 16, fill=1, stroke=0)
c.setFillColor(BONE); c.setFont("DM-Bd", 9); c.drawString(80, H - 270, "TURMA NO WHATSAPP")
c.setFillColor(BONE); c.setFont("DM-Bk", 60); c.drawString(80, H - 340, "Grátis")
c.setFillColor(BONE); c.setFont("DM", 10); c.drawString(80, H - 365, "Enquanto a Raquel estuda CNPI e Cert. Assessora.")
c.setFillColor(BONE); c.setFont("DM", 10); c.drawString(80, H - 380, "Não é freemium. É coerência regulatória CVM.")
c.setFillColor(BONE); c.setFont("DM-Bd", 9); c.drawString(80, H - 400, "Quem entra agora vira fundadora.")

# Right column — what's included
rx = 440; ry = H - 240
c.setFillColor(MOSS); c.setFont("DM-Bd", 10); c.drawString(rx, ry, "O QUE TEM DENTRO")
c.setStrokeColor(MOSS); c.setLineWidth(1.2); c.line(rx, ry - 6, rx + 28, ry - 6)
perks = [
    "Morning Call diário em áudio · 09:09",
    "Diário público de operações em tempo real",
    "Comunidade fechada no WhatsApp",
    "Acompanhamento da meta 1.000 PETR4 ao vivo",
    "Canal único de entrada: convite WhatsApp",
]
yy = ry - 26
for p in perks:
    c.setFillColor(INK); c.setFont("DM", 11)
    c.drawString(rx, yy, "—  " + p); yy -= 18

# Bottom band: regra
c.setFillColor(MOSS); c.setFont("DM-Bd", 9); c.drawString(60, 70, "REGRA")
c.setStrokeColor(MOSS); c.setLineWidth(1.2); c.line(60, 64, 60 + 28, 64)
c.setFillColor(INK); c.setFont("DM-Md", 11)
c.drawString(60, 46, "Até a Raquel ficar regular (CNPI + Cert. Assessora), nada é cobrado. Quando virar produto pago, fundadoras seguem com condição preservada.")
c.showPage()

# -------- PAGE 16: DON'TS --------
draw_bg(c, INK)
# manual chrome
c.setFont("DM-Bd", 9); c.setFillColor(BONE)
c.drawString(28, H - 24, "9PILLA · BRAND GUIDE · v2.0")
c.setFont("DM", 8.5); c.setFillColor(HexColor("#8a8782"))
c.drawRightString(W - 28, H - 24, "14 · DON'TS DEFINITIVOS")
c.setStrokeColor(HexColor("#2a2a28")); c.setLineWidth(0.5)
c.line(28, H - 30, W - 28, H - 30); c.line(28, 24, W - 28, 24)
c.setFillColor(HexColor("#8a8782")); c.setFont("DM", 8)
c.drawString(28, 12, "9Pilla — Liberdade. Em primeira pessoa.")
c.drawRightString(W - 28, 12, "16 / 16")

c.setFillColor(BONE); c.setFont("DM-Bd", 8.5)
spacing = 2.2; cx = 60
for ch in "14 · DON'TS DEFINITIVOS":
    c.drawString(cx, H - 80, ch); cx += c.stringWidth(ch, "DM-Bd", 8.5) + spacing

c.setFillColor(BONE); c.setFont("DM-Bk", 44); c.drawString(60, H - 150, "Nunca, jamais.")
c.setFillColor(MOSS); c.setFont("DM-Bk", 44); c.drawString(60 + c.stringWidth("Nunca, jamais", "DM-Bk", 44), H - 150, ".")

donts_l = [
    "Nunca dizer 'apostar', 'trader', 'coach'",
    "Nunca prometer rentabilidade ou retorno garantido",
    "Nunca dar sinal, call, recomendação direta",
    "Nunca escurecer ou clarear o Moss #3D5240",
    "Nunca usar bege diferente de #FAF7F1",
]
donts_r = [
    "Nunca usar emoji em copy oficial",
    "Nunca usar Papyrus, Comic Sans, Impact, Montserrat, Poppins…",
    "Nunca usar foto de banco de imagem genérica",
    "Nunca cobrar pela Turma antes de CNPI + Cert. Assessora",
    "Nunca prometer sinal ou call paga — nem na Turma grátis",
]
yy = H - 230
for d in donts_l:
    c.setFillColor(MOSS); c.setFont("DM-Bk", 14); c.drawString(60, yy, "×")
    c.setFillColor(BONE); c.setFont("DM-Md", 12); c.drawString(85, yy, d); yy -= 26
yy = H - 230
for d in donts_r:
    c.setFillColor(MOSS); c.setFont("DM-Bk", 14); c.drawString(440, yy, "×")
    c.setFillColor(BONE); c.setFont("DM-Md", 12); c.drawString(465, yy, d); yy -= 26

# Closing
c.setFillColor(MOSS); c.setFont("DM-Bk", 22)
c.drawString(60, 70, "O simples sempre vence.")

c.save()
print(f"Saved: {OUT}")
