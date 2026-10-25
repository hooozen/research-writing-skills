#!/usr/bin/env python3
"""Render one scientific chart from explicit JSON or an approved synthetic example.

Run --list to locate a chart without loading plotting dependencies. This small
adapter reuses the tested statistics and visual system in the gallery modules;
it is a reference renderer, not a substitute for a study's analysis protocol.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path
import sys

SKILL_ROOT = Path(__file__).resolve().parent.parent
CHART_IDS = ('boxplot', 'violin', 'scatter', 'line', 'histogram', 'ecdf', 'paired',
             'interval', 'heatmap', 'raincloud', 'roc', 'pr', 'calibration',
             'confusion', 'bland_altman', 'survival', 'volcano', 'pca', 'count_share')
ADVANCED = frozenset(('raincloud', 'roc', 'pr', 'calibration', 'confusion',
                       'bland_altman', 'survival', 'volcano', 'pca'))
DEFINITIONS = {
    'boxplot': 'Linear Q1/Q3 and median; observed whiskers within 1.5 IQR; every supplied point shown once.',
    'violin': 'Gaussian Scott-bandwidth KDE over observed range; equal maximum widths; median and all points.',
    'raincloud': 'Half Gaussian Scott-bandwidth KDE, box/median/1.5-IQR whiskers and all observations; equal density widths.',
    'scatter': 'One point per supplied x/y record; Pearson r is descriptive only; no fitted model or interval.',
    'line': 'Available observations per time; sample SD with ddof=1, not CI. Missing times remain gaps; n=1 has no SD.',
    'histogram': 'Pooled supplied values; count bins, left-closed/right-open except final bin. Exact edges are recorded.',
    'ecdf': 'Right-continuous empirical CDF; ties combined; each group uses its own observed n.',
    'paired': 'Only actual ID-matched pairs are connected; incomplete observed endpoints retained; no imputation or test.',
    'interval': 'Supplied estimates and bounds; no interval recomputation. Reference and interval meaning are supplied.',
    'heatmap': 'Supplied matrix on one explicit scale; null is missing, not zero; no normalization or clustering.',
    'roc': 'Labels 0/1, positive=1; score ties enter together. ROC AUC is trapezoidal threshold-curve area.',
    'pr': 'Positive=1; AP=sum(delta recall * attained precision), distinct from separately recorded trapezoidal PR area.',
    'calibration': 'Fixed supplied bins on [0,1]; actual bin means/frequencies/counts; empty bins remain absent. ECE is n-weighted absolute bin gap.',
    'confusion': 'True class on rows, predicted class on columns; score >= supplied threshold predicts 1; row fractions retain undefined rows.',
    'bland_altman': 'B-A against (A+B)/2; bias=mean difference; normal constant-spread descriptive limits=bias +/- 1.96 sample SD, not a CI.',
    'survival': 'Right-censored KM; same-time events before censor removal. Risk counts just before time use duration>=t; tails stop at last observation.',
    'volcano': 'Supplied effects/raw p-values; BH adjustment across supplied family. y=-log10(adjusted p); highlighting uses supplied criteria.',
    'pca': 'Explicit standardization: center and divide by sample SD; SVD eigenvalues=s^2/(n-1), percentages from all eigenvalues.',
    'count_share': 'Supplied nonnegative integer counts and denominator; relationship explicit; null or zero denominator has no defined share.',
}


def chart_catalog() -> dict:
    """Read the machine-readable routing table using only the standard library."""
    path = SKILL_ROOT / 'references/chart-index.json'
    catalog = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(catalog, dict) or not isinstance(catalog.get('charts'), list):
        raise ValueError('chart-index.json must contain a charts list.')
    return catalog


def _required(data, key):
    if key not in data:
        raise ValueError(f'Missing required field: {key}')
    return data[key]


def _number(value, name, *, nonnegative=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f'{name} must be a finite number.')
    if nonnegative and value < 0:
        raise ValueError(f'{name} must be nonnegative.')
    return value


def _vector(value, name, *, minimum=1, nullable=False):
    if not isinstance(value, list) or len(value) < minimum:
        raise ValueError(f'{name} must be a list with at least {minimum} values.')
    for x in value:
        if x is None and nullable:
            continue
        _number(x, name)
    return value


def _label(data, key):
    value = _required(data, key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{key} must be a nonempty label with its relevant unit.')
    return value


def _names(value, length, name):
    if not isinstance(value, list) or len(value) != length or any(not isinstance(v, str) or not v.strip() for v in value):
        raise ValueError(f'{name} must contain {length} nonempty strings.')
    if len(set(value)) != length:
        raise ValueError(f'{name} must be unique.')
    return value


def _groups(data, *, density=False):
    groups = _required(data, 'groups')
    if not isinstance(groups, dict) or not 1 <= len(groups) <= 3:
        raise ValueError('groups must map one to three named groups to raw observations; facet more groups explicitly.')
    for name, values in groups.items():
        if not isinstance(name, str) or not name.strip():
            raise ValueError('Group names must be nonempty strings.')
        _vector(values, f'groups.{name}', minimum=2 if density else 1)
        if density and len(set(values)) < 2:
            raise ValueError(f'{name}: density requires variation; use points/box/ECDF for constant observations.')
    _label(data, 'value_label')
    return groups


def _stats_groups(groups, np):
    summaries, ecdfs = {}, {}
    for name, values in groups.items():
        x = np.asarray(values, dtype=float)
        q1, median, q3 = np.quantile(x, [.25, .5, .75], method='linear')
        inside = x[(x >= q1-1.5*(q3-q1)) & (x <= q3+1.5*(q3-q1))]
        summaries[name] = dict(n=len(x), q1=q1, median=median, q3=q3,
                               mean=x.mean(), sd=x.std(ddof=1) if len(x)>1 else None,
                               whisker_low=inside.min(), whisker_high=inside.max())
        unique, counts = np.unique(x, return_counts=True)
        ecdfs[name] = dict(x=unique, cumulative=np.cumsum(counts)/len(x))
    return summaries, ecdfs


def prepare_chart(chart_id, data):
    """Validate one input contract and compute only that chart's summaries."""
    if chart_id not in CHART_IDS:
        raise ValueError(f'Unknown chart: {chart_id}')
    if not isinstance(data, dict):
        raise ValueError('Input must be a JSON object.')
    if 'synthetic' in data and not isinstance(data['synthetic'], bool):
        raise ValueError('synthetic must be true or false when supplied.')
    # JSON copying rejects nonportable values and keeps the source object intact.
    data = json.loads(json.dumps(data, allow_nan=False))
    import numpy as np
    import advanced_chart_gallery as advanced
    prepared = {'groups': {}}
    stats = {}
    if chart_id in {'boxplot','violin','histogram','ecdf','raincloud'}:
        groups = _groups(data, density=chart_id in {'violin','raincloud'})
        prepared['groups'] = groups
        summaries, ecdfs = _stats_groups(groups, np)
        if chart_id == 'raincloud':
            prepared['raincloud'] = groups; stats['raincloud'] = summaries
        elif chart_id == 'histogram':
            pooled = np.concatenate([np.asarray(x) for x in groups.values()])
            bins = data.get('bin_edges', 'auto')
            if bins != 'auto':
                _vector(bins, 'bin_edges', minimum=2)
                if np.any(np.diff(bins) <= 0) or min(pooled) < bins[0] or max(pooled) > bins[-1]:
                    raise ValueError('bin_edges must increase and contain every observation.')
            counts, edges = np.histogram(pooled, bins=bins)
            stats['histogram'] = dict(n=len(pooled), counts=counts, edges=edges, pooled_groups=list(groups))
        else:
            stats['groups'] = summaries
            if chart_id == 'ecdf': stats['ecdf'] = ecdfs
    elif chart_id == 'scatter':
        observations = _required(data, 'observations')
        if not isinstance(observations, list) or not observations:
            raise ValueError('observations must be a nonempty list of {x,y} records.')
        for row in observations:
            if not isinstance(row, dict): raise ValueError('Each observation must be an object with x and y.')
            _number(_required(row,'x'),'x'); _number(_required(row,'y'),'y')
        _label(data,'x_label'); _label(data,'y_label')
        x, y = np.array([r['x'] for r in observations]), np.array([r['y'] for r in observations])
        r = np.corrcoef(x,y)[0,1] if len(x)>1 and np.std(x)>0 and np.std(y)>0 else None
        prepared['scatter'] = [dict(snr_db=r['x'],error_um=r['y']) for r in observations]
        stats['scatter'] = dict(n=len(x),pearson_r=r)
    elif chart_id == 'line':
        times = _vector(_required(data,'times'),'times')
        if np.any(np.diff(times)<=0): raise ValueError('times must increase strictly, retaining actual time spacing.')
        subjects = _required(data,'subjects')
        if not isinstance(subjects,list) or not subjects: raise ValueError('subjects must contain ID-linked rows.')
        ids=[]
        for row in subjects:
            ids.append(_required(row,'id'))
            values=_vector(_required(row,'values'),'subject.values',nullable=True)
            if len(values)!=len(times): raise ValueError('Each subject values list must match times.')
        _names(ids,len(ids),'subject IDs'); _label(data,'time_label'); _label(data,'value_label')
        values=np.asarray([r['values'] for r in subjects],dtype=float)
        summaries=[]
        for t,column in zip(times,values.T):
            valid=column[np.isfinite(column)]
            summaries.append(dict(week=t,n=len(valid),mean=valid.mean() if len(valid) else None,
                                  sd=valid.std(ddof=1) if len(valid)>1 else None))
        if not np.isfinite(values).any(): raise ValueError('At least one time must have an observed value.')
        stats['line']=summaries
    elif chart_id == 'paired':
        pairs=_required(data,'pairs')
        if not isinstance(pairs,list) or not pairs: raise ValueError('pairs must be a nonempty ID-linked list.')
        ids=[]
        for row in pairs:
            ids.append(_required(row,'id'))
            for key in ['before','after']:
                value=_required(row,key)
                if value is not None: _number(value,key)
            if row['before'] is None and row['after'] is None: raise ValueError('A pair row must contain at least one observation.')
        _names(ids,len(ids),'pair IDs'); _label(data,'value_label')
        complete=[r for r in pairs if r['before'] is not None and r['after'] is not None]
        delta=np.asarray([r['after']-r['before'] for r in complete])
        prepared['paired']=pairs
        stats['paired']=dict(enrolled=len(pairs),complete=len(complete),incomplete=len(pairs)-len(complete),
                             baseline_n=sum(r['before'] is not None for r in pairs),
                             followup_n=sum(r['after'] is not None for r in pairs),
                             mean_change=delta.mean() if len(delta) else None)
    elif chart_id == 'interval':
        rows=_required(data,'estimates')
        if not isinstance(rows,list) or not rows: raise ValueError('estimates must contain supplied estimates and interval bounds.')
        for row in rows:
            _label(row,'label')
            m,lo,hi=[_number(_required(row,k),k) for k in ['estimate','low','high']]
            if not lo<=m<=hi: raise ValueError('Each supplied interval must contain its estimate.')
        _number(_required(data,'reference'),'reference'); _label(data,'value_label'); _label(data,'interval_label')
        stats['interval']=dict(estimates=rows,reference=data['reference'],interval_label=data['interval_label'])
    elif chart_id == 'heatmap':
        values=_required(data,'values')
        if not isinstance(values,list) or not values: raise ValueError('values must be a nonempty rectangular matrix.')
        width=len(_vector(values[0],'values row',nullable=True))
        for row in values:
            _vector(row,'values row',nullable=True)
            if len(row)!=width: raise ValueError('values must be rectangular.')
        _names(_required(data,'row_labels'),len(values),'row_labels')
        _names(_required(data,'column_labels'),width,'column_labels')
        bounds=_vector(_required(data,'limits'),'limits',minimum=2)
        if len(bounds)!=2 or bounds[0]>=bounds[1]: raise ValueError('limits must be [low,high] with low < high.')
        observed=[x for row in values for x in row if x is not None]
        if any(x<bounds[0] or x>bounds[1] for x in observed): raise ValueError('limits must include all observed cells; no silent color clipping.')
        _label(data,'value_label')
        prepared['heatmap']=dict(values=values,rows=data['row_labels'],columns=data['column_labels'],scale=bounds)
        stats['heatmap']=dict(shape=[len(values),width],missing=sum(x is None for row in values for x in row),limits=bounds)
    elif chart_id in {'roc','pr'}:
        stats['ranking']=advanced.binary_curves(_required(data,'labels'),_required(data,'scores'))
    elif chart_id == 'calibration':
        stats['calibration']=advanced.calibration_bins(_required(data,'labels'),_required(data,'probabilities'),_required(data,'bin_edges'))
    elif chart_id == 'confusion':
        threshold=_number(_required(data,'threshold'),'threshold')
        stats['confusion']=advanced.confusion_summary(_required(data,'labels'),_required(data,'scores'),threshold)
    elif chart_id == 'bland_altman':
        _label(data,'value_unit')
        stats['bland_altman']=advanced.agreement_summary(_required(data,'method_a'),_required(data,'method_b'))
    elif chart_id == 'survival':
        groups=_required(data,'groups')
        if not isinstance(groups,dict) or not 1<=len(groups)<=3: raise ValueError('survival groups must contain one to three named groups.')
        risk=_vector(_required(data,'risk_times'),'risk_times')
        if min(risk)<0 or np.any(np.diff(risk)<=0): raise ValueError('risk_times must be nonnegative and increase strictly.')
        _label(data,'time_unit')
        prepared['survival']=dict(groups=groups,risk_times=risk)
        stats['survival']={name:advanced.kaplan_meier(_required(row,'duration'),_required(row,'event'),risk) for name,row in groups.items()}
        if max(risk)>max(max(r['step_time']) for r in stats['survival'].values()):
            raise ValueError('risk_times must not imply follow-up beyond the last observation.')
    elif chart_id == 'volcano':
        effects=_vector(_required(data,'log2_fold_change'),'log2_fold_change')
        p=_vector(_required(data,'pvalues'),'pvalues')
        _names(_required(data,'ids'),len(effects),'ids')
        if len(p)!=len(effects) or min(p)<=0 or max(p)>1: raise ValueError('pvalues must be >0 and <=1 and match effects; supply a documented floor for underflow before plotting.')
        threshold=_number(_required(data,'adjusted_p_threshold'),'adjusted_p_threshold')
        effect_threshold=_number(_required(data,'absolute_log2_effect_threshold'),'absolute_log2_effect_threshold',nonnegative=True)
        if not 0<threshold<=1: raise ValueError('adjusted_p_threshold must be in (0,1].')
        adjusted=advanced.benjamini_hochberg(p)
        effects_array=np.asarray(effects)
        selected=(adjusted<threshold)&(np.abs(effects_array)>=effect_threshold)
        prepared['volcano']=data
        stats['volcano']=dict(adjusted_p=adjusted,selected=selected,hypotheses=len(effects),
                              selected_down=int(np.sum(selected&(effects_array<0))),
                              selected_up=int(np.sum(selected&(effects_array>0))))
    elif chart_id == 'pca':
        if _required(data,'preprocessing')!='standardize': raise ValueError('This reference supports explicit preprocessing="standardize"; adapt the analysis for other PCA protocols.')
        values=_required(data,'values'); row=advanced.pca_summary(values)
        labels=_required(data,'groups')
        if not isinstance(labels,list) or len(labels)!=row['n'] or any(not isinstance(x,str) or not x for x in labels) or not 1<=len(set(labels))<=3:
            raise ValueError('groups must supply one label per sample, using one to three group identities.')
        _names(_required(data,'feature_names'),row['features'],'feature_names')
        prepared['pca']=dict(groups=labels)
        stats['pca']=row
    elif chart_id == 'count_share':
        categories=_required(data,'categories');counts=_vector(_required(data,'counts'),'counts')
        _names(categories,len(counts),'categories'); _label(data,'unit')
        if any(isinstance(x,bool) or not isinstance(x,int) or x<0 for x in counts): raise ValueError('counts must be nonnegative integers.')
        denominator=_required(data,'denominator')
        if denominator is not None and (isinstance(denominator,bool) or not isinstance(denominator,int) or denominator<0): raise ValueError('denominator must be a nonnegative integer or null.')
        if denominator is not None and any(x>denominator for x in counts): raise ValueError('No category count may exceed its population denominator.')
        relationship=_required(data,'relationship')
        if relationship not in {'exclusive_exhaustive','overlapping','subset'}: raise ValueError('relationship must be exclusive_exhaustive, overlapping or subset.')
        if relationship=='exclusive_exhaustive' and denominator is not None and sum(counts)!=denominator: raise ValueError('Exclusive exhaustive counts must reconcile with denominator.')
        stats['count_share']=dict(categories=categories,counts=counts,denominator=denominator,
                                  relationship=relationship,shares=[x/denominator if denominator else None for x in counts])
    return prepared, advanced.clean_json(stats)


