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

## Report: whole-system explanation, aliases, and stage boundaries

**Prompt**

> 将零散研发笔记整理为一份中文阶段报告，给有机器学习基础、不了解本项目的跨学科研究人员讨论，请自行组织结构。全部为虚构教学材料，须标明，不新增实验。目标是让甲/乙图像分类在不确定时转交核验或人工。300张图像分为development 240张与test 60张；development内含initial 180张与calibration 60张；initial内144张拟合原模型、36张内部验证。内部验证不是test。“初判”和“快速判别”指同一组件，“二次核验”和“复核”指同一组件；质量筛选独立检查模糊或遮挡，不是二次核验的别称。普通使用时先质量筛选，再初判；初判产生类别与原始分数，原始分数不等于答对概率。calibration只用于调整分数解释和选定判断规则，在正式使用前完成。规则决定直接返回还是二次核验；核验收到图像、初判结果、参考图像及来源类别，产生候选答案与理由；本地规则仍无法接受时转人工。核验不更新初判模型。另一份笔记称“经验吸收器”，指可靠反馈到来后复制一个小型附加模块进行试学，原模型冻结；该附加模块称适配器，只学习判断的小幅修正。普通推理与反馈后的学习在不同时间发生。学习后的收益比较方案尚未确定，不能自行指派数据集职责。接口例子：图像通过质量筛选，初判甲，规则要求复核；复核提出乙，但本地证据不足，最终转人工，未自动改答、未自动训练。当前只完成初判与核验间接口原型及流程演练，适配器仍为设计；无性能、延迟或正式实验结果。下一步先确定更新比较方案，再实现学习模块。

**Review**

Read the report as a new project reader, not as a checklist of keywords. Its opening should establish the purpose, the normal-use route, the separate feedback-learning role, and current status before technical exposition. Section openings should form a coherent route, with details expanding that overview. Expect stable canonical names with necessary aliases explained once, quality screening kept distinct from label verification, and the adapter introduced through its purpose rather than merely named. Training/calibration, runtime verification, and later learning must remain separate; the supplied example ends in human review rather than automatic relabeling or training. Trace the parent–child dataset membership and distinguish 36-image internal validation from 60-image test. Do not let the unresolved learning comparison acquire invented dataset assignments, thresholds, parameters, results, or extra architecture. A compact flow/hierarchy can clarify relationships but cannot replace their meaning. Check for repetition: prose should interpret rather than recite every table row, and common missing-performance limits should not reappear at every section ending or in duplicate status inventories. No separate outline-approval question is needed. Record actual passages that explain relationships or still force the reader to guess; valid syntax alone is not a pass.

## Report: local revision without expanding the assignment

**Prompt**

> 以下是中文研究伙伴报告中的一个段落，只修改这一段，保留标题“本期变化”，不加术语表、图表或新方案。项目通过检查图像模糊程度来减少不合格输入，本期只实现质量规则，未评估效果；“图像质控”和“QC”在资料中指这同一项检查，和后续检查分类标签正确性的“标签核验”不同。原文：“本期构建QC治理与数据清洗协同底座，赋能标签核验闭环，全面提升下游泛化鲁棒性。”

**Review**

The revised paragraph should plainly identify what was implemented, why it exists, and what remains untested. It should use one clear canonical name, explain an alias only if retained, and keep image-quality screening distinct from label verification. No established downstream benefit follows from implementing a rule. Preserve the local-edit scope and heading; do not force a new whole-report scaffold, approval step, glossary, formula, or future architecture. Verify the actual prose conveys the relationship without relying on terms such as “底座” or “闭环” to stand in for an explanation; do not impose a universal word blacklist.

## Report: detailed model methods and custom module

**Prompt**

