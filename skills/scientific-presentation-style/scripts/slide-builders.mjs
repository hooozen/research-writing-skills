// Optional Artifact Tool adapter. All geometry is in 96-DPI CSS pixels.
// Call these functions inside the active presentation session callback.
export const px = points => points * 4 / 3;
const FRAME = {left: 176, top: 188, width: 920, height: 350};
const finite = value => typeof value === 'number' && Number.isFinite(value);
const requireFinite = (values, name) => {
  if (!Array.isArray(values) || !values.length || !values.every(finite)) throw new Error(`${name} needs finite observations.`);
};

function bounds(values, includeZero = false) {
  requireFinite(values, 'axis values');
  let low = Math.min(...values), high = Math.max(...values);
  if (includeZero) { low = Math.min(0, low); high = Math.max(0, high); }
  const span = Math.max(high - low, Math.abs(high) * .2, 1);
  const step = 10 ** Math.floor(Math.log10(span / 4));
  return {min: includeZero && low === 0 ? 0 : Math.floor((low - span * .08) / step) * step,
    max: Math.ceil((high + span * .12) / step) * step};
}

export function palette(tokens, mode = 'color') {
  if (!['color', 'grayscale'].includes(mode)) throw new Error('Use color or grayscale.');
  return {...tokens.colors, ...(mode === 'grayscale' ? tokens.grayscale : {})};
}

export function configureScientificTheme(presentation, tokens) {
  const c = tokens.colors;
  presentation.theme.defaultFont = tokens.fonts.cjk_demo;
  presentation.theme.colorScheme = {name: 'Scientific high-contrast blue', themeColors: {
    accent1: c.primary, accent2: c.secondary, accent3: c.third,
    accent4: c.neutral, accent5: c.light, accent6: c.axis,
    bg1: c.background, bg2: c.background, tx1: c.text, tx2: c.muted,
    dk1: '#000000', dk2: c.axis, lt1: '#FFFFFF', lt2: '#F2F4F7',
    hlink: c.primary, folHlink: c.third,
  }};
}

function text(slide, value, position, tokens, options = {}) {
  const shape = slide.shapes.add({geometry: 'textbox', name: options.name || value.slice(0, 35),
    position, fill: 'none', line: {fill: 'none', width: 0}});
  shape.text = value;
  shape.text.style = {typeface: tokens.fonts.cjk_demo, fontSize: px(options.points || 20),
    color: options.color || tokens.colors.text, bold: options.bold || false,
    alignment: options.align || 'left', verticalAlignment: 'middle', insets: 0};
  return shape;
}

function line(slide, x1, y1, x2, y2, color, width = 1.5, style = 'solid') {
  const left = Math.min(x1, x2), top = Math.min(y1, y2);
  const w = Math.max(Math.abs(x2 - x1), 1), h = Math.max(Math.abs(y2 - y1), 1);
  return slide.shapes.add({geometry: 'custom', name: 'data-line',
    position: {left, top, width: w, height: h}, fill: 'none', line: {fill: color, width, style},
    customPaths: [{width: w, height: h, commands: [
      {moveTo: {x: x1 - left, y: y1 - top}}, {lineTo: {x: x2 - left, y: y2 - top}},
    ]}]});
}

function marker(slide, x, y, color, square = false, hollow = false, size = 11) {
  return slide.shapes.add({geometry: square ? 'rect' : 'ellipse', name: 'observation',
    position: {left: x - size / 2, top: y - size / 2, width: size, height: size},
    fill: hollow ? '#FFFFFF' : color, line: {fill: color, width: 1.4}});
}

function blend(a, b, weight) {
  const rgb = value => [1, 3, 5].map(i => parseInt(value.slice(i, i + 2), 16));
  return '#' + rgb(a).map((v, i) => Math.round(v * (1 - weight) + rgb(b)[i] * weight).toString(16).padStart(2, '0')).join('');
}

function ink(background) {
  const linear = [1, 3, 5].map(i => parseInt(background.slice(i, i + 2), 16) / 255)
    .map(v => v <= .04045 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4);
  const luminance = linear.reduce((sum, v, i) => sum + v * [.2126, .7152, .0722][i], 0);
  return 1.05 / (luminance + .05) > (luminance + .05) / .05 ? '#FFFFFF' : '#000000';
}

