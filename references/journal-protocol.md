# 档案协议

档案是这场会话唯一不会消失的部分。**没有档案的访谈等于没发生。**

---

## 目录结构

```
<case-dir>/
├── state.yaml        机器可读的进度（唯一状态源）
├── problem.md        A：问题陈述（三句话）
├── goal.md           B：终点判据（形态 / 读者 / 通过线）
├── plan.md           C：候选路 + 选定方案 + 里程碑表
├── journal.md        对话流水，append-only
├── research.md       调研台账，append-only
├── decisions.md      设计决策与否决记录，append-only
├── parking-lot.md    跑题想法暂存
├── SKILL.draft.md    草稿
└── iterations/
    ├── v1.0.md
    └── v1.1.md
```

默认 `<cwd>/.skill-distill/sessions/<case-id>/`。
`--store skill` 时放 `<skill 目录>/sessions/<case-id>/`（跟着 skill 走，换项目也带着）。

---

## state.yaml 字段

```yaml
case_id: competitor-monitor-20261109
title: 每周竞品监控
created: 2026-11-09T13:20:00+08:00
updated: 2026-11-09T14:05:00+08:00
status: active          # active | paused | done | abandoned
intent: A               # A 蒸馏 | B 引导执行 | C 规划
phase: P2               # A: P0–P5 | B: G0–G4 | C: L0–L4
intent_history: []      # 换道记录：[{from, to, reason, at}]
version: v0.5           # 当前草稿版本
skill_name: weekly-competitor-monitor
target: user            # user | project

confirmed:              # 已问清的维度
  - trigger
  - input
  - output
inferred:               # 推断但未确认
  - decisions
open_questions:
  - 决策点 4：金额阈值到底是多少
dimensions_pending:
  - steps
  - pitfalls
  - boundary

research_count: 4
last_journal_line: 47   # 用于续写定位
```

规则：
- `state.yaml` 是**唯一状态源**。恢复会话只读它，不靠翻聊天记录。
- 每轮对话结束更新一次 `updated`、`phase`、`confirmed`、`last_journal_line`。
- `intent` 只在开场判一次；换道时改值并往 `intent_history` 追加，不覆盖历史。
- `status: done` 之后仍可被 REFINE 唤醒，改回 `active`。

---

## journal.md 格式

append-only，只增不改。每次会话开头写分隔头，之后每轮一条。

```markdown
# 会话流水 · competitor-monitor-20261109

## 2026-11-09 13:20 · 会话 1 · P0
- **问**：这个 skill 帮谁、在什么时刻、把什么事做完？（选项 A/B/C/D）
- **答**：B，团队每周一要做竞品价格对比，现在靠人肉翻 5 个站
- **所得**：场景明确，周频，5 个数据源
- **下一步**：P1 调研，先看有没有同类 skill

## 2026-11-09 13:26 · 会话 1 · P1
- **查**：~/.workbuddy/skills/ 无同类；WebSearch "competitor price monitoring workflow"
- **结论**：行业标准三段式 采集→归因→预警（见 R-002）
- **影响**：流程按三段拆，不按"打开网页"拆
```

字段固定四个：**问 / 答 / 所得 / 下一步**。有调研就加 **查 / 结论 / 影响**。

要求：
- 用户的回答尽量保留原话片段（后面写触发词要用）
- "所得"必须是你自己的判断，不是复述
- 一轮一条，不要合并多轮

---

## decisions.md 格式

记所有"做了选择"的地方，包括被否决的。这是三个月后还能解释"为什么这么设计"的唯一依据。

```markdown
## D-004 · 2026-11-09 · 输出格式定为 Markdown 表格
- 选项：A 表格 / B 邮件正文 / C 飞书卡片
- 选定：A
- 理由：用户实际交付就是贴到群里，表格最快
- 否决 B/C 的原因：B 需要额外排版，C 要接 API 超出范围
- 影响：输出章节、第五步验证条款
- 状态：已确认（用户）
```

`状态` 三选一：`已确认（用户）` / `AI 代定，待验证` / `已废弃`

---

## parking-lot.md 格式

跑题时接住想法，不打断当前维度。

```markdown
- [ ] 用户提到想顺便做"竞品公众号更新追踪"——超出本次范围，P5 后再评估
- [ ] 提到现有脚本在 /tools/scrape.py，可作为实现参考
```

会话结束时逐条过一遍：并入 / 另开 case / 丢弃。

---

## 版本规则

| 版本 | 时机 | 位置 |
|---|---|---|
| v0.1 | P0 完成 | state.yaml |
| v0.5 | P3 骨架确认 | state.yaml |
| v1.0 | P5 首次安装 | iterations/v1.0.md |
| v1.x | 内容补充（加步骤、改触发词） | iterations/v1.x.md |
| v2.0 | 结构重排（流程重组、边界改写） | iterations/v2.0.md |

每次迭代：
1. 复制当前 `SKILL.draft.md` 到 `iterations/v<新版本>.md`
2. 文件头加变更摘要（改了什么 / 为什么 / 影响哪些章节）
3. 更新 `state.yaml` 的 `version` 与 `updated`
4. `decisions.md` 追加一条

**永远保留旧版本**，回滚靠它。

---

## 恢复会话

用户说"继续上次那个 X" 时：

1. `ls ./.skill-distill/sessions/*/state.yaml`（以及 skill store 目录）
2. 按 `updated` 倒序找最近的、`status != done` 的，或标题匹配的
3. 读 `state.yaml` → 读 `journal.md` 末尾 20 行 → 读 `decisions.md` 末尾 5 条
4. 输出一行确认："接上 <case-id>，当前 P2，还差 步骤链/易错点/边界 三维度"
5. 从 `dimensions_pending` 第一条继续，不要重头问

不要要求用户复述之前说过的东西——档案里有。

---

## 三条路线的档案差异

底座一样，只有主产出文件不同。恢复时先读 `intent`，就知道该看哪个。

| 文件 | A 蒸馏 | B 引导执行 | C 规划 |
|---|---|---|---|
| `problem.md` | 必填（P0） | — | — |
| `goal.md` | — | 必填（G0） | 可复用（目标一致） |
| `plan.md` | — | — | 必填（L1–L3） |
| `research.md` | 必填 ≥3 条 | 按需 | 按需 |
| `SKILL.draft.md` | 必填 | — | — |
| `iterations/` | v1.0 = SKILL.md | v1.0 = 交付物 | v1.0 = plan.md |

**换道时的文件迁移**（不删旧文件，只改用途）：

- B → A：`goal.md` 直接改写成 `problem.md`，交付物进 `iterations/` 当样例
- C → B：`plan.md` 的里程碑直接变成 G1 的步骤，`goal.md` 从计划目标抄一行
- A → B：`problem.md` 的三句话里第三句就是 `goal.md` 的通过线

**恢复会话时**：`intent` 决定读哪个主文件，`phase` 决定从哪继续。两个都读，缺一不可。
