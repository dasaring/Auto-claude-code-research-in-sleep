# ARIS Agent Guide

> **For AI agents reading this repo cold.** If you are a human, see [README.md](README.md) or [docs/ARIS_INTRO.html](https://wanshuiyin.github.io/Auto-claude-code-research-in-sleep/ARIS_INTRO.html).

ARIS is a research harness: composable Markdown skills that orchestrate the ML research lifecycle through cross-model adversarial collaboration. Executor (Claude / Codex / Cursor / Antigravity / Copilot CLI) writes code & papers; reviewer (GPT-5.5 via Codex MCP, or Claude / Gemini via `claude-review` / `gemini-review` MCP) critiques in fresh threads.

> **Source of Truth.** This file is a *routing index*, not a specification.
> Behavior of a skill lives in `skills/<name>/SKILL.md`. System-wide
> contracts live in `skills/shared-references/*.md`. If this guide
> conflicts with a SKILL.md, the **SKILL.md wins**.

## Skill Locations & Platforms

| Platform | Skill root | Notes |
|----------|-----------|-------|
| Claude Code / Cursor / Trae / Antigravity / Copilot CLI | `skills/<name>/SKILL.md` | Mainline skills; native `SKILL.md` invocation |
| Codex CLI | `skills/skills-codex/<name>/SKILL.md` | Codex mirror; uses `spawn_agent` instead of `mcp__codex__codex` |
| Codex + Claude-review | `skills/skills-codex-claude-review/` | Overlay on top of `skills-codex/` |
| Codex + Gemini-review | `skills/skills-codex-gemini-review/` | Same pattern, Gemini reviewer |

**Full catalog**: [`docs/SKILLS_CATALOG.md`](docs/SKILLS_CATALOG.md) — **74 skills**, grouped by role.

Invocation syntax is identical across hosts:
```
/skill-name "arguments" — key: value, key2: value2
```

## Common Parameters

ARIS has **two independent control axes** plus scoped flags.

### Axis 1 — `effort` (depth / budget)

```
— effort: lite | balanced | max | beast      # default: balanced
```

Controls how many papers / ideas / rounds / pilots. Codex reasoning is **always `xhigh`** regardless of effort.

> **Personal note:** I mostly run `effort: lite` for exploratory sessions and only bump to `max` when I'm close to a submission deadline. Beast mode is overkill for solo research.

### Axis 2 — `assurance` (audit strictness, independent of effort)

```
— assurance: draft | polished | conference-ready | submission
```

Controls whether mandatory audits gate the final report. `lite` / `balanced` default to `draft`; `max` / `beast` default to `submission`. Override is legal: `--- effort: lite --- assurance: conference-ready` is meaningful. Spec: [`shared-references/assurance-contract.md`](skills/shared-references/assurance-contract.md).

### Other common parameters

```
— human checkpoint: true | false             # pause for approval (default: true)  # changed from false — I prefer manual gates
— AUTO_PROCEED: true | false                 # auto-continue at gates (default: true)
— difficulty: medium | hard | nightmare      # reviewer adversarial level
— venue: ICLR | NeurIPS | ICML | ...         # target venue
— sources: web, zotero, deepxiv, exa, ...    # literature sources
— gpu: local | remote | vast | modal         # GPU backend
— reviewer: codex | oracle-pro               # reviewer routing
```

### Scoped flags (skill-specific)

| Flag | Skill | Effect |
|------|-------|--------|
| `--- st
