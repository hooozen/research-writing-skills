#!/usr/bin/env python3
"""Reproducible synthetic examples, not an analysis pipeline for user data.

Run with --output-dir PATH [--language en|zh] [--mode color|grayscale].
Outputs nine final-size SVG/PNG/PDF figures, a browsing overview, a Markdown
gallery, raw JSON data and computed statistics.
Requires NumPy and Matplotlib; no network or optional statistics package.
"""
from __future__ import annotations

import argparse
import json
import textwrap
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import PercentFormatter
import numpy as np

from matplotlib_example import get_style, configure_typography, style_axes, layout_figure_header

DPI = 300
MM = 1 / 25.4
KINDS = ('boxplot', 'violin', 'scatter', 'line', 'histogram', 'ecdf', 'paired', 'interval', 'heatmap')
TITLES = {
    'boxplot': ('Box plot + observations', '箱线图与原始观测'),
    'violin': ('Violin plot + observations', '小提琴图与原始观测'),
    'scatter': ('Scatter plot', '散点图'),
    'line': ('Longitudinal mean ± SD', '折线图：均值与标准差'),
    'histogram': ('Histogram', '直方图'),
    'ecdf': ('Empirical cumulative distribution', '经验累积分布图'),
    'paired': ('Paired observations', '配对观测图'),
    'interval': ('Effect estimates + intervals', '效应估计与区间图'),
    'heatmap': ('Heatmap with a missing cell', '热图与缺失值'),
}
CAPTIONS = {
    'boxplot': ('Box: linearly interpolated Q1–Q3; line: median; whiskers: most extreme observations within 1.5 IQR. All observations shown once.', '箱体为线性插值Q1–Q3，中线为中位数；须延伸至1.5倍四分位距范围内最远的实际观测。所有点只显示一次。'),
    'violin': ('Gaussian KDE with Scott bandwidth, equal maximum widths, trimmed to observed range; points show actual sample sizes; black line: median.', '高斯核密度估计使用Scott带宽，最大宽度相同，曲线限定在观测范围；宽度不代表样本量；黑线为中位数。'),
    'scatter': ('One point per synthetic sample. Pearson r describes association only; no causal claim or significance test.', '每点为一个合成样本；Pearson r仅描述关联，不代表因果关系，也未作显著性检验。'),
    'line': ('Repeated synthetic samples, available cases at each visit; shaded band is sample SD, not CI. The missing visit breaks the line.', '同一批合成样本重复观测；各访视使用可用样本。阴影是样本标准差，不是置信区间；缺失访视处断线。'),
    'histogram': ('Both synthetic groups pooled. Fixed-width bins; y is count, not density. Bins are left-closed/right-open except the final bin.', '合并两组合成观测，固定组距；纵轴为频数，不是密度。区间左闭右开，最后一组包含右端点。'),
    'ecdf': ('Right-continuous step functions; ties combined; denominator is the number of observations in each group. No smoothing.', '右连续阶梯函数，合并重复取值；各组用自身观测数作分母，不作平滑。'),
    'paired': ('Same subject joined across visits; 12 complete pairs of 13 enrolled. One missing follow-up is excluded from paired differences.', '每条连线连接同一受试者的两次观测；13例中12对完整，1例缺失随访，不用于计算配对差值。'),
    'interval': ('MAE change = method − common reference pipeline. Intervals are supplied synthetic 95% CI fixtures, not estimated from raw samples.', '平均绝对误差差值＝方法−同一参照流程；95%置信区间是明确给定的合成夹具值，并非从样本数据估计。'),
    'heatmap': ('Mean absolute error in μm; shared 0–5 scale across cells. Gray / NA is missing, never zero; no row normalization. Cells are supplied synthetic aggregates; individual data and n are not supplied.', '颜色表示平均绝对误差（μm），所有单元格共用0–5色标；灰色NA为缺失而非零，不按行归一化。单元格为给定合成汇总值，无个体观测及n。'),
}


def translate(pair, language):
    return pair[language == 'zh']


