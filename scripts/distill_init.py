#!/usr/bin/env python3
"""初始化一个蒸馏 case 目录。

用法：
    python distill_init.py --case weekly-competitor-monitor-20261109 \
        --title "每周竞品监控" [--store user|project|skill] [--root <路径>]

默认 store=project，落在 <cwd>/.skill-distill/sessions/<case-id>/
store=user   -> ~/.workbuddy/.skill-distill/sessions/<case-id>/
store=skill  -> <本脚本上级 skill 目录>/sessions/<case-id>/（跟着 skill 走）

已存在则只补缺失文件，不覆盖已有内容。
"""
from __future__ import annotations

import argparse
import datetime as _dt
import os
import re
import sys
from pathlib import Path

CASE_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

STATE_TMPL = """case_id: {case_id}
title: {title}
created: {now}
updated: {now}
status: active            # active | paused | done | abandoned
phase: P0                 # P0 P1 P2 P3 P4 P5
version: v0.1
skill_name: {skill_name}
target: user              # user | project

confirmed: []             # 已问清：trigger input steps decisions output pitfalls boundary
inferred: []              # 推断未确认
open_questions: []
dimensions_pending:
  - trigger
  - input
  - steps
  - decisions
  - output
  - pitfalls
  - boundary

research_count: 0
last_journal_line: 0
"""

PROBLEM_TMPL = """# 问题陈述 · {title}

> 三句话，每句都要能被验证。写不出第三句就回 P0 继续问。

## 谁在什么场景下卡住了


## 现在怎么凑合解决的


## 做成 skill 后应该变成什么样（完成判据）

"""

JOURNAL_TMPL = """# 会话流水 · {case_id}

> append-only。每轮一条，字段：问 / 答 / 所得 / 下一步。有调研加：查 / 结论 / 影响。

## {stamp} · 会话 1 · P0
- **问**：
- **答**：
- **所得**：
- **下一步**：
"""

RESEARCH_TMPL = """# 调研台账 · {title}

> 每条必须有"改变了什么"。写不出影响的记录删掉。

## R-001 · {date} ·
- 来源：
- 查到了什么：
- 改变了什么：
- 可信度：高 / 中 / 低
"""

DECISIONS_TMPL = """# 设计决策 · {title}

> 包括被否决的方案。三个月后靠这个解释"为什么这么设计"。

## D-001 · {date} ·
- 选项：
- 选定：
- 理由：
- 否决其他选项的原因：
- 影响：
- 状态：已确认（用户） / AI 代定，待验证 / 已废弃
"""

PARKING_TMPL = """# 跑题暂存 · {title}

> 会话结束逐条处理：并入 / 另开 case / 丢弃。

"""

DRAFT_TMPL = """---
name: {skill_name}
description: >-
  <做什么 + 什么时候用，含 3–5 个用户真实会说的触发短语>
license: MIT
---

# <展示名称>

## 用途


## 何时用


## 何时不用


## 流程

### 步骤 1：

**验证**：

## 易错点

- ❌ → ✅

## 参考

- 无
"""


def resolve_case_dir(store: str, root: str | None, case_id: str) -> Path:
    if root:
        return Path(root).expanduser().resolve() / case_id
    if store == "skill":
        return Path(__file__).resolve().parent.parent / "sessions" / case_id
    if store == "user":
        return Path.home() / ".workbuddy" / ".skill-distill" / "sessions" / case_id
    return Path.cwd() / ".skill-distill" / "sessions" / case_id


def write_if_absent(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description="初始化 skill 蒸馏 case")
    ap.add_argument("--case", required=True, help="case-id，kebab-case")
    ap.add_argument("--title", required=True, help="人类可读标题")
    ap.add_argument(
        "--store",
        default="project",
        choices=["project", "user", "skill"],
        help="档案存放位置",
    )
    ap.add_argument("--root", default=None, help="自定义根目录（覆盖 store）")
    ap.add_argument("--skill-name", default=None, help="目标 skill 名，默认沿用 case-id 去掉日期")
    args = ap.parse_args()

    case_id = args.case.strip()
    if not CASE_RE.match(case_id):
        print(f"[x] case-id 不合法：{case_id!r}", file=sys.stderr)
        print("    需匹配 ^[a-z0-9]+(-[a-z0-9]+)*$（小写、连字符）", file=sys.stderr)
        return 2

    skill_name = args.skill_name or re.sub(r"-\d{8}$", "", case_id)
    if not CASE_RE.match(skill_name):
        print(f"[x] skill-name 不合法：{skill_name!r}", file=sys.stderr)
        return 2

    case_dir = resolve_case_dir(args.store, args.root, case_id)
    case_dir.mkdir(parents=True, exist_ok=True)
    (case_dir / "iterations").mkdir(exist_ok=True)

    now = _dt.datetime.now().astimezone()
    ctx = {
        "case_id": case_id,
        "title": args.title,
        "skill_name": skill_name,
        "now": now.isoformat(timespec="seconds"),
        "date": now.strftime("%Y-%m-%d"),
        "stamp": now.strftime("%Y-%m-%d %H:%M"),
    }

    files = {
        "state.yaml": STATE_TMPL,
        "problem.md": PROBLEM_TMPL,
        "journal.md": JOURNAL_TMPL,
        "research.md": RESEARCH_TMPL,
        "decisions.md": DECISIONS_TMPL,
        "parking-lot.md": PARKING_TMPL,
        "SKILL.draft.md": DRAFT_TMPL,
    }

    created, kept = [], []
    for name, tmpl in files.items():
        p = case_dir / name
        (created if write_if_absent(p, tmpl.format(**ctx)) else kept).append(name)

    print(f"[+] case: {case_id}")
    print(f"    title: {args.title}")
    print(f"    skill: {skill_name}")
    print(f"    dir  : {case_dir}")
    print(f"    新建 : {', '.join(created) if created else '(无)'}")
    if kept:
        print(f"    保留 : {', '.join(kept)}")
    print()
    print("    下一步：P0 用一句话问清场景，然后填 problem.md 三句话")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
