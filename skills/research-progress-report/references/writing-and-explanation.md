# Writing and Explanation

The goal is a report a reader follows on the first pass. That comes from a clear route and plain sentences, not from more checklists or denser terminology. The examples below show writing, not research results.

## 1. Fix the route before writing sentences

Privately settle the central question, the current answer, and the order in which the reader needs things. For each section, know its question, what the reader must already understand, which evidence belongs there, and how it leads to the next section. If those links are unclear, fix the structure first.

For a system or process, place each module in the whole flow before describing it, and keep steps that happen at different times apart (training, calibration, normal use, later feedback). For data, show which set contains which before describing what each subset is for.

The opening is a real overview, not a list of headings:

- **Too compressed:** "本期完成质控、校准与二次核验的联动设计，构建可信决策闭环。" The reader can't tell what the system does.
- **Clear:** "本项目希望让图像分类系统在没把握时把病例转给复核。流程是：先检查图像质量，再做初步分类；不确定的结果进入二次核验，仍无法确定的转人工。目前已完成初步分类与二次核验之间的接口原型，反馈后的学习方式还在设计。"

"下面依次介绍背景、模型和实验" is a table of contents. It doesn't tell the reader how those things relate.

## 2. Expand a question, not a pile of notes

Open each section with the question it answers or the point it makes. Add only the mechanism, reason, evidence or limit needed for that point. Put prerequisites before the step that depends on them. At a real transition, say what is still open and why the next step addresses it. Don't sprinkle stock transitions ("此外", "值得注意的是", "Furthermore") between every paragraph.

For an abstract mechanism, one concrete supplied case often explains more than another paragraph. Follow one input through the actual decisions to its output. If the model proposes a new label but the acceptance rule isn't met, say the case goes to human review; don't imply that proposing a label changes the answer.

Keep current decisions, implemented behavior, observations and future proposals visibly separate. If one section says the deployed model stays fixed, a later evaluation can't quietly assume the whole model is retrained. Name the dependency or mark it unresolved. Don't invent a more elaborate design to cover the gap.

## 3. One name per thing

Keep an internal list of each important term: the name you'll use, any aliases in the sources, what it means and what it does. Use the same name in headings, prose, figures, tables, formulas and code references.

- If sources say two names mean the same thing, say so once: "图像质量筛选（笔记中简称 QC）检查模糊和遮挡。" Then keep saying "图像质量筛选".
- Don't merge different tasks: checking whether an image is blurred and checking whether its label is right are different jobs, even if both get called "数据清洗".
- Distinguish a local subset from a similarly named project set: "训练集内的验证子集用于选模；项目测试集用于最终评价。"
- If aliases conflict or meanings drift, resolve them from the sources or name the ambiguity. A renamed label doesn't prove two things are the same.

A glossary can help a long technical document, but it doesn't replace introducing a term where it's first needed. Don't add a glossary to every report.

## 4. Explain why a concept shows up

For an unfamiliar concept, give the problem, a plain explanation and its role here, then the formal name, abbreviation or formula.

- **Name only:** "引入校准模块，完成置信分数语义对齐。"
- **Explained:** "模型给出的高分不一定代表同样高的正确率。为了让后面的判断规则有依据，先用带答案的数据检查并调整分数的含义，这一步叫校准。" Then give the actual method and evidence, without implying calibration already works.

If a term adds no needed distinction, drop it. If it's needed, keep the explanation rather than swapping it for a shorter, less familiar label.

## 5. Sentence style

### Chinese

| Do | Instead of |
|---|---|
| Use a verb: "清洗了数据", "删掉了 12 张模糊图像" | "对数据进行了清洗处理" (进行 / 开展 / 实现 / 完成 + noun) |
| Say what happens: "反馈到来后，先在模型副本上试学；只有其他病例的表现不下降才保留更新" | "通过多信号协同实现演化收益闭环" |
| Give the number and unit: "每张图耗时从 50 ms 降到 40 ms" | "处理速度大幅提升" |
| Keep "显著" for a stated statistical test | "效果显著" with no test |
| One idea per sentence; split long modifier chains | "基于多模态融合的面向临床场景的高鲁棒性的分级模型" |
| Headings that say something: "质量筛选后验证准确率从 75% 升到 80%" | "实验结果", "进展情况" |
| Paragraphs for reasoning; lists only for genuinely parallel items | An argument chopped into bullet fragments |
| Bold sparingly, for the one thing the reader must not miss | Bold on every other phrase |

Words like 赋能、抓手、闭环、底座、打通、全链路、多维度、深度融合、体系化、全面提升、突破性 usually stand in for a missing explanation. This isn't a blacklist; the test is whether you can say concretely what runs, on what, producing what. If you can, write that instead. If you can't, the sentence has no content yet.

Typography: put a space between Chinese and Latin letters or numbers (`准确率 80%`, `ResNet-18 模型`) and use full-width punctuation in Chinese sentences. Pick one convention and keep it. Introduce a technical term once as 中文名（English name, ABBR）, then use the Chinese name.

Avoid slogans, parallel-structure flourishes (排比), self-praise ("取得了重要突破") and filler openings ("随着……的快速发展"). The evidence should carry the weight.

### English

Prefer short active sentences with a concrete subject. Cut "leverage", "robust", "comprehensive", "novel", "significant" (unless tested), "in order to", and stacked hedges ("may potentially suggest"). Turn nominalizations back into verbs: "we performed an evaluation of" → "we evaluated".

## 6. Edit for meaning, then for length

Delete empty emphasis, abstract noun chains, vague pronouns and repeated evidence. Keep the reasons and context that make a short sentence understandable. An overview, a detailed section and a closing decision can visit the same topic as long as they do different jobs; don't repeat their wording.

Give each detailed fact one home. If a table already lists dataset membership and counts, the prose explains the distinction that matters instead of reciting rows. If the opening says what's done, later sections explain that work rather than adding another status inventory.

State a shared limitation once, clearly. After saying "only the interface prototype has run; performance hasn't been measured", don't end every component description with another version of "不能证明准确率提高". Repeat a caveat locally only when it prevents a different misunderstanding. A report should explain the work, not read like a repeated audit verdict.

## 7. Reader test

1. Read only the opening and the first lines of each section. Can a newcomer retell the problem, the approach, how the parts connect and what changed?
2. Read in order. For each new term, can the reader say why it's there and what it does? Can they tell similarly named sets and stages apart?
3. Trace the evidence behind each conclusion and the reason behind each next step.

If any answer depends on the chat, an unseen source or a guess, fix that passage before you shorten anything. Valid Markdown and rendered formulas don't mean the writing passes this test.
