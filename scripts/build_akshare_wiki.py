from __future__ import annotations

import hashlib
import re
import shutil
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = REPO_ROOT / "docs" / "akshare" / "数据字典"
WIKI_ROOT = REPO_ROOT / "docs" / "akshare" / "wiki"
TODAY = date(2026, 7, 26).isoformat()


@dataclass(frozen=True)
class SourceDoc:
    path: Path
    rel: Path
    body: str
    title: str
    source_page: str
    source_file: str


@dataclass
class InterfaceDoc:
    name: str
    slug: str
    title: str
    category_slug: str
    category_title: str
    source_rel: Path
    raw_rel: Path
    source_page: str
    heading_path: list[str]
    description: str
    target_url: str
    limit: str
    body: str


def yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def slugify(value: str) -> str:
    value = value.strip().lower().replace("_", "-")
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "page"


def read_source_body(text: str) -> tuple[str, str, str]:
    source_page = ""
    source_file = ""
    match = re.match(r"<!--\n(?P<meta>.*?)\n-->\n?", text, re.S)
    if match:
        for line in match.group("meta").splitlines():
            if line.startswith("来源页面:"):
                source_page = line.split(":", 1)[1].strip()
            elif line.startswith("源码文件:"):
                source_file = line.split(":", 1)[1].strip()
        return text[match.end() :].strip() + "\n", source_page, source_file
    return text.strip() + "\n", source_page, source_file


def markdown_title(body: str, fallback: str) -> str:
    for line in body.splitlines():
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if match:
            title = re.sub(r"\[(.*?)\]\([^)]*\)", r"\1", match.group(2)).strip()
            return title or fallback
    return fallback


def load_sources() -> list[SourceDoc]:
    docs: list[SourceDoc] = []
    for path in sorted(SOURCE_ROOT.rglob("*.md")):
        if path.name == "README.md":
            continue
        text = path.read_text(encoding="utf-8")
        body, source_page, source_file = read_source_body(text)
        rel = path.relative_to(SOURCE_ROOT)
        title = markdown_title(body, rel.with_suffix("").as_posix())
        docs.append(SourceDoc(path=path, rel=rel, body=body, title=title, source_page=source_page, source_file=source_file))
    return docs


def current_heading_path(lines: list[str], line_no: int) -> list[str]:
    headings: dict[int, str] = {}
    for line in lines[: line_no + 1]:
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if not match:
            continue
        level = len(match.group(1))
        title = re.sub(r"\[(.*?)\]\([^)]*\)", r"\1", match.group(2)).strip()
        headings = {k: v for k, v in headings.items() if k < level}
        headings[level] = title
    return [headings[level] for level in sorted(headings)]


DETAIL_HEADINGS = {
    "接口名称",
    "接口",
    "接口描述",
    "目标地址",
    "请求参数",
    "输入参数",
    "返回参数",
    "输出参数",
    "接口示例",
    "示例代码",
    "返回示例",
    "数据示例",
}


def heading_title(line: str) -> str:
    match = re.match(r"^#{1,6}\s+(.+?)\s*$", line)
    if not match:
        return ""
    return re.sub(r"\[(.*?)\]\([^)]*\)", r"\1", match.group(1)).strip()


def is_detail_heading(line: str) -> bool:
    title = heading_title(line)
    return title in DETAIL_HEADINGS or title.startswith("输出参数") or title.startswith("返回参数")


def nearest_heading_start(lines: list[str], line_no: int) -> int:
    for i in range(line_no, -1, -1):
        if re.match(r"^#{1,6}\s+", lines[i]) and not is_detail_heading(lines[i]):
            return i
    return line_no


def next_interface_block_start(lines: list[str], current_line: int, next_line: int) -> int:
    for i in range(current_line + 1, next_line):
        if re.match(r"^#{1,6}\s+", lines[i]) and not is_detail_heading(lines[i]):
            return i
    return nearest_heading_start(lines, next_line)


def extract_field(section: str, label: str) -> str:
    match = re.search(rf"^{re.escape(label)}:\s*(.+?)\s*$", section, re.M)
    return match.group(1).strip() if match else ""