def clean_json(value):
    """Keep missing observations as JSON null, never nonstandard NaN tokens."""
    if isinstance(value, dict):
        return {k: clean_json(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, np.ndarray)):
        return [clean_json(v) for v in value]
    if isinstance(value, (bool, np.bool_)):
        return bool(value)
    if isinstance(value, (np.integer, int)):
        return int(value)
    if isinstance(value, (np.floating, float)):
        return float(value) if np.isfinite(value) else None
    return value


def fixture_data():
    rng = np.random.default_rng(20260907)
    groups = {'A': np.r_[np.round(rng.normal(18, 2.5, 29), 1), 30.0].tolist(),
              'B': np.round(rng.normal(21, 3.2, 34), 1).tolist()}
    x = np.round(rng.uniform(15, 35, 48), 2)
    y = np.round(8.5 - .18 * x + rng.normal(0, .48, 48), 2)
    weeks = [0, 1, 2, 4, 8]
    values = np.round(rng.normal(20, 2, (12, 1)) + np.array([0, .4, 1, 1.8, 2.5]) + rng.normal(0, .7, (12, 5)), 2)
    values[:, 2] = np.nan
    values[-2:, -1] = np.nan
    before = np.round(rng.normal(22, 2.5, 13), 2)
    after = np.round(before - rng.normal(2.1, 1.6, 13), 2)
    after[-1] = np.nan
    return clean_json({
        'synthetic': True, 'seed': 20260907,
        'units': {'distribution': 'a.u.', 'scatter_x': 'dB', 'scatter_y': 'μm', 'longitudinal': 'a.u.', 'paired': 'a.u.', 'interval': 'μm', 'heatmap': 'μm'},
        'sampling': {'groups': 'one observation per synthetic sample; independent groups', 'scatter': 'one x/y pair per synthetic sample', 'longitudinal': 'same samples measured across visits; not independent time points', 'paired': 'sample IDs define pairing; incomplete follow-up is excluded only from paired analysis'},
        'groups': groups,
        'scatter': [{'id': f'S{i+1:02}', 'snr_db': a, 'error_um': b} for i, (a, b) in enumerate(zip(x, y))],
        'longitudinal': {'weeks': weeks, 'subjects': [{'id': f'L{i+1:02}', 'values': row} for i, row in enumerate(values)]},
        'paired': [{'id': f'P{i+1:02}', 'before': a, 'after': b} for i, (a, b) in enumerate(zip(before, after))],
        'interval': {'metric': 'difference in mean absolute error (method minus reference)', 'reference': 'same reference pipeline for all methods', 'provenance': 'supplied synthetic 95% confidence-interval fixtures; not computed from observations',
                     'rows': [{'method': name, 'estimate': m, 'low': lo, 'high': hi} for name, m, lo, hi in zip('ABCD', [-1.8, -.6, .4, 1.3], [-2.7, -1.4, -.2, .5], [-.9, .2, 1., 2.1])]},
        'heatmap': {'provenance': 'supplied synthetic aggregate mean absolute errors; no individual observations or cell sample sizes supplied', 'rows': ['V1', 'V2', 'V3', 'V4'], 'columns': ['D1', 'D2', 'D3', 'D4'], 'scale': [0, 5],
                    'values': [[3.4, 4.1, 3.8, 4.7], [3., 3.9, None, 4.5], [2.7, 3.6, 3.1, 4.], [2.8, 3.4, 3., 3.9]]},
    })