function axes(slide, tokens, colors, {xMin, xMax, yMin, yMax, xTicks, yTicks, xLabel, yLabel, frame = FRAME}) {
  const sx = x => frame.left + (x - xMin) / (xMax - xMin) * frame.width;
  const sy = y => frame.top + frame.height - (y - yMin) / (yMax - yMin) * frame.height;
  line(slide, frame.left, frame.top, frame.left, frame.top + frame.height, colors.axis, px(tokens.strokes_points.axis));
  line(slide, frame.left, frame.top + frame.height, frame.left + frame.width, frame.top + frame.height, colors.axis, px(tokens.strokes_points.axis));
  for (const v of yTicks || []) {
    line(slide, frame.left - 5, sy(v), frame.left, sy(v), colors.axis, 1.3);
    text(slide, String(v), {left: frame.left - 82, top: sy(v) - 17, width: 68, height: 34}, tokens,
      {points: 16.5, color: colors.muted, align: 'right', name: 'value-axis-tick'});
  }
  for (const tick of xTicks || []) {
    const value = typeof tick === 'object' ? tick.value : tick;
    const label = typeof tick === 'object' ? tick.label : String(tick);
    line(slide, sx(value), frame.top + frame.height, sx(value), frame.top + frame.height + 5, colors.axis, 1.3);
    text(slide, label, {left: sx(value) - 105, top: frame.top + frame.height + 12, width: 210, height: 44}, tokens,
      {points: 16.5, color: colors.muted, align: 'center', name: 'category-axis-tick'});
  }
  if (xLabel) text(slide, xLabel, {left: frame.left, top: frame.top + frame.height + 62, width: frame.width, height: 30}, tokens,
    {points: 16.5, align: 'center', name: 'x-axis-title'});
  if (yLabel) text(slide, yLabel, {left: frame.left, top: frame.top - 47, width: frame.width, height: 34}, tokens,
    {points: 16.5, name: 'value-axis-title'});
  return {sx, sy, frame};
}

function nativeAxis(tokens, title, options = {}) {
  return {title: title ? {text: title, textStyle: {fontSize: px(16.5), fill: tokens.colors.text}} : undefined,
    textStyle: {fontSize: px(16.5), fill: tokens.colors.muted},
    line: {fill: tokens.colors.axis, width: px(tokens.strokes_points.axis)},
    majorGridlines: null, minorGridlines: null, ...options};
}

function nativeChart(slide, type, config, tokens) {
  return slide.charts.add(type, {position: {left: 98, top: 166, width: 1080, height: 420},
    hasLegend: false, titlePlacement: 'none', chartFill: '#FFFFFF', plotAreaFill: '#FFFFFF',
    chartLine: {fill: 'none', width: 0}, plotAreaLine: {fill: 'none', width: 0},
    xAxis: nativeAxis(tokens), yAxis: nativeAxis(tokens), ...config});
}

function boxSummary(values) {
  requireFinite(values, 'box observations');
  const sorted = [...values].sort((a, b) => a - b);
  const quantile = p => {const h = (sorted.length - 1) * p, i = Math.floor(h); return sorted[i] + (h - i) * ((sorted[i + 1] ?? sorted[i]) - sorted[i]);};
  const q1 = quantile(.25), median = quantile(.5), q3 = quantile(.75), spread = q3 - q1;
  const inside = sorted.filter(v => v >= q1 - 1.5 * spread && v <= q3 + 1.5 * spread);
  return {q1, median, q3, low: inside[0], high: inside.at(-1)};
}

function drawCounts(slide, data, t, c) {
  requireFinite(data.counts, 'counts');
  if (data.counts.some(v => !Number.isInteger(v) || v < 0) || data.categories.length !== data.counts.length) throw new Error('Counts need aligned categories and nonnegative integers.');
  if (!['exclusive_exhaustive', 'overlapping', 'subset'].includes(data.relationship)) throw new Error('Declare category relationship.');
  if (data.denominator !== null && (!Number.isInteger(data.denominator) || data.denominator < 0 || data.counts.some(v => v > data.denominator))) throw new Error('Use a valid population denominator or null.');
  if (data.relationship === 'exclusive_exhaustive' && data.denominator !== null && data.counts.reduce((a, b) => a + b, 0) !== data.denominator) throw new Error('Exclusive exhaustive counts must reconcile with their denominator.');
  if (data.categories.length > 6) throw new Error('Reflow many categories into a horizontal or faceted layout.');
  if (data.roles && (data.roles.length !== data.counts.length || data.roles.some(v => !['primary', 'secondary', 'third', 'neutral'].includes(v)))) throw new Error('Category color roles must align with counts.');
  const colors = data.roles ? data.roles.map(role => c[role]) : data.counts.map(() => c.primary);
  nativeChart(slide, 'bar', {categories: data.categories,
    series: [{name: '计数', values: data.counts, fill: c.primary,
      points: data.counts.map((_, idx) => ({idx, fill: colors[idx]})),
      dataLabelOverrides: data.counts.map((v, idx) => ({idx,
        text: v.toLocaleString('en-US') + ' · ' + (data.denominator ? (100 * v / data.denominator).toFixed(1) + '%' : '占比不可用'),
        position: 'outEnd', textStyle: {fontSize: px(16.5), fill: c.text}}))}],
    barOptions: {direction: 'column', grouping: 'clustered', gapWidth: 95},
    yAxis: nativeAxis(t, `计数（${data.unit}）`, {...bounds(data.counts, true), numberFormatCode: '#,##0'}),
    xAxis: nativeAxis(t), dataLabels: {showValue: true, position: 'outEnd', textStyle: {fontSize: px(16.5), fill: c.text}},
  }, t);
}