def extract_description(section: str) -> str:
    direct = extract_field(section, "描述")
    if direct:
        return direct
    match = re.search(r"^#{2,6}\s*接口描述\s*\n+(.+?)\s*$", section, re.M)
    if match:
        return match.group(1).strip()
    return ""


def interface_topic(heading_path: list[str], fallback: str) -> str:
    generic = {"接口名称", "接口", "接口描述", fallback}
    for heading in reversed(heading_path):
        if heading not in generic:
            return heading
    return heading_path[-1] if heading_path else fallback


def find_interface_markers(lines: list[str]) -> list[tuple[int, str, str]]:
    markers: list[tuple[int, str, str]] = []
    for i, line in enumerate(lines):
        match = re.match(r"^接口:\s*([A-Za-z_][A-Za-z0-9_]*)\s*$", line)
        if match:
            markers.append((i, match.group(1), "akshare"))
            continue
        if re.match(r"^#{2,6}\s*接口名称\s*$", line):
            for j in range(i + 1, min(i + 6, len(lines))):
                candidate = lines[j].strip()
                if not candidate:
                    continue
                if re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", candidate):
                    markers.append((j, candidate, "qhkc"))
                break
    return markers


def build_interfaces(sources: list[SourceDoc]) -> list[InterfaceDoc]:
    raw_items: list[dict] = []
    for source in sources:
        lines = source.body.splitlines()
        markers = find_interface_markers(lines)
        for idx, (line_no, name, source_kind) in enumerate(markers):
            next_line = markers[idx + 1][0] if idx + 1 < len(markers) else len(lines)
            start = nearest_heading_start(lines, line_no)
            next_start = next_interface_block_start(lines, line_no, next_line) if idx + 1 < len(markers) else len(lines)
            end = max(line_no + 1, next_start)
            if next_start <= start:
                end = next_line
            body = "\n".join(lines[start:end]).strip() + "\n"
            heading_path = current_heading_path(lines, line_no)
            raw_items.append(
                {
                    "name": name,
                    "source": source,
                    "body": body,
                    "heading_path": heading_path,
                    "source_kind": source_kind,
                }
            )

    counts = Counter(item["name"] for item in raw_items)
    seen: Counter[str] = Counter()
    interfaces: list[InterfaceDoc] = []
    for item in raw_items:
        source: SourceDoc = item["source"]
        name = item["name"]
        seen[name] += 1
        base_slug = slugify(name)
        if counts[name] > 1:
            suffix = slugify(source.rel.with_suffix("").as_posix())
            slug = f"{base_slug}-{suffix}"
            if seen[name] > 1:
                slug = f"{slug}-{seen[name]}"
        else:
            slug = base_slug
        category_slug = slugify(source.rel.with_suffix("").as_posix())
        heading_path = item["heading_path"]
        topic = interface_topic(heading_path, name)
        title = f"{name} - {topic}" if topic and topic != name else name
        raw_rel = Path("raw") / "data-dictionary" / source.rel
        section = item["body"]
        interfaces.append(
            InterfaceDoc(
                name=name,
                slug=slug,
                title=title,
                category_slug=category_slug,
                category_title=source.title,
                source_rel=source.rel,
                raw_rel=raw_rel,
                source_page=source.source_page,
                heading_path=heading_path,
                description=extract_description(section),
                target_url=extract_field(section, "目标地址"),
                limit=extract_field(section, "限量"),
                body=section,
            )
        )
    return interfaces


