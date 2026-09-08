#!/usr/bin/env python3
"""Optional Matplotlib translation example for the Clinical Data Chart Style.

This is an example, not the required rendering implementation. The authoritative
cross-tool rules and tokens live in references/style-guide.md.
"""

from __future__ import annotations

import argparse
from numbers import Integral
from pathlib import Path
import re

import matplotlib.pyplot as plt
from matplotlib.layout_engine import PlaceHolderLayoutEngine
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


def _wrap_header(text_artist, renderer, width):
    """Wrap plain text to measured width, including CJK and explicit newlines."""
    source = text_artist.get_text()

    def fits(text):
        text_artist.set_text(text)
        return text_artist.get_window_extent(renderer).width <= width

    lines = []
    for paragraph in source.split('\n'):
        line = ''
        for token in re.findall(r'\S+\s*', paragraph):
            if fits((line + token).rstrip()):
                line += token
                continue
            if line:
                lines.append(line.rstrip())
                line = ''
            if fits(token.rstrip()):
                line = token
                continue
            # A CJK sentence or an unspaced identifier may exceed one line.
            for char in token:
                if not fits(line + char):
                    if not line:
                        raise ValueError('Header is too narrow; increase figure width.')
                    lines.append(line.rstrip())
                    line = ''
                line += char
        lines.append(line.rstrip())
    text_artist.set_text('\n'.join(lines))


def layout_card_header(fig, ax, card, title, *, subtitle=None, title_size=None,
                       padding=24, gap=12, min_plot_height=None,
                       plot_axes=None, grow_height=True):
    """Reserve a measured header inside one figure-coordinate card.

    Call after adding axes/colorbars and before export. Sizes are in points;
    padding=24 is 40 px at 120 DPI. Pass all axes sharing this card (including
    colorbars) as plot_axes. This owns their final vertical layout; do not run
    another layout engine afterwards. Re-run after changing fonts or size.
    By default, preserve the initial plot height and grow the figure for a
    taller header; set min_plot_height explicitly to allow a shorter plot.
    """
    engine = fig.get_layout_engine()
    if engine is not None and not isinstance(engine, PlaceHolderLayoutEngine):
        raise ValueError('Finish automatic layout and disable its engine before laying out the card.')
    panels = tuple(plot_axes) if plot_axes is not None else (ax,)
    if ax not in panels or any(panel.figure is not fig for panel in panels):
        raise ValueError('plot_axes must contain the title axis and belong to this figure.')
    # Repeated calls replace the header for this card without duplicating text.
    for artist in getattr(card, '_header_artists', ()):
        artist.remove()
    for loc in ('left', 'center', 'right'):
        ax.set_title('', loc=loc)
    heading = fig.text(0, 0, title, ha='left', va='top', color=VI['text'],
                       fontsize=title_size or plt.rcParams['axes.titlesize'],
                       fontweight='bold', linespacing=1.25, wrap=False)
    detail = fig.text(0, 0, subtitle, ha='left', va='top', color=VI['muted'],
                      fontsize=plt.rcParams['font.size'] * .8, wrap=False) if subtitle else None
    card._header_artists = (heading,) if detail is None else (heading, detail)
    positions = [panel.get_position().frozen() for panel in panels]
    bottom = min(pos.y0 for pos in positions)
    original_top = max(pos.y1 for pos in positions)
    if min_plot_height is None:
        min_plot_height = (original_top - bottom) * fig.bbox.height * 72 / fig.dpi

    for attempt in range(12):
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        fw, fh = fig.bbox.width, fig.bbox.height
        unit = fig.dpi / 72
        pad_px, gap_px = padding * unit, gap * unit
        bounds = card.get_window_extent(renderer)
        left = max(bounds.x0 + pad_px, ax.get_position().x0 * fw)
        right = bounds.x1 - pad_px
        if right - left < 2 * heading.get_fontsize() * unit:
            raise ValueError('Header is too narrow; increase figure width.')
        heading.set_position((left / fw, (bounds.y1 - pad_px) / fh))
        heading.set_text(title)
        _wrap_header(heading, renderer, right - left)
        header_bottom = heading.get_window_extent(renderer).y0
        if detail is not None:
            detail.set_position((left / fw, (header_bottom - gap_px / 2) / fh))
            detail.set_text(subtitle)
            _wrap_header(detail, renderer, right - left)
            header_bottom = detail.get_window_extent(renderer).y0
        # Include ticks, axis labels and colorbar decorations above the plot.
        extra_top = max(max(0, panel.get_tightbbox(renderer).y1 - panel.bbox.y1)
                        for panel in panels)
        top = min(original_top, (header_bottom - gap_px - extra_top) / fh)
        deficit = min_plot_height * unit - (top - bottom) * fh
        if deficit > .1:
            if not grow_height:
                raise ValueError('Header leaves too little plot space; increase figure height or shorten the title.')
            available_fraction = min(original_top, bounds.y1 / fh) - bottom
            if available_fraction <= 0:
                raise ValueError('Card and plot bounds leave no vertical space.')
            fig.set_size_inches(fig.get_figwidth(), fig.get_figheight() +
                                (deficit + gap_px) / available_fraction / fig.dpi)
            continue
        scale = (top - bottom) / (original_top - bottom)
        for panel, pos in zip(panels, positions):
            panel.set_position([pos.x0, bottom + (pos.y0 - bottom) * scale,
                                pos.width, pos.height * scale])
        fig.canvas.draw()
        # A long vertical label can protrude further after shrinking its axes.
        # Re-measure the final geometry instead of trusting the first estimate.
        renderer = fig.canvas.get_renderer()
        plot_top = max(panel.get_tightbbox(renderer).y1 for panel in panels)
        if plot_top <= header_bottom - gap_px + .25:
            return heading, detail
    raise ValueError('Header layout did not converge; increase figure size or simplify plot decorations.')


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
    layout_card_header(fig, ax, card, "Synthetic scan-size distribution")

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