function drawLine(slide, data, t, c, gray = false) {
  requireFinite(data.x, 'x');
  if (data.x.some((v, i) => i && v <= data.x[i - 1]) || !data.series.length || data.series.length > 3) throw new Error('Use increasing numeric time and one to three series.');
  data.series.forEach(s => {if (!Array.isArray(s.values) || s.values.length !== data.x.length || s.values.some(v => v !== null && !finite(v)) || !s.values.some(finite)) throw new Error('Time and observations must align; mark missing observations as null.');});
  const colors = [c.primary, c.secondary, c.third];
  nativeChart(slide, 'scatter', {scatterOptions: {style: 'lineWithMarkers'},
    series: data.series.map((s, i) => ({name: s.name, xValues: data.x, values: s.values,
      line: {fill: colors[i], width: px(t.strokes_points.series), style: gray && i ? ['solid', 'dashed', 'dotted'][i] : 'solid'},
      marker: {symbol: ['circle', 'square', 'triangle'][i], size: 6, fill: colors[i]}})),
    displayBlanksAs: 'gap',
    hasLegend: true, legend: {position: 'top', overlay: false, textStyle: {fontSize: px(16.5), fill: c.text}},
    xAxis: nativeAxis(t, data.x_label, bounds(data.x)),
    yAxis: nativeAxis(t, data.y_label, bounds(data.series.flatMap(s => s.values.filter(finite)))),
  }, t);
}

function drawScatter(slide, data, t, c) {
  if (!data.series.length || data.series.length > 3) throw new Error('Use one to three groups or reflow.');
  data.series.forEach(s => {requireFinite(s.x, 'x'); requireFinite(s.y, 'y'); if (s.x.length !== s.y.length) throw new Error('Scatter coordinates must align.');});
  nativeChart(slide, 'scatter', {scatterOptions: {style: 'marker'},
    series: data.series.map((s, i) => ({name: s.name, xValues: s.x, values: s.y,
      fill: [c.primary, c.secondary, c.third][i], line: {fill: 'none', width: 0},
      marker: {symbol: ['circle', 'square', 'triangle'][i], size: 6, fill: [c.primary, c.secondary, c.third][i]}})),
    hasLegend: true, legend: {position: 'top', overlay: false, textStyle: {fontSize: px(16.5), fill: c.text}},
    xAxis: nativeAxis(t, data.x_label, bounds(data.series.flatMap(s => s.x))),
    yAxis: nativeAxis(t, data.y_label, bounds(data.series.flatMap(s => s.y))),
  }, t);
}

function drawBoxes(slide, data, t, c) {
  const names = Object.keys(data.groups);
  if (names.length !== 2) throw new Error('The distribution layout needs two groups; reflow for more.');
  const range = bounds(Object.values(data.groups).flat(), true);
  const {sx, sy} = axes(slide, t, c, {xMin: .4, xMax: 2.6, yMin: range.min, yMax: range.max,
    xTicks: names.map((label, i) => ({value: i + 1, label: `${label}（n=${data.groups[label].length}）`})),
    yTicks: Array.from({length: 5}, (_, i) => range.min + (range.max - range.min) * i / 4), yLabel: data.value_label});
  names.forEach((name, i) => {
    const values = data.groups[name], s = boxSummary(values), color = [c.primary, c.secondary][i];
    const x = sx(i + 1), width = 88;
    line(slide, x, sy(s.low), x, sy(s.high), color, 1.5);
    for (const end of [s.low, s.high]) line(slide, x - 22, sy(end), x + 22, sy(end), color, 1.5);
    slide.shapes.add({geometry: 'rect', name: 'quartile-box', position: {left: x - width / 2, top: sy(s.q3), width, height: sy(s.q1) - sy(s.q3)},
      fill: blend('#FFFFFF', color, .16), line: {fill: color, width: 1.8}});
    line(slide, x - width / 2, sy(s.median), x + width / 2, sy(s.median), c.text, 1.5);
    values.forEach((value, j) => marker(slide, x + 100 + ((j * 37) % 11 - 5) * 2, sy(value), color, i === 1, false, 9));
  });
}

