#!/usr/bin/env python3
"""Optional Matplotlib translation example for the Clinical Data Chart Style.

This is an example, not the required rendering implementation. The authoritative
cross-tool rules and tokens live in references/style-guide.md.
"""

from __future__ import annotations

import argparse
from numbers import Integral
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


def configure_typography(dpi: float = 100) -> None:
    # Matplotlib font sizes are points; design tokens are pixels at output DPI.
    pt = 72 / dpi
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
            "font.size": 15 * pt,
            "axes.titleweight": "bold",
            "axes.titlesize": 26 * pt,
            "svg.fonttype": "none",
        }
    )


def count_share_label(value: int, total: int | None) -> str:
    """Format nonnegative counts; an absent/zero population has no percentage."""
    if isinstance(value, bool) or not isinstance(value, Integral) or value < 0:
        raise ValueError("value must be a nonnegative integer count")
    if total is None:
        return f"{value:,} · share unavailable"
    if isinstance(total, bool) or not isinstance(total, Integral) or total < 0 or value > total:
        raise ValueError("total must be an integer population at least as large as value")
    if total == 0:
        return f"{value:,} · share unavailable"
    return f"{value:,} · {value / total:.1%}"


def build_example(output: Path) -> None:
    dpi = 100
    pt = 72 / dpi
    configure_typography(dpi)

    labels = ["3 × 3 mm", "6 × 6 mm", "Other / unknown"]
    values = [14325, 12194, 2033]
    colors = [VI["primary"], VI["secondary"], VI["neutral"]]
    total = sum(values)

    fig, ax = plt.subplots(figsize=(10, 5.2), dpi=dpi)
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
    ax.set_title("Synthetic scan-size distribution", loc="left", color=VI["text"], pad=22)

    for bar, value in zip(bars, values):
        ax.text(
            value + total * 0.012,
            bar.get_y() + bar.get_height() / 2,
            count_share_label(value, total),
            va="center",
            ha="left",
            fontsize=15 * pt,
            fontweight="bold",
            color=VI["text"],
        )

    ax.set_xlim(0, max(values) * 1.42)
    ax.tick_params(axis="y", length=0, colors=VI["muted"], labelsize=15 * pt, pad=12)
    ax.tick_params(axis="x", bottom=False, labelbottom=False)
    for spine in ("top", "right", "bottom"):
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color(VI["baseline"])
    ax.spines["left"].set_linewidth(1.0)
    ax.grid(False)

    fig.text(
        0.945,
        0.065,
        f"Synthetic example · {total:,} scans · one size category per scan",
        ha="right",
        va="center",
        fontsize=12 * pt,
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
    output = Path(args.output)
    if output.suffix.lower() not in {".svg", ".png"}:
        parser.error("--output must end in .svg or .png")
    build_example(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
