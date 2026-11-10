import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {makeScientificSlide, statistics} from '../skills/scientific-presentation-style/scripts/slide-builders.mjs';

const base = new URL('../skills/scientific-presentation-style/', import.meta.url);
const tokens = JSON.parse(fs.readFileSync(new URL('assets/design-tokens.json', base)));
const examples = JSON.parse(fs.readFileSync(new URL('assets/example-data.json', base)));

// Capture authoring calls without a cloud session; live rendering is checked separately.
function collection() {
  return {items: [], add(config) {this.items.push(config); return config;}};
}
function render(kind, data) {
  const slides = collection();
  slides.add = () => {
    const slide = {shapes: collection(), charts: collection(), images: collection(), tables: collection(),
      speakerNotes: {}, background: {}, toSnapshot: () => ({aid: 'sl/test'})};
    slide.shapes.add = config => {
      let content;
      const shape = {...config, get text() {return content;},
        set text(value) {content = {value, style: {}};}};
      slide.shapes.items.push(shape);
      return shape;
    };
    slide.charts.add = (type, config) => {const chart = {type, ...config}; slide.charts.items.push(chart); return chart;};
    slides.items.push(slide);
    return slide;
  };
  makeScientificSlide({slides}, {kind, data, title: 'Evidence', caption: 'Supplied fixture', synthetic: true}, tokens);
  return slides.items[0];
}

test('linear quartiles and whiskers preserve an outlying observation', () => {
  assert.deepEqual(statistics.boxSummary([1, 2, 3, 4, 100]), {q1: 2, median: 3, q3: 4, low: 1, high: 4});
  const slide = render('boxplot', {groups: {A: [1, 2, 3, 4, 100], B: [2, 3, 4, 5]}, value_label: 'ms'});
  assert.equal(slide.shapes.items.filter(s => s.name === 'observation').length, 9);
  assert.deepEqual(JSON.parse(slide.speakerNotes.text).data.groups.A, [1, 2, 3, 4, 100]);
});

test('overlapping shares retain the actual population and a zero bar origin', () => {
  const chart = render('counts', {categories: ['A', 'B'], counts: [70, 55], denominator: 100, relationship: 'overlapping', unit: 'records'}).charts.items[0];
  assert.equal(chart.yAxis.min, 0);
  assert.deepEqual(chart.series[0].values, [70, 55]);
  assert.deepEqual(chart.series[0].dataLabelOverrides.map(p => p.text), ['70 · 70.0%', '55 · 55.0%']);
});

test('zero/unknown denominator never becomes a zero percentage', () => {
  for (const denominator of [0, null]) {
    const chart = render('counts', {categories: ['A'], counts: [0], denominator, relationship: 'subset', unit: 'records'}).charts.items[0];
    assert.equal(chart.series[0].dataLabelOverrides[0].text, '0 · 占比不可用');
  }
});

test('third category is neutral only when that semantic role is declared', () => {
  const data = {categories: ['A', 'B', 'C'], counts: [2, 3, 4], denominator: 9, relationship: 'exclusive_exhaustive', unit: 'records'};
  assert.deepEqual(render('counts', data).charts.items[0].series[0].points.map(p => p.fill), Array(3).fill(tokens.colors.primary));
  data.roles = ['primary', 'secondary', 'third'];
  assert.equal(render('counts', data).charts.items[0].series[0].points[2].fill, tokens.colors.third);
});

test('inconsistent exhaustive counts are rejected', () => {
  assert.throws(() => render('counts', {categories: ['A'], counts: [70], denominator: 100, relationship: 'exclusive_exhaustive', unit: 'records'}), /reconcile/);
});

test('native time coordinates and explicit missing observations are retained', () => {
  const chart = render('line', {x: [0, 2, 7], x_label: 'days', y_label: 'ms', series: [{name: 'A', values: [10, null, 12]}]}).charts.items[0];
  assert.equal(chart.type, 'scatter');
  assert.deepEqual(chart.series[0].xValues, [0, 2, 7]);
  assert.deepEqual(chart.series[0].values, [10, null, 12]);
  assert.equal(chart.displayBlanksAs, 'gap');
});

test('paired data retain every observed endpoint and only complete trajectories', () => {
  const slide = render('paired', examples.paired);
  const observations = slide.shapes.items.filter(s => s.name === 'observation');
  assert.equal(observations.length, 15);
  assert.equal(observations.filter(s => s.fill === '#FFFFFF').length, 1);
  assert.equal(slide.shapes.items.filter(s => s.geometry === 'custom' && s.line.fill === tokens.colors.neutral).length, 7);
  assert.equal(JSON.parse(slide.speakerNotes.text).data.pairs.at(-1).after, null);
});

test('paired labels cannot silently create duplicate subjects', () => {
  assert.throws(() => render('paired', {pairs: [{id: 'S1', before: 1, after: 2}, {id: 'S1', before: 2, after: 3}]}), /unique/);
});

test('invalid intervals are rejected instead of repaired by sorting', () => {
  assert.throws(() => render('interval', {reference: 0, estimates: [{label: 'A', estimate: 2, low: 3, high: 4}]}), /enclose/);
});

test('missing heatmap cells remain distinct from numeric zero and retain source values', () => {
  const data = {row_labels: ['A'], column_labels: ['zero', 'missing'], values: [[0, null]], limits: [0, 1], unit: 'score'};
  const slide = render('heatmap', data);
  const cells = slide.shapes.items.filter(s => s.name.startsWith('heatmap-cell'));
  assert.notEqual(cells[0].fill, cells[1].fill);
  assert.equal(slide.shapes.items.find(s => s.name === 'heatmap-value-0-1').text.value, 'NA');
  assert.deepEqual(JSON.parse(slide.speakerNotes.text).data.values, [[0, null]]);
  assert.throws(() => render('heatmap', {...data, values: [[0, 2]]}), /clipping/);
});

test('threshold ties enter ROC/PR together and PR retains prevalence', () => {
  const curves = statistics.binaryCurves({labels: [0, 1, 0, 1], scores: [.5, .5, .5, .5]});
  assert.deepEqual(curves.roc, [[0, 0], [1, 1]]);
  assert.deepEqual(curves.pr, [[0, 1], [0, .5], [1, .5]]);
  assert.equal(curves.prevalence, .5);
});

test('the supplied tied-score ROC has AUC 0.75 without synthesizing thresholds', () => {
  const data = {labels: [0, 1, 0, 1, 1, 0, 0, 1], scores: [.1, .9, .6, .6, .8, .4, .6, .2]};
  const points = statistics.binaryCurves(data).roc;
  const area = points.slice(1).reduce((sum, p, i) => sum + (p[0] - points[i][0]) * (p[1] + points[i][1]) / 2, 0);
  assert.equal(area, .75);
  assert.equal(points.length, new Set(data.scores).size + 1);
});

test('undefined ROC from a single class is rejected', () => {
  assert.throws(() => statistics.binaryCurves({labels: [1, 1], scores: [.2, .8]}), /both classes/);
});