> 为有机器学习基础但不了解项目的跨学科研究人员，写一份可独立阅读的中文 Markdown 组会报告，请组织结构。以下全部是合成教学材料，须显著标明，不新增实验。目标是二分类，阳性为甲。固定清单 split-v1 按受试者划分，互不重叠：训练16人192图、验证4人48图、测试10人60图，三个集合各有一半甲、一半乙。训练拟合参数，验证早停和选模，测试最终评价。输入单通道32×32；固定缩放后用训练集 mean=0.5/std=0.2 归一化，无增强。网络为 Conv2d(1,8,kernel=3,stride=1,padding=1) → ReLU → 自定义通道门控 → 全局平均池化 → Linear(8,1) logit。门控内部：对输入 B×8×32×32 全局平均得到 B×8，Linear(8,2) → ReLU → Linear(2,8) → sigmoid 得到 B×8 权重，reshape 为 B×8×1×1 后广播逐元素乘回原特征。所有参数随机初始化并训练，无冻结，无训练专用分支；门控借鉴 SE，当前无消融，不能声称门控带来收益。用整体图与门控展开图解释实际数据流，参考经典论文的画法并标明来源，不直接照搬网络。损失为无类别权重、无平滑、按样本平均的二元交叉熵，直接由 logits 计算；无额外正则项。Adam，lr=0.001，weight decay=0，恒定学习率；每设备 batch=8、2设备数据并行、梯度累积2次，每个 epoch 12个全局 minibatch、6次优化器更新。计划最多10 epochs，实际6 epochs/36次更新；每 epoch 验证。早停监控验证平均 BCE，越小越好，patience=2个验证轮次、min_delta=0、无预热。epoch4 验证 loss=0.42，为唯一最优；epoch5=0.43、epoch6=0.44，之后早停并恢复 epoch4（第24次更新）权重作为 ckpt-e4。训练随机种子11，其他运行环境信息未提供。最终推理用同样归一化和 sigmoid，固定阈值0.5，不做校准、测试增强或集成。ckpt-e4 在测试集 TP=24、FN=6、TN=27、FP=3；报告 accuracy、sensitivity、specificity 的公式、目的和结果。旧基线在相同测试集/推理协议下答对48/60，仅有该准确率；无逐图配对记录、置信区间或统计检验。总结与旧基线相比的观察和局限，不推断外部泛化或单模块贡献。完整细节可放明确链接的附录。

**Review**

Read the actual report and inspect both diagrams. Expect 300 images from 30 subjects, split proportions with explicit subject/image denominators, grouped independence, balanced classes and clear training/selection/testing boundaries. Trace B×1×32×32 → B×8×32×32 through the gate and B×8 → B×1; verify the gate's pooling, 8→2→8 projections, sigmoid, reshape and multiplication. Do not substitute addition or a stock SE diagram for this implementation. The mean BCE formula must define binary targets and probabilities/logits, its sample denominator and absence of extra terms; distinguish it from evaluation metrics. Expect effective batch 32, planned versus actual training duration, 12 minibatches versus 6 updates per epoch, stopping at epoch 6 and selection of epoch 4/update 24. Report supplied settings without guessing the runtime. Expect accuracy 85%, sensitivity 80%, specificity 90%, versus baseline accuracy 80% (+5 percentage points, +6.25% relative); no baseline sensitivity/specificity can be inferred. Explain metric purpose and positive class/threshold. No significance, exact corrected-case count, module attribution or external generalization follows. Methods may be in a linked appendix, but must remain present and understandable. Verify formulas, shapes, numbers, source/version labels and actual diagram readability; record any unavailable render inspection.

## Report: incomplete model evidence without fabricated completion

**Prompt**

> 为研究伙伴写一份不完整的中文模型研发进展草稿，请直接组织并标明缺失资料。目标是图像二分类，本周只把 ResNet-18 和一个自定义融合模块接通，尚未训练、早停、选模或评价。资料只有240张图像来自20人，拟按人划分，但比例和清单未定；自定义模块只知道接收两个分支，分支来源、张量尺寸、内部操作和融合方式都未提供。没有训练配置、损失定义、性能或引用。图能画到已有事实即可，不要自行设计模块，也不要用常见设置填空。

**Review**