def summarize(data):
    stats = {'groups': {}, 'line': [], 'ecdf': {}}
    for name, values in data['groups'].items():
        a = np.asarray(values)
        q1, median, q3 = np.quantile(a, [.25, .5, .75], method='linear')
        iqr = q3 - q1
        in_whiskers = a[(a >= q1 - 1.5 * iqr) & (a <= q3 + 1.5 * iqr)]
        stats['groups'][name] = dict(n=len(a), q1=q1, median=median, q3=q3, mean=a.mean(), sd=a.std(ddof=1), whisker_low=in_whiskers.min(), whisker_high=in_whiskers.max())
        unique, counts = np.unique(a, return_counts=True)
        stats['ecdf'][name] = dict(x=unique, cumulative=np.cumsum(counts) / len(a))
    pooled = np.concatenate(list(data['groups'].values()))
    counts, edges = np.histogram(pooled, bins=np.arange(9, 36, 3))
    stats['histogram'] = dict(counts=counts, edges=edges, n=len(pooled))
    values = np.asarray([row['values'] for row in data['longitudinal']['subjects']], dtype=float)
    for week, column in zip(data['longitudinal']['weeks'], values.T):
        valid = column[np.isfinite(column)]
        stats['line'].append(dict(week=week, n=len(valid), mean=valid.mean() if len(valid) else None, sd=valid.std(ddof=1) if len(valid) > 1 else None))
    pairs = [r for r in data['paired'] if r['before'] is not None and r['after'] is not None]
    delta = np.array([r['after'] - r['before'] for r in pairs])
    stats['paired'] = dict(enrolled=len(data['paired']), complete=len(pairs), excluded=len(data['paired'])-len(pairs), mean_change=delta.mean(), median_change=np.median(delta))
    stats['scatter'] = dict(n=len(data['scatter']), pearson_r=np.corrcoef([r['snr_db'] for r in data['scatter']], [r['error_um'] for r in data['scatter']])[0, 1])
    return clean_json(stats)


def configure(language, mode='color'):
    configure_typography(DPI, mode=mode)
    if language == 'zh':
        available = {f.name for f in font_manager.fontManager.ttflist}
        for name in ('Noto Sans CJK SC', 'PingFang SC', 'Microsoft YaHei', 'Arial Unicode MS', 'Heiti SC'):
            if name in available:
                plt.rcParams['font.sans-serif'] = [name, 'DejaVu Sans']
                break
        else:
            raise ValueError('Chinese output requires an installed CJK font; choose --language en otherwise.')


def _cell_text_color(background, ink):
    """Choose the more legible text colour on the actual mapped cell colour."""
    def luminance(color):
        rgb = np.asarray(matplotlib.colors.to_rgb(color))
        linear = np.where(rgb <= .04045, rgb / 12.92, ((rgb + .055) / 1.055) ** 2.4)
        return float(linear @ np.array([.2126, .7152, .0722]))
    value, dark = luminance(background), luminance(ink)
    return 'white' if 1.05 / (value + .05) > (value + .05) / (dark + .05) else ink


