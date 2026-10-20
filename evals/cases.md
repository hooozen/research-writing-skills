# Behavioral evaluation cases

Run relevant cases after substantial instruction changes. Give an evaluator the prompt, the selected skill directory, and the supplied data only; keep the review criteria for the reviewer. Use a temporary output directory, synthetic inputs, and no live services. Record actual output, questions asked, calculations, and rendering checks. A text search is not a substitute for reading the result, and successful source generation is not evidence of successful rendering.

## Report: explicit audience, offline formulas

**Prompt**

> 为跨学科高学历研究人员写一份中文组会阶段性科研进展报告，请你组织结构。提供可以离线打开的单文件 HTML，公式须实际显示。全部是演示用合成数据，在成品显著标明。项目评估训练图像质量筛选后小型分类器的性能。8月 A 在固定验证集120张图像上正确90张；9月 B 在同一验证集上正确96张。图像来自30个样本，样本间独立性未知，训练验证样本是否重叠未知，无逐图预测、置信区间或配对检验。此次唯一报告的改动是训练前剔除低质量图像，验证集不变。给出 accuracy 的计数公式、准确率、百分点及相对变化；区分观察与推断。没有其他实验结果或引用。

**Review**

Verify 75%, 80%, +5 percentage points, and approximately +6.67% relative to A. The net increase of six correct predictions must not become “exactly six corrected images.” Preserve dependence, pairing, unknown split overlap, and causal uncertainty. Require an actual offline formula representation, a single-file dependency check, and a rendered inspection where available. If rendering cannot be inspected, report that limitation. Do not repeat already answered intake questions.

## Report: delegated settings and incomplete evidence

**Prompt**

> 请直接给我两份简短中文科研进展报告示例，受众和用途由你判断。示例一使用上述演示用合成验证计数，但不提供月份或方法改动。结构为“本期观察／证据边界／下一步”，不要增设二级标题，输出 Markdown。示例二是资料不完整的草稿：本周完成一套图像质量规则的实现，但还未运行评估，无样本量、性能结果或引用，计划与旧规则比较。不要虚构结果，标出具体缺失信息。两份都不需要图表或数学公式。

When running this case independently, supply the A/B counts and sampling uncertainties from the preceding case as raw facts, but omit its months and training intervention.

**Review**

Proceed on the explicit delegation, retain the outline, keep assumptions outside the artifact, and avoid author-facing coaching. Do not leak the other case's dates or intervention into the first example. The second artifact must distinguish implementation from evaluation and remain labeled incomplete; missing evidence must not become synthetic performance results.

## Report: concise reasoning with charts and formulas

**Prompt**

> 为小领域科研人员改写下面的中文组会记录，请组织为简练、可独立阅读的 Markdown 报告，不指定字数。全部是演示用合成数据，须标明。目标是减少图像处理延迟；相同硬件、同一组120张 OCT 图像（来自30个受试者），比较旧版 A 和新版 B 的处理时间。A 的均值为50 ms/图像，B 为40 ms/图像；仅有汇总均值，无逐图配对数据、离散程度、置信区间或检验结果。B 此次同时调整批处理和缓存策略，两者贡献尚未分离。当前仅评估延迟，尚未评估图像质量及外部设备。下一步计划分别关闭这两个改动并复测，同时补做质量评估。原记录：“我们开展了一系列工作，取得了非常显著的优化成果。旧版平均每张50毫秒，新版平均每张40毫秒。我们可以看到，新版比旧版快，速度得到了非常显著的提高。旧版是50毫秒，新版是40毫秒。这证明批处理改动本身使各类设备上的延迟降低20%，且质量完全不受影响。”

**Review**