Expect a visibly incomplete draft with the known dataset size/unit, proposed subject-level split, integration status and specific missing inputs for split counts, actual architecture/module internals, loss, batch/optimizer/duration, stopping/selection and metrics/evaluation. A bounded diagram may show confirmed connectivity with unresolved inputs/operations clearly marked, but must not manufacture a standard ResNet variant's exact dimensions, concatenation, attention or module computation. Treat training/selection/evaluation as not performed, not as completed with unavailable scores; loss and training settings are unprovided, not confirmed absent. Do not generate guessed formulas, a 70/15/15 split, default BCE, a “disabled early stopping” claim, fake performance or empty result charts. Explain what evidence is required to complete the model account without turning the report into repeated boilerplate warnings. A classical-paper citation supports the reference architecture, not the unspecified custom module or actual run.

## Charts: composition, overlap, and continuous changes

**Prompt**

> Create three static figures and exact-value tables from these explicitly synthetic fixtures. Use $scientific-chart-style and output SVG plus PNG. Figure 1: 28,552 scans, with exclusive scan-size categories 3 × 3 mm = 14,325; 6 × 6 mm = 12,194; Other / unknown = 2,033. Figure 2: 100 scans; Blur flag = 70; Motion flag = 55; Unknown status = 0. A scan may carry both flags. Figure 3: processing-time change from each pipeline's own previous implementation (different reference implementations for A and B, not a comparison of absolute processing times), in ms: A mean −2.5, supplied example 95% interval [−3.2, −1.8]; B mean +1.2, interval [+0.4, +2.0]. These intervals are fixture values, not estimates derived from counts. Also explain how count = 0, population = 0 should be labeled.

**Review**

Check 50.2%, 42.7%, 7.1% for the exhaustive composition. The overlapping flags must use 100 as denominator and keep 70%, 55%, 0% despite their sum exceeding 100%; a composition stack would be misleading. The continuous figure must retain signs, milliseconds, interval endpoints and a zero reference, with no count/share labels. The empty population has no defined percentage. Verify exact values, neutral residual categories, explicit synthetic/source labels, font coverage, clipping, overlap, and legibility in actual renders.

## Portable report use

For the chart case integrated into a report, repeat with only the report skill installed. The agent should use a suitable available plotting tool and preserve evidence semantics without requiring installation of the optional chart-style companion or claiming to have loaded it.

## Common scientific figures

Use the chart skill to generate a box plot with observations, a scatter plot and a longitudinal line with uncertainty, using a bounded synthetic example request. Verify each chart's observation unit, exact source values and statistical definitions in the image as well as the source. The optional nine-chart gallery can provide reproducible fixtures; give a fresh evaluator only its raw data, skill instructions and task, not the expected statistics.

Probe two incomplete inputs without authorizing simulation: (1) request a box plot with only mean, SD and n; (2) request individual before/after lines for two independent groups with no pair IDs. The agent should identify missing information and propose a valid alternative, without fabricating quartiles, densities or pairing.

## Physical typography, long labels and colorbars

Use $scientific-chart-style with a long two-line header, first at 180 mm and then reflowed to 89 mm width, including a short fixed-height canvas. Repeat with Chinese labels and a heatmap colorbar, in B and D modes. Inspect the actual PNG, editable SVG and PDF at final size: titles, panel letters, axes, colorbar labels and legends must not overlap or be clipped. Long text should wrap and receive space without shrinking the physical font to fit. Export DPI must not change point sizes. A fixed canvas that is genuinely too small should cause re-layout or an honest limitation rather than an illegible export. Verify data, limits and group identities remain the same in print mode, with redundant marker/line distinctions. The white publication layout has no gray rounded card. Include an actual resize and export-backend change to check the final render again.

## Scientific chart: paired observations in both modes

**Prompt**

> 为paper准备一幅89mm单栏的前后配对图，彩色默认版与黑白打印版各一份，输出可编辑SVG和PNG，图注用中文。全部是合成教学数据须标明；每行为同一独立样本前后测量，单位a.u.：S1 10→8，S2 11→9，S3 12→11，S4 9→8，S5 10→缺失，S6 13→10，S7 8→9，S8 11→10。只展示已提供的观测，不新增实验或统计检验。