function drawPaired(slide, data, t, c) {
  const pairs = data.pairs;
  if (!Array.isArray(pairs) || !pairs.length || new Set(pairs.map(p => p.id)).size !== pairs.length || pairs.some(p => !p.id || [p.before, p.after].some(v => v !== null && !finite(v)))) throw new Error('Paired data need unique IDs and numeric or explicitly missing endpoints.');
  const beforeN = pairs.filter(p => p.before !== null).length, afterN = pairs.filter(p => p.after !== null).length;
  const range = bounds(pairs.flatMap(p => [p.before, p.after]).filter(finite));
  const {sx, sy} = axes(slide, t, c, {xMin: -.4, xMax: 1.4, yMin: range.min, yMax: range.max,
    xTicks: [{value: 0, label: `前测（n=${beforeN}）`}, {value: 1, label: `后测（n=${afterN}）`}],
    yTicks: Array.from({length: 4}, (_, i) => Number((range.min + (range.max - range.min) * i / 3).toFixed(1))), yLabel: data.value_label});
  for (const p of pairs) {
    const complete = p.before !== null && p.after !== null;
    if (complete) line(slide, sx(0), sy(p.before), sx(1), sy(p.after), c.neutral, 1.4);
    if (p.before !== null) marker(slide, sx(0), sy(p.before), c.primary, false, !complete);
    if (p.after !== null) marker(slide, sx(1), sy(p.after), c.secondary, true, !complete);
  }
}

function drawIntervals(slide, data, t, c) {
  if (!finite(data.reference) || data.estimates.some(r => ![r.estimate, r.low, r.high].every(finite) || r.low > r.estimate || r.high < r.estimate)) throw new Error('Interval endpoints must be supplied and enclose their estimates.');
  const f = {left: 280, top: 190, width: 800, height: 340};
  if (!data.estimates.length || data.estimates.length > 4) throw new Error('Use one to four estimates or reflow into more slides.');
  const range = bounds([data.reference, ...data.estimates.flatMap(r => [r.low, r.high])]);
  const sx = x => f.left + (x - range.min) / (range.max - range.min) * f.width;
  line(slide, sx(data.reference), f.top, sx(data.reference), f.top + f.height, c.muted, 1.3, 'dashed');
  data.estimates.forEach((r, i) => {
    const y = f.top + f.height * (i + .5) / data.estimates.length;
    text(slide, r.label, {left: 76, top: y - 20, width: 174, height: 40}, t, {points: 20, align: 'right'});
    line(slide, sx(r.low), y, sx(r.high), y, c.primary, px(t.strokes_points.interval));
    for (const v of [r.low, r.high]) line(slide, sx(v), y - 9, sx(v), y + 9, c.primary, 1.8);
    marker(slide, sx(r.estimate), y, c.primary);
    text(slide, `${r.estimate > 0 ? '+' : ''}${r.estimate.toFixed(1)}`, {left: sx(r.estimate) - 40, top: y - 49, width: 80, height: 32}, t, {points: 16.5, align: 'center'});
  });
  line(slide, f.left, f.top + f.height, f.left + f.width, f.top + f.height, c.axis, 1.3);
  for (let i = 0; i <= 4; i++) {const v = Number((range.min + (range.max - range.min) * i / 4).toFixed(2)); text(slide, String(v), {left: sx(v) - 40, top: f.top + f.height + 10, width: 80, height: 32}, t, {points: 16.5, align: 'center'});}
  text(slide, data.value_label, {left: f.left, top: 584, width: f.width, height: 30}, t, {points: 16.5, align: 'center'});
}

