# 交互式技能蒸馏器 (Interactive Skill Distiller)

把一个模糊想法、工作流或经验，通过**多轮对话引导 + 主动调研**，一步步蒸馏成可执行的 Agent Skill（`SKILL.md`）。

与一次性蒸馏的区别：它会问你问题、会去查资料、会把每一轮对话和决策写进磁盘、能中断后接着来、能增量迭代。

仓库：https://github.com/Songyuanhong-nnn/interactive-skill-distiller
站点：https://songyuanhong-nnn.github.io/interactive-skill-distiller/

---

## 安装

### 方式一：脚本（推荐）

在**本仓库根目录**执行（clone 或解压后进入该目录）：

```bash
# macOS / Linux / Git Bash
bash install.sh

# Windows PowerShell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

若你在上一级目录、目录名为 `interactive-skill-distiller`，则改用 `bash interactive-skill-distiller/install.sh`。

默认装到 `~/.workbuddy/skills/interactive-skill-distiller`，可传路径参数改位置。

### 方式二：git clone

```bash
git clone https://github.com/Songyuanhong-nnn/interactive-skill-distiller.git \
  ~/.workbuddy/skills/interactive-skill-distiller
```

### 方式三：手动

把仓库内所有文件复制到：

```
~/.workbuddy/skills/interactive-skill-distiller/
```

或项目级：`<项目根>/.workbuddy/skills/interactive-skill-distiller/`

装完重启会话或重新索引即可被识别。

---

## 怎么用

直接说人话就行，不需要叫 skill 名字：

```
我有个想法想做成的 skill，但还没想清楚，帮我一步步聊出来
把"每周竞品监控"这套流程固化成 skill
继续上次那个竞品监控的 skill，加一个自动生成周报的能力
看看那个 skill 的档案，当时为什么把触发词定成这样
```

触发词：`我想做一个 skill`、`把这个想法变成技能`、`这套流程想固化下来`、`帮我把经验沉淀成 skill`、`继续上次那个技能`、`给这个 skill 补点东西`。

---

## 它会怎么和你聊

每轮只问一件事，回复固定四段：

```
【进度】P2 访谈 · 维度 4/7 · 已确认 3 项 / 待定 2 项
【本轮所得】……
【调研补充】……
【请你定一件事】……（2–3 个选项 + 推荐项）
```

六阶段：`P0 立项` → `P1 调研` → `P2 七维度访谈` → `P3 骨架确认` → `P4 写作校验` → `P5 安装迭代`

---

## 会话档案

默认落在 `./.skill-distill/sessions/<case-id>/`：

| 文件 | 作用 |
|---|---|
| `state.yaml` | 唯一状态源：阶段、已确认维度、版本、status |
| `journal.md` | 逐轮对话流水，append-only |
| `research.md` | 调研台账，每条必须写"改变了什么" |
| `decisions.md` | 设计决策 + 被否决的方案 + 理由 |
| `problem.md` | P0 的三句话问题陈述 |
| `iterations/` | 每个交付版本快照，可回滚 |

加 `--store skill` 可把档案放进 skill 目录随身携带。

---

## 目录结构

```
interactive-skill-distiller/
├── SKILL.md                          主文件（六阶段流程）
├── README.md                         本文件
├── install.sh / install.ps1          安装脚本
├── references/
│   ├── interview-playbook.md         七维度问题库 + 追问话术
│   ├── research-playbook.md          调研套路 + 台账格式
│   ├── validation.md                 校验清单（硬性/建议/会话特有）
│   └── journal-protocol.md           档案协议 + 版本规则
├── assets/
│   └── skill.template.md             目标 skill 起稿模板
└── scripts/
    └── distill_init.py               一键建 case（幂等）
```

---

## 来源

改造自 [Minksgo/AgentSkill](https://github.com/Minksgo/AgentSkill) 的一次性蒸馏流水线，遵循 [Agent Skills 规范](https://agentskills.io/specification)。

v1.0.0 · 2026-11-09
