# Wiki Schema

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

Generated on 2026-07-26.
