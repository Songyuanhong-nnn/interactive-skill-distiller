# 交互式引导引擎 (Interactive Guide Engine)

> 安装名仍是 `interactive-skill-distiller`——这是历史包袱，最早它只做技能蒸馏。

一句话进来，先判断你要什么，再决定怎么陪你走：

| 你说话的样子 | 走哪条 | 产出 |
|---|---|---|
| "我想做一个 skill"、"这套流程固化下来" | **A 蒸馏** | 可复用的 `SKILL.md` |
| "帮我写/整理/做 X，但不知道从哪下手" | **B 引导执行** | 这一次要的交付物 |
| "帮我规划"、"排个计划"、"接下来怎么走" | **C 规划** | 行动序列 + 判据 + 依赖 |

三条路共用一个入口、一套档案、一种提问纪律。每轮落盘，中断可恢复，可增量迭代。

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

把仓库内所有文件复制到 `~/.workbuddy/skills/interactive-skill-distiller/`，或项目级 `<项目根>/.workbuddy/skills/` 下。装完重启会话或重新索引即可被识别。

---

## 怎么用

直接说人话，不用叫 skill 名字：

```
我想做一个 skill，帮我把每周竞品监控这套流程固化下来
帮我写一份行业分析，但我不确定从哪下手
帮我规划一下接下来三个月该做哪些事
```

触发词：`我想做一个 skill`、`这套流程固化下来`、`帮我沉淀成技能`、`帮我写 X 但不知道从哪开始`、`带我一步步来`、`帮我规划`、`排个计划`、`接下来怎么走`、`继续上次那个`。

---

## 它怎么跟你聊

每轮只问一件事，回复固定四段：

```
【进度】B · G2 第 2 步 · 已确认 3 项 / 待定 1 项
【本轮所得】……
【调研补充】……
【请你定一件事】……（2–3 个选项 + 推荐项）
```

三条路线的阶段：

```
A 蒸馏    P0 立项 → P1 调研 → P2 七维访谈 → P3 骨架 → P4 写作校验 → P5 安装
B 执行    G0 定终点 → G1 拆步 → G2 逐步做（一步一交付）→ G3 收尾校验 → G4 归档
C 规划    L0 定边界 → L1 两条候选路 → L2 拆里程碑 → L3 出计划 → L4 转执行
```

路线会换：做着做着发现"这事每周都要来一遍"，就从 B 升到 A，已有交付物直接当样例。

---

## 会话档案

默认落在 `./.skill-distill/sessions/<case-id>/`：

| 文件 | 作用 |
|---|---|
| `state.yaml` | 唯一状态源：intent、阶段、已确认项、版本 |
| `journal.md` | 逐轮对话流水，append-only |
| `decisions.md` | 设计决策 + 被否决的方案 + 理由 |
| `research.md` | 调研台账，每条须写"改变了什么" |
| `problem.md` / `goal.md` / `plan.md` | 三条路线各自的主产出 |
| `iterations/` | 每个交付版本快照，可回滚 |

加 `--store skill` 可把档案放进 skill 目录随身携带。

---

## 目录结构

```
interactive-skill-distiller/
├── SKILL.md                          主文件（路由 + 三条路线）
├── README.md
├── install.sh / install.ps1
├── references/
│   ├── routing.md                    意图判断信号表
│   ├── interview-playbook.md         A：七维度问题库
│   ├── research-playbook.md          A：调研套路
│   ├── guide-playbook.md             B：G0–G4 细节
│   ├── plan-playbook.md              C：L0–L4 细节
│   ├── validation.md                 校验清单（A–F）
│   └── journal-protocol.md           档案协议 + 版本规则
├── assets/
│   ├── skill.template.md             目标 skill 起稿模板
│   └── plan.template.md              计划表模板
└── scripts/
    └── distill_init.py               一键建 case（幂等）
```

---

## 来源

起点是 [Minksgo/AgentSkill](https://github.com/Minksgo/AgentSkill) 的一次性蒸馏流水线，遵循 [Agent Skills 规范](https://agentskills.io/specification)。v2 起从"蒸馏器"扩成"引导引擎"，三类意图共用一个入口。

v2.0.0 · 2026-11-12
