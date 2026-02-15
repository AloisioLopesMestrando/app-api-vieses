import base64
from pathlib import Path
from io import BytesIO
from datetime import datetime

import streamlit as st

from data.perguntas_api import PERGUNTAS_API
from data.perguntas_vieses import PERGUNTAS_VIESES
from data.interpretacoes import INTERPRETACOES

from utils.calculos import (
    classificar_perfil,
    calcular_media_vieses,
    top_vieses,
)
from utils.graficos import grafico_radar, fig_to_png_bytes


# PDF
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


# -----------------------------
# Config
# -----------------------------
APP_TITLE = "Meu Perfil de Investidor"
SICREDI_GREEN = "#2E7D32"
SICREDI_GREEN_DARK = "#1B5E20"

LOGO_PATH = "assets/sicredi.png"


def img_to_base64(path: str) -> str:
    p = Path(path)
    if not p.exists():
        return ""
    return base64.b64encode(p.read_bytes()).decode("utf-8")


LOGO_B64 = img_to_base64(LOGO_PATH)


def inject_css(watermark: bool = False) -> None:
    watermark_css = ""
    if watermark and LOGO_B64:
        watermark_css = f"""
        .block-container {{
            position: relative;
        }}
        .block-container:before {{
            content: "";
            position: fixed;
            right: 2.2rem;
            bottom: 1.8rem;
            width: 220px;
            height: 220px;
            background-image: url("data:image/png;base64,{LOGO_B64}");
            background-repeat: no-repeat;
            background-size: contain;
            opacity: 0.06;
            pointer-events: none;
            z-index: 0;
        }}
        """

    st.markdown(
        f"""
        <style>
        html, body, [class*="css"] {{
            font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial;
        }}
        .block-container {{
            max-width: 980px;
            padding-top: 2.2rem;
            padding-bottom: 2.5rem;
            z-index: 1;
        }}

        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}

        div.stButton > button {{
            border-radius: 14px;
            padding: 0.7rem 1.05rem;
            border: 1px solid rgba(46,125,50,0.25);
            background: linear-gradient(180deg, rgba(46,125,50,1), rgba(27,94,32,1));
            color: #fff;
            font-weight: 700;
            box-shadow: 0 8px 18px rgba(27,94,32,0.18);
        }}
        div.stButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 10px 22px rgba(27,94,32,0.22);
        }}
        div.stButton > button:disabled {{
            opacity: 0.55;
            cursor: not-allowed;
        }}

        .stTextInput input {{
            border-radius: 12px !important;
            padding: 0.75rem 0.9rem !important;
        }}

        .card {{
            background: #ffffff;
            border: 1px solid rgba(27,94,32,0.12);
            box-shadow: 0 10px 24px rgba(16, 24, 40, 0.08);
            border-radius: 18px;
            padding: 1.25rem 1.25rem;
        }}
        .soft-card {{
            background: rgba(46,125,50,0.06);
            border: 1px solid rgba(46,125,50,0.12);
            border-radius: 18px;
            padding: 1.05rem 1.1rem;
        }}
        .muted {{
            color: rgba(0,0,0,0.62);
        }}
        .hero {{
            border-radius: 22px;
            padding: 1.6rem 1.55rem;
            border: 1px solid rgba(46,125,50,0.14);
            background:
                radial-gradient(1200px 380px at 0% 0%, rgba(46,125,50,0.18), transparent 60%),
                radial-gradient(900px 320px at 100% 20%, rgba(46,125,50,0.10), transparent 55%),
                linear-gradient(180deg, rgba(255,255,255,1), rgba(46,125,50,0.04));
            box-shadow: 0 16px 34px rgba(16, 24, 40, 0.10);
        }}
        .hero-title {{
            font-size: 3.0rem;
            line-height: 1.05;
            margin: 0;
        }}
        .hero-sub {{
            font-size: 1.05rem;
            margin-top: 0.75rem;
            margin-bottom: 0;
            color: rgba(0,0,0,0.65);
        }}

        .progress-wrap {{
            margin-top: 0.25rem;
            margin-bottom: 1rem;
        }}
        .progress-meta {{
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 0.35rem;
            color: rgba(0,0,0,0.62);
            font-size: 0.95rem;
        }}

        div[role="radiogroup"] > label {{
            background: rgba(46,125,50,0.04);
            border: 1px solid rgba(46,125,50,0.10);
            padding: 0.65rem 0.8rem;
            border-radius: 14px;
            margin-bottom: 0.5rem;
        }}

        {watermark_css}
        </style>
        """,
        unsafe_allow_html=True,
    )