def frontmatter(title: str, page_type: str, tags: list[str], sources: list[str], extra: dict[str, str] | None = None) -> str:
    lines = [
        "---",
        f"title: {yaml_quote(title)}",
        f"created: {TODAY}",
        f"updated: {TODAY}",
        f"type: {page_type}",
        "tags: [" + ", ".join(tags) + "]",
        "sources: [" + ", ".join(sources) + "]",
    ]
    for key, value in (extra or {}).items():
        lines.append(f"{key}: {value}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def raw_frontmatter(source: SourceDoc, body: str) -> str:
    sha = hashlib.sha256(body.encode("utf-8")).hexdigest()
    return (
        "---\n"
        f"source_url: {source.source_page or source.source_file}\n"
        f"source_file: {source.source_file}\n"
        f"ingested: {TODAY}\n"
        f"sha256: {sha}\n"
        "---\n\n"
    )


def write_file(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def clean_wiki_root() -> None:
    if WIKI_ROOT.exists():
        shutil.rmtree(WIKI_ROOT)
    for subdir in [
        "raw/data-dictionary",
        "entities/interfaces",
        "concepts/categories",
        "comparisons",
        "queries",
        "_meta",
    ]:
        (WIKI_ROOT / subdir).mkdir(parents=True, exist_ok=True)


def build_schema() -> str:
    return f"""# Wiki Schema

## Domain
AKShare 数据字典知识库，覆盖 AKShare 官方文档 1.18.78 中的数据分类、接口函数、参数、返回字段、示例代码和来源页面。

## Conventions
- File names: lowercase, hyphen-separated slugs; AKShare function names are converted from underscores to hyphens.
- Every wiki page starts with YAML frontmatter.
- Use Obsidian-style double-bracket links to connect category pages, interface pages, and meta pages.
- Raw source files live under `raw/data-dictionary/` and are immutable snapshots of `docs/akshare/数据字典/`.
- Interface pages preserve the source section verbatim where possible; synthesis appears before the source excerpt.
- Every generated page is listed in `index.md`.
- Every generation or refresh is appended to `log.md`.

## Frontmatter
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [from taxonomy below]
sources: [raw/data-dictionary/source.md]
confidence: high | medium | low
---
```

## Tag Taxonomy
- `akshare`: all AKShare data dictionary pages.
- `data-dictionary`: imported AKShare dictionary content.
- `category`: AKShare data category pages.
- `interface`: AKShare function or pro_api endpoint pages.
- `parameters`: pages containing input parameter details.
- `returns`: pages containing output or return field details.
- `example`: pages containing executable example snippets.
- `stock`, `futures`, `bond`, `option`, `fx`, `currency`, `spot`, `interest-rate`, `fund`, `index`, `macro`, `crypto`, `bank`, `article`, `energy`, `event`, `hf`, `nlp`, `qdii`, `others`, `qhkc`, `tool`: source-domain tags.
- `meta`: generated navigation and health pages.

## Page Thresholds
- Create one category page for each source document under `docs/akshare/数据字典/`.
- Create one interface entity page for each detected `接口:` or `接口名称` block.
- Do not create extra pages for table columns, sample rows, or provider names unless they become a repeated research target.
- Split pages over roughly 200 lines only after a human asks for deeper normalization; source-preserving interface pages may temporarily exceed that limit.

## Entity Pages
Interface entity pages include:
- Overview with function name, category, heading path, description, target URL, and limit.
- Links to the category page and topic map.
- A source excerpt copied from the data dictionary.

## Concept Pages
Category concept pages include:
- Overview and source provenance.
- Interface count and links to every interface extracted from that category.
- Links back to `[[index]]` and `[[_meta/topic-map]]`.

## Update Policy
This wiki is generated from a timestamped official source snapshot. On refresh, regenerate the wiki from `docs/akshare/数据字典/`, compare git diff, and keep older source snapshots only if the user asks for version history.

Generated on {TODAY}.
"""


def domain_tag_for_source(rel: Path) -> str:
    first = rel.parts[0]
    mapping = {
        "interest_rate": "interest-rate",
        "dc": "crypto",
        "qhkc": "qhkc",
    }
    return mapping.get(first, first)


def build_category_page(source: SourceDoc, interfaces: list[InterfaceDoc]) -> str:
    raw_link = (Path("..") / ".." / "raw" / "data-dictionary" / source.rel).as_posix()
    source_ref = f"raw/data-dictionary/{source.rel.as_posix()}"
    tag = domain_tag_for_source(source.rel)
    lines = [
        frontmatter(
            title=source.title,
            page_type="concept",
            tags=["akshare", "data-dictionary", "category", tag],
            sources=[source_ref],
            extra={"confidence": "high"},
        ).rstrip(),
        f"# {source.title}",
        "",
        f"来源页面: {source.source_page or 'unknown'}",
        f"原始快照: [{source.rel.as_posix()}]({raw_link})",
        "",
        f"该分类从 AKShare 数据字典中抽取出 {len(interfaces)} 个接口页面。相关接口页统一放在 `entities/interfaces/`，并通过 `[[index]]` 与 `[[_meta/topic-map]]` 汇总。",
        "",
        "## 接口",
        "",
    ]
    if interfaces:
        for interface in sorted(interfaces, key=lambda item: item.name):
            summary = interface.description or "详见接口页"
            lines.append(f"- [[{interface.slug}|{interface.name}]] - {summary}")
    else:
        lines.append("- 该源页面没有检测到标准接口块，保留为分类与原始来源导航页。")
    lines.extend(["", "## 相关", "", "- [[index]]", "- [[_meta/topic-map]]", ""])
    return "\n".join(lines)


def build_interface_page(interface: InterfaceDoc) -> str:
    source_ref = f"raw/data-dictionary/{interface.source_rel.as_posix()}"
    tags = ["akshare", "data-dictionary", "interface", domain_tag_for_source(interface.source_rel)]
    if "输入参数" in interface.body or "请求参数" in interface.body:
        tags.append("parameters")
    if "输出参数" in interface.body or "返回参数" in interface.body:
        tags.append("returns")
    if "接口示例" in interface.body or "示例代码" in interface.body:
        tags.append("example")
    display_path = [heading for heading in interface.heading_path if heading not in DETAIL_HEADINGS]
    breadcrumbs = " > ".join(display_path) if display_path else interface.category_title
    lines = [
        frontmatter(
            title=interface.title,
            page_type="entity",
            tags=tags,
            sources=[source_ref],
            extra={"confidence": "high"},
        ).rstrip(),
        f"# {interface.name}",
        "",
        f"- 分类: [[{interface.category_slug}|{interface.category_title}]]",
        f"- 主题路径: {breadcrumbs}",
    ]
    if interface.description:
        lines.append(f"- 描述: {interface.description}")
    if interface.target_url:
        lines.append(f"- 目标地址: {interface.target_url}")
    if interface.limit:
        lines.append(f"- 限量: {interface.limit}")
    lines.extend(
        [
            f"- 来源页面: {interface.source_page or 'unknown'}",
            "",
            "## 相关",
            "",
            f"- [[{interface.category_slug}|{interface.category_title}]]",
            "- [[_meta/topic-map]]",
            "",
            "## 源文摘录",
            "",
            interface.body.strip(),
            "",
        ]
    )
    return "\n".join(lines)


def build_topic_map(sources: list[SourceDoc], by_category: dict[str, list[InterfaceDoc]]) -> str:
    lines = [
        frontmatter(
            title="AKShare Topic Map",
            page_type="summary",
            tags=["akshare", "data-dictionary", "meta"],
            sources=[],
            extra={"confidence": "high"},
        ).rstrip(),
        "# AKShare Topic Map",
        "",
        "这个页面按官方数据分类组织 wiki 页面，适合在 Obsidian 图谱或 VS Code 搜索前先快速定位。",
        "",
    ]
    for source in sources:
        category_slug = slugify(source.rel.with_suffix("").as_posix())
        interfaces = sorted(by_category.get(category_slug, []), key=lambda item: item.name)
        lines.extend([f"## [[{category_slug}|{source.title}]]", "", f"- 接口数: {len(interfaces)}"])
        if interfaces:
            preview = interfaces[:30]
            lines.append("- 常用入口:")
            for item in preview:
                lines.append(f"  - [[{item.slug}|{item.name}]]")
            if len(interfaces) > len(preview):
                lines.append(f"  - 另有 {len(interfaces) - len(preview)} 个接口，见分类页。")
        lines.append("")
    return "\n".join(lines)


def build_index(sources: list[SourceDoc], interfaces: list[InterfaceDoc]) -> str:
    total_pages = len(sources) + len(interfaces) + 1
    lines = [
        "# Wiki Index",
        "",
        "> AKShare 数据字典 wiki 内容目录。每个页面都来自官方数据字典快照，并保留可追溯来源。",
        f"> Last updated: {TODAY} | Total pages: {total_pages}",
        "",
        "## Concepts",
        "",
    ]
    for source in sources:
        category_slug = slugify(source.rel.with_suffix("").as_posix())
        count = sum(1 for item in interfaces if item.category_slug == category_slug)
        lines.append(f"- [[{category_slug}|{source.title}]] - 数据分类，包含 {count} 个接口。")
    lines.extend(["", "## Entities", ""])
    grouped: dict[str, list[InterfaceDoc]] = defaultdict(list)
    for interface in interfaces:
        grouped[interface.category_slug].append(interface)
    for source in sources:
        category_slug = slugify(source.rel.with_suffix("").as_posix())
        items = sorted(grouped.get(category_slug, []), key=lambda item: item.name)
        if not items:
            continue
        lines.extend([f"### {source.title}", ""])
        for item in items:
            summary = item.description or "接口说明"
            lines.append(f"- [[{item.slug}|{item.name}]] - {summary}")
        lines.append("")
    lines.extend(["## Comparisons", "", "- 暂无。", "", "## Queries", "", "- 暂无。", "", "## Meta", "", "- [[_meta/topic-map|AKShare Topic Map]]", ""])
    return "\n".join(lines)


def build_log(sources: list[SourceDoc], interfaces: list[InterfaceDoc]) -> str:
    return f"""# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`

## [{TODAY}] create | AKShare data dictionary wiki initialized
- Domain: AKShare 官方数据字典。
- Source directory: `docs/akshare/数据字典/`.
- Raw source snapshots: {len(sources)}.
- Category pages: {len(sources)}.
- Interface pages: {len(interfaces)}.
- Generated files: `SCHEMA.md`, `index.md`, `log.md`, `raw/`, `concepts/categories/`, `entities/interfaces/`, `_meta/topic-map.md`.
"""


def lint_wikilinks() -> list[str]:
    pages = {
        path.relative_to(WIKI_ROOT).with_suffix("").as_posix(): path
        for path in WIKI_ROOT.rglob("*.md")
        if not path.relative_to(WIKI_ROOT).as_posix().startswith("raw/")
    }
    aliases = {Path(key).name for key in pages}
    aliases.update(pages.keys())
    broken: list[str] = []
    pattern = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
    for path in WIKI_ROOT.rglob("*.md"):
        if path.relative_to(WIKI_ROOT).as_posix().startswith("raw/"):
            continue
        for match in pattern.finditer(path.read_text(encoding="utf-8")):
            target = match.group(1)
            if target not in aliases:
                broken.append(f"{path.relative_to(WIKI_ROOT)} -> {target}")
    return broken


def main() -> None:
    sources = load_sources()
    interfaces = build_interfaces(sources)
    by_category: dict[str, list[InterfaceDoc]] = defaultdict(list)
    for interface in interfaces:
        by_category[interface.category_slug].append(interface)

    clean_wiki_root()
    write_file(WIKI_ROOT / "SCHEMA.md", build_schema())

    for source in sources:
        raw_body = source.body
        write_file(WIKI_ROOT / "raw" / "data-dictionary" / source.rel, raw_frontmatter(source, raw_body) + raw_body)

    for source in sources:
        category_slug = slugify(source.rel.with_suffix("").as_posix())
        out = WIKI_ROOT / "concepts" / "categories" / f"{category_slug}.md"
        write_file(out, build_category_page(source, by_category.get(category_slug, [])))

    for interface in interfaces:
        out = WIKI_ROOT / "entities" / "interfaces" / f"{interface.slug}.md"
        write_file(out, build_interface_page(interface))

    write_file(WIKI_ROOT / "_meta" / "topic-map.md", build_topic_map(sources, by_category))
    write_file(WIKI_ROOT / "index.md", build_index(sources, interfaces))
    write_file(WIKI_ROOT / "log.md", build_log(sources, interfaces))

    broken = lint_wikilinks()
    print(f"sources={len(sources)}")
    print(f"interfaces={len(interfaces)}")
    print(f"wiki_markdown_files={sum(1 for _ in WIKI_ROOT.rglob('*.md'))}")
    print(f"broken_wikilinks={len(broken)}")
    for item in broken[:20]:
        print(f"BROKEN {item}")
    if broken:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