def draw(kind, ax, data, stats, language='en', compact=False, mode='color'):
    """Draw one example; colour modes alter encodings, never data or statistics."""
    if kind not in KINDS:
        raise ValueError(f'Unknown chart kind: {kind}')
    t = lambda en, zh: zh if language == 'zh' else en
    style = get_style(mode)
    colors = style['palette'][:2]
    markers = style['markers'][:2]
    style_axes(ax, mode=mode)
    ax.set_facecolor(style['canvas'])
    ax.tick_params(labelsize=7)
    # A browsing overview has small titles; final-size single figures place this
    # identification in the figure header and retain full captions in Markdown.
    if compact:
        ax.set_title(textwrap.fill(translate(TITLES[kind], language), 34),
                     loc='left', fontsize=7, pad=6, fontweight='normal')
    groups = [np.array(v) for v in data['groups'].values()]
    if kind in ('boxplot', 'violin'):
        if kind == 'boxplot':
            artists = ax.boxplot(groups, positions=[1, 2], widths=.40, whis=1.5,
                                 patch_artist=True, showfliers=False,
                                 medianprops={'color': style['text'], 'linewidth': .7},
                                 whiskerprops={'color': style['muted'], 'linewidth': .6},
                                 capprops={'color': style['muted'], 'linewidth': .6})
            for body, color in zip(artists['boxes'], colors):
                body.set_facecolor(matplotlib.colors.to_rgba(color, .16))
                body.set_edgecolor(color)
                body.set_linewidth(.7)
        else:
            artists = ax.violinplot(groups, positions=[1, 2], widths=.75,
                                    showextrema=False, showmedians=True, bw_method='scott')
            for body, color in zip(artists['bodies'], colors):
                body.set_facecolor(color); body.set_edgecolor(color); body.set_alpha(.20)
                body.set_linewidth(.6)
            artists['cmedians'].set_color(style['text'])
            artists['cmedians'].set_linewidth(.7)
        jitter = np.random.default_rng(19)
        for i, (values, color, marker) in enumerate(zip(groups, colors, markers), 1):
            ax.scatter(i + jitter.uniform(-.10, .10, len(values)), values,
                       s=7, marker=marker, color=color, alpha=.85,
                       edgecolors='white', linewidths=.2, zorder=3)
        ax.set_xticks([1, 2], [f'{t("Group", "组")} {name}\nn = {len(v)}'
                              for name, v in zip('AB', groups)])
        ax.set_ylabel(t('Measurement (a.u.)', '测量值（a.u.）')); ax.set_xlim(.5, 2.5)
    elif kind == 'scatter':
        ax.scatter([r['snr_db'] for r in data[kind]], [r['error_um'] for r in data[kind]],
                   color=style['primary'], s=9, alpha=.8, edgecolors='white', linewidths=.25)
        ax.set_xlabel(t('Signal-to-noise ratio (dB)', '信噪比（dB）'))
        ax.set_ylabel(t('Absolute error (μm)', '绝对误差（μm）'))
        ax.text(.98, .97, f'n = {stats[kind]["n"]}\nr = {stats[kind]["pearson_r"]:.2f}',
                transform=ax.transAxes, ha='right', va='top', fontsize=6.5)
    elif kind == 'line':
        weeks = np.array([r['week'] for r in stats[kind]])
        mean = np.array([r['mean'] for r in stats[kind]], dtype=float)
        sd = np.array([r['sd'] for r in stats[kind]], dtype=float)
        ax.fill_between(weeks, mean-sd, mean+sd, color=style['primary'], alpha=.14, linewidth=0)
        ax.plot(weeks, mean, color=style['primary'], marker=markers[0], linewidth=1, markersize=2.8)
        ax.set_xticks(weeks); ax.set_xlabel(t('Week', '周'))
        ax.set_ylabel(t('Measurement (a.u.)', '测量值（a.u.）'))
        if not np.any(np.isfinite(mean)):
            raise ValueError('A line plot requires at least one observed time point.')
        finite_sd = np.nan_to_num(sd, nan=0)
        lo, hi = np.nanmin(mean-finite_sd), np.nanmax(mean+finite_sd)
        ax.set_ylim(lo-.6, hi+1.1)
        for row in stats[kind]:
            if row['mean'] is not None:
                error = row['sd'] if row['sd'] is not None else 0
                ax.text(row['week'], row['mean']+error+.23, f'n={row["n"]}',
                        ha='center', fontsize=6)
            else:
                ax.text(row['week'], lo+.2, t('No data', '无数据'), ha='center',
                        color=style['muted'], fontsize=6)
    elif kind == 'histogram':
        counts, edges = np.array(stats[kind]['counts']), np.array(stats[kind]['edges'])
        ax.bar(edges[:-1], counts, width=np.diff(edges), align='edge',
               color=style['primary'], edgecolor=style['canvas'], linewidth=.45)
        ax.set_xlabel(t('Measurement (a.u.)', '测量值（a.u.）'))
        ax.set_ylabel(t('Count', '频数')); ax.set_ylim(0, max(counts)*1.2)
        ax.set_xticks(edges[::2])
        ax.text(.98, .97, f'n = {stats[kind]["n"]}', transform=ax.transAxes,
                ha='right', va='top', fontsize=6.5)
    elif kind == 'ecdf':
        lo, hi = min(v.min() for v in groups)-1, max(v.max() for v in groups)+1
        for name, color, linestyle in zip('AB', colors, style['linestyles']):
            row = stats[kind][name]
            ax.step([lo, *row['x'], hi], [0, *row['cumulative'], 1], where='post',
                    color=color, linestyle=linestyle, linewidth=1,
                    label=f'{name} · n={stats["groups"][name]["n"]}')
        ax.set_xlim(lo, hi); ax.set_ylim(-.03, 1.03)
        ax.yaxis.set_major_formatter(PercentFormatter(1))
        ax.set_xlabel(t('Measurement (a.u.)', '测量值（a.u.）'))
        ax.set_ylabel(t('Cumulative proportion', '累计比例'))
        ax.legend(frameon=False, loc='upper left', fontsize=6.5, handlelength=2.5)
    elif kind == 'paired':
        for row in data[kind]:
            if row['before'] is not None and row['after'] is not None:
                ax.plot([0, 1], [row['before'], row['after']], color=style['neutral'],
                        linewidth=.55, alpha=.7)
                for x, key, color, marker in zip([0, 1], ['before', 'after'], colors, markers):
                    ax.scatter(x, row[key], color=color, marker=marker, s=9,
                               edgecolors='white', linewidths=.25, zorder=3)
        ax.set_xticks([0, 1], [t('Before', '前测'), t('After', '后测')]); ax.set_xlim(-.35, 1.35)
        ax.set_ylabel(t('Measurement (a.u.)', '测量值（a.u.）'))
        ax.margins(y=.18)
        ax.text(.98, .97, f'{stats[kind]["complete"]} '+t('complete pairs', '对完整观测'),
                transform=ax.transAxes, ha='right', va='top', fontsize=6)
    elif kind == 'interval':
        for i, row in enumerate(data[kind]['rows']):
            m, lo, hi = (row[key] for key in ('estimate', 'low', 'high'))
            ax.errorbar(m, i, xerr=[[m-lo], [hi-m]], fmt=markers[0],
                        color=style['primary'], markersize=3, capsize=2.5, linewidth=.8)
        ax.axvline(0, color=style['muted'], linewidth=.6, linestyle='--')
        ax.set_yticks(range(4), [t('Method ', '方法 ')+r['method'] for r in data[kind]['rows']])
        ax.invert_yaxis(); ax.set_xlim(-3.2, 3.2); ax.set_xticks([-3, -2, -1, 0, 1, 2, 3])
        ax.set_xlabel(t('Δ MAE (μm)', '平均绝对误差差值（μm）'))
    elif kind == 'heatmap':
        matrix = np.asarray(data[kind]['values'], dtype=float)
        pale = tuple(.9+.1*c for c in matplotlib.colors.to_rgb(style['primary']))
        cmap = LinearSegmentedColormap.from_list('scientific_sequential', [style['canvas'], pale, style['primary']])
        cmap = cmap.with_extremes(bad=style['neutral'])
        im = ax.pcolormesh(np.arange(matrix.shape[1]+1), np.arange(matrix.shape[0]+1),
                           np.ma.masked_invalid(matrix), cmap=cmap,
                           vmin=data[kind]['scale'][0], vmax=data[kind]['scale'][1],
                           shading='flat', rasterized=False, edgecolors='none')
        for (i, j), value in np.ndenumerate(matrix):
            background = style['neutral'] if np.isnan(value) else cmap(im.norm(value))
            ax.text(j+.5, i+.5, 'NA' if np.isnan(value) else f'{value:.1f}',
                    va='center', ha='center', fontsize=6.5,
                    color=_cell_text_color(background, style['text']))
        ax.set_xlim(0, matrix.shape[1]); ax.set_ylim(matrix.shape[0], 0)
        ax.set_xticks(np.arange(matrix.shape[1])+.5, data[kind]['columns'])
        ax.set_yticks(np.arange(matrix.shape[0])+.5, data[kind]['rows'])
        ax.set_xlabel(t('Dataset', '数据集')); ax.set_ylabel(t('Method version', '方法版本'))
        ax.tick_params(length=0, pad=3)
        ax.spines[:].set_visible(False)
        bar = ax.figure.colorbar(im, ax=ax, fraction=.045, pad=.06)
        bar.outline.set_visible(False)
        bar.solids.set_rasterized(False); bar.solids.set_edgecolor('face')
        bar.set_label(t('MAE (μm)', '平均绝对误差（μm）'), fontsize=6.5,
                      color=style['muted'], labelpad=3)
        bar.ax.tick_params(labelsize=6.5, colors=style['muted'], width=.5, length=2)