function drawHeatmap(slide, data, t, c) {
  if (!Array.isArray(data.values) || data.values.length !== data.row_labels.length || data.values.some(row => row.length !== data.column_labels.length || row.some(v => v !== null && !finite(v)))) throw new Error('Heatmap values must align with both label arrays.');
  const [lo, hi] = data.limits;
  if (![lo, hi].every(finite) || hi <= lo) throw new Error('Heatmap needs a nondegenerate shared scale.');
  if (data.values.some(row => row.some(v => v !== null && (v < lo || v > hi)))) throw new Error('Declare a scale covering the supplied values instead of silently clipping them.');
  const left = 290, top = 196, width = 620, height = 340;
  const cw = width / data.column_labels.length, ch = height / data.row_labels.length;
  const color = v => {const p = Math.min(1, Math.max(0, (v - lo) / (hi - lo))); return p < .5 ? blend('#FFFFFF', c.light, p * 2) : blend(c.light, c.primary, (p - .5) * 2);};
  data.values.forEach((row, i) => row.forEach((value, j) => {
    const fill = value === null ? c.neutral : color(value);
    slide.shapes.add({geometry: 'rect', name: `heatmap-cell-${i}-${j}`, position: {left: left + j * cw, top: top + i * ch, width: cw, height: ch}, fill, line: {fill, width: .2}});
    text(slide, value === null ? 'NA' : value.toFixed(2), {left: left + j * cw, top: top + i * ch + ch / 2 - 25, width: cw, height: 50}, t, {points: 20, color: ink(fill), align: 'center', name: `heatmap-value-${i}-${j}`});
  }));
  data.row_labels.forEach((label, i) => text(slide, label, {left: 76, top: top + i * ch + ch / 2 - 20, width: 190, height: 40}, t, {points: 18, align: 'right'}));
  data.column_labels.forEach((label, j) => text(slide, label, {left: left + j * cw, top: top + height + 16, width: cw, height: 40}, t, {points: 18, align: 'center'}));
  const n = 32;
  for (let i = 0; i < n; i++) {
    const fill = color(hi - (hi - lo) * (i + .5) / n);
    slide.shapes.add({geometry: 'rect', name: 'colorbar-step', position: {left: 982, top: top + i * height / n, width: 24, height: height / n + .2}, fill, line: {fill, width: .2}});
  }
  for (const fraction of [0, .5, 1]) text(slide, (hi - fraction * (hi - lo)).toFixed(1), {left: 1022, top: top + fraction * height - 18, width: 70, height: 36}, t, {points: 16.5});
  text(slide, data.unit, {left: 950, top: 566, width: 220, height: 36}, t, {points: 16.5, align: 'center'});
}

function binaryCurves(data) {
  requireFinite(data.scores, 'classification scores');
  if (data.labels.length !== data.scores.length || data.labels.some(v => ![0, 1].includes(v))) throw new Error('Classification needs aligned binary labels and scores.');
  const positives = data.labels.filter(v => v === 1).length, negatives = data.labels.length - positives;
  if (!positives || !negatives) throw new Error('ROC needs both classes.');
  const thresholds = [...new Set(data.scores)].sort((a, b) => b - a);
  const roc = [[0, 0]], pr = [[0, 1]];
  let previousRecall = 0;
  for (const threshold of thresholds) {
    let tp = 0, fp = 0;
    data.scores.forEach((s, i) => {if (s >= threshold) data.labels[i] ? tp++ : fp++;});
    const recall = tp / positives, precision = tp / (tp + fp);
    roc.push([fp / negatives, recall]);
    pr.push([previousRecall, precision], [recall, precision]);
    previousRecall = recall;
  }
  return {roc, pr, prevalence: positives / data.labels.length};
}

function drawPerformance(slide, data, t, c) {
  const curves = binaryCurves(data);
  for (const [i, name, points, xLabel, yLabel, reference] of [
    [0, 'ROC', curves.roc, '假阳性率', '真阳性率', [[0, 0], [1, 1]]],
    [1, 'PR', curves.pr, '召回率', '精确率', [[0, curves.prevalence], [1, curves.prevalence]]],
  ]) {
    nativeChart(slide, 'scatter', {position: {left: 58 + i * 612, top: 166, width: 550, height: 420},
      title: name, titlePlacement: 'aboveChart', titleTextStyle: {fontSize: px(20), fill: c.text},
      scatterOptions: {style: 'line'},
      series: [{name: '曲线', xValues: points.map(p => p[0]), values: points.map(p => p[1]),
        line: {fill: c.primary, width: px(t.strokes_points.series)}, marker: {symbol: 'none'}},
      {name: '参照', xValues: reference.map(p => p[0]), values: reference.map(p => p[1]),
        line: {fill: c.neutral, width: 1.5, style: 'dashed'}, marker: {symbol: 'none'}}],
      xAxis: nativeAxis(t, xLabel, {min: 0, max: 1, majorUnit: .5, numberFormatCode: '0%', textStyle: {fontSize: px(15), fill: c.muted}}),
      yAxis: nativeAxis(t, yLabel, {min: 0, max: 1, majorUnit: .5, numberFormatCode: '0%', textStyle: {fontSize: px(15), fill: c.muted}}),
    }, t);
  }
}

