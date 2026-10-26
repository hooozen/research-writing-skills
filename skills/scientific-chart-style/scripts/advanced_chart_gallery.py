#!/usr/bin/env python3
"""Nine reproducible synthetic scientific figures; not a user-data analysis tool.

Uses only NumPy, Matplotlib and the standard library. All numerical definitions
are explicit below; choosing a figure does not validate its assumptions.
Run with --output-dir PATH [--mode color|grayscale] [--language en|zh].
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap, to_rgb
import numpy as np

from matplotlib_example import configure_typography, get_style, layout_figure_header, style_axes

DPI = 300
MM = 1 / 25.4
KINDS = ('raincloud', 'roc', 'pr', 'calibration', 'confusion', 'bland_altman', 'survival', 'volcano', 'pca')
TITLES = {
    'raincloud': ('Raincloud: distribution and observations', '雨云图：分布与原始观测'),
    'roc': ('Receiver operating characteristic', '受试者工作特征曲线'),
    'pr': ('Precision–recall curve', '精确率–召回率曲线'),
    'calibration': ('Calibration with bin sample sizes', '校准图与分箱样本量'),
    'confusion': ('Confusion matrix at a fixed threshold', '固定阈值的混淆矩阵'),
    'bland_altman': ('Agreement between two measurements', '两种测量的一致性'),
    'survival': ('Kaplan–Meier survival and numbers at risk', 'Kaplan–Meier生存与风险集人数'),
    'volcano': ('Effect size and adjusted p-value', '效应量与多重校正后的p值'),
    'pca': ('Principal components of standardized features', '标准化特征的主成分'),
}
CAPTIONS = {
    'raincloud': (
        'One point per independent synthetic observation. Half-violins use Gaussian Scott-bandwidth KDE trimmed to the observed range; equal maximum widths do not encode n. Boxes show linear Q1–Q3, median and 1.5-IQR observed whiskers. All points, including outliers, remain visible once.',
        '每点为一个独立合成观测。半小提琴为高斯Scott带宽核密度，限定于观测范围，最大宽度相同不代表n。箱体为线性插值Q1–Q3、中位数和1.5 IQR范围内最远观测；所有点（含离群点）只显示一次。'),
    'roc': (
        'Positive class = 1; one probability and label per independent synthetic case. All tied scores enter together at score ≥ threshold. ROC AUC uses trapezoidal interpolation across threshold points. No confidence interval or significance test is implied.',
        '正类为1，每个独立合成样本有一个概率和标签。预测规则为分数≥阈值，相同分数同时进入。ROC AUC按阈值点之间梯形积分；未提供置信区间或显著性检验。'),
    'pr': (
        'The empirical PR step uses the precision attained after each recall increase (pre-step in increasing-recall order). AP = sum Δrecall × precision, without interpolation; the separately reported trapezoidal PR area is a different quantity. The dotted baseline is positive-class prevalence.',
        '经验PR阶梯以每次召回率增加后的精确率覆盖该区间（召回率递增时使用前阶梯）。AP为Δ召回率×精确率之和，不插值；另列的梯形PR面积是不同量。虚线为正类比例。'),
    'calibration': (
        'Five fixed-width probability bins on [0,1]; bins are left-closed/right-open except the last includes 1. Plot each nonempty bin at its actual mean probability and observed positive fraction; annotate n. Empty bins are retained in the table, not interpolated. ECE is the sample-count-weighted absolute bin gap and depends on binning. No CI is shown.',
        '在[0,1]上固定等宽分5箱；左闭右开，最后一箱包含1。非空箱显示实际平均预测概率、阳性比例及n；空箱在表中保留，不插值。ECE是按样本量加权的分箱绝对差，依赖分箱；未绘制置信区间。'),
    'confusion': (
        'Rows = true class; columns = predicted class, positive = 1, threshold = 0.5 with equality positive. Color shows within-true-class fraction on one common 0–1 scale; each cell reports count and row percentage. Missing/undefined row denominators are never zero-filled.',
        '行为真实类别，列为预测类别；正类为1，阈值0.5且等于阈值判正。颜色为真实类别内比例，统一0–1色标；每格列出数量与行百分比。零分母的未定义比例不能补成零。'),
    'bland_altman': (
        'One complete pair per independent synthetic unit. x = (A+B)/2; y = B−A. Bias is mean difference; limits of agreement = bias ± 1.96 × sample SD (ddof=1), not confidence limits. These descriptive normal-difference limits do not establish acceptable agreement; no repeated-measure correction or CI is supplied.',
        '每个独立合成单位一对完整测量；横轴(A+B)/2，纵轴B−A。偏倚为平均差，一致性界限为偏倚±1.96×样本SD（ddof=1），不是置信限。该正态差值假设下的描述性范围不证明一致性可接受；未处理重复测量或估计置信区间。'),
    'survival': (
        'Right-censored synthetic independent units, common time origin; event = 1, censoring = 0. S(t)=product(1−d/n) over event times; events precede censor removal at a tied time. Plus signs mark censoring at post-event survival. Risk counts are immediately before each displayed time (duration ≥ t). Curves stop at each group’s last observation. No CI, competing-risk estimate or log-rank test is supplied; interpretation requires non-informative censoring.',
        '合成独立单位采用同一时间原点、右删失；事件=1、删失=0。S(t)为事件时刻(1−d/n)的累积乘积；同刻先计事件再移除删失。加号标记删失时事件后的生存率。风险集为显示时刻前人数（时长≥t）；各组曲线止于本组末次观测。未给置信区间、竞争风险估计或log-rank检验；解释需非信息删失假设。'),
    'volcano': (
        'Each point is a supplied synthetic effect estimate and raw p-value, not a test computed from expression data. BH-adjusted p-values use all supplied hypotheses; y = −log10(adjusted p). Demonstration thresholds are adjusted p < 0.05 and |log2 fold change| ≥ 1. Color and marker identify direction; these thresholds are illustrative, not a default scientific decision.',
        '每点为给定合成效应量和原始p值，未从表达数据执行检验。BH校正使用全部给定假设；纵轴为−log10(校正p)。演示阈值为校正p<0.05且|log2倍数变化|≥1，以颜色和点形区分方向；该阈值仅示范，不是默认科学判定。'),
    'pca': (
        'Rows are independent synthetic units; all four features are centered and divided by their sample SD before SVD. Axis percentages are computed eigenvalue / total eigenvalue, with eigenvalues s²/(n−1). Group labels only color the unsupervised projection. No group-separation test, causal claim, ellipse or train/test generalization is implied.',
        '每行为一个独立合成单位；4个特征先中心化并除以各自样本SD，再SVD。坐标百分比由特征值/全部特征值计算，特征值为s²/(n−1)。组标签只用于无监督投影着色；不代表组间检验、因果、置信椭圆或训练测试泛化。'),
}
SOURCES = {
    'ranking': 'https://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html',
    'roc': 'https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html',
    'calibration': 'https://scikit-learn.org/stable/modules/calibration.html',
    'survival': 'https://www.statsmodels.org/stable/generated/statsmodels.duration.survfunc.SurvfuncRight.html',
    'fdr': 'https://www.statsmodels.org/stable/generated/statsmodels.stats.multitest.fdrcorrection.html',
    'pca': 'https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html',
}


def translate(pair, language):
    return pair[language == 'zh']


def clean_json(value):
    if isinstance(value, dict):
        return {key: clean_json(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, np.ndarray)):
        return [clean_json(item) for item in value]
    if isinstance(value, (bool, np.bool_)):
        return bool(value)
    if isinstance(value, (np.integer, int)):
        return int(value)
    if isinstance(value, (np.floating, float)):
        return float(value) if np.isfinite(value) else None
    return value


def _binary_arrays(labels, scores):
    y, p = np.asarray(labels), np.asarray(scores, dtype=float)
    if y.ndim != 1 or p.ndim != 1 or not len(y) or len(y) != len(p):
        raise ValueError('Labels and scores must be equal-length nonempty vectors.')
    if not np.all(np.isin(y, [0, 1])) or not np.all(np.isfinite(p)):
        raise ValueError('Labels must be 0/1 and all scores finite.')
    return y.astype(int), p


def binary_curves(labels, scores):
    """Tie-grouped binary threshold curves; AP is not trapezoidal PR area."""
    y, p = _binary_arrays(labels, scores)
    positives, negatives = int(y.sum()), int((1-y).sum())
    if not positives or not negatives:
        raise ValueError('Both positive and negative classes are required for these examples.')
    order = np.argsort(-p, kind='stable')
    ys, ps = y[order], p[order]
    last = np.r_[np.flatnonzero(np.diff(ps) != 0), len(ps)-1]
    tp = np.r_[0, np.cumsum(ys)[last]]
    fp = np.r_[0, last+1-np.cumsum(ys)[last]]
    recall, fpr = tp/positives, fp/negatives
    precision = np.r_[1., tp[1:]/(tp[1:]+fp[1:])]
    auc = np.sum(np.diff(fpr)*(recall[:-1]+recall[1:])/2)
    ap = np.sum(np.diff(recall)*precision[1:])
    pr_area = np.sum(np.diff(recall)*(precision[:-1]+precision[1:])/2)
    return clean_json(dict(n=len(y), positives=positives, negatives=negatives,
                           prevalence=positives/len(y), thresholds=[None, *ps[last]],
                           fpr=fpr, tpr=recall, recall=recall, precision=precision,
                           roc_auc=auc, average_precision=ap, trapezoidal_pr_auc=pr_area))


def calibration_bins(labels, probabilities, edges=None):
    y, p = _binary_arrays(labels, probabilities)
    if np.any((p < 0) | (p > 1)):
        raise ValueError('Calibration needs probabilities in [0,1], not arbitrary scores.')
    boundaries = np.asarray(edges if edges is not None else np.linspace(0, 1, 6), dtype=float)
    if boundaries.ndim != 1 or len(boundaries) < 2 or boundaries[0] != 0 or boundaries[-1] != 1 or np.any(np.diff(boundaries) <= 0):
        raise ValueError('Calibration edges must increase strictly from 0 to 1.')
    membership = np.minimum(np.searchsorted(boundaries, p, side='right')-1, len(boundaries)-2)
    rows, weighted_gap = [], 0.
    for i, (low, high) in enumerate(zip(boundaries[:-1], boundaries[1:])):
        selected = membership == i
        n = int(selected.sum())
        mean = float(p[selected].mean()) if n else None
        observed = float(y[selected].mean()) if n else None
        rows.append(dict(low=low, high=high, n=n, mean_probability=mean, observed_fraction=observed))
        if n:
            weighted_gap += n*abs(mean-observed)
    return clean_json(dict(n=len(y), edges=boundaries, bins=rows, ece=weighted_gap/len(y),
                           brier_score=np.mean((p-y)**2)))


def confusion_summary(labels, scores, threshold=.5):
    y, p = _binary_arrays(labels, scores)
    matrix = np.zeros((2, 2), dtype=int)
    np.add.at(matrix, (y, (p >= threshold).astype(int)), 1)
    denominator = matrix.sum(axis=1)
    fractions = np.divide(matrix, denominator[:, None],
                          out=np.full((2, 2), np.nan), where=denominator[:, None] > 0)
    return clean_json(dict(counts=matrix, row_fraction=fractions, true_class_n=denominator,
                           threshold=threshold, positive_class=1, equality='positive'))


def agreement_summary(method_a, method_b):
    a, b = np.asarray(method_a, dtype=float), np.asarray(method_b, dtype=float)
    if a.ndim != 1 or b.shape != a.shape or len(a) < 2 or not np.isfinite(a).all() or not np.isfinite(b).all():
        raise ValueError('Agreement needs at least two finite complete independent pairs.')
    difference = b-a
    bias, sd = difference.mean(), difference.std(ddof=1)
    return clean_json(dict(n=len(a), pair_mean=(a+b)/2, difference=difference,
                           bias=bias, sample_sd=sd, loa_low=bias-1.96*sd, loa_high=bias+1.96*sd))


def kaplan_meier(durations, events, risk_times=None):
    """Right censoring only; no delayed entry, weights or competing events."""
    time, event = np.asarray(durations, dtype=float), np.asarray(events)
    if time.ndim != 1 or event.shape != time.shape or not len(time) or not np.isfinite(time).all() or np.any(time < 0) or not np.isin(event, [0, 1]).all():
        raise ValueError('KM needs finite nonnegative durations and one 0/1 event code per unit.')
    survival, rows, censor_times, censor_survival = 1., [], [], []
    for t in np.unique(time):
        at_risk = int(np.count_nonzero(time >= t))
        failures = int(np.count_nonzero((time == t) & (event == 1)))
        censored = int(np.count_nonzero((time == t) & (event == 0)))
        survival *= 1-failures/at_risk
        rows.append(dict(time=t, at_risk=at_risk, events=failures, censored=censored, survival=survival))
        censor_times.extend([t]*censored)
        censor_survival.extend([survival]*censored)
    grid = np.asarray(risk_times if risk_times is not None else [0, 4, 8, 12], dtype=float)
    return clean_json(dict(n=len(time), event_count=int(np.sum(event)),
                           censor_count=int(np.sum(1-event)), table=rows,
                           step_time=[0., *[r['time'] for r in rows]],
                           step_survival=[1., *[r['survival'] for r in rows]],
                           censor_times=censor_times, censor_survival=censor_survival,
                           risk_times=grid, n_at_risk=[np.count_nonzero(time >= t) for t in grid]))


def benjamini_hochberg(pvalues):
    p = np.asarray(pvalues, dtype=float)
    if p.ndim != 1 or not len(p) or not np.isfinite(p).all() or np.any((p < 0) | (p > 1)):
        raise ValueError('BH requires a nonempty vector of finite p-values in [0,1].')
    order = np.argsort(p, kind='stable')
    adjusted_sorted = np.minimum.accumulate((p[order]*len(p)/np.arange(1, len(p)+1))[::-1])[::-1]
    adjusted = np.empty_like(adjusted_sorted)
    adjusted[order] = np.minimum(adjusted_sorted, 1)
    return adjusted


def pca_summary(features):
    x = np.asarray(features, dtype=float)
    if x.ndim != 2 or min(x.shape) < 2 or not np.isfinite(x).all():
        raise ValueError('PCA requires a finite matrix with at least two rows and features.')
    means, scales = x.mean(axis=0), x.std(axis=0, ddof=1)
    if np.any(scales == 0):
        raise ValueError('Remove or justify constant features before this standardized PCA.')
    z = (x-means)/scales
    _, singular, components = np.linalg.svd(z, full_matrices=False)
    # Fix the otherwise arbitrary sign of each component for reproducible figures.
    sign = np.sign(components[np.arange(len(components)), np.abs(components).argmax(axis=1)])
    components *= sign[:, None]
    scores = z @ components.T
    variance = singular**2/(len(x)-1)
    return clean_json(dict(n=len(x), features=x.shape[1], mean=means, sample_sd=scales,
                           components=components, scores=scores, singular_values=singular,
                           explained_variance=variance, explained_variance_ratio=variance/variance.sum()))


def fixture_data():
    rng = np.random.default_rng(20261025)
    rain = {'A': np.round(rng.normal(5.0, .65, 40), 3),
            'B': np.r_[np.round(rng.normal(6.0, .80, 43), 3), 8.8]}
    latent = np.linspace(.015, .985, 100)
    labels = (rng.random(100) < latent).astype(int)
    probabilities = np.round(np.clip(.05+.9*latent+rng.normal(0, .12, 100), 0, 1), 2)
    method_a = np.round(rng.uniform(10, 30, 36), 3)
    method_b = np.round(method_a+.35+rng.normal(0, .65, 36), 3)
    effect = np.r_[rng.normal(0, .65, 64), rng.normal(-1.7, .25, 8), rng.normal(1.7, .25, 8)]
    pvalues = np.r_[rng.uniform(.04, 1, 64), 10**rng.uniform(-5, -2.7, 16)]
    latent_features = rng.normal(0, 1, (36, 2))
    group = np.repeat(['A', 'B', 'C'], 12)
    latent_features[:, 0] += np.repeat([-.9, .1, .8], 12)
    loadings = np.array([[1, .8, -.3, .5], [.1, -.2, 1., .7]])
    features = latent_features@loadings + rng.normal(0, .35, (36, 4))
    return clean_json(dict(
        synthetic=True, seed=20261025,
        sampling='Each example has its own synthetic units; panels are not a shared study.',
        raincloud=rain,
        classification=dict(labels=labels, probability=probabilities, positive_class=1,
                            threshold=.5, unit='independent synthetic case'),
        bland_altman=dict(method_a=method_a, method_b=method_b, unit='a.u.',
                          pairing='one complete A/B pair per independent synthetic unit'),
        survival=dict(unit='month', time_origin='enrolment; no delayed entry', risk_times=[0, 4, 8, 12], groups={
            'A': dict(duration=[2,3,3,4,5,7,8,8,9,10,12,12], event=[1,0,1,1,0,1,0,1,1,0,1,0]),
            'B': dict(duration=[3,4,5,6,6,8,10,11,11,12,13,14], event=[1,0,1,0,1,1,0,1,0,0,1,0])}),
        volcano=dict(ids=[f'F{i+1:02}' for i in range(80)], log2_fold_change=effect, pvalues=pvalues,
                     provenance='supplied synthetic effect estimates and p-values; no expression-data test',
                     adjusted_p_threshold=.05, absolute_log2_effect_threshold=1.),
        pca=dict(ids=[f'U{i+1:02}' for i in range(36)], groups=group,
                 feature_names=['Feature 1','Feature 2','Feature 3','Feature 4'], values=features,
                 preprocessing='pooled descriptive PCA: center each feature and divide by sample SD')))


def summarize(data):
    classification = data['classification']
    pca = pca_summary(data['pca']['values'])
    adjusted = benjamini_hochberg(data['volcano']['pvalues'])
    effect = np.asarray(data['volcano']['log2_fold_change'])
    selected = (adjusted < data['volcano']['adjusted_p_threshold']) & (np.abs(effect) >= data['volcano']['absolute_log2_effect_threshold'])
    rain = {}
    for name, values in data['raincloud'].items():
        x = np.asarray(values)
        q1, median, q3 = np.quantile(x, [.25, .5, .75], method='linear')
        inside = x[(x >= q1-1.5*(q3-q1)) & (x <= q3+1.5*(q3-q1))]
        rain[name] = dict(n=len(x), q1=q1, median=median, q3=q3,
                          whisker_low=inside.min(), whisker_high=inside.max())
    return clean_json(dict(raincloud=rain,
        ranking=binary_curves(classification['labels'], classification['probability']),
        calibration=calibration_bins(classification['labels'], classification['probability']),
        confusion=confusion_summary(classification['labels'], classification['probability'], classification['threshold']),
        bland_altman=agreement_summary(data['bland_altman']['method_a'], data['bland_altman']['method_b']),
        survival={name: kaplan_meier(row['duration'], row['event'], data['survival']['risk_times'])
                  for name, row in data['survival']['groups'].items()},
        volcano=dict(adjusted_p=adjusted, selected=selected, selected_down=int(np.sum(selected & (effect < 0))),
                     selected_up=int(np.sum(selected & (effect > 0))), hypotheses=len(effect)), pca=pca))


def configure(language='en', mode='color'):
    if language not in ('en', 'zh'):
        raise ValueError('language must be en or zh')
    configure_typography(DPI, mode=mode)
    if language == 'zh':
        installed = {font.name for font in font_manager.fontManager.ttflist}
        for name in ('Noto Sans CJK SC', 'PingFang SC', 'Arial Unicode MS', 'Microsoft YaHei', 'Heiti SC'):
            if name in installed:
                plt.rcParams['font.sans-serif'] = [name, 'DejaVu Sans']
                break
        else:
            raise ValueError('Chinese figures need an installed CJK font; use --language en otherwise.')


def _sequential(style):
    return LinearSegmentedColormap.from_list('scientific_sequential', ['#F4F6F6', style['primary']])


def _ink_on_color(rgba, text):
    def luminance(rgb):
        x = np.asarray(rgb[:3])
        z = np.where(x <= .04045, x/12.92, ((x+.055)/1.055)**2.4)
        return float(z@np.array([.2126,.7152,.0722]))
    background, foreground = luminance(rgba), luminance(to_rgb(text))
    return 'white' if 1.05/(background+.05) > (background+.05)/(foreground+.05) else text


def draw(kind, ax, data, stats, language='en', compact=False, mode='color'):
    if kind not in KINDS:
        raise ValueError(f'Unknown chart kind: {kind}')
    t = lambda en, zh: zh if language == 'zh' else en
    style = get_style(mode)
    colors = style['palette']
    markers = style['markers']
    style_axes(ax)
    ax.set_facecolor('white')
    ax.set_title(translate(TITLES[kind], language), loc='left', fontsize=7, pad=7)
    if kind == 'raincloud':
        for i, (name, values) in enumerate(data[kind].items()):
            color = colors[i % len(colors)]
            violin = ax.violinplot([values], positions=[i], widths=.64, showextrema=False, bw_method='scott')
            body = violin['bodies'][0]
            body.get_paths()[0].vertices[:, 0] = np.minimum(body.get_paths()[0].vertices[:, 0], i)
            body.set_facecolor(color); body.set_edgecolor(color); body.set_alpha(.24)
            ax.boxplot([values], positions=[i+.055], widths=.09, showfliers=False,
                       boxprops=dict(color=color, linewidth=.7), medianprops=dict(color=style['text'], linewidth=.7),
                       whiskerprops=dict(color=color, linewidth=.6), capprops=dict(color=color, linewidth=.6))
            jitter = np.random.default_rng(17+i).uniform(.17, .35, len(values))
            ax.scatter(i+jitter, values, s=7, marker=markers[i], color=color,
                       alpha=.7, edgecolors='none', zorder=3)
        ax.set_xticks(range(2), [f'{name}\nn={len(values)}' for name, values in data[kind].items()])
        ax.set_xlim(-.48, 1.55)
        ax.set_ylabel(t('Measurement (a.u.)', '测量值（a.u.）'))
    elif kind in ('roc', 'pr'):
        row = stats['ranking']
        if kind == 'roc':
            ax.plot([0,1],[0,1], color=style['neutral'], linestyle=':', linewidth=.7)
            ax.plot(row['fpr'], row['tpr'], color=colors[0], linewidth=1.1,
                    label=f'ROC AUC = {row["roc_auc"]:.3f}')
            ax.set_xlabel(t('False-positive rate', '假阳性率')); ax.set_ylabel(t('True-positive rate', '真阳性率'))
        else:
            ax.axhline(row['prevalence'], color=style['neutral'], linestyle=':', linewidth=.7,
                       label=t('Prevalence', '正类比例'))
            ax.step(row['recall'], row['precision'], where='pre', color=colors[0], linewidth=1.1,
                    label=f'AP = {row["average_precision"]:.3f}')
            ax.set_xlabel(t('Recall', '召回率')); ax.set_ylabel(t('Precision', '精确率'))
        ax.set_xlim(-.025,1.025); ax.set_ylim(-.025,1.025)
        ax.set_xticks([0,.5,1]); ax.set_yticks([0,.5,1])
        ax.legend(loc='lower right' if kind == 'roc' else 'lower left', frameon=False, fontsize=6.5)
        if not compact:
            ax.text(.97,.97,f'n={row["n"]}; positive={row["positives"]}',transform=ax.transAxes,
                    ha='right',va='top',fontsize=6)
    elif kind == 'calibration':
        rows = stats[kind]['bins']
        ax.plot([0,1],[0,1],color=style['neutral'],linestyle=':',linewidth=.7)
        for row in rows:
            if row['n']:
                ax.scatter(row['mean_probability'],row['observed_fraction'],s=16,color=colors[0],marker=markers[0],zorder=3)
                if not compact:
                    ax.annotate(f'n={row["n"]}', (row['mean_probability'],row['observed_fraction']),
                                xytext=(0,6),textcoords='offset points',ha='center',fontsize=6)
        # Individual bins remain separate; a connecting curve can imply unsupported interpolation.
        ax.set_xlim(-.025,1.025); ax.set_ylim(-.05,1.12)
        ax.set_xticks([0,.5,1]); ax.set_yticks([0,.5,1])
        ax.set_xlabel(t('Mean predicted probability', '平均预测概率'))
        ax.set_ylabel(t('Observed positive fraction', '实际阳性比例'))
        ax.text(.97,.05,f'ECE = {stats[kind]["ece"]:.3f}',transform=ax.transAxes,ha='right',fontsize=6.5)
    elif kind == 'confusion':
        row = stats[kind]
        fractions = np.asarray(row['row_fraction'],dtype=float)
        cmap = _sequential(style).with_extremes(bad=style['neutral'])
        image = ax.pcolormesh(np.arange(3),np.arange(3),np.ma.masked_invalid(fractions),
                              cmap=cmap,vmin=0,vmax=1,edgecolors='white',linewidth=.4,rasterized=False)
        for (i,j), value in np.ndenumerate(fractions):
            label = f'{row["counts"][i][j]}\n'+('NA' if not np.isfinite(value) else f'{value:.0%}')
            background = to_rgb(style['neutral']) if not np.isfinite(value) else cmap(value)
            ink = _ink_on_color(background, '#000000' if mode == 'color' else style['text'])
            ax.text(j+.5,i+.5,label,ha='center',va='center',color=ink,fontsize=7)
        ax.set_xlim(0,2); ax.set_ylim(2,0)
        ax.set_xticks([.5,1.5], ['0','1']); ax.set_yticks([.5,1.5], ['0','1'])
        ax.tick_params(length=0)
        ax.set_xlabel(t('Predicted class', '预测类别')); ax.set_ylabel(t('True class', '真实类别'))
        for edge in ax.spines.values(): edge.set_visible(False)
        bar=ax.figure.colorbar(image,ax=ax,fraction=.045,pad=.05,ticks=[0,.5,1])
        bar.outline.set_visible(False); bar.set_label(t('Row fraction', '行比例'),fontsize=6.5)
        bar.solids.set_rasterized(False); bar.solids.set_edgecolor('face')
        bar.ax.tick_params(labelsize=6.5,width=.5,length=2)
    elif kind == 'bland_altman':
        row=stats[kind]
        ax.scatter(row['pair_mean'],row['difference'],s=11,color=colors[0],alpha=.75,edgecolors='none')
        labels=[('loa_high',t('Upper LoA', '上界')),('bias',t('Bias', '偏倚')),('loa_low',t('Lower LoA', '下界'))]
        for key,label in labels:
            ax.axhline(row[key],color=colors[1] if key=='bias' else style['neutral'],
                       linestyle='-' if key=='bias' else '--',linewidth=.8)
            if not compact:
                ax.text(.98,row[key],f'{label} {row[key]:+.2f}',transform=ax.get_yaxis_transform(),
                        ha='right',va='bottom',fontsize=6,bbox=dict(facecolor='white',edgecolor='none',pad=.6))
        span=max(row['loa_high']-row['loa_low'],.1)
        ax.set_ylim(min(min(row['difference']),row['loa_low'])-.17*span,
                    max(max(row['difference']),row['loa_high'])+.22*span)
        ax.set_xlabel(t('Mean of A and B (a.u.)', 'A与B均值（a.u.）'))
        ax.set_ylabel(t('B − A (a.u.)', 'B − A（a.u.）'))
    elif kind == 'survival':
        risk=[]
        for i,(name,row) in enumerate(stats[kind].items()):
            ax.step(row['step_time'],row['step_survival'],where='post',color=colors[i],
                    linestyle=style['linestyles'][i],linewidth=1.1,label=f'{name} (n={row["n"]})')
            ax.scatter(row['censor_times'],row['censor_survival'],marker='+',s=20,color=colors[i],linewidth=.7)
            risk.append(row['n_at_risk'])
        ax.set_ylim(-.025,1.06); ax.set_xlim(0,max(max(v['step_time']) for v in stats[kind].values())+.3)
        ax.set_xticks([0,4,8,12]); ax.set_yticks([0,.5,1])
        ax.set_xlabel(t('Time (months)', '时间（月）')); ax.set_ylabel(t('Survival probability', '生存概率'))
        ax.legend(frameon=False,fontsize=6.5,loc='lower left')
        if not compact:
            ax.text(0,-.23,t('Numbers at risk just before time', '各时刻前的风险集人数'),
                    transform=ax.transAxes,fontsize=6,ha='left')
            # Data-x / axes-y transform aligns counts with the actual time ticks.
            for i,(name,counts) in enumerate(zip(stats[kind],risk)):
                y=-.39-i*.12
                ax.text(-.05,y,name,transform=ax.transAxes,ha='right',va='center',fontsize=6)
                for time,count in zip(data[kind]['risk_times'],counts):
                    text=ax.text(time,y,str(count),transform=ax.get_xaxis_transform(),
                                 ha='center',va='center',fontsize=6)
                    text.set_gid(f'km-risk-{name}-{time}')
    elif kind == 'volcano':
        row,raw=stats[kind],data[kind]
        effect=np.asarray(raw['log2_fold_change']); adjusted=np.asarray(row['adjusted_p'])
        if np.any(adjusted <= 0):
            raise ValueError('This log-scale example requires strictly positive adjusted p-values.')
        y=-np.log10(adjusted); selected=np.asarray(row['selected'])
        for mask,color,marker,label in [
            (~selected,style['neutral'],'o',t('Below criteria', '未达演示标准')),
            (selected&(effect<0),colors[0],'v',t('Negative effect', '负向效应')),
            (selected&(effect>0),colors[1],'^',t('Positive effect', '正向效应'))]:
            ax.scatter(effect[mask],y[mask],s=12,color=color,marker=marker,alpha=.8,edgecolors='none',label=label)
        for x in [-raw['absolute_log2_effect_threshold'],raw['absolute_log2_effect_threshold']]:
            ax.axvline(x,color=style['neutral'],linestyle=':',linewidth=.6)
        ax.axhline(-np.log10(raw['adjusted_p_threshold']),color=style['neutral'],linestyle=':',linewidth=.6)
        ax.set_ylim(bottom=-.1)
        ax.set_xlabel(t('log2 fold change', 'log2倍数变化'))
        ax.set_ylabel(t('−log10(BH-adjusted p)', '−log10（BH校正p）'))
        if not compact: ax.legend(frameon=False,fontsize=6,loc='upper center')
    elif kind == 'pca':
        scores=np.asarray(stats[kind]['scores']); labels=np.asarray(data[kind]['groups'])
        for i,name in enumerate(dict.fromkeys(labels)):
            mask=labels==name
            ax.scatter(scores[mask,0],scores[mask,1],s=13,color=colors[i],marker=markers[i],
                       edgecolors='white',linewidth=.2,alpha=.85,label=f'{name} (n={mask.sum()})')
        ratios=stats[kind]['explained_variance_ratio']
        ax.axhline(0,color=style['neutral'],linestyle=':',linewidth=.5,zorder=0)
        ax.axvline(0,color=style['neutral'],linestyle=':',linewidth=.5,zorder=0)
        ax.set_xlabel(f'PC1 ({ratios[0]:.1%})'); ax.set_ylabel(f'PC2 ({ratios[1]:.1%})')
        ax.legend(frameon=False,fontsize=6,loc='upper left',bbox_to_anchor=(1.02,1),borderaxespad=0)
    return ax


def data_table(kind, data, stats):
    if kind == 'raincloud':
        headers=['Group','n','Q1','Median','Q3','Lower whisker','Upper whisker']
        rows=[[name,*[r[k] for k in ('n','q1','median','q3','whisker_low','whisker_high')]] for name,r in stats[kind].items()]
    elif kind in ('roc','pr'):
        row=stats['ranking']
        headers=['n','Positive','Prevalence','ROC AUC','AP (step)','PR area (trapezoid)']
        rows=[[row[k] for k in ('n','positives','prevalence','roc_auc','average_precision','trapezoidal_pr_auc')]]
    elif kind=='calibration':
        headers=['Low','High','n','Mean probability','Observed positive fraction']
        rows=[[r[k] for k in ('low','high','n','mean_probability','observed_fraction')] for r in stats[kind]['bins']]
    elif kind=='confusion':
        headers=['True class','Predicted 0: count','Predicted 1: count','True-class n']
        rows=[[i,*stats[kind]['counts'][i],stats[kind]['true_class_n'][i]] for i in range(2)]
    elif kind=='bland_altman':
        headers=['n','Mean difference','Sample SD','Lower LoA','Upper LoA']
        rows=[[stats[kind][k] for k in ('n','bias','sample_sd','loa_low','loa_high')]]
    elif kind=='survival':
        headers=['Group','n','Events','Censored',*[f'At risk before {x}' for x in data[kind]['risk_times']]]
        rows=[[name,r['n'],r['event_count'],r['censor_count'],*r['n_at_risk']] for name,r in stats[kind].items()]
    elif kind=='volcano':
        headers=['Hypotheses','Selected negative','Selected positive','Adjusted p threshold','Absolute log2 effect threshold']
        rows=[[stats[kind]['hypotheses'],stats[kind]['selected_down'],stats[kind]['selected_up'],
               data[kind]['adjusted_p_threshold'],data[kind]['absolute_log2_effect_threshold']]]
    else:
        headers=['Component','Eigenvalue','Explained variance ratio']
        rows=[[i+1,v,r] for i,(v,r) in enumerate(zip(stats[kind]['explained_variance'],stats[kind]['explained_variance_ratio']))]
    fmt=lambda value:'NA' if value is None else f'{value:.4f}' if isinstance(value,float) else str(value)
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |',
                      *['| '+' | '.join(map(fmt,row))+' |' for row in rows]])


def validate_figure(fig):
    """Check the final canvas, including colorbars, risk rows and outside legends."""
    fig.canvas.draw()
    renderer=fig.canvas.get_renderer()
    canvas=fig.bbox
    axes_bounds=[]
    for i,ax in enumerate(fig.axes):
        bounds=ax.get_tightbbox(renderer)
        if bounds is not None:
            axes_bounds.append(bounds)
            if bounds.x0 < canvas.x0-1 or bounds.y0 < canvas.y0-1 or bounds.x1 > canvas.x1+1 or bounds.y1 > canvas.y1+1:
                raise ValueError(f'Axes {i}, including labels and extra artists, leaves final canvas: {bounds.bounds}')
    for text in fig.texts:
        if not text.get_visible() or not text.get_text():
            continue
        bounds=text.get_window_extent(renderer)
        if bounds.x0 < canvas.x0-1 or bounds.y0 < canvas.y0-1 or bounds.x1 > canvas.x1+1 or bounds.y1 > canvas.y1+1:
            raise ValueError(f'Figure text leaves final canvas: {text.get_text()}')
        if any(bounds.overlaps(other) for other in axes_bounds):
            raise ValueError(f'Figure title or note overlaps plot decorations: {text.get_text()}')


def generate(output_dir, language='en', mode='color'):
    configure(language, mode)
    style=get_style(mode)
    output_dir=Path(output_dir); figures=output_dir/'figures'; figures.mkdir(parents=True,exist_ok=True)
    data=fixture_data(); stats=summarize(data)
    for filename,obj in [('data.json',data),('statistics.json',stats)]:
        (output_dir/filename).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    dimensions={}
    for kind in KINDS:
        width=180 if kind in ('survival','bland_altman','confusion','volcano') else 89
        height=112 if kind=='survival' else 87
        fig,ax=plt.subplots(figsize=(width*MM,height*MM),dpi=150)
        right=.75 if kind=='pca' else .88 if kind=='confusion' else .95
        fig.subplots_adjust(left=.18,right=right,top=.90,bottom=.38 if kind=='survival' else .22)
        draw(kind,ax,data,stats,language,mode=mode)
        ax.set_title('')
        fig.text(.18,.035,'Synthetic data · demonstration only' if language=='en' else '合成数据 · 仅用于演示',
                 fontsize=6,color=style['muted'])
        layout_figure_header(fig,ax,translate(TITLES[kind],language),
                             title_size=7,plot_axes=fig.axes)
        validate_figure(fig)
        dimensions[kind]={'width':fig.get_figwidth()*25.4,'height':fig.get_figheight()*25.4}
        for suffix in ('svg','png','pdf'):
            fig.savefig(figures/f'{kind}.{suffix}',dpi=DPI,facecolor='white')
        plt.close(fig)
    fig,axes=plt.subplots(3,3,figsize=(285*MM,270*MM),dpi=160)
    fig.subplots_adjust(left=.075,right=.97,top=.92,bottom=.075,hspace=.70,wspace=.58)
    for letter,kind,ax in zip('abcdefghi',KINDS,axes.flat):
        if kind=='pca':
            position=ax.get_position()
            ax.set_position([position.x0,position.y0,position.width*.77,position.height])
        draw(kind,ax,data,stats,language,compact=True,mode=mode)
        ax.text(-.18,1.11,letter,transform=ax.transAxes,fontsize=8,fontweight='bold')
    fig.suptitle('Advanced scientific figures · synthetic data' if language=='en' else '进阶科研图表 · 全部为合成数据',
                 x=.075,ha='left',fontsize=10)
    fig.text(.075,.015,'Definitions, exact values, risk tables and limitations accompany the individual figures.' if language=='en'
             else '单图及配套表格包含计算定义、精确数值、风险集和解释边界。',fontsize=7,color=style['muted'])
    validate_figure(fig)
    fig.savefig(output_dir/'overview.png',dpi=160,facecolor='white');plt.close(fig)
    parts=['# Advanced scientific figure examples — synthetic data',
           'All values are synthetic demonstration fixtures. These examples are not an analysis pipeline for user data.',
           f'Visual mode: `{mode}`. Figure text language: `{language}`. Raw JSON retains unrounded numerical values.',
           '[Raw observations](data.json) · [Computed statistics](statistics.json)',
           '![Nine advanced synthetic scientific figure examples](overview.png)']
    for kind in KINDS:
        parts += [f'## {translate(TITLES[kind],language)}',f'![{translate(TITLES[kind],language)}](figures/{kind}.svg)',
                  translate(CAPTIONS[kind],language),data_table(kind,data,stats),
                  f'[PNG](figures/{kind}.png) · [SVG](figures/{kind}.svg) · [PDF](figures/{kind}.pdf)']
    parts += ['## Definition references',*[f'- [{key}]({url})' for key,url in SOURCES.items()]]
    (output_dir/'gallery.md').write_text('\n\n'.join(parts)+'\n',encoding='utf-8')
    manifest=dict(synthetic=True,seed=data['seed'],mode=mode,language=language,kinds=list(KINDS),
                  numpy=np.__version__,matplotlib=matplotlib.__version__,
                  font_family=plt.rcParams['font.sans-serif'],font_points=7,
                  figure_dimensions_mm=dimensions,layout_check='final rendered canvas including labels, risk rows, colorbars and legends',
                  formulas='See captions and source; no interval/significance inference beyond explicit synthetic examples.')
    (output_dir/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return data,stats


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',required=True)
    parser.add_argument('--mode',choices=['color','grayscale'],default='color')
    parser.add_argument('--language',choices=['en','zh'],default='en')
    args=parser.parse_args()
    generate(args.output_dir,args.language,args.mode)
    print(f'Wrote {len(KINDS)} synthetic examples in {args.mode} mode to {args.output_dir}')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