def _draw_groups(kind, ax, data, stats, style, np, language='en'):
    translate = lambda en, zh: zh if language == 'zh' else en
    import matplotlib.colors as colors
    groups=data['groups']; positions=list(range(1,len(groups)+1)); arrays=[np.asarray(x) for x in groups.values()]
    palette,markers=style['palette'],style['markers']
    if kind=='boxplot':
        boxes=ax.boxplot(arrays,positions=positions,widths=.4,patch_artist=True,showfliers=False,
                         medianprops={'color':style['text'],'linewidth':.7},
                         whiskerprops={'color':style['muted'],'linewidth':.6},capprops={'color':style['muted'],'linewidth':.6})
        for body,color in zip(boxes['boxes'],palette):
            body.set_facecolor(colors.to_rgba(color,.16));body.set_edgecolor(color)
    elif kind in {'violin','raincloud'}:
        for i,(position,values) in enumerate(zip(positions,arrays)):
            violins=ax.violinplot([values],positions=[position],widths=.75,showextrema=False,showmedians=kind=='violin',bw_method='scott')
            body=violins['bodies'][0]
            if kind=='raincloud':
                body.get_paths()[0].vertices[:,0]=np.minimum(body.get_paths()[0].vertices[:,0],position)
                ax.boxplot([values],positions=[position+.055],widths=.09,showfliers=False,
                           boxprops={'color':palette[i],'linewidth':.7},
                           whiskerprops={'color':palette[i],'linewidth':.6},
                           capprops={'color':palette[i],'linewidth':.6},
                           medianprops={'color':style['text'],'linewidth':.7})
            body.set_facecolor(palette[i]);body.set_edgecolor(palette[i]);body.set_alpha(.2)
            if kind=='violin':
                violins['cmedians'].set_color(style['text']);violins['cmedians'].set_linewidth(.7)
    if kind in {'boxplot','violin','raincloud'}:
        jitter=np.random.default_rng(19)
        for i,(position,values) in enumerate(zip(positions,arrays)):
            x=position+jitter.uniform(.17,.35,len(values)) if kind=='raincloud' else position+jitter.uniform(-.1,.1,len(values))
            ax.scatter(x,values,color=palette[i],marker=markers[i],s=7,alpha=.85,edgecolors='white',linewidths=.2,zorder=3)
        ax.set_xticks(positions,[f'{name}\nn={len(values)}' for name,values in groups.items()]);ax.set_xlim(.5,len(groups)+.55)
        ax.set_ylabel(data['value_label'])
    elif kind=='ecdf':
        lo=min(x.min() for x in arrays);hi=max(x.max() for x in arrays);margin=max((hi-lo)*.06,.1)
        for i,(name,row) in enumerate(stats['ecdf'].items()):
            ax.step([lo-margin,*row['x'],hi+margin],[0,*row['cumulative'],1],where='post',
                    color=palette[i],linestyle=style['linestyles'][i],label=f'{name} (n={len(groups[name])})')
        ax.set_xlim(lo-margin,hi+margin);ax.set_ylim(-.03,1.03);ax.set_xlabel(data['value_label']);ax.set_ylabel(translate('Cumulative proportion','累计比例'));ax.legend(loc='best')
    elif kind=='histogram':
        row=stats['histogram'];edges=np.asarray(row['edges'])
        ax.bar(edges[:-1],row['counts'],width=np.diff(edges),align='edge',color=palette[0],edgecolor='white',linewidth=.45)
        ax.set_xlabel(data['value_label']);ax.set_ylabel(translate('Count','频数'));ax.set_ylim(bottom=0)