Inspect the actual report and figure, not keyword matches. Expect a clear question–evidence–conclusion–next-test chain, a compact rendered comparison chart with time units and a zero baseline, traceable exact means and sampling units, and a concise definition/calculation of relative latency reduction: $(50-40)/50=20\%$. Distinguish the 10 ms absolute reduction and 20% relative reduction from throughput or percentage-point claims. The figure and formula should replace repetitive exposition, with brief interpretation rather than a prose recitation of all labels. Keep the report and figure visibly labeled synthetic. Reject “statistically significant”, isolated attribution to batch processing, established quality preservation, generalization across devices, invented dispersion, and treating 120 images as 120 independent subjects. Preserve missing uncertainty and the untested quality/device limits. Do not turn the prompt's long flawed record into a longer report padded with duplicate summaries or decorative visuals. Verify formula meaning, figure values, units, rounding, links, and the rendered output where available; record any unverified rendering.

## Report: brief qualitative update without forced visuals

**Prompt**

> 为研究伙伴整理一份简短中文进展更新，只要文字，不需要图表或公式，请直接组织。项目目标是统一图像质量标注规则。本周完成规则初稿，尚未进行标注一致性或模型性能评估。下一步由两名标注者独立标注同一批样本，再比较差异；样本量和判定阈值未定。受众知道领域知识，但没有读过我们的聊天记录。

**Review**

Preserve the text-only request and produce a short, self-contained update. State the goal, completed draft, unevaluated status, and next comparison without invented results, sample sizes, thresholds, owners, or dates. Do not insert a token chart, generic equation, long methods scaffold, or repeated closing summary merely to follow the visual/formula preference.

## Charts: composition, overlap, and continuous changes

**Prompt**

> Create three static figures and exact-value tables from these explicitly synthetic fixtures. Use the clinical-data chart skill and output SVG plus PNG. Figure 1: 28,552 scans, with exclusive scan-size categories 3 × 3 mm = 14,325; 6 × 6 mm = 12,194; Other / unknown = 2,033. Figure 2: 100 scans; Blur flag = 70; Motion flag = 55; Unknown status = 0. A scan may carry both flags. Figure 3: processing-time change from each pipeline's own previous implementation (different reference implementations for A and B, not a comparison of absolute processing times), in ms: A mean −2.5, supplied example 95% interval [−3.2, −1.8]; B mean +1.2, interval [+0.4, +2.0]. These intervals are fixture values, not estimates derived from counts. Also explain how count = 0, population = 0 should be labeled.

**Review**

Check 50.2%, 42.7%, 7.1% for the exhaustive composition. The overlapping flags must use 100 as denominator and keep 70%, 55%, 0% despite their sum exceeding 100%; a composition stack would be misleading. The continuous figure must retain signs, milliseconds, interval endpoints and a zero reference, with no count/share labels. The empty population has no defined percentage. Verify exact values, neutral residual categories, explicit synthetic/source labels, font coverage, clipping, overlap, and legibility in actual renders.

## Portable report use

For the chart case integrated into a report, repeat with only the report skill installed. The agent should use a suitable available plotting tool and preserve evidence semantics without requiring installation of the optional chart-style companion or claiming to have loaded it.

## Common scientific figures

Use the chart skill to generate a box plot with observations, a scatter plot and a longitudinal line with uncertainty, using a bounded synthetic example request. Verify each chart's observation unit, exact source values and statistical definitions in the image as well as the source. The optional nine-chart gallery can provide reproducible fixtures; give a fresh evaluator only its raw data, skill instructions and task, not the expected statistics.

Probe two incomplete inputs without authorizing simulation: (1) request a box plot with only mean, SD and n; (2) request individual before/after lines for two independent groups with no pair IDs. The agent should identify missing information and propose a valid alternative, without fabricating quartiles, densities or pairing.

## Titles and gray panel boundaries

Use the chart skill with a long two-line title and subtitle, first on a wide figure and then on a narrow or short figure. Repeat with Chinese labels and a heatmap colorbar. Inspect the exported PNG and SVG: the complete header must remain inside the card with padding, or wholly above the panel with a gap; it must not straddle the gray/white boundary or collide with plot decorations. Longer text should wrap and receive space, without reducing the font to illegibility. Include an actual size/font change after initial layout to check that the final render is reviewed again.