def data_table(kind, data, stats, language):
    """Readable numerical companions; unrounded values remain in JSON."""
    t = lambda en, zh: zh if language == 'zh' else en
    if kind in ('boxplot', 'violin', 'ecdf'):
        headers = [t('Group','组'), 'n', 'Q1', t('Median','中位数'), 'Q3', t('Lower whisker','下须'), t('Upper whisker','上须')]
        rows = [[name, *[r[k] for k in ('n','q1','median','q3','whisker_low','whisker_high')]] for name, r in stats['groups'].items()]
    elif kind == 'scatter':
        headers = ['n', 'Pearson r']; rows = [[stats[kind]['n'],stats[kind]['pearson_r']]]
    elif kind == 'line':
        headers = [t('Week','周'), 'n', t('Mean','均值'), t('Sample SD','样本标准差')]
        rows = [[r[k] for k in ('week','n','mean','sd')] for r in stats[kind]]
    elif kind == 'histogram':
        edges, counts = stats[kind]['edges'], stats[kind]['counts']
        headers = [t('Bin (a.u.)','区间（a.u.）'), t('Count','频数')]
        rows = [[f'[{lo}, {hi}{"]" if i==len(counts)-1 else ")"}', count] for i, (lo,hi,count) in enumerate(zip(edges[:-1], edges[1:], counts))]
    elif kind == 'paired':
        headers = ['ID', t('Before','前测'), t('After','后测'), t('After − before','后测 − 前测')]
        rows = [[r['id'],r['before'],r['after'],None if r['before'] is None or r['after'] is None else r['after']-r['before']] for r in data[kind]]
    elif kind == 'interval':
        headers = [t('Method','方法'), t('Estimate (μm)','估计（μm）'), t('Lower bound','下界'), t('Upper bound','上界')]
        rows = [[r[k] for k in ('method','estimate','low','high')] for r in data[kind]['rows']]
    else:
        headers = [t('Version','版本'), *data[kind]['columns']]
        rows = [[name,*values] for name, values in zip(data[kind]['rows'],data[kind]['values'])]
    fmt = lambda value: 'NA' if value is None else f'{value:.3f}' if isinstance(value,float) else str(value)
    return '\n'.join(['| '+' | '.join(headers)+' |', '| '+' | '.join(['---']*len(headers))+' |', *['| '+' | '.join(map(fmt,row))+' |' for row in rows]])