def _draw_custom(kind, ax, data, stats, style, np, language='en'):
    translate = lambda en, zh: zh if language == 'zh' else en
    if kind=='paired':
        for row in data['pairs']:
            complete=row['before'] is not None and row['after'] is not None
            if complete: ax.plot([0,1],[row['before'],row['after']],color=style['neutral'],linewidth=.55,zorder=1)
            for i,key in enumerate(['before','after']):
                if row[key] is not None:
                    ax.scatter(i,row[key],s=11,marker=style['markers'][i],facecolors=style['palette'][i] if complete else 'none',
                               edgecolors=style['palette'][i],linewidths=.6,zorder=3)
        row=stats['paired'];ax.set_xticks([0,1],[translate('Before','前测')+f'\nn={row["baseline_n"]}',translate('After','后测')+f'\nn={row["followup_n"]}']);ax.set_xlim(-.35,1.35)
        ax.set_ylabel(data['value_label']);ax.margins(y=.18)
        ax.text(.98,.98,str(row['complete'])+' '+translate('complete pairs','对完整观测'),transform=ax.transAxes,ha='right',va='top',fontsize=6)
    elif kind=='scatter':
        row=stats['scatter']
        ax.scatter([r['x'] for r in data['observations']],[r['y'] for r in data['observations']],
                   color=style['primary'],s=9,alpha=.8,edgecolors='white',linewidths=.25)
        ax.set_xlabel(data['x_label']);ax.set_ylabel(data['y_label'])
        correlation=translate('undefined','未定义') if row['pearson_r'] is None else f'{row["pearson_r"]:.2f}'
        ax.text(.98,.97,f'n={row["n"]}\nr={correlation}',transform=ax.transAxes,
                ha='right',va='top',fontsize=6.5)
    elif kind=='interval':
        for i,row in enumerate(data['estimates']):
            ax.errorbar(row['estimate'],i,xerr=[[row['estimate']-row['low']],[row['high']-row['estimate']]],
                        fmt=style['markers'][0],color=style['primary'],capsize=2.5,linewidth=.8)
        ax.axvline(data['reference'],color=style['muted'],linestyle='--',linewidth=.6)
        ax.set_yticks(range(len(data['estimates'])),[r['label'] for r in data['estimates']]);ax.invert_yaxis()
        ax.set_xlabel(data['value_label'])
    elif kind=='count_share':
        from matplotlib_example import count_share_label
        row=stats['count_share'];counts=row['counts'];scale=max(max(counts),1)
        palette=[style['neutral'] if any(s in label.lower() for s in ['other','unknown','missing']) else style['palette'][i%3]
                 for i,label in enumerate(row['categories'])]
        bars=ax.barh(row['categories'],counts,height=.58,color=palette)
        if len(counts)>3: # Count lengths identify categories; retain neutral residual categories.
            for bar,label in zip(bars,row['categories']):
                bar.set_color(style['neutral'] if any(s in label.lower() for s in ['other','unknown','missing']) else style['primary'])
        if style['primary']=='#34383C':
            for i,bar in enumerate(bars):
                bar.set_hatch(style['hatches'][i%3]);bar.set_edgecolor(style['baseline']);bar.set_linewidth(.5)
        for bar,count in zip(bars,counts):
            ax.text(count+scale*.03,bar.get_y()+bar.get_height()/2,count_share_label(count,row['denominator']).replace('share unavailable',translate('share unavailable','占比不可用')),va='center',fontsize=7)
        ax.invert_yaxis();ax.set_xlim(0,scale*1.72);ax.tick_params(axis='y',length=0);ax.set_xlabel(translate('Count','计数')+f' ({data["unit"]})')


