from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.pdfbase.pdfmetrics import stringWidth

import os

OUTPUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "9Pilla_Brandbook_V2.pdf")

MOSS = colors.HexColor("#3D5240")
BONE = colors.HexColor("#FAF7F1")
INK = colors.HexColor("#0A0A0A")
LINE = colors.HexColor("#E7E2D8")
MUTED = colors.HexColor("#7A7670")
SAND = colors.HexColor("#EFE7DA")
WHITE = colors.white


class BrandDoc(BaseDocTemplate):
    def __init__(self, filename):
        super().__init__(
            filename,
            pagesize=A4,
            leftMargin=18 * mm,
            rightMargin=18 * mm,
            topMargin=20 * mm,
            bottomMargin=18 * mm,
            title="9Pilla Brandbook V2",
            author="Perplexity Computer",
        )
        frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            id="normal",
        )
        self.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=self.decorate)])

    def decorate(self, canvas, doc):
        canvas.saveState()
        canvas.setFillColor(BONE)
        canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.4)
        canvas.line(18 * mm, 18 * mm, A4[0] - 18 * mm, 18 * mm)
        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica", 7)
        canvas.drawString(18 * mm, 12 * mm, "9Pilla Brandbook V2 · Perplexity Computer")
        canvas.drawRightString(A4[0] - 18 * mm, 12 * mm, str(doc.page))
        canvas.restoreState()


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="CoverTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=44,
        leading=46,
        textColor=BONE,
        alignment=TA_CENTER,
        spaceAfter=10,
    )
)
styles.add(
    ParagraphStyle(
        name="CoverSub",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=13,
        leading=18,
        textColor=BONE,
        alignment=TA_CENTER,
    )
)
styles.add(
    ParagraphStyle(
        name="CoverNote",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=MUTED,
        alignment=TA_CENTER,
    )
)
styles.add(
    ParagraphStyle(
        name="H1",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=25,
        leading=29,
        textColor=INK,
        spaceBefore=6,
        spaceAfter=12,
    )
)
styles.add(
    ParagraphStyle(
        name="H2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=MOSS,
        spaceBefore=10,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.6,
        leading=14,
        textColor=INK,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        name="Small",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=MUTED,
    )
)
styles.add(
    ParagraphStyle(
        name="Pull",
        parent=styles["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=17,
        leading=22,
        textColor=MOSS,
        alignment=TA_CENTER,
        spaceBefore=8,
        spaceAfter=8,
    )
)


def p(text, style="Body"):
    return Paragraph(text, styles[style])


def bullet(items):
    return [p("• " + item) for item in items]


def section(title):
    return [p(title, "H1")]


def table(data, widths=None, header=True):
    t = Table(data, colWidths=widths, hAlign="LEFT")
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), MOSS if header else SAND),
        ("TEXTCOLOR", (0, 0), (-1, 0), BONE if header else INK),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.2),
        ("LEADING", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.35, LINE),
        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    t.setStyle(TableStyle(style))
    return t


def card(title, body, fill=colors.white):
    t = Table(
        [[p(f"<b>{title}</b>", "Body")], [p(body, "Body")]],
        colWidths=[A4[0] - 36 * mm],
    )
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), SAND),
                ("BACKGROUND", (0, 1), (-1, 1), fill),
                ("BOX", (0, 0), (-1, -1), 0.35, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return t


story = []

# Cover
story.append(Spacer(1, 40 * mm))
cover = Table(
    [[p("9Pilla", "CoverTitle")], [p("Brandbook V2 · Liberdade. Em primeira pessoa.", "CoverSub")]],
    colWidths=[A4[0] - 36 * mm],
    rowHeights=[34 * mm, 22 * mm],
)
cover.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, -1), MOSS),
            ("BOX", (0, 0), (-1, -1), 0, MOSS),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ]
    )
)
story.append(cover)
story.append(Spacer(1, 16 * mm))
story.append(p("Educação financeira que transforma, sem promessa vazia, sem guru e sem fórmula secreta.", "Pull"))
story.append(p("Documento de marca, voz, visual, conteúdo, operação comercial e expansão de canais.", "CoverNote"))
story.append(PageBreak())