**Review**

Inspect the actual figures and caption. Expect seven complete trajectories matched by ID, with S5's missing follow-up disclosed and no invented zero or connecting line to a fabricated value. A figure may also retain S5's observed baseline if distinguished and explained; it must not silently turn eight enrolled units into eight pairs. Preserve a.u., explicitly synthetic labels, exact values and the same limits/group identities in both modes. Expect B colors and a designed D print mode with readable point/line distinctions, 89 mm export width and editable SVG text. Check final-size glyphs, legend/label collisions and traceable data; no significance or unsupported interval should appear.

## Advanced chart definitions and incomplete inputs

Run bounded independent requests using raw supplied data: tied positive/negative scores for ROC/PR, probabilities with an empty calibration bin, two paired measurement vectors for agreement, and durations/events including an event/censor tie for KM. Use a known p-value vector with shuffled order for BH and a small feature matrix for PCA. Do not give an evaluator the computed expectations. Review actual curve points, AP versus trapezoidal PR area, bin support and empty-bin gaps, B−A direction and LoA versus confidence limits, risk-set timing and censor marks, restored BH order, and actual PCA explained variance. Inspect color/print exports and numeric companions, not just summary labels.

Also probe a requested violin from mean/SD/n, ROC from only a confusion matrix, and KM from only aggregate event proportions. The skill should identify the missing observations/scores/durations instead of fabricating them. Do not force inference or an advanced chart when the supplied evidence supports only a simpler descriptive display.

## Agent reference retrieval: one chart, supplied input

Give an independent Agent only the skill path and this prompt, with an isolated output directory. Ask it to record files actually opened and commands used after fulfilling the task; do not supply review criteria or require it to inspect every reference.

**Prompt**

> 请用我给出的合成验证数据做一张ROC单图，正类为1，使用默认配色，导出可编辑SVG和PNG，并简要说明AUC。不要使用skill内置示例数据，不新增置信区间或检验。label=[0,1,0,1,1,0,0,1]；score=[0.1,0.9,0.6,0.6,0.8,0.4,0.6,0.2]。

**Review**

Verify that the Agent finds the ROC card via the text/JSON index, reads only relevant material and uses supplied input rather than example mode. It should not need a nine-panel image, all chart cards or a full gallery's source. Expect a single ROC with AUC 0.750, tie-grouped thresholds, eight supplied observations and editable SVG text. Check actual files, values and rendered PNG, not merely the final claim. Record retrieval/implementation obstacles rather than assuming file counts establish lower token use.

## Agent reference retrieval: the nineteenth chart and print mode

**Prompt**

> 给这批合成演示记录画一张计数与占比条形图，N=100条记录，标记A有70条、标记B有55条，同一记录可以同时带两个标记。图上直接标注数量和占比，单位为记录，使用黑白打印模式，导出SVG和PNG。不要调用整套图册或改用内置例子。

**Review**

Verify direct discovery of `count_share`, one-chart invocation and D print encodings. Expect 70/100 and 55/100, no normalization by 125 and no composition stack. Keep supplied units, denominator, overlap and synthetic status explicit, including localized structural labels when Chinese is selected. Record only files actually read, verify absence of unrelated figure exports and inspect readability at final size.

## Agent reference retrieval: insufficient raw observations

**Prompt**

> 我需要两个实验组的小提琴图，只有这些汇总值：A组mean=10、SD=2、n=30；B组mean=12、SD=3、n=28。请用paper风格。这里没有提供原始观测，也没有授权生成模拟数据。

**Review**

The Agent should locate the violin requirements and state that these summaries cannot determine a density or raw distribution. It must not generate pseudo-observations or run a synthetic example as the answer. A clearly labeled mean±supplied-SD alternative is permissible, provided it is distinguished from the requested violin, retains supplied n, invents no units/independence, and adds no unsupported SE/CI/test. Record questions that would be necessary for the violin. In bounded testing, keep questions in the output record rather than contacting a real user.
