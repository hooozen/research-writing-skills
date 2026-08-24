#!/usr/bin/env python3
"""Optional Matplotlib translation example for the Clinical Data Chart Style.

This is an example, not the required rendering implementation. The authoritative
cross-tool rules and tokens live in references/style-guide.md.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


VI = {
    "canvas": "#FFFFFF",
    "card": "#F2F2F2",
    "primary": "#3D8DFF",
    "secondary": "#6DCBF4",
    "light": "#BFE8FA",
    "neutral": "#A8AFB8",
    "baseline": "#D4D4D4",
    "text": "#000000",
    "muted": "#5F6670",
}


def configure_typography() -> None:
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": [
                "Helvetica Neue",
                "Helvetica",
                "Arial",
                "Noto Sans",
                "DejaVu Sans",
            ],
            "font.size": 15,
            "axes.titleweight": "bold",
            "axes.titlesize": 26,
            "svg.fonttype": "none",
        }
    )


def count_share_label(value: int, total: int) -> str:
    return f"{value:,} · {value / total:.1%}"


def build_example(output: Path) -> None:
    configure_typography()

    labels = ["En-face", "OCTA", "Fundus"]
    values = [14325, 12194, 2033]
    colors = [VI["primary"], VI["secondary"], VI["neutral"]]
    total = sum(values)

    fig, ax = plt.subplots(figsize=(10, 5.2), dpi=120)
    fig.patch.set_facecolor(VI["canvas"])
    card = FancyBboxPatch(
        (0.012, 0.025),
        0.976,
        0.95,
        boxstyle="round,pad=0.0,rounding_size=0.025",
        transform=fig.transFigure,
        facecolor=VI["card"],
        edgecolor="none",
        zorder=-10,
    )
    fig.add_artist(card)
    ax.set_facecolor("none")

    bars = ax.barh(labels, values, color=colors, height=0.62)
    ax.invert_yaxis()
    ax.set_title("Image modality (n · %)", loc="left", color=VI["text"], pad=22)

    for bar, value in zip(bars, values):
        ax.text(
            value + total * 0.012,
            bar.get_y() + bar.get_height() / 2,
            count_share_label(value, total),
            va="center",
            ha="left",
            fontsize=15,
            fontweight="bold",
            color=VI["text"],
        )

    ax.set_xlim(0, max(values) * 1.42)
    ax.tick_params(axis="y", length=0, colors=VI["muted"], labelsize=15, pad=12)
    ax.tick_params(axis="x", bottom=False, labelbottom=False)
    for spine in ("top", "right", "bottom"):
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color(VI["baseline"])
    ax.spines["left"].set_linewidth(1.0)
    ax.grid(False)

    fig.text(
        0.945,
        0.065,
        "Example data · replace with verified source",
        ha="right",
        va="center",
        fontsize=11,
        color=VI["muted"],
    )
    fig.subplots_adjust(left=0.17, right=0.94, top=0.79, bottom=0.16)

    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Wrote {output}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", default="matplotlib_vi_example.svg", help="SVG or PNG output path"
    )
    args = parser.parse_args()
    build_example(Path(args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
