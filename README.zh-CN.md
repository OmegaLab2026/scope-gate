# Scope Gate

**先闭合范围，再开始写代码。**

[English](README.md)

Scope Gate 是一个单一职责的通用 Agent Skill：在进入实现前，把交付请求固化为五项范围卡，并在工作区写入 `SCOPE.md`。五项分别是目标、输入输出、必须完成、明确不做和验收标准；范围闭合后立即停止，交给后续设计或执行环节。

![Scope Gate 演示](docs/demo.gif)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agent Skill: portable](https://img.shields.io/badge/Agent_Skill-portable-111827.svg)](https://agentskills.io/)
[![Scope fields: 5](https://img.shields.io/badge/Scope_fields-5-0f766e.svg)](skills/scope-gate/SKILL.md)

## 为什么使用 Scope Gate

需求很容易从第一次提问扩展到第一次提交。模型可能在交付边界尚未确定时，就开始做技术设计、拆票或直接写代码。Scope Gate 增加一个短而明确的检查点：

```text
请求 -> 五项范围卡 -> SCOPE.md -> 设计与交付
```

它的价值不在多写一份文档，而在于留下一个可供后续工作核对的闭合基线。

- 固定五项，避免范围讨论失焦。
- 明确不做，提前暴露容易被误纳入的相邻工作。
- 可观察的验收条件，减少“基本完成”这类主观判断。
- 带版本的 `SCOPE.md`，在工作区保留已确认基线。
- 强制停止边界，不把 ADR、拆票、估工和实现混入范围澄清。

Scope Gate 保持单一职责和平台中立。它不替代完整的需求工程、架构评审或项目管理，也不依赖某一个 Agent 宿主。

## 快速开始

Scope Gate 使用可移植的 Agent Skill 结构。以下命令均在目标项目根目录执行，会把 `skills/scope-gate` 复制到对应宿主的项目级 Skill 目录；命令末尾的 `-y` 表示无提示安装，并保持这一项目级默认。将 `--copy` 改为 `--global --copy` 可安装到宿主的用户级目录，部分宿主还需启用用户级发现。若安装时宿主已在运行，安装后需重启或 reload 会话，运行中的宿主可能仍缓存着旧技能列表。命令需要 Node.js 和 npm。

<details>
<summary><strong>Codex</strong></summary>

```bash
npx --yes skills@latest add OmegaLab2026/scope-gate --skill scope-gate --agent codex --copy -y
```

输入 `$scope-gate`。[官方文档](https://developers.openai.com/codex/skills/)

</details>

<details>
<summary><strong>Claude Code</strong></summary>

```bash
npx --yes skills@latest add OmegaLab2026/scope-gate --skill scope-gate --agent claude-code --copy -y
```

输入 `/scope-gate`。[官方文档](https://code.claude.com/docs/en/skills)

</details>

<details>
<summary><strong>DeepSeek Harness（DSH）</strong></summary>

```bash
npx --yes skills@latest add OmegaLab2026/scope-gate --skill scope-gate --agent pi --copy -y
```

该命令通过 `skills` CLI 的 Pi 兼容目标写入 DSH 会扫描的共享 `.agents/skills`。装好后需新开会话或刷新 DSH 窗口，`/` 里才会列出 `scope-gate`：DSH 的技能目录按会话预取缓存，外部安装不会自动使其失效。也可以直接让 Agent 通过 DSH 的 `skill` 工具调用它。[官方文档](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md)

</details>

<details>
<summary><strong>Cursor</strong></summary>

```bash
npx --yes skills@latest add OmegaLab2026/scope-gate --skill scope-gate --agent cursor --copy -y
```

在 Agent 输入 `/` 并选择 `scope-gate`。[官方文档](https://cursor.com/docs/context/skills)

</details>

<details>
<summary><strong>Gemini CLI</strong></summary>

```bash
npx --yes skills@latest add OmegaLab2026/scope-gate --skill scope-gate --agent gemini-cli --copy -y
```

请求 Agent 使用 `scope-gate` skill，然后用 `/skills list` 确认是否已发现。[官方文档](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills.md)

</details>

<details>
<summary><strong>Pi</strong></summary>

```bash
npx --yes skills@latest add OmegaLab2026/scope-gate --skill scope-gate --agent pi --copy -y
```

输入 `/skill:scope-gate`；编辑 Skill 后可用 `/reload` 重载。[官方文档](https://pi.dev/docs/latest/skills)

</details>

<details>
<summary><strong>Oh My Pi</strong></summary>

```bash
npx --yes skills@latest add OmegaLab2026/scope-gate --skill scope-gate --agent pi --copy -y
```

该命令通过 `skills` CLI 的 Pi 兼容目标写入 Oh My Pi 默认加载的 `.agents/skills`。输入 `/skill:scope-gate`；若斜杠命令不可用，启用 `skills.enableSkillCommands`。[官方文档](https://github.com/can1357/oh-my-pi/blob/main/docs/skills.md)

</details>

<details>
<summary><strong>OpenCode</strong></summary>

```bash
npx --yes skills@latest add OmegaLab2026/scope-gate --skill scope-gate --agent opencode --copy -y
```

请求 Agent 使用 `scope-gate` skill。[官方文档](https://opencode.ai/docs/skills/)

</details>

<details>
<summary><strong>WorkBuddy（需手动封装）</strong></summary>

先将本项目的 `SKILL.md` 封装为 WorkBuddy 的 `skill.yml` 格式并发布到 Skill Marketplace，再从 Marketplace 安装。[Marketplace 文档](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills-Market) · [Skill 格式](https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Practice-Cases/Create-Skills)

</details>

<details>
<summary><strong>Qoder</strong></summary>

```bash
npx --yes skills@latest add OmegaLab2026/scope-gate --skill scope-gate --agent qoder --copy -y
```

输入 `/scope-gate`；若 Qoder 已在运行，用 `/skills reload` 刷新。[官方文档](https://docs.qoder.com/cli/Skills)

</details>

<details>
<summary><strong>Trae</strong></summary>

```bash
npx --yes skills@latest add OmegaLab2026/scope-gate --skill scope-gate --agent trae --copy -y
```

请求 Agent 使用 `scope-gate` skill。[官方文档](https://docs.trae.ai/ide/skills)

</details>


`--agent pi` 安装会写入可移植的项目级 `.agents/skills/scope-gate` 文件夹；Codex、Cursor、Gemini CLI、Pi、Oh My Pi、OpenCode 和 DeepSeek Harness（DSH）均可发现该目录。当请求明确需要交付范围澄清时，支持隐式调用的宿主也可能自动选择该 Skill。

## 示例

输入：

```text
为管理后台增加 CSV 导入校验，确保错误的客户文件在写入数据前被拒绝。
```

Scope Gate 生成五项范围卡并写入 `SCOPE.md`。完整示例见 [example scope](examples/SCOPE.md)。

```markdown
## Goal

Reject malformed customer CSV files before any row is persisted.

## Inputs / Outputs

- Input: a customer CSV file and the documented import schema.
- Output: a validation result that identifies rejected rows and prevents partial writes.

## Must do

- Validate the file against the documented schema before persistence.

## Won't do

- Redesigning the import interface.

## Acceptance

- A malformed fixture produces a failed validation result and persists zero rows.
```

## 强制边界

| 字段 | 必须写清的内容 |
| --- | --- |
| `Goal` | 一个可观察的交付结果及其边界 |
| `Inputs / Outputs` | 已有或必需的输入，以及完成态交付物 |
| `Must do` | 达成目标所需的最小义务集合 |
| `Won't do` | 明确排除的相邻工作 |
| `Acceptance` | 每项必须完成对应的可复核通过条件 |

Scope Gate 在 ADR、技术设计、拆票、估工、排期和实现之前停止。这些请求属于另一项任务。

影响范围的提问必须包含：问题简要分析、2–4 个互斥方案和一个明确推荐。

## 兼容性与验证

Scope Gate 使用可移植的 Agent Skill 目录结构：

```text
skills/scope-gate/
|-- SKILL.md
`-- agents/
    `-- openai.yaml
```

`agents/openai.yaml` 只提供 OpenAI 宿主的可选 UI 元数据；其他宿主至少只需要 `SKILL.md`。

仓库检查：

```powershell
python tests/validate_scope.py
python -m unittest discover -s tests -v
```

结构检查覆盖 frontmatter、固定五项标题契约、版本元数据、示例范围卡、路由样例、UI 配置和 README 资产。项目同时使用 OpenAI `skill-creator` 的校验脚本检查 skill 结构。这些检查不等同于对任意运行时模型行为的完整验证，真实代理运行测试仍需单独开展。

## 参与贡献

所有改动都应服务于一个目标：闭合交付范围，然后停止。

提交改动时：

1. 保持五项标题及其顺序不变。
2. 保持提问协议和版本规则不变。
3. 调用行为变化时，同步更新路由样例。
4. 运行上述两条验证命令。
5. 说明改动如何收紧或放松停止边界。

把项目扩展到 ADR、计划、估工或实现，不属于本项目范围。

## 许可证

[MIT](LICENSE)