function drawStyle(slide, t) {
  const roles = [['主色', 'primary'], ['对照色', 'secondary'], ['第三组', 'third'], ['其他或缺失', 'neutral']];
  roles.forEach(([label, key], i) => {
    const y = 198 + i * 86;
    slide.shapes.add({geometry: 'rect', name: 'palette-reference', position: {left: 82, top: y, width: 48, height: 42}, fill: t.colors[key], line: {fill: 'none', width: 0}});
    text(slide, `${label}  ${t.colors[key]}`, {left: 156, top: y - 3, width: 430, height: 50}, t, {points: 20});
  });
  text(slide, '投影阅读字号', {left: 724, top: 194, width: 430, height: 48}, t, {points: 24, bold: true});
  text(slide, '标题 33 pt\n正文 20 pt\n图表轴与标签 16.5 pt\n图注与数据来源 15 pt', {left: 724, top: 258, width: 430, height: 220}, t, {points: 20});
}

function tableValues(data) {
  if (!Array.isArray(data.columns) || data.columns.length < 2 || data.columns.length > 6 ||
      !Array.isArray(data.rows) || !data.rows.length || data.rows.length > 5) throw new Error('Use two to six columns and one to five body rows; split larger tables.');
  for (const column of data.columns) {
    if (!column.label || !['text', 'integer', 'number', 'percent'].includes(column.kind) ||
        column.weight !== undefined && (!finite(column.weight) || column.weight <= 0) ||
        column.digits !== undefined && (!Number.isInteger(column.digits) || column.digits < 0 || column.digits > 6)) throw new Error('Declare table column labels, types, positive widths and precision.');
  }
  if (data.rows.some(row => !Array.isArray(row) || row.length !== data.columns.length)) throw new Error('Table rows must align with all declared columns.');
  const selected = [...(data.highlight_rows || []), ...(data.total_row === undefined ? [] : [data.total_row])];
  if (selected.some(i => !Number.isInteger(i) || i < 0 || i >= data.rows.length)) throw new Error('Table emphasis must refer to existing body rows.');
  return [data.columns.map(col => col.label), ...data.rows.map(row => row.map((value, i) => {
    const col = data.columns[i];
    if (value === null) return data.missing_label || '—';
    if (col.kind === 'text') {
      if (typeof value !== 'string') throw new Error('Text table cells require strings or explicit null.');
      return value;
    }
    if (!finite(value) || col.kind === 'integer' && !Number.isInteger(value) ||
        col.kind === 'percent' && (value < 0 || value > 1)) throw new Error('Numeric cells need finite values; percentages use proportions from zero to one.');
    const digits = col.kind === 'integer' ? 0 : col.digits ?? 1;
    return (col.kind === 'percent' ? value * 100 : value).toLocaleString('en-US', {minimumFractionDigits: digits, maximumFractionDigits: digits});
  }))];
}

function drawTable(slide, data, t, c) {
  const values = tableValues(data), columns = data.columns.length;
  const width = 1120, weights = data.columns.map(col => col.weight ?? 1), total = weights.reduce((a, b) => a + b, 0);
  const table = slide.tables.add({rows: values.length, columns, left: 80, top: 196, width,
    height: 72 + 64 * data.rows.length, columnWidths: weights.map(v => width * v / total), values});
  table.styleOptions = {headerRow: false, bandedRows: false, bandedColumns: false, firstColumn: false, lastColumn: false, totalRow: false};
  table.borders.assign({style: 'solid', fill: 'none', width: 0});
  table.rows[0].height = 72;
  for (let r = 1; r < values.length; r++) table.rows[r].height = 64;
  for (let col = 0; col < columns; col++) {
    const alignment = data.columns[col].kind === 'text' ? 'left' : 'right';
    table.cells.block({row: 0, column: col, rowCount: values.length, columnCount: 1}).assign({
      fill: c.background, textStyle: {typeface: t.fonts.cjk_demo, fontSize: px(t.type_points.table ?? 18), color: c.text, alignment, verticalAlignment: 'middle'},
      margins: {left: 16, right: 16, top: 12, bottom: 12},
    });
  }
  table.cells.block({row: 0, column: 0, rowCount: 1, columnCount: columns}).assign({
    fill: c.primary, textStyle: {bold: true, color: '#FFFFFF'},
    borders: {top: {fill: c.primary, width: 1.6}, bottom: {fill: c.primary, width: 1.6}},
  });
  for (const row of data.highlight_rows || []) table.cells.block({row: row + 1, column: 0, rowCount: 1, columnCount: columns}).assign({fill: blend('#FFFFFF', c.primary, .1)});
  if (data.total_row !== undefined) table.cells.block({row: data.total_row + 1, column: 0, rowCount: 1, columnCount: columns}).assign({
    textStyle: {bold: true}, borders: {top: {fill: c.axis, width: 1.2}},
  });
  table.cells.block({row: values.length - 1, column: 0, rowCount: 1, columnCount: columns}).assign({borders: {bottom: {fill: c.axis, width: 1.6}}});
}