def init_state():
    defaults = {
        "step": "home",  # home | api | trans_vieses | vieses | resultado | profissional
        "nome": "",
        "api_idx": 0,
        "vies_idx": 0,
        "respostas_api": [],
        "respostas_vieses": {},
        "perfil_api": None,
        "score_api": None,
        "medias_vieses": None,
        "top_vieses": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def total_questions():
    return len(PERGUNTAS_API) + len(PERGUNTAS_VIESES)


def current_global_index():
    if st.session_state.step == "api":
        return st.session_state.api_idx
    if st.session_state.step == "trans_vieses":
        return len(PERGUNTAS_API)
    if st.session_state.step == "vieses":
        return len(PERGUNTAS_API) + st.session_state.vies_idx
    if st.session_state.step in ("resultado", "profissional"):
        return total_questions()
    return 0


def render_logo():
    if Path(LOGO_PATH).exists():
        st.image(LOGO_PATH, width=170)


def render_progress():
    total = total_questions()
    idx = current_global_index()
    pct = min(max((idx / total), 0.0), 1.0)
    st.markdown(
        f"""
        <div class="progress-wrap">
          <div class="progress-meta">
            <div><strong>Progresso</strong></div>
            <div>{int(pct*100)}%</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.progress(pct)


def cache_results_if_needed():
    """Compute results once and store in session_state (so professional page can reuse)."""
    if st.session_state.perfil_api is None or st.session_state.medias_vieses is None:
        perfil, score_api = classificar_perfil(PERGUNTAS_API, st.session_state.respostas_api)
        medias = calcular_media_vieses(PERGUNTAS_VIESES, st.session_state.respostas_vieses)
        top = top_vieses(medias, top_n=3)

        st.session_state.perfil_api = perfil
        st.session_state.score_api = score_api
        st.session_state.medias_vieses = medias
        st.session_state.top_vieses = top


# -----------------------------
# PDF generator (Respondente)
# -----------------------------
def hex_to_rgb01(hex_color: str):
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4))


def draw_soft_gradient(c: canvas.Canvas, x, y, w, h, top_hex="#E8F5E9", bottom_hex="#FFFFFF", steps=24):
    """Fake a soft vertical gradient using multiple rectangles (works everywhere)."""
    r1, g1, b1 = hex_to_rgb01(top_hex)
    r2, g2, b2 = hex_to_rgb01(bottom_hex)
    for i in range(steps):
        t = i / max(steps - 1, 1)
        r = r1 + (r2 - r1) * t
        g = g1 + (g2 - g1) * t
        b = b1 + (b2 - b1) * t
        c.setFillColorRGB(r, g, b)
        c.setStrokeColorRGB(r, g, b)
        yi = y + (h * (1 - (i + 1) / steps))
        c.rect(x, yi, w, h / steps, fill=1, stroke=0)


def make_pdf_bytes(nome: str, perfil: str, score_api: int, radar_png: bytes, top_list, interpretacoes: dict) -> bytes:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    W, H = A4

    # Background soft gradient (Option B)
    draw_soft_gradient(c, 0, 0, W, H, top_hex="#E8F5E9", bottom_hex="#FFFFFF", steps=28)

    # Header band
    band_h = 3.3 * cm
    draw_soft_gradient(c, 0, H - band_h, W, band_h, top_hex="#DFF3E1", bottom_hex="#F7FBF7", steps=18)

    # Logo
    if Path(LOGO_PATH).exists():
        logo_img = ImageReader(LOGO_PATH)
        c.drawImage(logo_img, 1.6 * cm, H - 2.7 * cm, width=4.0 * cm, height=1.5 * cm, mask="auto")

    # Title
    c.setFillColorRGB(0.10, 0.12, 0.16)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(6.2 * cm, H - 2.2 * cm, "Meu Perfil de Investidor")

    # Subtitle
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0.25, 0.28, 0.32)
    c.drawString(6.2 * cm, H - 2.8 * cm, "Resultado do respondente (uso educacional)")

    # Name + date
    c.setFillColorRGB(0.12, 0.14, 0.18)
    c.setFont("Helvetica", 10)
    c.drawString(1.6 * cm, H - 3.9 * cm, f"Respondente: {nome}")
    c.drawRightString(W - 1.6 * cm, H - 3.9 * cm, f"Data: {datetime.now().strftime('%d/%m/%Y')}")

    # Profile box
    box_y = H - 6.1 * cm
    box_h = 2.0 * cm
    c.setFillColorRGB(0.90, 0.97, 0.91)  # light green
    c.setStrokeColorRGB(0.70, 0.86, 0.72)
    c.roundRect(1.6 * cm, box_y, W - 3.2 * cm, box_h, 12, fill=1, stroke=1)

    c.setFillColorRGB(0.10, 0.12, 0.16)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2.2 * cm, box_y + 1.25 * cm, "Perfil de risco (API):")
    c.setFillColorRGB(0.10, 0.35, 0.16)
    c.drawString(6.1 * cm, box_y + 1.25 * cm, f"{perfil}")
    c.setFillColorRGB(0.25, 0.28, 0.32)
    c.setFont("Helvetica", 10)
    c.drawString(2.2 * cm, box_y + 0.55 * cm, f"Pontuação: {score_api}")

    # Radar
    radar_y = H - 14.4 * cm
    radar_w = W - 3.2 * cm
    radar_h = 7.6 * cm
    try:
        img = ImageReader(BytesIO(radar_png))
        c.drawImage(img, 1.6 * cm, radar_y, width=radar_w, height=radar_h, preserveAspectRatio=True, anchor="c")
    except Exception:
        c.setFillColorRGB(0.3, 0.3, 0.3)
        c.drawString(2 * cm, radar_y + 3 * cm, "Não foi possível renderizar o gráfico.")

    # Suggestions title
    text_y = radar_y - 0.9 * cm
    c.setFillColorRGB(0.10, 0.12, 0.16)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1.6 * cm, text_y, "Sugestões para o respondente (vieses mais relevantes)")

    # Suggestions blocks (top vieses)
    y = text_y - 0.7 * cm
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0.20, 0.22, 0.26)

    def draw_wrapped(text, x, y, max_w, leading=13):
        """Simple wrap for reportlab."""
        words = text.split()
        line = ""
        lines = []
        for w in words:
            test = (line + " " + w).strip()
            if c.stringWidth(test, "Helvetica", 10) <= max_w:
                line = test
            else:
                lines.append(line)
                line = w
        if line:
            lines.append(line)
        for ln in lines:
            c.drawString(x, y, ln)
            y -= leading
        return y

    max_w = W - 3.2 * cm
    for vies, media in top_list:
        bloco = interpretacoes.get(vies, {}).get("respondente_txt", "")
        # Heading
        c.setFillColorRGB(0.10, 0.35, 0.16)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(1.6 * cm, y, f"• {vies} (média: {media:.2f})")
        y -= 0.45 * cm

        # Body
        c.setFillColorRGB(0.20, 0.22, 0.26)
        c.setFont("Helvetica", 10)
        y = draw_wrapped(bloco, 2.0 * cm, y, max_w - 0.4 * cm, leading=13)
        y -= 0.35 * cm

        # New page if needed
        if y < 2.3 * cm:
            # footer
            c.setFillColorRGB(0.35, 0.35, 0.35)
            c.setFont("Helvetica", 8)
            c.drawString(1.6 * cm, 1.2 * cm, "Material educacional. Não substitui aconselhamento profissional.")
            c.showPage()
            draw_soft_gradient(c, 0, 0, W, H, top_hex="#E8F5E9", bottom_hex="#FFFFFF", steps=28)
            y = H - 2.2 * cm

    # Footer
    c.setFillColorRGB(0.35, 0.35, 0.35)
    c.setFont("Helvetica", 8)
    c.drawString(1.6 * cm, 1.2 * cm, "Material educacional. Não substitui aconselhamento profissional. "
                                    "Resultado baseado em autorrelato.")
    c.save()
    buffer.seek(0)
    return buffer.read()


# -----------------------------
# Text blocks (Professional page)
# -----------------------------
def bloco_perfil_profissional(perfil: str):
    """Guidelines that depend on the API profile."""
    if perfil == "Conservador":
        return [
            "Priorize previsibilidade, liquidez e preservação de capital.",
            "Evite exposições que gerem desconforto com marcação a mercado; explique variações e horizonte.",
            "Use linguagem de objetivos (reserva, curto prazo) e combine revisão periódica simples."
        ]
    if perfil == "Moderado":
        return [
            "Equilibre segurança e busca por retorno: diversificação por indexador/prazo/risco.",
            "Trabalhe expectativas: oscilações podem existir; alinhe horizonte e capacidade de manter estratégia.",
            "Estruture carteira por objetivos e rebalanço programado."
        ]
    # Arrojado
    return [
        "Cliente tende a tolerar mais risco; mesmo assim, imponha limites de concentração e liquidez.",
        "Explique riscos específicos (crédito, duration, volatilidade) e crie “regras de proteção”.",
        "Use cenários e acompanhamento para evitar decisões reativas e excesso de giro."
    ]


# -----------------------------
# Screens
# -----------------------------
def screen_home():
    inject_css(watermark=False)
    render_logo()

    st.markdown(
        f"""
        <div class="hero">
          <h1 class="hero-title">{APP_TITLE}</h1>
          <p class="hero-sub">
            Bem-vindo(a)! Em poucos minutos, vamos identificar seu <strong>perfil de investidor</strong> e
            os <strong>vieses comportamentais</strong> que podem influenciar suas decisões financeiras.
            <br><br>
            <span class="muted">Não existem respostas certas ou erradas. Responda com sinceridade.</span>
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    nome = st.text_input("Digite seu nome", value=st.session_state.nome, placeholder="Ex.: Aloísio Lopes")
    st.session_state.nome = nome.strip()

    col1, col2 = st.columns([1, 3])
    with col1:
        can_start = len(st.session_state.nome) >= 2
        if st.button("Iniciar", disabled=not can_start):
            st.session_state.step = "api"
            st.session_state.api_idx = 0
            st.session_state.respostas_api = []
            st.session_state.vies_idx = 0
            st.session_state.respostas_vieses = {}
            st.session_state.perfil_api = None
            st.session_state.score_api = None
            st.session_state.medias_vieses = None
            st.session_state.top_vieses = None
            st.rerun()

    with col2:
        st.markdown(
            "<div class='muted'>Dica: responda em um ambiente calmo, sem pressa. O resultado é uma "
            "orientação comportamental e não substitui análise profissional.</div>",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)


def screen_api():
    inject_css(watermark=True)
    render_logo()
    render_progress()

    idx = st.session_state.api_idx
    total_api = len(PERGUNTAS_API)
    q = PERGUNTAS_API[idx]

    st.markdown(
        f"""
        <div class="card">
          <h2 style="margin-top:0;">Pergunta {idx+1} de {total_api}</h2>
          <p class="muted" style="margin-top:-0.5rem;">Selecione uma alternativa para avançar.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"### {q['texto']}")

    op_labels = [f"{op['codigo']}) {op['descricao']}" for op in q["opcoes"]]
    choice = st.radio(
        "Escolha uma opção:",
        options=list(range(len(op_labels))),
        format_func=lambda i: op_labels[i],
        index=None,  # IMPORTANT: no default selection
        key=f"api_choice_{idx}",
    )

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Próxima"):
            if choice is None:
                st.warning("Selecione uma opção para continuar.")
            else:
                codigo = q["opcoes"][choice]["codigo"]
                if len(st.session_state.respostas_api) == idx:
                    st.session_state.respostas_api.append(codigo)
                else:
                    st.session_state.respostas_api[idx] = codigo

                if idx + 1 < total_api:
                    st.session_state.api_idx += 1
                    st.rerun()
                else:
                    st.session_state.step = "trans_vieses"
                    st.rerun()

    with col2:
        st.markdown(
            "<div class='muted'>Você verá o resultado ao final, junto com os vieses mais relevantes.</div>",
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


def screen_trans_vieses():
    inject_css(watermark=True)
    render_logo()
    render_progress()

    st.markdown(
        f"""
        <div class="card">
          <h1 style="margin-top:0;">Agora vamos falar sobre comportamento</h1>
          <div class="soft-card" style="margin-top:1rem;">
            <p style="margin:0;">
              <strong>{st.session_state.nome}</strong>, até aqui identificamos seu <strong>perfil de investidor</strong>.
              Agora você responderá afirmações relacionadas ao seu <strong>comportamento ao investir</strong>.
            </p>
            <div style="margin-top:0.9rem;">
              <strong>Escala de 1 a 5</strong><br>
              1 = Discordo totalmente<br>
              5 = Concordo totalmente
            </div>
            <p class="muted" style="margin-top:0.9rem; margin-bottom:0;">
              Não existem respostas certas ou erradas. Responda de forma sincera.
            </p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    if st.button("Iniciar Questionário de Vieses"):
        st.session_state.step = "vieses"
        st.session_state.vies_idx = 0
        st.rerun()


def screen_vieses():
    inject_css(watermark=True)
    render_logo()
    render_progress()

    idx = st.session_state.vies_idx
    total_v = len(PERGUNTAS_VIESES)
    item = PERGUNTAS_VIESES[idx]

    # Não mostrar o nome do viés
    st.markdown(
        f"""
        <div class="card">
          <h2 style="margin-top:0;">Afirmação {idx+1} de {total_v}</h2>
          <p class="muted" style="margin-top:-0.5rem;">Indique seu nível de concordância para avançar.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"### {item['texto']}")

    choice = st.radio(
        "Indique seu nível de concordância:",
        options=[1, 2, 3, 4, 5],
        index=None,  # IMPORTANT: no default selection
        horizontal=True,
        key=f"vies_choice_{idx}",
        format_func=lambda x: str(x),
    )

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Próxima"):
            if choice is None:
                st.warning("Selecione um número de 1 a 5 para continuar.")
            else:
                st.session_state.respostas_vieses[item["id"]] = int(choice)

                if idx + 1 < total_v:
                    st.session_state.vies_idx += 1
                    st.rerun()
                else:
                    st.session_state.step = "resultado"
                    st.rerun()

    with col2:
        st.markdown(
            "<div class='muted'>Dica: pense no seu comportamento típico, não em um caso isolado.</div>",
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


def screen_resultado():
    inject_css(watermark=True)
    render_logo()
    cache_results_if_needed()

    perfil = st.session_state.perfil_api
    score_api = st.session_state.score_api
    medias = st.session_state.medias_vieses
    top = st.session_state.top_vieses

    st.markdown(
        f"""
        <div class="card">
          <h1 style="margin-top:0;">Resultado</h1>
          <div class="soft-card" style="margin-top:1rem;">
            <p style="margin:0;">
              <strong>{st.session_state.nome}</strong>, seu perfil de risco é:
              <span style="color:{SICREDI_GREEN_DARK}; font-weight:800;"> {perfil}</span>
              <span class="muted">(pontuação: {score_api})</span>
            </p>
            <p class="muted" style="margin-top:0.7rem; margin-bottom:0;">
              A seguir, estão seus vieses mais relevantes (com base nas maiores médias relativas).
            </p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    fig = grafico_radar(medias)
    radar_png = fig_to_png_bytes(fig)   # <-- gera o PNG antes de limpar a figura
    st.pyplot(fig, clear_figure=True)


    # ---- Buttons row: PDF + Professional page
    st.write("")
    colA, colB, colC = st.columns([1.1, 1.6, 1.3])

    with colA:
        # generate pdf bytes on demand (fast)
        pdf_bytes = make_pdf_bytes(
            nome=st.session_state.nome,
            perfil=perfil,
            score_api=score_api,
            radar_png=radar_png,
            top_list=top,
            interpretacoes=INTERPRETACOES,
        )
        st.download_button(
            "🖨️ Gerar PDF",
            data=pdf_bytes,
            file_name=f"resultado_{st.session_state.nome.replace(' ', '_')}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

    with colB:
        if st.button("👔 Recomendações para o Profissional", use_container_width=True):
            st.session_state.step = "profissional"
            st.rerun()

    with colC:
        if st.button("🔁 Refazer", use_container_width=True):
            st.session_state.step = "home"
            st.session_state.api_idx = 0
            st.session_state.vies_idx = 0
            st.session_state.respostas_api = []
            st.session_state.respostas_vieses = {}
            st.session_state.perfil_api = None
            st.session_state.score_api = None
            st.session_state.medias_vieses = None
            st.session_state.top_vieses = None
            st.rerun()

    st.write("")
    st.markdown("## 🧠 Sugestões para o respondente")

    for vies, media in top:
        bloco_html = INTERPRETACOES.get(vies, {}).get("respondente_html", "")
        bloco_html = bloco_html.replace("```", "").replace("</div>", "").strip()
 
        st.markdown(
            f"""
            <div class="card" style="border-left:8px solid {SICREDI_GREEN};">
              <h3 style="margin-top:0;">{vies} <span class="muted">(média: {media:.2f})</span></h3>
              <div class="soft-card" style="margin-top:0.85rem;">
                {bloco_html}
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.caption("Obs.: este resultado é educacional e não substitui uma análise profissional completa.")


def screen_profissional():
    inject_css(watermark=True)
    render_logo()
    cache_results_if_needed()

    perfil = st.session_state.perfil_api
    score_api = st.session_state.score_api
    top = st.session_state.top_vieses

    st.markdown(
        f"""
        <div class="card">
          <h1 style="margin-top:0;">Recomendações para o Profissional</h1>
          <div class="soft-card" style="margin-top:1rem;">
            <p style="margin:0;">
              <strong>Respondente:</strong> {st.session_state.nome}<br>
              <strong>Perfil (API):</strong> <span style="color:{SICREDI_GREEN_DARK}; font-weight:800;">{perfil}</span>
              <span class="muted">(pontuação: {score_api})</span>
            </p>
            <p class="muted" style="margin-top:0.7rem; margin-bottom:0;">
              Esta página é voltada ao assessor/profissional que aplicou o questionário, com orientações de condução
              e recomendações integrando <strong>perfil de risco</strong> e <strong>vieses predominantes</strong>.
            </p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.markdown("## 🎯 Diretrizes gerais conforme o perfil (API)")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    itens = bloco_perfil_profissional(perfil)
    st.markdown("<ul>" + "".join([f"<li>{i}</li>" for i in itens]) + "</ul>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    st.markdown("## 🧩 Leitura integrada: viés + perfil")
    for vies, media in top:
        assessor_html = INTERPRETACOES.get(vies, {}).get("assessor_html", "")
        extra = INTERPRETACOES.get(vies, {}).get("extras_por_perfil", {}).get(perfil, "")

        assessor_html = assessor_html.replace("```", "").strip()
        extra = extra.replace("```", "").strip()



        st.markdown(
            f"""
            <div class="card" style="border-left:8px solid {SICREDI_GREEN};">
              <h3 style="margin-top:0;">{vies} <span class="muted">(média: {media:.2f})</span></h3>
              <div class="soft-card" style="margin-top:0.85rem;">
                {assessor_html}
              </div>
              <div class="soft-card" style="margin-top:0.85rem;">
                <strong>Como ajustar a recomendação considerando o perfil {perfil}</strong><br>
                {extra}
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("⬅️ Voltar ao Resultado", use_container_width=True):
            st.session_state.step = "resultado"
            st.rerun()
    with col2:
        st.caption("Dica: use esta página como roteiro de atendimento e registre premissas/expectativas.")


# -----------------------------
# Main
# -----------------------------
def main():
    st.set_page_config(page_title=APP_TITLE, page_icon="🟢", layout="centered")
    init_state()

    step = st.session_state.step
    if step == "home":
        screen_home()
    elif step == "api":
        screen_api()
    elif step == "trans_vieses":
        screen_trans_vieses()
    elif step == "vieses":
        screen_vieses()
    elif step == "resultado":
        screen_resultado()
    elif step == "profissional":
        screen_profissional()
    else:
        st.session_state.step = "home"
        st.rerun()


if __name__ == "__main__":
    main()

