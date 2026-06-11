from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np


def grafico_radar(vieses_medias):
    """Gera o gráfico radar dos vieses comportamentais."""
    labels = list(vieses_medias.keys())
    values = list(vieses_medias.values())

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
    values += values[:1]
    angles = np.concatenate([angles, [angles[0]]])

    fig = plt.figure(figsize=(5.2, 5.2))
    ax = plt.subplot(111, polar=True)

    plt.xticks(angles[:-1], labels, color="#1F2937", size=10)
    ax.set_rlabel_position(0)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(["1", "2", "3", "4", "5"], color="#6B7280", size=8)
    ax.set_ylim(0, 5)
    ax.grid(color="#D1D5DB", linewidth=0.8, alpha=0.85)
    ax.spines["polar"].set_color("#D1D5DB")

    ax.plot(angles, values, linewidth=2.4, linestyle="solid", color="#2E7D32")
    ax.fill(angles, values, color="#2E7D32", alpha=0.18)

    fig.patch.set_alpha(0)
    ax.set_facecolor("#FFFFFF")
    fig.subplots_adjust(left=0.16, right=0.84, top=0.88, bottom=0.12)

    return fig


def fig_to_png_bytes(fig):
    """Converte uma figura Matplotlib em PNG para uso na tela e no PDF."""
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    buf.seek(0)
    return buf.read()
