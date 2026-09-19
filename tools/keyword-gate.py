#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
keyword-gate.py — skill 关键词监测/限制门禁 v1.0

扫描 skill 资产（默认 2skillCode/，可指定目录），对每个 SKILL.md 做三件事：
  1. 监测  ：校验 frontmatter 完整（name/description/metadata + 触发场景/工作流程/边界纪律）
             并从 description 提取关键词（'关键词：' 或 '关键词:' 后的逗号/顿号分隔列表）
  2. 限制  ：全局关键词唯一性（同名关键词不得被多个 skill 声明，避免误触发）；
             语言专属约束（`ts`/`typescript` 等 TS 词只能出现在名字含 `ts` 的 skill，
             `py`/`python` 只能出现在名字含 `py` 的 skill）；配置化，可加规则
  3. 报告  ：人类可读或 --json；违规 exit 1（可作阶段一门禁）

用法：
  python keyword-gate.py [--dir 2skillCode] [--json] [--fail-warning]
  # 自定义限制规则：--rule "word:scope:allowed_ids" 或编辑下方 RULES

参数化点（D-05 纪律）：
  - LANG_WORDS   : 语言关键词 → 允许出现的 skill 名片段（范围）
  - GLOBAL_ONLY  : 只能全局唯一、不允许出现在多 skill 的关键词
  - REQUIRED_SECTIONS : 每个 SKILL.md 必须含的章节
