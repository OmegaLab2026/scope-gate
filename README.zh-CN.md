# Scope Gate

**先闭合范围，再开始写代码。**

[English](README.md)

Scope Gate 是一个范围很窄的 Codex skill：在进入实现前，把交付请求固化为五项范围卡，并在工作区写入 `SCOPE.md`。五项分别是目标、输入输出、必须完成、明确不做和验收标准；范围闭合后立即停止，交给后续设计或执行环节。

![Scope Gate 演示](docs/demo.gif)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Skill: Codex](https://img.shields.io/badge/Skill-Codex-111827.svg)](https://developers.openai.com/codex/skills/)
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

Scope Gate 的职责刻意保持狭窄。它不替代完整的需求工程、架构评审或项目管理。

## 快速开始

前提：当前 Codex 版本支持 skills。参见 [Codex skills 文档](https://developers.openai.com/codex/skills/)。

将 skill 文件夹复制到 Codex 的 skills 目录：

```powershell
$source = Resolve-Path ".\skills\scope-gate"
$destination = Join-Path $env:USERPROFILE ".codex\skills\scope-gate"
Copy-Item -LiteralPath $source -Destination $destination -Recurse
```

如果设置了自定义 `CODEX_HOME`，目标路径应为 `$CODEX_HOME\skills\scope-gate`。如果 Codex 没有立即发现新 skill，请按要求重启或重新加载。

显式调用：

```text
Use $scope-gate to scope this request before implementation.
```

当请求明确需要交付范围澄清时，skill 也可能被模型自动选用。

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

Scope Gate 使用 Codex skill 目录结构：

```text
skills/scope-gate/
|-- SKILL.md
`-- agents/
    `-- openai.yaml
```

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