story += section("Essência")
story.append(p("A 9Pilla é uma marca de educação financeira aplicada, construída em primeira pessoa. O coração da marca é mostrar, com transparência, como uma pessoa real estuda, opera, registra e aprende no mercado financeiro usando o próprio dinheiro."))
story.append(p("<b>Posicionamento:</b> a 9Pilla é o diário público de uma mulher que opera o próprio dinheiro e transforma mercado financeiro em linguagem simples, rastreável e humana."))
story.append(p("Liberdade. Em primeira pessoa.", "Pull"))
story.append(table([
    ["Elemento", "Definição"],
    ["Slogan institucional", "Educação financeira que transforma"],
    ["Tagline de oferta", "Liberdade. Em primeira pessoa."],
    ["Frase-âncora", "O simples sempre vence."],
    ["Ritual", "Morning Call 09:09"],
    ["Oferta", "Turma 9Pilla"],
    ["Trilha educacional", "Sobe."],
]))

story += section("Arquitetura da marca")
story.append(p("<b>9Pilla</b> é a marca-mãe. Ela guarda site, Instagram, comunidade, produtos, diário de operações, conteúdo educacional e expansão futura."))
story += bullet([
    "<b>Turma 9Pilla:</b> comunidade paga com Morning Call, diário de operações próprias e bastidores.",
    "<b>Morning Call 09:09:</b> ritual de segunda a sexta, às 09:09.",
    "<b>Sobe.:</b> trilha educacional de 4 camadas para iniciantes.",
    "<b>Diário de Bordo 9Pilla:</b> relatos pessoais de operações, nunca sinais ou calls.",
])

story += section("Público")
story.append(p("O público prioritário são mulheres brasileiras de 25 a 45 anos que querem construir liberdade financeira com autonomia, mas estão cansadas de conteúdo financeiro frio, masculino, professoral ou cheio de promessa."))
story.append(card("Dores", "Medo de começar. Finanças parecem complexas. Cansaço de gurus. Desconfiança de resultados sem processo. Falta de pertencimento em comunidades financeiras tradicionais."))
story.append(Spacer(1, 3 * mm))
story.append(card("Desejos", "Entender dinheiro sem julgamento. Ver alguém real fazendo. Aprender com risco explícito. Sentir pertencimento. Construir liberdade financeira com método e clareza."))

story += section("Voz")
story.append(card("A 9Pilla é", "Simples, direta, honesta, feminina sem clichê e ambiciosa com pé no chão. Explica sem diminuir a inteligência de ninguém."))
story.append(Spacer(1, 3 * mm))
story.append(card("A 9Pilla não é", "Guru, coach, trader ostentação, fintech azul genérica, professoral demais, infantilizada ou sensacionalista."))
story.append(p("Banco verbal: “Extrato, não promessa.” “Risco calculado, posição dimensionada.” “Opero com o meu dinheiro.” “Dinheiro também é emocional.” “Aqui a gente lê, aprende e aplica.”"))

story += section("Blindagem regulatória")
story.append(p("A regra-mãe é: a 9Pilla comunica relatos pessoais e conteúdo educacional. Não comunica recomendação de investimento. Toda peça que mostra operação, lucro, print ou resultado precisa de disclaimer."))
story.append(card("Use", "Eu operei. Eu comprei. Minha entrada foi. Meu risco era. Minha saída foi. Meu resultado foi. O que eu aprendi."))
story.append(Spacer(1, 3 * mm))
story.append(card("Não use", "Compre. Venda. Entre agora. Sinal. Call. Garantido. Tiro certo. Lucro certo. Faça igual."))
story.append(p("<b>Disclaimer padrão:</b> Conteúdo educacional e relato pessoal de operações próprias. Não constitui recomendação de investimento. Operações em renda variável e opções envolvem riscos. Resultados passados não garantem resultados futuros."))

