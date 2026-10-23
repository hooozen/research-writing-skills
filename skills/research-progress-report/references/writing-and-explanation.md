# Organize First, Then Explain

Use this guide for drafting, restructuring, or repairing unclear reports. The aim is a report the reader can follow on first reading, not a longer checklist or a denser collection of technical terms. The examples below are schematic writing examples, not research results.

## Establish the route before expanding it

Privately identify the central question, supported answer or current state, and the reader's route through the explanation. For each proposed section, identify its question, prerequisite context, relevant evidence, and connection to what follows. If those connections are unclear, repair the organization before writing more detail.

For a process or module, establish its place in the whole system and distinguish steps that occur at different times. For data, show parent–child or overlap relationships before listing local roles. For a proposed solution, explain the actual problem before its mechanism. Do not choose extra components merely because the sources mention them.

The visible opening should give a substantive overview, not expose the internal planning map. For example:

- **Too compressed:** “本期完成质控、校准与二次核验的联动设计，构建可信决策闭环。” The reader cannot tell what the system does or how the pieces relate.
- **Clearer:** “本项目希望让图像分类系统在把握不足时转交复核。整体流程是先检查图像质量，再做初步分类；不确定的结果进入二次核验，仍无法确定的转人工。目前已完成初步分类与二次核验之间的接口原型，反馈后的学习方式仍在设计。” This establishes purpose, flow, and current status before implementation details.

An overview is not an inventory. “下面依次介绍背景、模型和实验” gives a directory, not the relationship between those subjects. Preserve a user outline, but make the connections within it explicit. In a very short update, the first sentence can do this work.

## Expand a question, not a pile of source fragments

Start each section with the question it answers or the point it establishes. Add only the mechanism, rationale, evidence, or limit needed to understand that point. Place a prerequisite before the operation that depends on it. At a substantial transition, identify what remains unresolved and why the next step addresses it; avoid adding stock transition phrases between every paragraph.

For an interface or mechanism, a concrete supplied example often explains more than another abstract paragraph. Follow one input through the actual decisions to its output. For example, if a model proposes a revised label but the acceptance rule is unmet, say that the case is sent for human review; do not imply that proposing a label automatically changes the answer. A process diagram should show this distinction too.

Keep current decisions, implemented behavior, observations, and future proposals separate. If an earlier section says the deployed model stays fixed, a later evaluation cannot silently claim that updating the whole model measures the value of a different deployed action. Explain the dependency or identify the design as unresolved. Do not invent a more complex design to hide the gap.

## Keep names and meanings stable

Maintain an internal map of canonical name, supplied aliases, meaning, and role for important terms. Use it across headings, text, figures, tables, formulas, and relevant code identifiers. Choose names that make the real distinction visible.

- If the sources establish equivalence, introduce it once: “图像质量筛选（笔记中简称 QC）检查模糊和遮挡。” Continue using “图像质量筛选”.
- Do not merge related but distinct tasks: checking whether an image is blurred and checking whether its label is correct are different operations. State their relationship rather than calling both “数据清洗” without explanation.
- Distinguish a local subset from a similarly named project set: “训练集内的验证子集用于选模；项目测试集用于最终评价。” Preserve the supplied actual roles; do not infer them from names alone.
- If aliases conflict or scope changes, resolve the meaning from the sources or state the ambiguity. A renamed label is not evidence that two entities are identical.

A glossary can help a long technical document, but it cannot replace introducing a concept where it is first needed. Do not add a visible terminology table to every report.

## Explain why a new concept appears

For a consequential unfamiliar concept, connect the current problem, a plain explanation, and its role here. Then supply the formal name, abbreviation, or equation if it helps. Calibrate depth to the audience; explain the project-specific use even when the underlying method is familiar.

- **Name without explanation:** “引入校准模块，完成置信分数语义对齐。”
- **Explain the role:** “模型给出的高分不一定代表同样高的正确率。为了让后续判断规则有可靠依据，先用带答案的数据检查和调整分数的解释；这一步称为校准。” Follow with the actual method and evidence when available, rather than implying that calibration is already successful.

Technical synonyms, English full names, and formulas do not explain purpose by themselves. If a term adds no necessary distinction, remove it. If a concept is needed, keep the explanation rather than replacing it with a shorter unfamiliar label.

## Edit for meaning, then brevity

Prefer a concrete actor, action, object, and consequence. For example, replace “通过多信号协同实现演化收益闭环” with the actual supported procedure: “得到可靠反馈后，先在模型副本上尝试学习；只有其他病例的表现改善、原有能力也保持得住，才考虑保留更新。” This is a schematic design explanation, not a claim that a tested system has achieved those outcomes.

Delete empty emphasis, abstract noun chains, ornate academic wording, unexplained pronouns, and repeated evidence. Keep the reasons and context that make a short sentence understandable. A useful overview, a detailed explanation, and a final decision can revisit the same topic while doing different jobs; avoid repeating their wording or full contents.

Give detailed information one main home. If a table or hierarchy already shows dataset membership and counts, prose should explain the consequential distinction rather than repeat every row and total. If the opening states what is complete, later sections should explain that work rather than add another status inventory. Include a separate status table only when it adds a useful comparison.

Consolidate shared evidence limits. For example, after clearly stating that only an interface prototype was exercised and performance has not been measured, do not end every component description with another version of “不能证明准确率提高”. Retain a local qualification when it prevents a different misunderstanding, such as distinguishing a proposed label from an accepted answer. A report should explain the work, not read like a repeated audit verdict.

Use a figure to expose relationships or evidence and a formula to specify a quantity. Before either, establish the question; after it, state the necessary interpretation or limit. Do not make readers decode a diagram of undefined terms or infer a method's purpose from its equation.

## Read as someone new to the project

First read only the opening and section openings. Can the reader explain the central problem, overall approach, how the pieces connect, and what changed? Then read in order. For each important new term, can the reader say why it appears and what it does here? Can they distinguish similarly named entities, data subsets, and stages? Finally, trace the evidence behind each conclusion and the reason behind the next action.

If any answer depends on the chat, an unseen source, or a relationship the reader must guess, repair that passage. Do this before final shortening. Structural validation and correct formula rendering do not establish that the writing passes this reader check.