function drawEmpty(slide, t) {
  const shape = slide.shapes.add({geometry: 'rect', name: 'replace-with-chart', placeholderType: 'chart',
    position: {left: 96, top: 178, width: 1088, height: 380}, fill: '#FFFFFF', line: {fill: t.colors.neutral, width: 1.5, style: 'dashed'}});
  text(slide, '图表区域', {left: 100, top: 314, width: 1080, height: 50}, t, {points: 28, color: t.colors.muted, align: 'center'});
  text(slide, '标题交代主题，图注交代样本、单位、区间定义和来源', {left: 100, top: 384, width: 1080, height: 44}, t, {points: 18, color: t.colors.muted, align: 'center'});
  return shape;
}

const renderers = {counts: drawCounts, line: drawLine, scatter: drawScatter, boxplot: drawBoxes,
  paired: drawPaired, interval: drawIntervals, heatmap: drawHeatmap, performance: drawPerformance, table: drawTable};

export function makeScientificSlide(presentation, specification, tokens) {
  if (!specification || typeof specification.title !== 'string' || typeof specification.caption !== 'string') throw new Error('Supply a title and an explicit evidence caption.');
  const known = [...Object.keys(renderers), 'style', 'empty', 'grayscale'];
  if (!known.includes(specification.kind)) throw new Error('Unsupported layout; choose a documented kind or adapt using the chart mapping.');
  if (specification.kind === 'table') tableValues(specification.data);
  const c = palette(tokens, specification.kind === 'grayscale' ? 'grayscale' : 'color');
  const slide = specification.reuseIndex === undefined ? presentation.slides.add({width: tokens.canvas.width_px, height: tokens.canvas.height_px}) : presentation.slides.getItem(specification.reuseIndex);
  if (slide.shapes.items.length || slide.charts.items.length || slide.images.items.length || slide.tables.items.length) throw new Error('Reuse only an empty slide; preserve existing content.');
  slide.background.fill = c.background;
  text(slide, specification.title, {left: 64, top: 42, width: 1152, height: 64}, tokens, {points: tokens.type_points.title, bold: true, name: 'slide-title'});
  if (specification.subtitle) text(slide, specification.subtitle, {left: 66, top: 112, width: 1148, height: 40}, tokens, {points: 18, color: c.muted, name: 'slide-subtitle'});
  if (specification.kind === 'style') drawStyle(slide, tokens);
  else if (specification.kind === 'empty') drawEmpty(slide, tokens);
  else if (specification.kind === 'grayscale') drawLine(slide, specification.data, tokens, c, true);
  else renderers[specification.kind](slide, specification.data, tokens, c);
  const caption = (specification.synthetic ? '合成示例，仅展示样式。' : '') + specification.caption;
  text(slide, caption, {left: 66, top: 624, width: 1148, height: 64}, tokens, {points: tokens.type_points.caption, color: c.muted, name: 'evidence-caption'});
  slide.speakerNotes.text = JSON.stringify({layout: specification.kind, synthetic: specification.synthetic || false,
    data: specification.data || null, caption: specification.caption,
    editability: specification.kind === 'table' ? 'native editable table; values are literal and calculated cells require refresh after source changes' :
      specification.kind === 'counts' ? 'native chart; refresh custom count/share label text after counts or denominator change' :
      ['line', 'scatter', 'performance', 'grayscale'].includes(specification.kind) ? 'native chart' : 'native editable shapes; regenerate after data changes'}, null, 2);
  return slide.toSnapshot().aid;
}

