# Wiki Schema

## Domain
MindGo / SuperMind 数据源知识仓库。覆盖通过 SuperMind API、数据平台数据字典、远程 Jupyter 脚本执行、以及 indexmap/arsenal 内部接口获取行情、基本信息、财务、因子、问财和全市场股票数据的方法。

## Conventions
- Wiki path: `docs/mindgo/wiki/`.
- File names: lowercase hyphenated English slugs; source-derived Chinese titles are kept in page title, not filename.
- Every wiki page starts with YAML frontmatter.
- Use wikilinks between pages; every concept/entity/comparison/query page should link to at least two other pages.
- Raw sources in `raw/` are immutable snapshots with `source_url`, `ingested`, and `sha256` frontmatter.
- Prefer concise synthesis pages. Long source tables belong in `raw/` or category catalog pages.
- Update `index.md` and append `log.md` after every ingest/update.

## Frontmatter
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [mindgo, api]
sources: [raw/articles/source.md]
confidence: high | medium | low
---
```

## Tag Taxonomy
- Domain: mindgo, supermind, data-source, data-dictionary
- Access Methods: api, jupyter, indexmap, arsenal, local-sdk
- Data Types: market-data, intraday, fundamentals, securities, factors, risk-model, iwencai, ifind, trading, files, utilities
- Asset Classes: stock, futures, options, funds, bonds, index, forex, td
- Operations: setup, security, troubleshooting, workflow, catalog, comparison, query

Rule: every tag used in page frontmatter must appear in this taxonomy.

## Page Thresholds
- Create a page when a data access method, data family, API group, or operational concern is central to the MindGo data source workflow.
- Do not create pages for individual data tables unless they need synthesis beyond the data dictionary. Keep table-level detail in category catalog pages and raw sources.
- Split catalog pages when they become hard to scan.

## Update Policy
When downloaded docs change, re-ingest raw sources, compare hashes, update affected synthesis pages, then log the change.