"""
import argparse
import json
import re
import sys
from pathlib import Path

# ── 参数化点（能配置就配置）──────────────────────────────────────────────
LANG_WORDS = {          # 语言词 → 允许的目录名片段；空列表 = 任意语言 skill 均可
    'ts': ['ts'],
    'typescript': ['ts'],
    'py': ['py', 'python'],
    'python': ['py', 'python'],
    'java': ['java'],
    'go': ['go', 'golang'],
}
GLOBAL_ONLY = []        # 这些关键词全局唯一，不得重复（如 '门禁'/'证据链' 之类核心词）
REQUIRED_SECTIONS = ['触发场景', '工作流程', '边界纪律']   # SKILL.md 必含章节
REQUIRED_FRONTMATTER = ['name', 'description', 'metadata']
# ─────────────────────────────────────────────────────────────────────────

KEYWORD_RE = re.compile(r'关键词[:：]\s*([^\n]+)')
SECTION_RE = re.compile(r'^##\s+(.+)$', re.M)
FM_RE = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.S)


def parse_frontmatter(text):
    m = FM_RE.match(text)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ':' in line:
            k, v = line.split(':', 1)
            out[k.strip()] = v.strip()
        elif line.strip() and not line.strip().startswith('#'):
            # 子键行（如 metadata 下的 author/version）：把父 key 记为存在
            # 只要缩进大于 0 或前一行是顶层 key，就标记顶层 key 存在
            indent = len(line) - len(line.lstrip())
            if indent > 0:
                # 找到最近的顶层 key：此处简化，子键存在即说明其父块存在
                # 通过记录"已看到顶层 key 且其后有子键"判断
                pass
    # 扫描子键：任意行有前导空白（缩进）且其上是顶层 key，则顶层 key 存在
    lines = m.group(1).splitlines()
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped or ':' not in stripped or stripped.startswith('#'):
            continue
        k, v = stripped.split(':', 1)
        # 顶层 key（无缩进）→ 记录（值可为空，只要 key 存在）
        if line == line.lstrip():
            out.setdefault(k.strip(), v.strip())
    return out


def extract_keywords(description):
    m = KEYWORD_RE.search(description or '')
    if not m:
        return []
    return [w.strip() for w in re.split(r'[,，、;；]', m.group(1)) if w.strip()]


def check_skill(path):
    """返回 (issues, meta)。issues: list[str]"""
    issues = []
    text = path.read_text(encoding='utf-8')
    fm = parse_frontmatter(text)

    # 1. frontmatter 必填（metadata 为块状字段，存在即可；name/description 值须非空）
    for k in REQUIRED_FRONTMATTER:
        if k not in fm:
            issues.append(f'[frontmatter] 缺字段: {k}')
        elif k != 'metadata' and not fm[k]:
            issues.append(f'[frontmatter] 字段为空: {k}')

    # 2. 必含章节
    sections = set(SECTION_RE.findall(text))
    for s in REQUIRED_SECTIONS:
        if s not in sections:
            issues.append(f'[section] 缺章节: {s}')

    # 3. 提取关键词
    keywords = extract_keywords(fm.get('description', ''))
    meta = {'name': fm.get('name', path.parent.name),
            'keywords': keywords,
            'dir': path.parent.name}
    return issues, meta


def lang_allowed(word, dirname):
    """语言关键词是否允许出现在该目录名。"""
    allowed = LANG_WORDS.get(word)
    if allowed is None:
        return True          # 非语言词不受限
    if not allowed:
        return True          # 空列表 = 任意
    return any(frag in dirname for frag in allowed)


def main():
    ap = argparse.ArgumentParser(description='skill 关键词监测/限制门禁')
    ap.add_argument('--dir', default='2skillCode', help='skill 根目录')
    ap.add_argument('--json', action='store_true', help='输出 JSON')
    ap.add_argument('--fail-warning', action='store_true',
                    help='warning 级违规也使 exit 1（默认仅 error 级）')
    args = ap.parse_args()

    root = Path(args.dir)
    if not root.is_dir():
        print(json.dumps({'ok': False, 'error': f'目录不存在: {root}'}))
        sys.exit(1)

    skills = {}
    all_issues = []
    for skill_md in sorted(root.rglob('SKILL.md')):
        issues, meta = check_skill(skill_md)
        skills[meta['name']] = meta
        for i in issues:
            all_issues.append({'skill': meta['name'], 'dir': meta['dir'], 'severity': 'error', 'msg': i})

    # 语言专属约束
    for name, meta in skills.items():
        dirname = meta['dir']
        for w in meta['keywords']:
            wl = w.lower()
            if not lang_allowed(wl, dirname):
                all_issues.append({
                    'skill': name, 'dir': dirname, 'severity': 'error',
                    'msg': f'语言关键词 "{w}" 不允许出现在 {dirname}（应含 {LANG_WORDS.get(wl, [])} 片段）'})

    # 关键词全局唯一性（error：核心词/不在允许范围的词跨 skill 冲突；warning：其它词重复）
    # 语言词允许在"同语言范围内"的多个 skill 重复（如 typescript 在 ts 系多个 skill），
    # 语言词出现在错误目录已由上方 lang_allowed 逐 skill 拦截，这里不再重复报错。
    seen = {}
    for name, meta in skills.items():
        for w in meta['keywords']:
            wl = w.lower()
            seen.setdefault(wl, []).append(name)
    for w, names in seen.items():
        if len(names) <= 1:
            continue
        if w in GLOBAL_ONLY:
            all_issues.append({'skill': ','.join(names), 'dir': '-', 'severity': 'error',
                               'msg': f'核心关键词 "{w}" 在多个 skill 重复: {names}'})
        elif w in LANG_WORDS:
            # 语言词：确认所有出现处都在其允许范围内；若是，视为正常（同语言多专家）
            allowed = LANG_WORDS[w]
            all_in_scope = all(
                (not allowed) or any(frag in skills[n]['dir'] for frag in allowed)
                for n in names)
            if not all_in_scope:
                all_issues.append({'skill': ','.join(names), 'dir': '-', 'severity': 'error',
                                   'msg': f'语言关键词 "{w}" 出现范围不一致: {names}'})
        else:
            all_issues.append({'skill': ','.join(names), 'dir': '-', 'severity': 'warning',
                               'msg': f'关键词 "{w}" 在多个 skill 重复: {names}'})

    has_error = any(i['severity'] == 'error' for i in all_issues)
    has_warning = any(i['severity'] == 'warning' for i in all_issues)
    fail = has_error or (has_warning and args.fail_warning)

    result = {
        'ok': not fail,
        'skill_count': len(skills),
        'issue_count': len(all_issues),
        'errors': [i for i in all_issues if i['severity'] == 'error'],
        'warnings': [i for i in all_issues if i['severity'] == 'warning'],
        'skills': skills,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f'== keyword-gate == skill 数: {len(skills)}')
        for i in all_issues:
            print(f'  [{i["severity"]:^7}] {i["skill"]}: {i["msg"]}')
        print(f'结论: {"PASS" if not fail else "FAIL"} '
              f'(error={result["issue_count"] - len(result["warnings"])}, warning={len(result["warnings"])})')

    sys.exit(0 if not fail else 1)


if __name__ == '__main__':
    main()