export function tableSpecifications(examples) {
  if (examples.synthetic !== true) throw new Error('Template demonstrations require an explicit synthetic flag.');
  const d = examples.count_share;
  if (d.relationship !== 'exclusive_exhaustive' || !Number.isInteger(d.denominator) || d.denominator <= 0 ||
      d.counts.some(v => !Number.isInteger(v) || v < 0) || d.counts.reduce((a, b) => a + b, 0) !== d.denominator) throw new Error('Table composition counts must reconcile with their declared denominator.');
  return [
    {kind: 'table', title: '结果对比表', subtitle: '固定单位、统一精度，浅蓝行标出当前方案', data: examples.result_table,
      caption: '同一测试集：60 张图像来自 10 名对象，其中阳性 30 张。— 表示未评估；箭头表示优选方向，未提供区间或检验。'},
    {kind: 'table', title: '样本构成表', subtitle: '数量与占比并列，表头明确统计单位', data: {
      columns: [{label: '类别', kind: 'text', weight: 2}, {label: '记录数（条）', kind: 'integer'}, {label: '占比（%）', kind: 'percent', digits: 1}],
      rows: [...d.categories.map((name, i) => [name, d.counts[i], d.counts[i] / d.denominator]), ['合计', d.denominator, 1]], total_row: d.categories.length,
    }, caption: '分母为 28,552 条记录，三类互斥且穷尽。占比保留一位小数。\n与前面的计数图使用相同数据；合计按原始计数计算。'},
    {kind: 'table', title: '方法与参数表', subtitle: '取值与含义分列，未提供的设置明确写出', data: examples.parameter_table,
      caption: '这些设置仅为模板示例。“未提供”表示缺少资料，不表示该规则已关闭。'},
  ].map(spec => ({...spec, synthetic: true}));
}

export function templateSpecifications(examples) {
  if (examples.synthetic !== true) throw new Error('Template demonstrations require an explicit synthetic flag.');
  const common = {synthetic: true};
  return [
    {kind: 'style', title: '统一配色与阅读规格', caption: '白底、无阴影和装饰卡片。沿用同一字体层级、组别颜色和留白规则。'},
    {kind: 'counts', title: '计数与占比', subtitle: '零起点与直接数值标签', data: examples.count_share, caption: '分母为 28,552 条记录，三类互斥且穷尽。占比保留一位小数。'},
    {kind: 'line', title: '连续时间测量', subtitle: '数值时间轴保留真实间隔', data: examples.line, caption: '每条线代表一个合成个体，四个实际时间点。未绘制群体均值或不确定性区间。'},
    {kind: 'scatter', title: '连续变量之间的关系', subtitle: '颜色与点形同时区分组别', data: examples.scatter, caption: '每个点代表一条合成记录，每组 n=6。未添加回归线、显著性或因果结论。'},
    {kind: 'boxplot', title: '组间分布与个体观测', subtitle: '箱体、须线与原始点保持同一套视觉规则', data: examples.boxplot, caption: '每组 n=12。四分位数使用线性插值；须线延伸至距箱体不超过 1.5 倍四分位距的最远观测，保留全部原始点。'},
    {kind: 'paired', title: '同一对象的前后观测', subtitle: '连接线只连接真实配对', data: examples.paired, caption: '8 个合成对象，其中 7 对完整。S8 缺失后测，空心点保留其前测，不补零、不伪造连接线。'},
    {kind: 'interval', title: '效应量与不确定性', subtitle: '保留方向、单位与零参照', data: examples.interval, caption: '区间为明确给定的合成 95% 区间。数值表示各模型相对自身基线的误差变化，未添加显著性标记。'},
    {kind: 'heatmap', title: '矩阵热图', subtitle: '连续色阶与缺失状态分开编码', data: examples.heatmap, caption: '所有单元格使用共同的 0–1 色阶。NA 表示缺失，灰色不表示较低分数。'},
    {kind: 'performance', title: '分类模型的 ROC 与 PR 曲线', subtitle: 'ROC：真阳性率与假阳性率；PR：精确率与召回率', data: examples.classification, caption: '同一组 8 条合成分类记录，正负样本各 4 条。灰线分别为 ROC 对角线与 PR 阳性比例参照。'},
    ...tableSpecifications(examples),
    {kind: 'grayscale', title: '灰度打印模式', subtitle: '线型与点形补充明暗差异', data: examples.line, caption: '与彩色时间图使用相同数据、坐标范围和字体。保留实线、虚线及圆点、方点差异。'},
    {kind: 'empty', title: '研究问题或主要发现', caption: '图注：样本与独立单位、指标及单位、参照、区间定义、数据来源。'},
  ].map(specification => ({...common, ...specification, synthetic: !['style', 'empty'].includes(specification.kind)}));
}

export const statistics = {boxSummary, binaryCurves};
