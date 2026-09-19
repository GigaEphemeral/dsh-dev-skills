# keyword-gate.py — skill 关键词监测/限制门禁

> v1.0｜Python 3.9+（纯标准库）｜阶段一 skill 产出的门禁脚本

## 作用

扫描 skill 资产（默认 `1skillCode/`），对每个 SKILL.md：

1. **监测**：校验 frontmatter 必填（name/description/metadata）+ 必含章节（触发场景/工作流程/边界纪律）+ 从 description 提取关键词（`关键词：` 后的逗号/顿号分隔列表）。
2. **限制**：
   - 语言专属约束：`ts`/`typescript` 关键词只能出现在目录名含 `ts` 的 skill；`py`/`python` 只能在含 `py` 的（预留扩展）
   - 关键词全局唯一性：语言词/核心词跨 skill 重复 = error；其它词重复 = warning
3. **报告**：人类可读或 `--json`；违规 exit 1（可挂进阶段一门禁）。

## 用法

```bash
python tools/keyword-gate.py                          # 扫 1skillCode/，默认
python tools/keyword-gate.py --dir 1skillCode --json  # JSON 输出
python tools/keyword-gate.py --fail-warning           # warning 也使 exit 1
```

## 参数化点（D-05 纪律：能配置就配置）

| 常量 | 说明 |
|---|---|
| `LANG_WORDS` | 语言关键词 → 允许的目录名片段；新增语言（如 `java`）在此登记 |
| `GLOBAL_ONLY` | 必须全局唯一的关键词 |
| `REQUIRED_SECTIONS` | 每个 SKILL.md 必含章节 |
| `REQUIRED_FRONTMATTER` | 必填 frontmatter 字段 |

扩展新语言专家时：建 `R4-py-architect/` 等目录 + 在 `LANG_WORDS` 加 `'py': ['py']`，脚本即自动校验该语言的词只进对应目录。

## 自检

```bash
python tools/keyword-gate.py --json | python -c "import json,sys; d=json.load(sys.stdin); print('PASS' if d['ok'] else 'FAIL', d['issue_count'])"
```