def render_chart(chart_id, data, output_dir, *, mode='color', language='en', formats=('svg','png')):
    """Render only the requested chart; no synthetic data are introduced here."""
    if mode not in {'color','grayscale'}: raise ValueError('mode must be color or grayscale.')
    if language not in {'en','zh'}: raise ValueError('language must be en or zh.')
    if isinstance(formats,str): formats=tuple(x.strip() for x in formats.split(','))
    formats=tuple(dict.fromkeys(formats))
    if not formats or any(x not in {'svg','png','pdf'} for x in formats): raise ValueError('formats must select svg, png and/or pdf.')
    prepared,stats=prepare_chart(chart_id,data)
    import numpy as np
    import matplotlib
    import matplotlib.pyplot as plt
    import scientific_chart_gallery as basic
    import advanced_chart_gallery as advanced
    from matplotlib_example import get_style,style_axes,layout_figure_header
    basic.configure(language,mode)
    style=get_style(mode)
    matplotlib.rcParams['svg.hashsalt']='scientific-chart-style-'+chart_id+'-'+mode
    width=180 if chart_id in {'survival','bland_altman','confusion','volcano','count_share'} else 89
    height=112 if chart_id=='survival' else max(80,8*len(data.get('categories',[]))+35) if chart_id=='count_share' else 87
    fig,ax=plt.subplots(figsize=(width/25.4,height/25.4),dpi=150)
    right=.75 if chart_id=='pca' else .83 if chart_id=='heatmap' else .88 if chart_id=='confusion' else .95
    left=.23 if chart_id in {'interval','count_share'} else .21
    fig.subplots_adjust(left=left,right=right,top=.84,bottom=.38 if chart_id=='survival' else .22)
    style_axes(ax,mode=mode)
    try:
        if chart_id in {'boxplot','violin','histogram','ecdf','raincloud'}:
            _draw_groups(chart_id,ax,data,stats,style,np,language)
        elif chart_id in {'paired','interval','count_share','scatter'}:
            _draw_custom(chart_id,ax,data,stats,style,np,language)
        elif chart_id in ADVANCED:
            advanced.draw(chart_id,ax,prepared,stats,language,mode=mode)
            if chart_id=='bland_altman':
                ax.set_xlabel(('Mean of A and B' if language=='en' else 'A与B均值')+f' ({data["value_unit"]})');ax.set_ylabel(f'B − A ({data["value_unit"]})')
            if chart_id=='survival':
                ax.set_xticks(data['risk_times']);ax.set_xlabel(('Time' if language=='en' else '时间')+f' ({data["time_unit"]})')
        else:
            basic.draw(chart_id,ax,prepared,stats,language,mode=mode)
            if chart_id=='scatter': ax.set_xlabel(data['x_label']);ax.set_ylabel(data['y_label'])
            elif chart_id=='line': ax.set_xlabel(data['time_label']);ax.set_ylabel(data['value_label'])
            elif chart_id=='heatmap':
                ax.set_xlabel(data.get('column_axis_label','Column' if language=='en' else '列'));ax.set_ylabel(data.get('row_axis_label','Row' if language=='en' else '行'))
                fig.axes[-1].set_ylabel(data['value_label'])
        ax.set_title('')
        titles=advanced.TITLES if chart_id in ADVANCED else basic.TITLES
        fallback=('Count and share' if language=='en' else '计数与占比') if chart_id=='count_share' else ('Heatmap' if language=='en' else '热图') if chart_id=='heatmap' else titles[chart_id][language=='zh']
        title=data.get('title',fallback)
        if not isinstance(title,str): raise ValueError('title must be a string.')
        note=('Synthetic data · demonstration only' if language=='en' else '合成数据 · 仅用于演示') if data.get('synthetic',False) else ('Supplied data · see data/statistics companions' if language=='en' else '给定数据 · 详见数据与统计伴随文件')
        fig.text(left,.035,note,fontsize=6,color=style['muted'])
        subtitle=data['interval_label'] if chart_id=='interval' else None
        if chart_id=='count_share':
            denominator=('unknown' if language=='en' else '未知') if data['denominator'] is None else str(data['denominator'])
            relationship=data['relationship'].replace('_',' ') if language=='en' else {'exclusive_exhaustive':'互斥且完整','overlapping':'可重叠','subset':'部分子集'}[data['relationship']]
            subtitle=('Denominator: ' if language=='en' else '分母：')+f'{denominator} {data["unit"]}; {relationship}'
        layout_figure_header(fig,ax,title,subtitle=subtitle,title_size=7,plot_axes=fig.axes)
        advanced.validate_figure(fig)
        output=Path(output_dir);output.mkdir(parents=True,exist_ok=True)
        artifacts={}
        for suffix in formats:
            path=output/f'{chart_id}.{suffix}'
            metadata={'Date':None} if suffix=='svg' else {'CreationDate':None,'ModDate':None} if suffix=='pdf' else None
            fig.savefig(path,dpi=300,facecolor='white',metadata=metadata)
            if suffix=='svg':
                path.write_text('\n'.join(line.rstrip() for line in path.read_text(encoding='utf-8').splitlines())+'\n',encoding='utf-8')
            artifacts[suffix]=str(path)
        source=json.loads(json.dumps(data,allow_nan=False))
        (output/'data.json').write_text(json.dumps(source,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
        (output/'statistics.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
        manifest=dict(chart=chart_id,synthetic=data.get('synthetic',False),mode=mode,language=language,
                      formats=list(formats),width_mm=fig.get_figwidth()*25.4,height_mm=fig.get_figheight()*25.4,
                      font_points=7,definition=DEFINITIONS[chart_id],
                      source_sha256=hashlib.sha256(json.dumps(source,sort_keys=True,ensure_ascii=False,allow_nan=False).encode()).hexdigest(),
                      numpy=np.__version__,matplotlib=matplotlib.__version__)
        (output/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        return {'chart':chart_id,'artifacts':artifacts,'metadata':manifest}
    finally:
        plt.close(fig)


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--list',action='store_true',help='Print the chart routing table without loading plotting libraries.')
    parser.add_argument('--chart',choices=CHART_IDS)
    group=parser.add_mutually_exclusive_group()
    group.add_argument('--input',type=Path,help='Explicit input JSON for this chart.')
    group.add_argument('--example',action='store_true',help='Use this chart\'s explicitly synthetic reference JSON.')
    parser.add_argument('--output-dir',type=Path)
    parser.add_argument('--mode',choices=['color','grayscale'],default='color')
    parser.add_argument('--language',choices=['en','zh'],default='en')
    parser.add_argument('--formats',default='svg,png')
    args=parser.parse_args(argv)
    try:
        if args.list:
            if args.chart or args.input or args.example or args.output_dir: parser.error('--list is a read-only routing request; do not combine it with rendering options.')
            print(json.dumps(chart_catalog(),ensure_ascii=False,indent=2));return 0
        if not args.chart or not args.output_dir: parser.error('Rendering requires --chart and --output-dir.')
        if not args.input and not args.example: parser.error('Provide --input JSON or explicitly choose --example; no data are fabricated by default.')
        if args.example:
            entries={row['id']:row for row in chart_catalog()['charts']}
            entry=entries[args.chart]
            relative=entry.get('input',f'references/examples/{args.chart}.json')
            path=(SKILL_ROOT/relative).resolve()
            if not path.is_relative_to(SKILL_ROOT): raise ValueError('Example input must remain inside the skill.')
        else: path=args.input
        data=json.loads(path.read_text(encoding='utf-8'))
        if args.example:
            if data.get('synthetic') is not True: raise ValueError('--example requires a clearly labeled synthetic fixture.')
        result=render_chart(args.chart,data,args.output_dir,mode=args.mode,language=args.language,formats=args.formats)
        print(json.dumps(result,ensure_ascii=False,indent=2));return 0
    except (ValueError,KeyError,OSError,json.JSONDecodeError) as error:
        parser.exit(2,f'error: {error}\n')


if __name__=='__main__':
    raise SystemExit(main())