story += section("Identidade visual")
story.append(p("A direção criativa deve ser editorial, premium, simples e proprietária, unindo mercado financeiro real, lifestyle de liberdade e clube de leitura/inteligência prática."))
story.append(table([
    ["Token", "Hex", "Uso"],
    ["Moss", "#3D5240", "cor principal, botões, acentos, marca"],
    ["Bone", "#FAF7F1", "fundo principal"],
    ["Ink", "#0A0A0A", "texto principal"],
    ["Line", "#E7E2D8", "bordas e divisórias"],
    ["Muted", "#7A7670", "texto secundário"],
    ["Sand", "#EFE7DA", "blocos suaves"],
], widths=[35 * mm, 35 * mm, 94 * mm]))
story.append(p("<b>Logo:</b> wordmark tipográfico forte, serifado robusto, limpo e com personalidade. A referência é Pearhaus: premium sem parecer fintech genérica."))
story.append(p("<b>Tipografia:</b> serif robusta no logo, DM Sans para títulos e corpo, numerais tabulares para resultados e operações."))

story += section("Instagram")
story.append(p("<b>Bio recomendada:</b> 9Pilla · Liberdade financeira em primeira pessoa. Morning Call 09:09 + diário de operações próprias. Educação, extrato e processo. Sem promessa. Entre na Turma 9Pilla ↓"))
story.append(table([
    ["Pilar", "Função", "Formato"],
    ["Diário de operações", "Prova e transparência", "Reels, Stories, print comentado"],
    ["Educação simples", "Salvar e compartilhar", "Carrossel, post estático"],
    ["Dinheiro emocional", "Conexão", "Stories, Reels"],
    ["Bastidores da Raquel", "Humanização", "Stories, foto real"],
    ["Comunidade", "Conversão", "Depoimentos, convites, FAQ"],
    ["Leitura e repertório", "Diferenciação Book Club", "Carrossel, Stories"],
], widths=[45 * mm, 55 * mm, 64 * mm]))

story += section("Site e Hubla")
story.append(p("O site público www.9pilla.com já apresenta a marca como Book Club, com leitura, investimento, liberdade financeira, comunidade e o e-book Papo de Grana Simplificado.<super>1</super>"))
story.append(p("O ajuste estratégico é manter o Book Club como camada de repertório, mas levar o CTA principal para a Turma 9Pilla e o checkout Hubla."))
story += bullet([
    "Criar produto na Hubla.",
    "Gerar checkout.",
    "Inserir link no botão principal, bloco de produto, CTA final e bio do Instagram.",
    "Testar mobile e aba anônima.",
])

story += section("Expansão de canais")
story.append(table([
    ["Ordem", "Canal", "Papel"],
    ["1", "Instagram", "prioridade inicial; público-alvo e relacionamento"],
    ["2", "TikTok", "descoberta e viralidade"],
    ["3", "YouTube Shorts", "reaproveitamento pesquisável dos cortes"],
    ["4", "YouTube longo", "profundidade futura"],
    ["5", "Spotify", "exposição e reflexão de marca"],
], widths=[18 * mm, 45 * mm, 101 * mm]))

story += section("Próximos passos")
story += bullet([
    "Criar e configurar o produto dentro da Hubla.",
    "Gerar link de checkout e substituir no site.",
    "Atualizar bio, link da bio e destaques do Instagram.",
    "Publicar sequência de stories de abertura.",
    "Criar templates fixos para Reels, Stories e carrosséis.",
    "Só depois: abrir TikTok, Shorts e, mais à frente, Spotify.",
])
story.append(Spacer(1, 10 * mm))
story.append(p("Fonte: <a href='https://www.9pilla.com' color='#3D5240'>www.9pilla.com</a>", "Small"))

doc = BrandDoc(OUTPUT)
doc.build(story)
print(OUTPUT)
