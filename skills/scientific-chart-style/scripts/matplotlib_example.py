#!/usr/bin/env python3
"""Optional Matplotlib translation of Scientific Chart Style.

High-contrast blue is the default; --mode grayscale selects print style D.
Font sizes are physical points at final size, independent of export DPI.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from numbers import Integral
from pathlib import Path
import re
import matplotlib.pyplot as plt
from matplotlib.layout_engine import PlaceHolderLayoutEngine

VI = {
    'canvas': '#FFFFFF', 'card': '#FFFFFF',
    'primary': '#1464D2', 'secondary': '#B64B00', 'third': '#7A3DB8',
    'light': '#BFD5F4', 'neutral': '#586575', 'baseline': '#34383C',
    'text': '#24282C', 'muted': '#626B73',
    'palette': ['#1464D2', '#B64B00', '#7A3DB8'],
    'markers': ['o', 's', '^'], 'linestyles': ['-', '--', ':'],
    'hatches': ['', '//', '..'],
}

def get_style(mode: str = 'color') -> dict:
    """Independent tokens; grayscale is a designed print mode."""
    if mode not in {'color', 'grayscale'}:
        raise ValueError('mode must be color or grayscale')
    style = deepcopy(VI)
    if mode == 'grayscale':
        style.update(primary='#34383C', secondary='#70767B', third='#92989E',
                     light='#E0E3E5', neutral='#B7BCC0',
                     palette=['#34383C', '#70767B', '#92989E'])
    return style

def configure_typography(dpi: float = 300, *, mode: str = 'color') -> dict:
    if dpi <= 0:
        raise ValueError('dpi must be positive')
    style = get_style(mode)
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'Helvetica', 'Noto Sans', 'DejaVu Sans'],
        'font.size': 7, 'axes.labelsize': 7, 'axes.titlesize': 7,
        'axes.titleweight': 'normal', 'axes.labelpad': 3.5,
        'xtick.labelsize': 6.5, 'ytick.labelsize': 6.5,
        'legend.fontsize': 6.5, 'legend.frameon': False,
        'axes.linewidth': .6, 'lines.linewidth': 1.0,
        'lines.markersize': 3, 'xtick.major.size': 2.5, 'ytick.major.size': 2.5,
        'xtick.major.width': .6, 'ytick.major.width': .6,
        'xtick.major.pad': 2.5, 'ytick.major.pad': 2.5,
        'text.color': style['text'], 'axes.labelcolor': style['text'],
        'axes.edgecolor': style['baseline'], 'xtick.color': style['baseline'],
        'ytick.color': style['baseline'], 'figure.facecolor': 'white',
        'axes.facecolor': 'white', 'savefig.facecolor': 'white',
        'axes.grid': False, 'svg.fonttype': 'none', 'pdf.fonttype': 42, 'ps.fonttype': 42,
    })
    return style

def style_axes(ax, *, mode: str = 'color') -> None:
    style = get_style(mode)
    ax.set_facecolor('white')
    ax.spines[['top', 'right']].set_visible(False)
    for edge in ['left', 'bottom']:
        ax.spines[edge].set_color(style['baseline'])
        ax.spines[edge].set_linewidth(.6)
    ax.tick_params(direction='out', width=.6, length=2.5)
    ax.grid(False)

def _wrap_header(text_artist, renderer, width):
    """Wrap measured plain text, retaining CJK and long identifiers."""
    source = text_artist.get_text()
    def fits(text):
        text_artist.set_text(text)
        return text_artist.get_window_extent(renderer).width <= width
    lines = []
    for paragraph in source.split('\n'):
        line = ''
        for token in re.findall(r'\S+\s*', paragraph):
            if fits((line+token).rstrip()):
                line += token
                continue
            if line:
                lines.append(line.rstrip()); line = ''
            if fits(token.rstrip()):
                line = token
                continue
            for char in token:
                if not fits(line+char):
                    if not line:
                        raise ValueError('Header is too narrow; increase figure width.')
                    lines.append(line.rstrip()); line = ''
                line += char
        lines.append(line.rstrip())
    text_artist.set_text('\n'.join(lines))

def layout_figure_header(fig, ax, title, *, subtitle=None, title_size=None,
                         padding=6, gap=4, min_plot_height=None,
                         plot_axes=None, grow_height=True):
    """Reserve a measured white header without shrinking publication fonts.

    Dimensions are points. Call after axes/colorbars exist and automatic layout
    has finished. This owns final vertical positions. Re-run after a resize.
    Grow height to preserve initial physical plot height, or report insufficient
    space with grow_height=False for a fixed page.
    """
    engine = fig.get_layout_engine()
    if engine is not None and not isinstance(engine, PlaceHolderLayoutEngine):
        raise ValueError('Finish automatic layout and disable its engine before laying out the header.')
    panels = tuple(plot_axes) if plot_axes is not None else (ax,)
    if ax not in panels or any(p.figure is not fig for p in panels):
        raise ValueError('plot_axes must include ax and belong to this figure.')
    for artist in getattr(fig, '_scientific_header_artists', ()):
        artist.remove()
    for loc in ['left', 'center', 'right']:
        ax.set_title('', loc=loc)
    heading = fig.text(0, 0, title, ha='left', va='top', fontsize=title_size or 7,
                       color=VI['text'], linespacing=1.2)
    detail = fig.text(0, 0, subtitle, ha='left', va='top', fontsize=6.5,
                      color=VI['muted'], linespacing=1.2) if subtitle else None
    fig._scientific_header_artists = (heading,) if detail is None else (heading, detail)
    positions = [p.get_position().frozen() for p in panels]
    bottom = min(p.y0 for p in positions)
    original_top = max(p.y1 for p in positions)
    if min_plot_height is None:
        min_plot_height = (original_top-bottom)*fig.get_figheight()*72
    if original_top <= bottom:
        raise ValueError('Invalid plot bounds.')
    for _ in range(12):
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        fw, fh = fig.bbox.width, fig.bbox.height
        unit = fig.dpi/72
        left = max(padding*unit, ax.get_position().x0*fw)
        right = fw-padding*unit
        if right-left < 2*heading.get_fontsize()*unit:
            raise ValueError('Header is too narrow; increase figure width.')
        heading.set_position((left/fw, 1-padding*unit/fh))
        heading.set_text(title)
        _wrap_header(heading, renderer, right-left)
        header_bottom = heading.get_window_extent(renderer).y0
        if detail is not None:
            detail.set_position((left/fw, (header_bottom-gap*unit/2)/fh))
            detail.set_text(subtitle)
            _wrap_header(detail, renderer, right-left)
            header_bottom = detail.get_window_extent(renderer).y0
        extra_top = max(max(0, p.get_tightbbox(renderer).y1-p.bbox.y1) for p in panels)
        top = min(original_top, (header_bottom-gap*unit-extra_top)/fh)
        deficit = min_plot_height*unit-(top-bottom)*fh
        if deficit > .1:
            if not grow_height:
                raise ValueError('Header leaves too little plot space; increase figure height or shorten the title.')
            fig.set_size_inches(fig.get_figwidth(), fig.get_figheight()+(deficit+gap*unit)/(original_top-bottom)/fig.dpi)
            continue
        scale = (top-bottom)/(original_top-bottom)
        for p, pos in zip(panels, positions):
            p.set_position([pos.x0, bottom+(pos.y0-bottom)*scale, pos.width, pos.height*scale])
        fig.canvas.draw()
        renderer = fig.canvas.get_renderer()
        plot_top = max(p.get_tightbbox(renderer).y1 for p in panels)
        if plot_top <= header_bottom-gap*unit+.25:
            return heading, detail
    raise ValueError('Header layout did not converge; increase figure height or simplify decorations.')

def count_share_label(value: int, total: int | None) -> str:
    if isinstance(value, bool) or not isinstance(value, Integral) or value < 0:
        raise ValueError('value must be a nonnegative integer count')
    if total is None:
        return f'{value:,} · share unavailable'
    if isinstance(total, bool) or not isinstance(total, Integral) or total < 0 or value > total:
        raise ValueError('total must be an integer population at least as large as value')
    if total == 0:
        return f'{value:,} · share unavailable'
    return f'{value:,} · {value/total:.1%}'

def build_example(output: Path, *, mode: str = 'color') -> None:
    style = configure_typography(mode=mode)
    labels = ['Category A', 'Category B', 'Other / unknown']
    values = [14325, 12194, 2033]
    total = sum(values)
    fig, ax = plt.subplots(figsize=(180/25.4, 80/25.4), dpi=150)
    style_axes(ax, mode=mode)
    bars = ax.barh(labels, values, height=.58,
                   color=[style['primary'], style['secondary'], style['neutral']],
                   linewidth=.5, edgecolor='white')
    if mode == 'grayscale':
        for bar, hatch in zip(bars, ['', '//', '..']):
            bar.set_hatch(hatch); bar.set_edgecolor(style['baseline'])
    ax.invert_yaxis()
    for bar, value in zip(bars, values):
        ax.text(value+total*.012, bar.get_y()+bar.get_height()/2,
                count_share_label(value, total), va='center', fontsize=7)
    ax.set_xlim(0, max(values)*1.43)
    ax.tick_params(axis='y', length=0)
    ax.tick_params(axis='x', bottom=False, labelbottom=False)
    ax.spines['bottom'].set_visible(False)
    fig.subplots_adjust(left=.19, right=.96, top=.80, bottom=.18)
    fig.text(.19, .055, f'Synthetic example · {total:,} records · exclusive categories',
             fontsize=6.5, color=style['muted'])
    layout_figure_header(fig, ax, 'Synthetic category distribution')
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=300, facecolor='white')
    plt.close(fig)
    print(f'Wrote {output}')

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='scientific_chart_example.svg')
    parser.add_argument('--mode', choices=['color', 'grayscale'], default='color')
    args = parser.parse_args()
    output = Path(args.output)
    if output.suffix.lower() not in {'.svg', '.png', '.pdf'}:
        parser.error('--output must end in .svg, .png or .pdf')
    build_example(output, mode=args.mode)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
