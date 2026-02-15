import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO


def grafico_radar(vieses_medias):
    """
    Gera gráfico radar dos vieses comportamentais
    """
    labels = list(vieses_medias.keys())
    values = list(vieses_medias.values())

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
    values += values[:1]
    angles = np.concatenate([angles, [angles[0]]])

    fig = plt.figure(figsize=(9, 6))
    ax = plt.subplot(111, polar=True)

    plt.xticks(angles[:-1], labels, color="black", size=11)
    ax.set_rlabel_position(0)

    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(["1", "2", "3", "4", "5"], color="gray", size=9)
    ax.set_ylim(0, 5)

    ax.plot(
        angles,
        values,
        linewidth=2,
        linestyle="solid",
        color="#2E7D32"
    )

    ax.fill(
        angles,
        values,
        color="#2E7D32",
        alpha=0.25
    )

    plt.title(
        "Vieses Comportamentais Predominantes",
        size=14,
        y=1.08
    )

    return fig


def fig_to_png_bytes(fig):
    """
    Converte um matplotlib figure em PNG (bytes),
    usado para embutir o gráfico no PDF.
    """
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=200)
    plt.close(fig)
    buf.seek(0)
    return buf.read()
