#!/usr/bin/env python3
"""Build the textual chart index and individual reference previews.

The ordinary Agent path is chart-index.md -> one card -> one single-chart call.
This maintenance command refreshes the shipped examples. --check is read-only:
it checks recorded source/input/image hashes without rerendering on CI fonts.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
from importlib.metadata import PackageNotFoundError, version
import json
import os
from pathlib import Path
import re
import struct
import sys
import tempfile
import xml.etree.ElementTree as ET

SKILL_ROOT = Path(__file__).resolve().parents[1]
CHART_IDS = frozenset({
    'count_share', 'boxplot', 'violin', 'scatter', 'line', 'histogram', 'ecdf',
    'paired', 'interval', 'heatmap', 'raincloud', 'roc', 'pr', 'calibration',
    'confusion', 'bland_altman', 'survival', 'volcano', 'pca',
})
SOURCE_PATHS = (
    'scripts/build_chart_references.py', 'scripts/render_chart.py',
    'scripts/matplotlib_example.py', 'scripts/scientific_chart_gallery.py',
    'scripts/advanced_chart_gallery.py', 'references/chart-index.json',
    'references/style-guide.md',
)
REGISTRY = 'references/chart-index.json'
INDEX = 'references/chart-index.md'
MANIFEST = 'references/examples/manifest.json'


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resource(root: Path, relative: str) -> Path:
    """Resolve a portable registry resource, including symlink boundaries."""
    if not isinstance(relative, str) or not relative or '\\' in relative:
        raise ValueError(f'Invalid resource path: {relative!r}')
    path = Path(relative)
    if path.is_absolute() or '..' in path.parts or re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', relative):
        raise ValueError(f'Resource must be a skill-relative path without traversal: {relative!r}')
    result = root / path
    if not result.resolve().is_relative_to(root.resolve()):
        raise ValueError(f'Resource leaves the skill through a symlink: {relative!r}')
    return result


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as error:
        raise ValueError(f'{path}: {error}') from error


def load_registry(root: Path) -> list[dict]:
    registry = read_json(resource(root, REGISTRY))
    if not isinstance(registry, dict) or type(registry.get('schema_version')) is not int or registry['schema_version'] != 1:
        raise ValueError('Chart registry must be an object with schema_version=1.')
    charts = registry.get('charts')
    if not isinstance(charts, list) or not all(isinstance(item, dict) for item in charts):
        raise ValueError('Chart registry charts must be a list of objects.')
    identifiers = [item.get('id') for item in charts]
    if any(not isinstance(name, str) for name in identifiers) or len(set(identifiers)) != len(identifiers):
        raise ValueError('Chart IDs must be strings and unique.')
    if set(identifiers) != CHART_IDS:
        raise ValueError(f'Chart registry must contain exactly the 19 supported IDs; found {identifiers!r}.')
    for item in charts:
        name = item['id']
        for field in ('name', 'question'):
            if not isinstance(item.get(field), str) or not item[field].strip():
                raise ValueError(f'{name}: {field} must be nonempty text.')
        inputs = item.get('required_inputs')
        if not (isinstance(inputs, str) and inputs.strip() or isinstance(inputs, list) and inputs and
                all(isinstance(value, str) and value.strip() for value in inputs)):
            raise ValueError(f'{name}: required_inputs must be text or a nonempty list of field names.')
        if item.get('family') not in {'basic', 'advanced', 'count'}:
            raise ValueError(f'{name}: invalid family.')
        expected = {
            'guide': f'references/charts/{name}.md',
            'input': f'references/examples/{name}.json',
            'svg': f'references/examples/{name}.svg',
            'png': f'references/examples/{name}.png',
        }
        for field, relative in expected.items():
            resource(root, item.get(field))
            if item[field] != relative:
                raise ValueError(f'{name}: {field} must map to {relative!r}.')
    return charts


def _table_text(text) -> str:
    return ' '.join(str(text).split()).replace('|', '\\|')


def index_markdown(charts: list[dict]) -> str:
    """Generate navigation, not a compulsory image gallery or duplicate manual."""
    parts = [
        '# Chart Index: 19 Scientific Encodings',
        'Start with the question and available inputs. Choose one chart ID, read only its card, '
        'and inspect its individual SVG or PNG only when visual detail is needed. '
        'The card specifies the statistical definition, input format, limitations and a short runnable example.',
        'The linked inputs and previews are **synthetic reference examples**, not research findings. '
        'B teal/terracotta is the default; generate D print mode with `--mode grayscale`. '
        'Keep the shared [style guide](style-guide.md) authoritative for appearance.',
        '| ID / chart card | Use when | Required inputs | Example data | Individual preview |',
        '|---|---|---|---|---|',
    ]
    for item in charts:
        name = item['id']
        inputs = item['required_inputs']
        if isinstance(inputs, list):
            inputs = ', '.join(inputs)
        rel = lambda field: os.path.relpath(item[field], 'references').replace(os.sep, '/')
        parts.append(f'| [`{name}`: {_table_text(item["name"])}]({rel("guide")}) '
                     f'| {_table_text(item["question"])} | {_table_text(inputs)} '
                     f'| [JSON]({rel("input")}) | [SVG]({rel("svg")}) · [PNG]({rel("png")}) |')
    parts += [
        '\n## Run one example',
        'From the skill directory, use an output directory in the task workspace. '
        'The following creates only the ROC example and its numerical/export companions:',
        '```sh\npython scripts/render_chart.py --chart roc --example --output-dir /tmp/roc-reference\n```',
        'For actual supplied data, replace `--example` with `--input /path/to/task/roc.json`. '
        '`--input` and `--example` are mutually exclusive; no data is silently synthesized. '
        'Use `--formats svg,png,pdf` when all three exports are needed. '
        '[Renderer](../scripts/render_chart.py) · [machine-readable index](chart-index.json).',
        '\n## Maintenance and optional browsing',
        'The [preview manifest](examples/manifest.json) records fixture, source and output hashes. '
        '`python scripts/build_chart_references.py --check` verifies this mapping without rendering. '
        'Refreshing all shipped reference images is a maintainer action, not a prerequisite for drawing one chart. '
        'The older [basic](scientific-chart-examples.md) and [advanced](advanced-chart-guide.md) guides '
        'remain optional background; their contact sheets are not required Agent input.',
    ]
    return '\n\n'.join(parts[:3]) + '\n\n' + '\n'.join(parts[3:3+len(charts)+2]) + '\n\n' + '\n\n'.join(parts[3+len(charts)+2:]) + '\n'


def source_hashes(root: Path) -> dict[str, str]:
    return {name: digest(resource(root, name)) for name in SOURCE_PATHS}


def preview_properties(svg: Path, png: Path) -> dict:
    try:
        document = ET.parse(svg).getroot()
    except (OSError, ET.ParseError) as error:
        raise ValueError(f'{svg}: invalid SVG: {error}') from error
    if document.tag.rsplit('}', 1)[-1] != 'svg':
        raise ValueError(f'{svg}: root is not SVG.')
    tags = {element.tag.rsplit('}', 1)[-1] for element in document.iter()}
    if 'text' not in tags or 'image' in tags:
        raise ValueError(f'{svg}: reference SVG must retain editable text and vector marks.')
    def physical(value):
        match = re.fullmatch(r'([0-9.]+)(pt|mm|cm|in)', value or '')
        if not match:
            raise ValueError(f'{svg}: SVG dimensions need physical units.')
        number, unit = float(match[1]), match[2]
        if number <= 0:
            raise ValueError(f'{svg}: SVG dimensions must be positive.')
        return round(number * {'pt': 25.4/72, 'mm': 1, 'cm': 10, 'in': 25.4}[unit], 6)
    content = png.read_bytes()
    if len(content) < 24 or content[:8] != b'\x89PNG\r\n\x1a\n' or content[12:16] != b'IHDR':
        raise ValueError(f'{png}: invalid PNG signature/header.')
    width, height = struct.unpack('>II', content[16:24])
    if not width or not height:
        raise ValueError(f'{png}: PNG dimensions must be positive.')
    return {'svg_dimensions_mm': {'width': physical(document.get('width')),
                                  'height': physical(document.get('height'))},
            'png_pixels': {'width': width, 'height': height}}


def check_references(root: Path = SKILL_ROOT) -> list[str]:
    """Read-only freshness/integrity check; never invokes Matplotlib/rendering."""
    errors = []
    try:
        charts = load_registry(root)
        manifest = read_json(resource(root, MANIFEST))
        if not isinstance(manifest, dict) or type(manifest.get('schema_version')) is not int or manifest['schema_version'] != 1:
            raise ValueError('Preview manifest must be an object with schema_version=1.')
        if manifest.get('mode') != 'color':
            errors.append('Reference manifest mode must be color (approved B default).')
        if manifest.get('sources') != source_hashes(root):
            errors.append('Reference sources changed; refresh the shipped previews and manifest.')
        records = manifest.get('charts')
        if not isinstance(records, dict) or set(records) != CHART_IDS:
            raise ValueError('Preview manifest must contain exactly the 19 chart IDs.')
        if resource(root, INDEX).read_text(encoding='utf-8') != index_markdown(charts):
            errors.append('Text chart index is stale or its registry mapping changed.')
        for item in charts:
            name, record = item['id'], records[item['id']]
            if not isinstance(record, dict):
                errors.append(f'{name}: invalid manifest entry.'); continue
            for field in ('guide', 'input', 'svg', 'png'):
                path = resource(root, item[field])
                if record.get(field) != item[field]:
                    errors.append(f'{name}: manifest {field} mapping changed.')
                if not path.is_file():
                    errors.append(f'{name}: missing {field} file {item[field]}.'); continue
                if record.get(f'{field}_sha256') != digest(path):
                    errors.append(f'{name}: {field} content changed; refresh reference manifest.')
            data = read_json(resource(root, item['input']))
            if not isinstance(data, dict) or data.get('synthetic') is not True:
                errors.append(f'{name}: shipped example input must be a labeled synthetic object.')
            if all(resource(root, item[field]).is_file() for field in ('svg', 'png')):
                properties = preview_properties(resource(root, item['svg']), resource(root, item['png']))
                if any(record.get(key) != value for key, value in properties.items()):
                    errors.append(f'{name}: recorded preview dimensions changed.')
    except (OSError, ValueError, KeyError, TypeError) as error:
        errors.append(str(error))
    return errors


def _atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.'+path.name, delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(content)
    try:
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def build_references(root: Path = SKILL_ROOT, renderer=None) -> dict:
    """Render to temporary staging; publish generated source files only on success."""
    root = Path(root)
    charts = load_registry(root)
    sources = source_hashes(root)
    inputs = {}
    input_hashes = {}
    for item in charts:
        if not resource(root, item['guide']).is_file():
            raise ValueError(f'{item["id"]}: missing chart card {item["guide"]}.')
        data = read_json(resource(root, item['input']))
        if not isinstance(data, dict) or data.get('synthetic') is not True:
            raise ValueError(f'{item["id"]}: shipped example input must be a labeled synthetic object.')
        inputs[item['id']] = data
        input_hashes[item['id']] = {field: digest(resource(root, item[field])) for field in ('guide', 'input')}
    if renderer is None:
        # --check and registry lookup do not import any plotting implementation.
        sys.path.insert(0, str(root/'scripts'))
        try:
            renderer = importlib.import_module('render_chart').render_chart
        finally:
            sys.path.pop(0)
    manifest = {'schema_version': 1, 'generator': 'scripts/build_chart_references.py',
                'mode': 'color', 'style': 'B muted teal/terracotta', 'sources': sources,
                'charts': {}}
    try:
        manifest['libraries'] = {name: version(name) for name in ('matplotlib', 'numpy')}
    except PackageNotFoundError:
        manifest['libraries'] = {}
    with tempfile.TemporaryDirectory(prefix='chart-reference-build-') as temporary:
        stage = Path(temporary)
        staged = {}
        for item in charts:
            name = item['id']
            output = stage/name
            output.mkdir()
            renderer(name, inputs[name], output, mode='color', formats=('svg', 'png'))
            files = {suffix: list(output.rglob('*.'+suffix)) for suffix in ('svg', 'png')}
            if any(len(paths) != 1 for paths in files.values()):
                raise ValueError(f'{name}: renderer must generate exactly one SVG and one PNG reference.')
            svg, png = files['svg'][0], files['png'][0]
            record = {field: item[field] for field in ('guide', 'input', 'svg', 'png')}
            for field in ('guide', 'input'):
                record[f'{field}_sha256'] = input_hashes[name][field]
            for field, path in [('svg', svg), ('png', png)]:
                record[f'{field}_sha256'] = digest(path)
                staged[item[field]] = path
            record.update(preview_properties(svg, png))
            manifest['charts'][name] = record
        if source_hashes(root) != sources:
            raise ValueError('Rendering sources changed during the build; rerun after edits settle.')
        for item in charts:
            record = manifest['charts'][item['id']]
            for field in ('guide', 'input'):
                if digest(resource(root, item[field])) != record[f'{field}_sha256']:
                    raise ValueError(f'{item["id"]}: input/card changed during the build; rerun after edits settle.')
        for relative, path in staged.items():
            _atomic_write(resource(root, relative), path.read_bytes())
        _atomic_write(resource(root, INDEX), index_markdown(charts).encode('utf-8'))
        _atomic_write(resource(root, MANIFEST), (json.dumps(manifest, ensure_ascii=False, indent=2)+'\n').encode('utf-8'))
    errors = check_references(root)
    if errors:
        raise ValueError('\n'.join(errors))
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Verify the shipped index/previews without modifying files.')
    parser.add_argument('--skill-root', type=Path, default=SKILL_ROOT, help=argparse.SUPPRESS)
    args = parser.parse_args()
    try:
        if args.check:
            errors = check_references(args.skill_root)
            if errors:
                for error in errors:
                    print(error, file=sys.stderr)
                return 1
            print('Verified 19 single-chart references; no rendering or writes performed.')
        else:
            manifest = build_references(args.skill_root)
            print(f'Built {len(manifest["charts"])} individual SVG/PNG references and the textual index.')
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