def _validate_bounds(fig):
    """Reject clipped final-size exports rather than relying on a tight crop."""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    bounds = fig.bbox
    boxes = [ax.get_tightbbox(renderer) for ax in fig.axes]
    boxes.extend(text.get_window_extent(renderer) for text in fig.texts if text.get_visible())
    for box in boxes:
        if box is not None and (box.x0 < bounds.x0-.5 or box.y0 < bounds.y0-.5 or
                                box.x1 > bounds.x1+.5 or box.y1 > bounds.y1+.5):
            raise ValueError('Final-size text or axes extend beyond the canvas; increase margins.')


def generate(output_dir, language='en', mode='color'):
    """Export final-size figures and separate browsing/traceability companions."""
    configure(language, mode)
    style = get_style(mode)
    output_dir = Path(output_dir)
    figures = output_dir/'figures'; figures.mkdir(parents=True, exist_ok=True)
    data = fixture_data(); stats = summarize(data)
    for filename, obj in (('data.json', data), ('statistics.json', stats)):
        (output_dir/filename).write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf-8')
    dimensions = {}
    for kind in KINDS:
        fig, ax = plt.subplots(figsize=(89*MM, 78*MM), dpi=DPI)
        # The colourbar's tick labels and vertical label need their own right margin.
        fig.subplots_adjust(left=.21, right=.83 if kind == 'heatmap' else .95,
                            top=.79, bottom=.22)
        draw(kind, ax, data, stats, language, mode=mode)
        label = 'Synthetic data · demonstration only' if language == 'en' else '合成数据 · 仅用于图表演示'
        # Long statistical captions belong next to the figure in gallery.md,
        # not in a large banner inside the manuscript panel.
        layout_figure_header(fig, ax, translate(TITLES[kind], language),
                             subtitle=label, title_size=7, plot_axes=fig.axes)
        dimensions[kind] = dict(width_mm=fig.get_figwidth()*25.4,
                                height_mm=fig.get_figheight()*25.4)
        _validate_bounds(fig)
        for suffix in ('svg', 'png', 'pdf'):
            fig.savefig(figures/f'{kind}.{suffix}', dpi=DPI, facecolor=style['canvas'])
        plt.close(fig)
    # This is a large browsing contact sheet, not a nine-panel figure to shrink
    # to one column. Each individual file above retains 7 pt text at 89 mm.
    fig, axes = plt.subplots(3, 3, figsize=(270*MM, 245*MM), dpi=180)
    fig.patch.set_facecolor(style['canvas'])
    fig.subplots_adjust(left=.075, right=.96, bottom=.075, top=.91, hspace=.72, wspace=.65)
    for letter, kind, ax in zip('abcdefghi', KINDS, axes.flat):
        draw(kind, ax, data, stats, language, compact=True, mode=mode)
        ax.text(-.26, 1.08, letter, transform=ax.transAxes, fontsize=8, fontweight='bold')
    fig.suptitle('Scientific chart examples · synthetic data' if language == 'en' else '常用科研图表样例 · 全部为合成数据',
                 x=.075, ha='left', fontsize=10, fontweight='normal')
    fig.text(.075,.025, 'Browsing overview; use individual final-size files for manuscripts.' if language == 'en' else '此图用于浏览；论文请使用按最终尺寸导出的单图。',
             color=style['muted'], fontsize=7)
    fig.savefig(output_dir/'overview.png', dpi=180, facecolor=style['canvas']); plt.close(fig)
    title = '# Scientific chart examples — synthetic data' if language == 'en' else '# 常用科研图表样例（全部为合成数据）'
    intro = ('Nine reproducible examples with publication-size typography. All observations and interval fixtures are synthetic; no research findings or significance claims.'
             if language == 'en' else '九种可复现的科研图表，使用最终印刷尺寸字号。所有观测和区间均为合成演示，不代表真实研究发现或显著性证据。')
    parts = [title, intro,
             f'Mode: `{mode}`. Figures are 89 mm wide; ordinary labels use 7 pt at the exported size. The overview is for browsing only.' if language == 'en' else f'模式：`{mode}`。单图宽89 mm，普通标签在导出尺寸为7 pt；总览仅用于浏览。',
             'Table values are rounded to 3 decimal places; JSON retains full precision.' if language == 'en' else '表中小数保留3位；JSON保留完整精度。a.u.表示任意单位。',
             '[Raw observations / 原始数据](data.json) · [Exact statistics / 精确统计量](statistics.json)',
             '![Overview / 总览](overview.png)']
    for kind in KINDS:
        title = translate(TITLES[kind], language)
        parts += [f'## {title}', f'![{title}](figures/{kind}.svg)',
                  translate(CAPTIONS[kind], language), data_table(kind, data, stats, language),
                  f'[PNG](figures/{kind}.png) · [SVG](figures/{kind}.svg) · [PDF](figures/{kind}.pdf)']
    (output_dir/'gallery.md').write_text('\n\n'.join(parts)+'\n', encoding='utf-8')
    (output_dir/'manifest.json').write_text(json.dumps({'synthetic':True,'seed':20260907,
        'language':language,'mode':mode,'charts':list(KINDS),'dimensions':dimensions,
        'font_size_pt':7,'raster_dpi':DPI,'numpy':np.__version__,
        'matplotlib':matplotlib.__version__}, indent=2)+'\n')
    return data, stats


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--language', choices=('en','zh'), default='en')
    parser.add_argument('--mode', choices=('color','grayscale'), default='color')
    args = parser.parse_args()
    generate(args.output_dir, args.language, args.mode)
    print(f'Generated {len(KINDS)} synthetic figures in {args.output_dir}')


if __name__ == '__main__':
    main()
