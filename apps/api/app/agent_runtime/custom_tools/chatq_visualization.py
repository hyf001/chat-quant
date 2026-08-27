from __future__ import annotations

import argparse
import html
import io
import json
import os
import shlex
from collections.abc import Iterable
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal, Required, TypedDict, cast
from urllib.parse import quote

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from app.core.config import get_settings
from app.schema.agent_runtime import AgentExecutionCommand

CHATQ_VISUALIZATION_SERVER_NAME = "chatq"
CHATQ_VISUALIZATION_MCP_TOOL_NAME = "visualization"
CHATQ_VISUALIZATION_TOOL_NAME = (
    f"mcp__{CHATQ_VISUALIZATION_SERVER_NAME}__{CHATQ_VISUALIZATION_MCP_TOOL_NAME}"
)

MAX_SPEC_FILE_BYTES = 2 * 1024 * 1024
MAX_ROWS = 5000
MIN_CHART_HEIGHT = 240
MAX_CHART_HEIGHT = 1200
VISUALIZATION_ASSET_ROUTE = "/visualization-assets"
VISUALIZATION_STATIC_DIR = Path(__file__).resolve().parents[2] / "static" / "visualization-assets"
VISUALIZATION_ASSET_FILES = (
    "tailwindcss-3.4.16.js",
    "lucide.js",
    "echarts.5.6.0.min.js",
)

Kind = Literal["chart", "table", "card", "report"]
ChartType = Literal["line", "bar", "pie", "scatter", "heatmap", "candlestick"]
CardFormat = Literal["number", "integer", "percent", "currency", "string"]
RawSpec = dict[str, Any]
JsonObject = dict[str, Any]
TableRow = list[object]

CHART_TYPES = {"line", "bar", "pie", "scatter", "heatmap", "candlestick"}
CARD_FORMATS = {"number", "integer", "percent", "currency", "string"}
PIE_COLORS = [
    "#316a9e",
    "#c9851a",
    "#16845f",
    "#d4483b",
    "#343941",
    "#8a6f2a",
    "#4f8f78",
    "#9a5f55",
    "#5d7fa4",
    "#b78b2f",
    "#2f6f56",
    "#a9443a",
    "#6d746f",
    "#7c6f42",
    "#3f6f8d",
]

ROOT_KEYS: dict[str, set[str]] = {
    "chart": {
        "kind",
        "title",
        "subtitle",
        "type",
        "data",
        "x",
        "series",
        "height",
        "source",
        "options",
    },
    "table": {"kind", "title", "subtitle", "data", "height", "source"},
    "card": {"kind", "title", "subtitle", "cards", "source"},
    "report": {
        "kind",
        "title",
        "subtitle",
        "layout",
        "cards",
        "charts",
        "tables",
        "source",
    },
}
NESTED_CHART_KEYS = ROOT_KEYS["chart"]
NESTED_TABLE_KEYS = ROOT_KEYS["table"]
CARD_KEYS = {"label", "value", "unit", "format", "decimals", "icon", "description"}
DATA_KEYS = {"columns", "rows"}
SERIES_KEYS = {"name", "field", "fields", "name_field", "value_field", "item_style", "stack"}
X_KEYS = {"field"}
LAYOUT_KEYS = {"columns"}


class ToolSchema(TypedDict):
    type: str
    properties: dict[str, object]
    required: list[str]
    additionalProperties: bool


class ToolArtifact(TypedDict):
    asset_type: str
    asset_id: str
    title: str


class ToolPayload(TypedDict, total=False):
    ok: Required[bool]
    operator: Required[object]
    data: object
    summary: str
    artifacts: list[ToolArtifact]
    error_code: str
    message: str
    detail: JsonObject


class ValidationIssuePayload(TypedDict, total=False):
    path: Required[str]
    code: Required[str]
    message: Required[str]
    hint: str


class TabularData(TypedDict):
    columns: list[str]
    rows: list[TableRow]


class XSpec(TypedDict):
    field: str


class CandlestickFields(TypedDict):
    open: str
    close: str
    low: str
    high: str


class ScatterFields(TypedDict):
    x: str
    y: str


class HeatmapFields(TypedDict):
    x: str
    y: str
    value: str


class SeriesSpec(TypedDict, total=False):
    name: Required[str]
    field: str
    fields: CandlestickFields | ScatterFields | HeatmapFields
    name_field: str
    value_field: str
    item_style: JsonObject
    stack: str


class CardSpec(TypedDict, total=False):
    label: Required[str]
    value: Required[object]
    unit: str
    format: CardFormat
    decimals: int
    icon: str
    description: str


class LayoutSpec(TypedDict, total=False):
    columns: int


class ChartSpec(TypedDict, total=False):
    kind: Literal["chart"]
    title: Required[str]
    subtitle: str
    type: Required[ChartType]
    data: Required[TabularData]
    x: XSpec
    series: Required[list[SeriesSpec]]
    height: int
    source: str
    options: JsonObject


class TableSpec(TypedDict, total=False):
    kind: Literal["table"]
    title: Required[str]
    subtitle: str
    data: Required[TabularData]
    height: int
    source: str


class CardGroupSpec(TypedDict, total=False):
    kind: Literal["card"]
    title: Required[str]
    subtitle: str
    cards: Required[list[CardSpec]]
    source: str


class ReportSpec(TypedDict, total=False):
    kind: Literal["report"]
    title: Required[str]
    subtitle: str
    layout: LayoutSpec
    cards: list[CardSpec]
    charts: list[ChartSpec]
    tables: list[TableSpec]
    source: str


VisualizationSpec = ChartSpec | TableSpec | CardGroupSpec | ReportSpec


class ValidationSuccessData(TypedDict):
    file: str
    kind: object
    issues: list[ValidationIssuePayload]


class RenderSuccessData(TypedDict):
    file: str
    kind: str
    output_file: str
    iframe_url: str
    asset_base_url: str


class ChatqVisualizationCommandRequest(BaseModel):
    command: str = Field(min_length=1)

    model_config = ConfigDict(extra="forbid")


class ToolExecutionError(Exception):
    def __init__(
        self,
        error_code: str,
        message: str,
        *,
        detail: JsonObject | None = None,
    ) -> None:
        super().__init__(message)
        self.error_code = error_code
        self.message = message
        self.detail = detail or {}


@dataclass(frozen=True)
class ValidationIssue:
    path: str
    code: str
    message: str
    hint: str | None = None

    def to_dict(self) -> ValidationIssuePayload:
        payload: ValidationIssuePayload = {
            "path": self.path,
            "code": self.code,
            "message": self.message,
        }
        if self.hint:
            payload["hint"] = self.hint
        return payload


@dataclass(frozen=True)
class ToolTextResult:
    text: str
    is_error: bool = False


@dataclass(frozen=True)
class LoadedSpec:
    path: Path
    relative_path: str
    data: RawSpec


def build_chatq_visualization_tool_schema() -> ToolSchema:
    return {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": (
                    "chatq-visualization style command line. Examples: "
                    "chart render --file chart.json --output-file visualization/chart.html, "
                    "report render --file report.json --output-file visualization/report.html, "
                    "validate --file report.json, or schema chart."
                ),
            },
        },
        "required": ["command"],
        "additionalProperties": False,
    }


async def handle_chatq_visualization_tool(
    command: AgentExecutionCommand,
    args: JsonObject,
) -> ToolTextResult:
    try:
        request = ChatqVisualizationCommandRequest.model_validate(args)
        return await execute_chatq_visualization_command(command, request.command)
    except ValidationError as exc:
        return ToolTextResult(
            _format_cli_error(
                "chatq_visualization input is invalid",
                detail={"errors": _jsonable(exc.errors())},
            ),
            is_error=True,
        )
    except ToolExecutionError as exc:
        return ToolTextResult(_format_cli_error(exc.message, _error_detail(exc)), True)


async def execute_chatq_visualization_command(
    command: AgentExecutionCommand,
    command_line: str,
) -> ToolTextResult:
    try:
        argv = shlex.split(command_line)
    except ValueError as exc:
        return ToolTextResult(_format_cli_error(f"Failed to parse command: {exc}"), True)
    return await execute_chatq_visualization_argv(command, argv)


async def execute_chatq_visualization_argv(
    command: AgentExecutionCommand,
    argv: list[str],
) -> ToolTextResult:
    parser = build_command_parser()
    stdout = io.StringIO()
    stderr = io.StringIO()
    try:
        with redirect_stdout(stdout), redirect_stderr(stderr):
            args = parser.parse_args(argv)
    except SystemExit as exc:
        output = stdout.getvalue() or stderr.getvalue()
        code = exc.code if isinstance(exc.code, int) else 1
        return ToolTextResult(output.rstrip(), code != 0)

    try:
        payload = run_cli_command(command, args)
    except ToolExecutionError as exc:
        payload = _error_payload(exc.error_code, exc.message, exc.detail, operator=_operator(args))
        text = format_cli_payload(payload, as_json=getattr(args, "json", False))
        return ToolTextResult(text, True)

    return ToolTextResult(format_cli_payload(payload, as_json=getattr(args, "json", False)))


def build_command_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="chatq-visualization",
        description="Validate and render strict Chat-Quant visualization specs.",
    )
    subparsers = parser.add_subparsers(dest="command_group", required=True)

    for kind in ("chart", "table", "card", "report"):
        group = subparsers.add_parser(kind, help=f"Render a {kind} visualization.")
        group_subparsers = group.add_subparsers(dest="command", required=True)
        render = group_subparsers.add_parser("render", help=f"Render a {kind} spec to HTML.")
        render.add_argument("--file", required=True, help="Spec file path under the project.")
        render.add_argument(
            "--output-file",
            required=True,
            help=(
                "Output HTML path under the project. "
                "Use visualization/name.html by default unless the user asks otherwise."
            ),
        )
        render.add_argument("--json", action="store_true", help="Return a JSON result.")

    validate = subparsers.add_parser("validate", help="Validate a visualization spec file.")
    validate.add_argument("--file", required=True, help="Spec file path under the project.")
    validate.add_argument(
        "--kind",
        choices=["chart", "table", "card", "report"],
        default=None,
        help="Optional expected kind.",
    )
    validate.add_argument("--json", action="store_true", help="Return a JSON result.")

    schema = subparsers.add_parser("schema", help="Show a spec schema example.")
    schema.add_argument("kind", choices=["chart", "table", "card", "report"])
    schema.add_argument("--json", action="store_true", help="Return machine-readable schema.")

    return parser


def run_cli_command(command: AgentExecutionCommand, args: argparse.Namespace) -> ToolPayload:
    project_dir = _resolve_project_dir(command.project_dir)

    if args.command_group == "schema":
        return _success(
            "schema",
            schema_for_kind(args.kind),
            summary=f"Visualization schema: {args.kind}",
        )

    if args.command_group == "validate":
        loaded = load_spec(project_dir, args.file)
        expected_kind = args.kind
        issues = validate_spec(loaded.data, expected_kind=expected_kind)
        if issues:
            raise _validation_error(loaded, issues, expected_kind=expected_kind)
        data: ValidationSuccessData = {
            "file": loaded.relative_path,
            "kind": loaded.data.get("kind"),
            "issues": [],
        }
        return _success(
            "validate",
            data,
            summary="Visualization spec is valid.",
        )

    if args.command_group in {"chart", "table", "card", "report"} and args.command == "render":
        expected_kind = str(args.command_group)
        loaded = load_spec(project_dir, args.file)
        issues = validate_spec(loaded.data, expected_kind=expected_kind)
        if issues:
            raise _validation_error(loaded, issues, expected_kind=expected_kind)
        output_path = _resolve_output_file(project_dir, args.output_file)
        spec = cast(VisualizationSpec, loaded.data)
        html_text = render_spec(spec)
        _write_html_atomic(output_path, html_text)
        relative_output = _relative_to_project(project_dir, output_path)
        data: RenderSuccessData = {
            "file": loaded.relative_path,
            "kind": expected_kind,
            "output_file": relative_output,
            "iframe_url": project_visualization_html_url(command.project_id, relative_output),
            "asset_base_url": visualization_asset_url(),
        }
        return _success(
            f"{expected_kind} render",
            data,
            summary="Visualization HTML generated.",
            artifacts=[
                {
                    "asset_type": "html",
                    "asset_id": relative_output,
                    "title": str(loaded.data.get("title") or relative_output),
                }
            ],
        )

    raise ToolExecutionError(
        "CHATQ_VISUALIZATION_COMMAND_UNSUPPORTED",
        f"Unsupported command: {_operator(args)}",
    )


def load_spec(project_dir: Path, file_path: str) -> LoadedSpec:
    path = _resolve_input_file(project_dir, file_path)
    try:
        size = path.stat().st_size
    except OSError as exc:
        raise ToolExecutionError(
            "CHATQ_VISUALIZATION_FILE_STAT_FAILED",
            "Visualization spec file cannot be inspected",
            detail={"file": str(path), "reason": str(exc)},
        ) from exc
    if size > MAX_SPEC_FILE_BYTES:
        raise ToolExecutionError(
            "CHATQ_VISUALIZATION_FILE_TOO_LARGE",
            "Visualization spec file is too large",
            detail={
                "file": _relative_to_project(project_dir, path),
                "max_bytes": MAX_SPEC_FILE_BYTES,
                "actual_bytes": size,
            },
        )
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ToolExecutionError(
            "CHATQ_VISUALIZATION_FILE_ENCODING_INVALID",
            "Visualization spec file must be UTF-8 text",
            detail={"file": _relative_to_project(project_dir, path), "reason": str(exc)},
        ) from exc

    try:
        parsed = _parse_spec_text(path, text)
    except ToolExecutionError as exc:
        exc.detail.setdefault("file", _relative_to_project(project_dir, path))
        raise

    if not isinstance(parsed, dict):
        raise ToolExecutionError(
            "CHATQ_VISUALIZATION_SPEC_ROOT_INVALID",
            "Visualization spec root must be an object",
            detail={"file": _relative_to_project(project_dir, path)},
        )
    return LoadedSpec(path=path, relative_path=_relative_to_project(project_dir, path), data=parsed)


def _parse_spec_text(path: Path, text: str) -> Any:
    suffix = path.suffix.lower()
    if suffix == ".json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ToolExecutionError(
                "CHATQ_VISUALIZATION_JSON_INVALID",
                "Visualization JSON spec cannot be parsed",
                detail={"line": exc.lineno, "column": exc.colno, "reason": exc.msg},
            ) from exc
    if suffix in {".yaml", ".yml"}:
        try:
            import yaml  # type: ignore[import-not-found]
        except ImportError as exc:
            raise ToolExecutionError(
                "CHATQ_VISUALIZATION_YAML_UNAVAILABLE",
                "YAML visualization specs require PyYAML; use .json or install PyYAML",
            ) from exc
        try:
            return yaml.safe_load(text)
        except yaml.YAMLError as exc:
            raise ToolExecutionError(
                "CHATQ_VISUALIZATION_YAML_INVALID",
                "Visualization YAML spec cannot be parsed",
                detail={"reason": str(exc)},
            ) from exc
    raise ToolExecutionError(
        "CHATQ_VISUALIZATION_FILE_TYPE_UNSUPPORTED",
        "Visualization spec file must be .json, .yaml, or .yml",
        detail={"suffix": suffix or "(none)"},
    )


def validate_spec(spec: RawSpec, *, expected_kind: str | None = None) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    kind = spec.get("kind")
    if not isinstance(kind, str) or kind not in ROOT_KEYS:
        issues.append(
            ValidationIssue(
                "kind",
                "KIND_INVALID",
                'kind must be one of "chart", "table", "card", or "report"',
            )
        )
        return issues
    if expected_kind is not None and kind != expected_kind:
        issues.append(
            ValidationIssue(
                "kind",
                "KIND_MISMATCH",
                f'expected kind "{expected_kind}" but got "{kind}"',
            )
        )
    if kind == "chart":
        _validate_chart(spec, "root", issues, require_kind=True)
    elif kind == "table":
        _validate_table(spec, "root", issues, require_kind=True)
    elif kind == "card":
        _validate_card_group(spec, "root", issues, require_kind=True)
    elif kind == "report":
        _validate_report(spec, "root", issues)
    return issues


def _validate_report(spec: RawSpec, path: str, issues: list[ValidationIssue]) -> None:
    _check_unknown_keys(spec, ROOT_KEYS["report"], path, issues)
    _require_text(spec, "title", f"{path}.title", issues)
    _validate_optional_text(spec, "subtitle", f"{path}.subtitle", issues)
    _validate_optional_text(spec, "source", f"{path}.source", issues)
    layout = spec.get("layout", {"columns": 2})
    if "layout" in spec:
        if not isinstance(layout, dict):
            issues.append(
                ValidationIssue(f"{path}.layout", "TYPE_INVALID", "layout must be an object")
            )
        else:
            _check_unknown_keys(layout, LAYOUT_KEYS, f"{path}.layout", issues)
            columns = layout.get("columns", 2)
            if not isinstance(columns, int) or columns < 1 or columns > 3:
                issues.append(
                    ValidationIssue(
                        f"{path}.layout.columns",
                        "VALUE_INVALID",
                        "layout.columns must be an integer between 1 and 3",
                    )
                )
    for key in ("cards", "charts", "tables"):
        if key in spec and not isinstance(spec[key], list):
            issues.append(
                ValidationIssue(f"{path}.{key}", "TYPE_INVALID", f"{key} must be an array")
            )
    has_content = any(
        isinstance(spec.get(key), list) and spec[key]
        for key in ("cards", "charts", "tables")
    )
    if not has_content:
        issues.append(
            ValidationIssue(
                path,
                "CONTENT_EMPTY",
                "report must contain at least one card, chart, or table",
            )
        )
    for index, card in enumerate(spec.get("cards") or []):
        if not isinstance(card, dict):
            issues.append(
                ValidationIssue(
                    f"{path}.cards[{index}]",
                    "TYPE_INVALID",
                    "card must be an object",
                )
            )
            continue
        _validate_single_card(card, f"{path}.cards[{index}]", issues)
    for index, chart in enumerate(spec.get("charts") or []):
        if not isinstance(chart, dict):
            issues.append(
                ValidationIssue(
                    f"{path}.charts[{index}]",
                    "TYPE_INVALID",
                    "chart must be an object",
                )
            )
            continue
        _validate_chart(chart, f"{path}.charts[{index}]", issues, require_kind=False)
    for index, table in enumerate(spec.get("tables") or []):
        if not isinstance(table, dict):
            issues.append(
                ValidationIssue(
                    f"{path}.tables[{index}]",
                    "TYPE_INVALID",
                    "table must be an object",
                )
            )
            continue
        _validate_table(table, f"{path}.tables[{index}]", issues, require_kind=False)


def _validate_chart(
    spec: RawSpec,
    path: str,
    issues: list[ValidationIssue],
    *,
    require_kind: bool,
) -> None:
    allowed_keys = ROOT_KEYS["chart"] if require_kind else NESTED_CHART_KEYS
    _check_unknown_keys(spec, allowed_keys, path, issues)
    if require_kind:
        _require_kind(spec, "chart", f"{path}.kind", issues)
    elif "kind" in spec:
        _require_kind(spec, "chart", f"{path}.kind", issues)
    _require_text(spec, "title", f"{path}.title", issues)
    _validate_optional_text(spec, "subtitle", f"{path}.subtitle", issues)
    _validate_optional_text(spec, "source", f"{path}.source", issues)
    chart_type = spec.get("type")
    if not isinstance(chart_type, str) or chart_type not in CHART_TYPES:
        issues.append(
            ValidationIssue(
                f"{path}.type",
                "CHART_TYPE_INVALID",
                f"chart type must be one of {sorted(CHART_TYPES)}",
            )
        )
    table = _validate_tabular_data(spec.get("data"), f"{path}.data", issues)
    if "x" not in spec and chart_type != "pie":
        issues.append(ValidationIssue(f"{path}.x", "FIELD_REQUIRED", "x is required"))
    elif "x" in spec:
        _validate_x(spec["x"], f"{path}.x", issues, table)
    series = spec.get("series")
    if not isinstance(series, list) or not series:
        issues.append(
            ValidationIssue(f"{path}.series", "FIELD_REQUIRED", "series must be a non-empty array")
        )
        return
    if chart_type == "heatmap" and len(series) != 1:
        issues.append(
            ValidationIssue(
                f"{path}.series",
                "SERIES_COUNT_INVALID",
                "heatmap charts must define exactly one series",
            )
        )
    for index, item in enumerate(series):
        if not isinstance(item, dict):
            issues.append(
                ValidationIssue(
                    f"{path}.series[{index}]",
                    "TYPE_INVALID",
                    "series item must be an object",
                )
            )
            continue
        _validate_series(item, f"{path}.series[{index}]", issues, table, chart_type)
    height = spec.get("height")
    if height is not None and (
        not isinstance(height, int) or height < MIN_CHART_HEIGHT or height > MAX_CHART_HEIGHT
    ):
        issues.append(
            ValidationIssue(
                f"{path}.height",
                "VALUE_INVALID",
                f"height must be an integer between {MIN_CHART_HEIGHT} and {MAX_CHART_HEIGHT}",
            )
        )
    if "options" in spec and not isinstance(spec["options"], dict):
        issues.append(
            ValidationIssue(f"{path}.options", "TYPE_INVALID", "options must be an object")
        )


def _validate_table(
    spec: RawSpec,
    path: str,
    issues: list[ValidationIssue],
    *,
    require_kind: bool,
) -> None:
    allowed_keys = ROOT_KEYS["table"] if require_kind else NESTED_TABLE_KEYS
    _check_unknown_keys(spec, allowed_keys, path, issues)
    if require_kind:
        _require_kind(spec, "table", f"{path}.kind", issues)
    elif "kind" in spec:
        _require_kind(spec, "table", f"{path}.kind", issues)
    _require_text(spec, "title", f"{path}.title", issues)
    _validate_optional_text(spec, "subtitle", f"{path}.subtitle", issues)
    _validate_optional_text(spec, "source", f"{path}.source", issues)
    _validate_tabular_data(spec.get("data"), f"{path}.data", issues)


def _validate_card_group(
    spec: RawSpec,
    path: str,
    issues: list[ValidationIssue],
    *,
    require_kind: bool,
) -> None:
    _check_unknown_keys(spec, ROOT_KEYS["card"], path, issues)
    if require_kind:
        _require_kind(spec, "card", f"{path}.kind", issues)
    _require_text(spec, "title", f"{path}.title", issues)
    _validate_optional_text(spec, "subtitle", f"{path}.subtitle", issues)
    _validate_optional_text(spec, "source", f"{path}.source", issues)
    cards = spec.get("cards")
    if not isinstance(cards, list) or not cards:
        issues.append(
            ValidationIssue(f"{path}.cards", "FIELD_REQUIRED", "cards must be a non-empty array")
        )
        return
    for index, card in enumerate(cards):
        if not isinstance(card, dict):
            issues.append(
                ValidationIssue(
                    f"{path}.cards[{index}]",
                    "TYPE_INVALID",
                    "card must be an object",
                )
            )
            continue
        _validate_single_card(card, f"{path}.cards[{index}]", issues)


def _validate_single_card(card: RawSpec, path: str, issues: list[ValidationIssue]) -> None:
    _check_unknown_keys(card, CARD_KEYS, path, issues)
    _require_text(card, "label", f"{path}.label", issues)
    if "value" not in card:
        issues.append(ValidationIssue(f"{path}.value", "FIELD_REQUIRED", "value is required"))
    elif card["value"] is None or card["value"] == "":
        issues.append(ValidationIssue(f"{path}.value", "VALUE_EMPTY", "value cannot be empty"))
    fmt = card.get("format", "string")
    if not isinstance(fmt, str) or fmt not in CARD_FORMATS:
        issues.append(
            ValidationIssue(
                f"{path}.format",
                "FORMAT_INVALID",
                f"format must be one of {sorted(CARD_FORMATS)}",
            )
        )
    elif fmt != "string" and "value" in card and not _is_number(card["value"]):
        issues.append(
            ValidationIssue(
                f"{path}.value",
                "NUMBER_INVALID",
                f'value must be numeric when format is "{fmt}"',
            )
        )
    decimals = card.get("decimals")
    if decimals is not None and (not isinstance(decimals, int) or decimals < 0):
        issues.append(
            ValidationIssue(
                f"{path}.decimals",
                "VALUE_INVALID",
                "decimals must be a non-negative integer",
            )
        )
    for key in ("unit", "icon", "description"):
        if key in card and card[key] is not None and not isinstance(card[key], str):
            issues.append(
                ValidationIssue(f"{path}.{key}", "TYPE_INVALID", f"{key} must be a string")
            )


def _validate_tabular_data(
    data: object,
    path: str,
    issues: list[ValidationIssue],
) -> TabularData | None:
    if not isinstance(data, dict):
        issues.append(
            ValidationIssue(path, "TYPE_INVALID", "data must be an object with columns and rows")
        )
        return None
    _check_unknown_keys(data, DATA_KEYS, path, issues)
    columns = data.get("columns")
    rows = data.get("rows")
    if not isinstance(columns, list) or not columns:
        issues.append(
            ValidationIssue(f"{path}.columns", "FIELD_REQUIRED", "data.columns must be non-empty")
        )
        return None
    invalid_columns = [index for index, value in enumerate(columns) if not isinstance(value, str)]
    if invalid_columns:
        issues.append(
            ValidationIssue(
                f"{path}.columns",
                "TYPE_INVALID",
                "every column name must be a string",
                hint=f"invalid indexes: {invalid_columns}",
            )
        )
    duplicate_columns = sorted({value for value in columns if columns.count(value) > 1})
    if duplicate_columns:
        issues.append(
            ValidationIssue(
                f"{path}.columns",
                "DUPLICATE_COLUMN",
                "data.columns cannot contain duplicate names",
                hint=f"duplicates: {duplicate_columns}",
            )
        )
    if not isinstance(rows, list) or not rows:
        issues.append(
            ValidationIssue(f"{path}.rows", "FIELD_REQUIRED", "data.rows must be non-empty")
        )
        return {"columns": columns, "rows": []}
    if len(rows) > MAX_ROWS:
        issues.append(
            ValidationIssue(
                f"{path}.rows",
                "ROW_LIMIT_EXCEEDED",
                f"data.rows cannot exceed {MAX_ROWS} rows",
                hint="split the report or reduce rows before rendering",
            )
        )
    for index, row in enumerate(rows):
        if not isinstance(row, list):
            issues.append(
                ValidationIssue(f"{path}.rows[{index}]", "TYPE_INVALID", "row must be an array")
            )
            continue
        if len(row) != len(columns):
            issues.append(
                ValidationIssue(
                    f"{path}.rows[{index}]",
                    "ROW_LENGTH_MISMATCH",
                    f"row has {len(row)} values but data.columns has {len(columns)} columns",
                    hint=f"columns are {columns}",
                )
            )
    return cast(TabularData, {"columns": columns, "rows": rows})


def _validate_x(
    x: object,
    path: str,
    issues: list[ValidationIssue],
    table: TabularData | None,
) -> None:
    if not isinstance(x, dict):
        issues.append(ValidationIssue(path, "TYPE_INVALID", "x must be an object"))
        return
    _check_unknown_keys(x, X_KEYS, path, issues)
    _require_field_ref(x, "field", f"{path}.field", issues, table)


def _validate_series(
    series: RawSpec,
    path: str,
    issues: list[ValidationIssue],
    table: TabularData | None,
    chart_type: object,
) -> None:
    _check_unknown_keys(series, SERIES_KEYS, path, issues)
    _require_text(series, "name", f"{path}.name", issues)
    if "item_style" in series and not isinstance(series["item_style"], dict):
        issues.append(
            ValidationIssue(f"{path}.item_style", "TYPE_INVALID", "item_style must be an object")
        )
    if chart_type in {"line", "bar"}:
        field = _require_field_ref(series, "field", f"{path}.field", issues, table)
        if field:
            _require_numeric_column(table, field, f"{path}.field", issues)
        if "stack" in series and not isinstance(series["stack"], str):
            issues.append(
                ValidationIssue(f"{path}.stack", "TYPE_INVALID", "stack must be a string")
            )
        return
    if chart_type == "scatter":
        fields = _require_fields_object(series, f"{path}.fields", issues)
        for key in ("x", "y"):
            field = _require_field_ref(fields, key, f"{path}.fields.{key}", issues, table)
            if field:
                _require_numeric_column(table, field, f"{path}.fields.{key}", issues)
        return
    if chart_type == "heatmap":
        fields = _require_fields_object(series, f"{path}.fields", issues)
        for key in ("x", "y", "value"):
            field = _require_field_ref(fields, key, f"{path}.fields.{key}", issues, table)
            if key == "value" and field:
                _require_numeric_column(table, field, f"{path}.fields.{key}", issues)
        return
    if chart_type == "candlestick":
        fields = _require_fields_object(series, f"{path}.fields", issues)
        for key in ("open", "close", "low", "high"):
            field = _require_field_ref(fields, key, f"{path}.fields.{key}", issues, table)
            if field:
                _require_numeric_column(table, field, f"{path}.fields.{key}", issues)
        return
    if chart_type == "pie":
        name_field = _require_field_ref(series, "name_field", f"{path}.name_field", issues, table)
        value_field = _require_field_ref(
            series,
            "value_field",
            f"{path}.value_field",
            issues,
            table,
        )
        if value_field:
            _require_numeric_column(table, value_field, f"{path}.value_field", issues)
        if name_field and value_field and name_field == value_field:
            issues.append(
                ValidationIssue(
                    f"{path}.value_field",
                    "FIELD_INVALID",
                    "name_field and value_field must be different",
                )
            )


def _require_fields_object(
    value: RawSpec,
    path: str,
    issues: list[ValidationIssue],
) -> RawSpec:
    fields = value.get("fields")
    if not isinstance(fields, dict):
        issues.append(ValidationIssue(path, "FIELD_REQUIRED", "fields must be an object"))
        return {}
    return fields


def _require_field_ref(
    value: RawSpec,
    key: str,
    path: str,
    issues: list[ValidationIssue],
    table: TabularData | None,
) -> str | None:
    field = value.get(key)
    if not isinstance(field, str) or not field:
        issues.append(ValidationIssue(path, "FIELD_REQUIRED", f"{key} is required"))
        return None
    columns = table.get("columns") if table else None
    if isinstance(columns, list) and field not in columns:
        issues.append(
            ValidationIssue(
                path,
                "FIELD_NOT_FOUND",
                f'field "{field}" does not exist in data.columns',
                hint=f"available fields: {columns}",
            )
        )
        return None
    return field


def _require_numeric_column(
    table: TabularData | None,
    field: str,
    path: str,
    issues: list[ValidationIssue],
) -> None:
    if table is None:
        return
    columns = table.get("columns")
    rows = table.get("rows")
    if not isinstance(columns, list) or field not in columns or not isinstance(rows, list):
        return
    field_index = columns.index(field)
    for row_index, row in enumerate(rows):
        if not isinstance(row, list) or len(row) <= field_index:
            continue
        value = row[field_index]
        if not _is_number(value):
            issues.append(
                ValidationIssue(
                    f"{path}.data.rows[{row_index}]",
                    "NUMBER_INVALID",
                    f'field "{field}" must be numeric',
                    hint=f"value: {value!r}",
                )
            )


def render_spec(spec: VisualizationSpec) -> str:
    kind = spec["kind"]
    if kind == "chart":
        chart = cast(ChartSpec, spec)
        return _render_page(
            str(chart["title"]),
            subtitle=chart.get("subtitle"),
            source=chart.get("source"),
            cards=[],
            charts=[chart],
            tables=[],
        )
    if kind == "table":
        table = cast(TableSpec, spec)
        return _render_page(
            str(table["title"]),
            subtitle=table.get("subtitle"),
            source=table.get("source"),
            cards=[],
            charts=[],
            tables=[table],
        )
    if kind == "card":
        card_group = cast(CardGroupSpec, spec)
        return _render_page(
            str(card_group["title"]),
            subtitle=card_group.get("subtitle"),
            source=card_group.get("source"),
            cards=card_group["cards"],
            charts=[],
            tables=[],
        )
    if kind == "report":
        report = cast(ReportSpec, spec)
        layout = report.get("layout") or {}
        return _render_page(
            str(report["title"]),
            subtitle=report.get("subtitle"),
            source=report.get("source"),
            cards=report.get("cards") or [],
            charts=report.get("charts") or [],
            tables=report.get("tables") or [],
            columns=int(layout.get("columns", 2)),
        )
    raise ToolExecutionError(
        "CHATQ_VISUALIZATION_KIND_UNSUPPORTED",
        f"Unsupported visualization kind: {kind}",
    )


def project_visualization_html_url(project_id: str, output_file: str) -> str:
    api_prefix = get_settings().api_prefix.rstrip("/")
    quoted_project_id = quote(project_id, safe="")
    quoted_file = quote(output_file, safe="/")
    return f"{api_prefix}/projects/{quoted_project_id}/visualization-html/{quoted_file}"


def visualization_asset_url() -> str:
    api_prefix = get_settings().api_prefix.rstrip("/")
    return f"{api_prefix}{VISUALIZATION_ASSET_ROUTE}" if api_prefix else VISUALIZATION_ASSET_ROUTE


def _render_page(
    title: str,
    *,
    subtitle: str | None = None,
    source: str | None = None,
    cards: list[CardSpec],
    charts: list[ChartSpec],
    tables: list[TableSpec],
    columns: int = 2,
) -> str:
    chart_options = [_build_echarts_option(chart) for chart in charts]
    chart_payload = json.dumps(chart_options, ensure_ascii=False)
    safe_title = html.escape(title)
    header_meta = _render_page_meta(subtitle, source)
    cards_html = "\n".join(_render_card(card) for card in cards)
    tables_html = "\n".join(_render_table(table, index) for index, table in enumerate(tables))
    charts_html = "\n".join(
        _render_chart_panel(chart, index)
        for index, chart in enumerate(charts)
    )
    card_section = f'<section class="cards-grid">{cards_html}</section>' if cards else ""
    chart_section = (
        f'<section class="charts-grid" style="--columns: {columns}">{charts_html}</section>'
        if charts
        else ""
    )
    table_section = f'<section class="tables-stack">{tables_html}</section>' if tables else ""
    modal_html = _render_chart_modal() if charts else ""
    asset_url = visualization_asset_url()
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{safe_title}</title>
  <script src="{asset_url}/tailwindcss-3.4.16.js"></script>
  <script src="{asset_url}/lucide.js"></script>
  <script src="{asset_url}/echarts.5.6.0.min.js"></script>
  <style>
    :root {{
      --cq-app: #f6f7f3;
      --cq-panel: #fffdf8;
      --cq-soft: #f0f3ee;
      --cq-line: #d9ded6;
      --cq-strong: #b7c0b6;
      --cq-ink: #171a16;
      --cq-muted: #6d746f;
      --cq-graphite: #343941;
      --cq-brand: #16845f;
      --cq-blue: #316a9e;
      --cq-signal: #c9851a;
      --cq-risk: #d4483b;
      --cq-gain-soft: #e6f3ec;
      --cq-compare-soft: #e3eef7;
    }}
    body {{
      margin: 0;
      background:
        linear-gradient(90deg, rgba(23, 26, 22, 0.035) 1px, transparent 1px),
        linear-gradient(0deg, rgba(23, 26, 22, 0.028) 1px, transparent 1px),
        var(--cq-app);
      background-size: 28px 28px;
      color: var(--cq-ink);
      font-family:
        Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    .page {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 18px;
    }}
    header {{
      background: rgba(255, 253, 248, 0.86);
      border: 1px solid var(--cq-line);
      border-radius: 8px;
      box-shadow: 0 10px 30px rgba(38, 49, 42, 0.06);
      margin-bottom: 14px;
      padding: 15px 16px;
    }}
    h1 {{
      font-size: 20px;
      line-height: 1.25;
      margin: 0;
    }}
    .page-subtitle {{
      color: var(--cq-muted);
      font-size: 13px;
      line-height: 1.6;
      margin: 6px 0 0;
    }}
    .page-meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 10px;
    }}
    .meta-pill {{
      background: var(--cq-soft);
      border: 1px solid var(--cq-line);
      border-radius: 6px;
      color: var(--cq-muted);
      font-size: 12px;
      line-height: 1.4;
      max-width: 100%;
      overflow-wrap: anywhere;
      padding: 5px 8px;
    }}
    .cards-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 12px;
      margin-bottom: 14px;
    }}
    .card, .panel {{
      background: var(--cq-panel);
      border: 1px solid var(--cq-line);
      border-radius: 8px;
      box-shadow: 0 8px 24px rgba(38, 49, 42, 0.055);
    }}
    .card {{
      overflow: hidden;
      padding: 14px;
      transition: box-shadow 0.2s ease, transform 0.2s ease;
    }}
    .card:hover {{
      box-shadow: 0 12px 30px rgba(38, 49, 42, 0.10);
      transform: translateY(-1px);
    }}
    .card-header {{
      align-items: center;
      display: flex;
      gap: 10px;
      margin-bottom: 12px;
    }}
    .card-icon {{
      align-items: center;
      background: var(--cq-gain-soft);
      border-radius: 8px;
      color: var(--cq-brand);
      display: inline-flex;
      flex: 0 0 auto;
      height: 34px;
      justify-content: center;
      width: 34px;
    }}
    .card-icon svg {{
      height: 18px;
      width: 18px;
    }}
    .card-label {{
      color: var(--cq-muted);
      font-size: 12px;
      font-weight: 650;
      letter-spacing: 0;
      line-height: 1.3;
    }}
    .card-value {{
      align-items: baseline;
      display: flex;
      gap: 6px;
      min-width: 0;
    }}
    .card-number {{
      color: var(--cq-ink);
      font-size: 28px;
      font-weight: 720;
      letter-spacing: 0;
      line-height: 1.15;
      overflow-wrap: anywhere;
    }}
    .card-unit, .card-description {{
      color: var(--cq-muted);
      font-size: 13px;
    }}
    .card-description {{
      margin-top: 10px;
    }}
    .charts-grid {{
      display: grid;
      grid-template-columns: repeat(var(--columns), minmax(0, 1fr));
      gap: 14px;
      margin-bottom: 14px;
    }}
    .panel {{
      padding: 14px;
    }}
    .panel-header {{
      align-items: center;
      display: flex;
      gap: 12px;
      justify-content: space-between;
      margin-bottom: 10px;
    }}
    .panel-title {{
      align-items: center;
      display: flex;
      gap: 8px;
      min-width: 0;
    }}
    .panel-title-stack {{
      min-width: 0;
    }}
    .title-indicator {{
      background: var(--cq-signal);
      border-radius: 2px;
      flex: 0 0 auto;
      height: 18px;
      width: 4px;
    }}
    .panel-header h2 {{
      font-size: 16px;
      line-height: 1.3;
      margin: 0;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }}
    .panel-subtitle, .panel-source {{
      color: var(--cq-muted);
      font-size: 12px;
      line-height: 1.45;
      margin-top: 4px;
      overflow-wrap: anywhere;
    }}
    .panel-source {{
      color: var(--cq-muted);
      opacity: 0.82;
    }}
    .chart-toolbar {{
      align-items: center;
      display: inline-flex;
      flex: 0 0 auto;
      gap: 6px;
    }}
    .icon-button {{
      align-items: center;
      background: var(--cq-panel);
      border: 1px solid var(--cq-line);
      border-radius: 6px;
      color: var(--cq-muted);
      cursor: pointer;
      display: inline-flex;
      height: 32px;
      justify-content: center;
      padding: 0;
      transition: border-color 0.2s ease, color 0.2s ease, background 0.2s ease;
      width: 32px;
    }}
    .icon-button:hover {{
      background: var(--cq-compare-soft);
      border-color: var(--cq-blue);
      color: var(--cq-blue);
    }}
    .icon-button svg {{
      height: 16px;
      width: 16px;
    }}
    .chart {{
      min-height: 240px;
      width: 100%;
    }}
    .tables-stack {{
      display: grid;
      gap: 16px;
    }}
    .table-wrap {{
      overflow: auto;
    }}
    table {{
      border-collapse: collapse;
      min-width: 100%;
    }}
    th, td {{
      border-bottom: 1px solid var(--cq-line);
      font-size: 13px;
      padding: 10px 12px;
      text-align: left;
      white-space: nowrap;
    }}
    th {{
      background: var(--cq-soft);
      color: var(--cq-graphite);
      font-weight: 650;
      padding: 0;
    }}
    tbody tr:hover {{
      background: var(--cq-soft);
    }}
    .sort-button {{
      align-items: center;
      background: transparent;
      border: 0;
      color: inherit;
      cursor: pointer;
      display: flex;
      font: inherit;
      gap: 8px;
      justify-content: space-between;
      letter-spacing: 0;
      min-width: 100%;
      padding: 10px 12px;
      text-align: left;
    }}
    .sort-button:hover {{
      background: rgba(217, 222, 214, 0.55);
    }}
    .sort-arrows {{
      align-items: center;
      color: var(--cq-strong);
      display: inline-flex;
      flex-direction: column;
      font-size: 8px;
      line-height: 0.85;
    }}
    th.sorted-asc .sort-up,
    th.sorted-desc .sort-down {{
      color: var(--cq-blue);
    }}
    .modal-overlay {{
      align-items: center;
      background: rgba(23, 26, 22, 0.62);
      display: none;
      inset: 0;
      justify-content: center;
      opacity: 0;
      padding: 24px;
      position: fixed;
      transition: opacity 0.2s ease;
      z-index: 1000;
    }}
    .modal-overlay.show {{
      display: flex;
      opacity: 1;
    }}
    .modal-content {{
      background: var(--cq-panel);
      border-radius: 8px;
      box-shadow: 0 20px 60px rgba(38, 49, 42, 0.18);
      display: flex;
      flex-direction: column;
      max-height: 90vh;
      max-width: 1200px;
      overflow: hidden;
      transform: scale(0.98);
      transition: transform 0.2s ease;
      width: min(1200px, 96vw);
    }}
    .modal-overlay.show .modal-content {{
      transform: scale(1);
    }}
    .modal-header {{
      align-items: center;
      border-bottom: 1px solid var(--cq-line);
      display: flex;
      gap: 12px;
      justify-content: space-between;
      padding: 14px 16px;
    }}
    .modal-title {{
      align-items: center;
      display: flex;
      font-size: 16px;
      font-weight: 700;
      gap: 8px;
      min-width: 0;
    }}
    .modal-body {{
      padding: 16px;
    }}
    .modal-chart {{
      height: min(68vh, 640px);
      min-height: 420px;
      width: 100%;
    }}
    @media (max-width: 900px) {{
      .page {{
        padding: 16px;
      }}
      .charts-grid {{
        grid-template-columns: 1fr;
      }}
      .panel-header {{
        align-items: flex-start;
      }}
      .modal-overlay {{
        padding: 10px;
      }}
      .modal-chart {{
        min-height: 320px;
      }}
    }}
  </style>
</head>
<body>
  <main class="page">
    <header>
      <h1>{safe_title}</h1>
      {header_meta}
    </header>
    {card_section}
    {chart_section}
    {table_section}
  </main>
  {modal_html}
  <script>
    const chartOptions = {chart_payload};
    const chartInstances = [];
    const PIE_COLORS = {json.dumps(PIE_COLORS)};

    function deepClone(value) {{
      return JSON.parse(JSON.stringify(value));
    }}

    function normalizeChartOption(option) {{
      option.color = option.color || PIE_COLORS;
      if (!option.grid && option.xAxis && option.yAxis) {{
        option.grid = {{ left: '4%', right: '4%', top: 48, bottom: 52, containLabel: true }};
      }} else if (option.grid) {{
        option.grid.containLabel = true;
      }}
      if (option.legend) {{
        option.legend.type = option.legend.type || 'scroll';
      }}
      const firstSeries = Array.isArray(option.series) ? option.series[0] : null;
      const chartType = firstSeries ? firstSeries.type : '';
      const supportsZoom = (
        chartType === 'line' || chartType === 'bar' || chartType === 'candlestick'
      );
      if (supportsZoom && !option.dataZoom) {{
        option.dataZoom = [
          {{ type: 'inside', start: 0, end: 100, zoomOnMouseWheel: true, moveOnMouseMove: true }},
          {{ type: 'slider', start: 0, end: 100, height: 20, bottom: 6 }}
        ];
      }}
      if (chartType === 'candlestick' && option.yAxis && !Array.isArray(option.yAxis)) {{
        option.yAxis.scale = option.yAxis.scale !== undefined ? option.yAxis.scale : true;
      }}
      if (chartType === 'pie') {{
        option.series.forEach((series) => {{
          if (!Array.isArray(series.data)) return;
          series.data.forEach((item, index) => {{
            if (item && typeof item === 'object') {{
              item.itemStyle = item.itemStyle || {{}};
              item.itemStyle.color = item.itemStyle.color || PIE_COLORS[index % PIE_COLORS.length];
            }}
          }});
        }});
      }}
      if (option.xAxis && !Array.isArray(option.xAxis)) {{
        option.xAxis.splitLine = option.xAxis.splitLine || {{
          show: true,
          lineStyle: {{ color: '#d9ded6', type: 'dashed' }}
        }};
      }}
      if (option.yAxis && !Array.isArray(option.yAxis)) {{
        option.yAxis.splitLine = option.yAxis.splitLine || {{
          show: true,
          lineStyle: {{ color: '#d9ded6', type: 'dashed' }}
        }};
      }}
      return option;
    }}

    chartOptions.forEach((option, index) => {{
      const el = document.getElementById(`chart-${{index}}`);
      if (!el) return;
      const normalized = normalizeChartOption(deepClone(option));
      const chart = echarts.init(el);
      chart.setOption(normalized, true);
      chartInstances[index] = {{
        chart,
        option: normalized,
        title: el.dataset.chartTitle || ''
      }};
      if (window.ResizeObserver) {{
        const resizeObserver = new ResizeObserver(() => chart.resize());
        resizeObserver.observe(el);
      }}
    }});

    window.addEventListener('resize', () => {{
      chartInstances.forEach((entry) => entry.chart.resize());
    }});

    document.querySelectorAll('[data-chart-zoom]').forEach((button) => {{
      button.addEventListener('click', () => openChartModal(Number(button.dataset.chartIndex)));
    }});

    let modalChart = null;

    function openChartModal(index) {{
      const entry = chartInstances[index];
      const modal = document.getElementById('chart-modal');
      const modalChartEl = document.getElementById('modal-chart');
      if (!entry || !modal || !modalChartEl) return;
      modal.querySelector('.modal-title-text').textContent = entry.title || '图表详情';
      modal.classList.add('show');
      document.body.style.overflow = 'hidden';
      if (modalChart) {{
        modalChart.dispose();
      }}
      modalChart = echarts.init(modalChartEl);
      modalChart.setOption(deepClone(entry.option), true);
      setTimeout(() => modalChart.resize(), 0);
    }}

    function closeChartModal() {{
      const modal = document.getElementById('chart-modal');
      if (!modal) return;
      modal.classList.remove('show');
      document.body.style.overflow = '';
      if (modalChart) {{
        modalChart.dispose();
        modalChart = null;
      }}
    }}

    document.querySelectorAll('[data-modal-close]').forEach((button) => {{
      button.addEventListener('click', closeChartModal);
    }});

    const modal = document.getElementById('chart-modal');
    if (modal) {{
      modal.addEventListener('click', (event) => {{
        if (event.target === modal) closeChartModal();
      }});
    }}

    document.addEventListener('keydown', (event) => {{
      if (event.key === 'Escape') closeChartModal();
    }});

    const sortStates = {{}};

    document.querySelectorAll('[data-sort-button]').forEach((button) => {{
      button.addEventListener('click', () => {{
        sortTable(button.dataset.tableId, Number(button.dataset.columnIndex));
      }});
    }});

    function sortTable(tableId, columnIndex) {{
      const table = document.getElementById(tableId);
      if (!table) return;
      const tbody = table.querySelector('tbody');
      const header = table.querySelector(`th[data-column-index="${{columnIndex}}"]`);
      if (!tbody || !header) return;
      const rows = Array.from(tbody.querySelectorAll('tr'));
      sortStates[tableId] = sortStates[tableId] || {{}};
      const currentState = sortStates[tableId][columnIndex] || null;
      const nextState = currentState === null ? 'asc' : currentState === 'asc' ? 'desc' : null;
      sortStates[tableId][columnIndex] = nextState;
      table.querySelectorAll('th').forEach((th) => {{
        th.classList.remove('sorted-asc', 'sorted-desc');
      }});
      if (nextState) {{
        header.classList.add(`sorted-${{nextState}}`);
      }}
      rows.sort((a, b) => {{
        if (!nextState) {{
          return Number(a.dataset.originalIndex) - Number(b.dataset.originalIndex);
        }}
        const aValue = a.cells[columnIndex].textContent.trim();
        const bValue = b.cells[columnIndex].textContent.trim();
        const aNumber = Number(aValue.replace(/[^0-9.-]/g, ''));
        const bNumber = Number(bValue.replace(/[^0-9.-]/g, ''));
        const bothNumeric = Number.isFinite(aNumber) && Number.isFinite(bNumber);
        const comparison = bothNumeric
          ? aNumber - bNumber
          : aValue.localeCompare(bValue, 'zh-CN');
        return nextState === 'asc' ? comparison : -comparison;
      }});
      rows.forEach((row) => tbody.appendChild(row));
    }}

    if (window.lucide) {{
      lucide.createIcons();
    }}
  </script>
</body>
</html>
"""


def _render_chart_panel(chart: ChartSpec, index: int) -> str:
    title = html.escape(str(chart.get("title")))
    meta_html = _render_panel_meta(chart.get("subtitle"), chart.get("source"))
    return (
        f"""
        <section class="panel chart-panel">
          <div class="panel-header">
            <div class="panel-title">
              <span class="title-indicator"></span>
              <div class="panel-title-stack">
                <h2>{title}</h2>
                {meta_html}
              </div>
            </div>
            <div class="chart-toolbar">
              <button
                type="button"
                class="icon-button chart-zoom-btn"
                data-chart-zoom
                data-chart-index="{index}"
                title="放大"
                aria-label="放大图表 {title}"
              >
                <i data-lucide="maximize-2"></i>
              </button>
            </div>
          </div>
          <div
            id="chart-{index}"
            class="chart"
            data-chart-title="{title}"
            style="height: {int(chart.get("height", 420))}px"
          ></div>
        </section>
        """
    )


def _render_chart_modal() -> str:
    return """
  <div id="chart-modal" class="modal-overlay" aria-hidden="true">
    <div class="modal-content" role="dialog" aria-modal="true">
      <div class="modal-header">
        <div class="modal-title">
          <span class="title-indicator"></span>
          <span class="modal-title-text">图表详情</span>
        </div>
        <button
          type="button"
          class="icon-button"
          data-modal-close
          title="关闭"
          aria-label="关闭"
        >
          <i data-lucide="x"></i>
        </button>
      </div>
      <div class="modal-body">
        <div id="modal-chart" class="modal-chart"></div>
      </div>
    </div>
  </div>
"""


def _render_card(card: CardSpec) -> str:
    value = _format_card_value(card["value"], card.get("format", "string"), card.get("decimals"))
    unit = card.get("unit")
    description = card.get("description")
    icon = str(card.get("icon") or "bar-chart-2")
    return f"""
      <article class="card">
        <div class="card-header">
          <span class="card-icon"><i data-lucide="{html.escape(icon)}"></i></span>
          <div class="card-label">{html.escape(str(card["label"]))}</div>
        </div>
        <div class="card-value">
          <span class="card-number">{html.escape(value)}</span>
          {f'<span class="card-unit">{html.escape(str(unit))}</span>' if unit else ''}
        </div>
        {_render_card_description(description)}
      </article>
    """


def _render_card_description(description: object) -> str:
    if not description:
        return ""
    return f'<div class="card-description">{html.escape(str(description))}</div>'


def _render_table(table: TableSpec, index: int) -> str:
    data = table["data"]
    columns = data["columns"]
    rows = data["rows"]
    table_id = f"table-{index}"
    title = html.escape(str(table["title"]))
    meta_html = _render_panel_meta(table.get("subtitle"), table.get("source"))
    head = "".join(
        f"""
              <th data-column-index="{column_index}">
                <button
                  type="button"
                  class="sort-button"
                  data-sort-button
                  data-table-id="{table_id}"
                  data-column-index="{column_index}"
                >
                  <span>{html.escape(str(column))}</span>
                  <span class="sort-arrows" aria-hidden="true">
                    <span class="sort-up">▲</span>
                    <span class="sort-down">▼</span>
                  </span>
                </button>
              </th>
        """
        for column_index, column in enumerate(columns)
    )
    body = "\n".join(
        f'<tr data-original-index="{row_index}">'
        + "".join(f"<td>{html.escape(_display_value(value))}</td>" for value in row)
        + "</tr>"
        for row_index, row in enumerate(rows)
    )
    return f"""
      <section class="panel">
        <div class="panel-header">
          <div class="panel-title">
            <span class="title-indicator"></span>
            <div class="panel-title-stack">
              <h2>{title}</h2>
              {meta_html}
            </div>
          </div>
        </div>
        <div class="table-wrap">
          <table id="{table_id}">
            <thead><tr>{head}</tr></thead>
            <tbody>{body}</tbody>
          </table>
        </div>
      </section>
    """


def _render_page_meta(subtitle: str | None, source: str | None) -> str:
    subtitle_html = (
        f'<p class="page-subtitle">{html.escape(subtitle)}</p>'
        if subtitle
        else ""
    )
    source_html = (
        f'<div class="page-meta"><span class="meta-pill">数据源：{html.escape(source)}</span></div>'
        if source
        else ""
    )
    return f"{subtitle_html}{source_html}"


def _render_panel_meta(subtitle: str | None, source: str | None) -> str:
    parts: list[str] = []
    if subtitle:
        parts.append(f'<div class="panel-subtitle">{html.escape(subtitle)}</div>')
    if source:
        parts.append(f'<div class="panel-source">数据源：{html.escape(source)}</div>')
    return "".join(parts)


def _build_echarts_option(chart: ChartSpec) -> JsonObject:
    chart_type = chart["type"]
    data = chart["data"]
    columns = data["columns"]
    rows = data["rows"]
    options = dict(chart.get("options") or {})
    option: JsonObject = {
        "tooltip": {"trigger": "axis" if chart_type != "pie" else "item"},
        "legend": {"type": "scroll"},
        **options,
    }
    if chart_type == "pie":
        series_options = []
        for item in chart["series"]:
            name_idx = columns.index(item["name_field"])
            value_idx = columns.index(item["value_field"])
            pie_data = [
                {"name": row[name_idx], "value": _number(row[value_idx])}
                for row in rows
            ]
            series_options.append(
                {
                    "name": item["name"],
                    "type": "pie",
                    "radius": "62%",
                    "data": pie_data,
                }
            )
        option["series"] = series_options
        return option

    if chart_type == "heatmap":
        item = chart["series"][0]
        fields = item["fields"]
        x_idx = columns.index(fields["x"])
        y_idx = columns.index(fields["y"])
        x_values = _ordered_unique(row[x_idx] for row in rows)
        y_values = _ordered_unique(row[y_idx] for row in rows)
        option.setdefault("grid", _default_grid())
        option["xAxis"] = {"type": "category", "data": x_values}
        option["yAxis"] = {"type": "category", "data": y_values}
        option["visualMap"] = option.get(
            "visualMap",
            {
                "min": 0,
                "max": max(_number(row[columns.index(fields["value"])]) for row in rows),
                "calculable": True,
                "orient": "horizontal",
                "left": "center",
                "bottom": 4,
            },
        )
        option["series"] = [_build_series(chart_type, item, columns, rows)]
        return option

    x_field = chart["x"]["field"]
    x_idx = columns.index(x_field)
    x_values = [row[x_idx] for row in rows]
    option.setdefault("grid", _default_grid())
    option["xAxis"] = {"type": "category", "data": x_values}
    option["yAxis"] = {"type": "value"}
    option.setdefault(
        "dataZoom",
        [
            {"type": "inside", "start": 0, "end": 100},
            {"type": "slider", "start": 0, "end": 100, "height": 18, "bottom": 8},
        ],
    )
    if chart_type == "candlestick":
        option["yAxis"]["scale"] = True
    option["series"] = [_build_series(chart_type, item, columns, rows) for item in chart["series"]]
    return option


def _default_grid() -> JsonObject:
    return {
        "left": "4%",
        "right": "4%",
        "top": 48,
        "bottom": 52,
        "containLabel": True,
    }


def _build_series(
    chart_type: str,
    series: SeriesSpec,
    columns: list[str],
    rows: list[TableRow],
) -> JsonObject:
    result: JsonObject = {"name": series["name"], "type": chart_type}
    if "item_style" in series:
        result["itemStyle"] = series["item_style"]
    if chart_type in {"line", "bar"}:
        idx = columns.index(series["field"])
        result["data"] = [_number(row[idx]) for row in rows]
        if series.get("stack"):
            result["stack"] = series["stack"]
        return result
    if chart_type == "candlestick":
        fields = series["fields"]
        indexes = [columns.index(fields[key]) for key in ("open", "close", "low", "high")]
        result["data"] = [[_number(row[index]) for index in indexes] for row in rows]
        return result
    if chart_type == "scatter":
        fields = series["fields"]
        x_idx = columns.index(fields["x"])
        y_idx = columns.index(fields["y"])
        result["data"] = [[_number(row[x_idx]), _number(row[y_idx])] for row in rows]
        return result
    if chart_type == "heatmap":
        fields = series["fields"]
        x_idx = columns.index(fields["x"])
        y_idx = columns.index(fields["y"])
        value_idx = columns.index(fields["value"])
        x_values = _ordered_unique(row[x_idx] for row in rows)
        y_values = _ordered_unique(row[y_idx] for row in rows)
        result["data"] = [
            [x_values.index(row[x_idx]), y_values.index(row[y_idx]), _number(row[value_idx])]
            for row in rows
        ]
        return result
    raise ToolExecutionError(
        "CHATQ_VISUALIZATION_CHART_TYPE_UNSUPPORTED",
        f"Unsupported chart type: {chart_type}",
    )


def _write_html_atomic(output_path: Path, html_text: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = output_path.with_name(f".{output_path.name}.tmp")
    tmp_path.write_text(html_text, encoding="utf-8")
    os.replace(tmp_path, output_path)


def _validation_error(
    loaded: LoadedSpec,
    issues: list[ValidationIssue],
    *,
    expected_kind: str | None,
) -> ToolExecutionError:
    return ToolExecutionError(
        "VISUALIZATION_VALIDATION_FAILED",
        "visualization validation failed",
        detail={
            "file": loaded.relative_path,
            "kind": loaded.data.get("kind"),
            "expected_kind": expected_kind,
            "errors": [issue.to_dict() for issue in issues],
        },
    )


def _check_unknown_keys(
    value: RawSpec,
    allowed: set[str],
    path: str,
    issues: list[ValidationIssue],
) -> None:
    for key in sorted(value):
        if key not in allowed:
            issues.append(
                ValidationIssue(
                    f"{path}.{key}",
                    "UNKNOWN_FIELD",
                    f'unknown field "{key}"',
                    hint=f"allowed fields: {sorted(allowed)}",
                )
            )


def _require_kind(
    spec: RawSpec,
    expected: str,
    path: str,
    issues: list[ValidationIssue],
) -> None:
    if spec.get("kind") != expected:
        issues.append(
            ValidationIssue(path, "KIND_MISMATCH", f'expected kind "{expected}"')
        )


def _require_text(
    value: RawSpec,
    key: str,
    path: str,
    issues: list[ValidationIssue],
) -> None:
    if key not in value:
        issues.append(ValidationIssue(path, "FIELD_REQUIRED", f"{key} is required"))
    elif not isinstance(value[key], str) or not value[key].strip():
        issues.append(ValidationIssue(path, "TYPE_INVALID", f"{key} must be a non-empty string"))


def _validate_optional_text(
    value: RawSpec,
    key: str,
    path: str,
    issues: list[ValidationIssue],
) -> None:
    if key in value and (not isinstance(value[key], str) or not value[key].strip()):
        issues.append(ValidationIssue(path, "TYPE_INVALID", f"{key} must be a non-empty string"))


def _is_number(value: object) -> bool:
    if isinstance(value, bool) or value is None or value == "":
        return False
    try:
        float(value)
    except (TypeError, ValueError):
        return False
    return True


def _number(value: object) -> float:
    if not _is_number(value):
        raise ToolExecutionError(
            "CHATQ_VISUALIZATION_NUMBER_INVALID",
            "Invalid numeric value reached renderer after validation",
            detail={"value": repr(value)},
        )
    return float(value)


def _format_card_value(value: object, fmt: object, decimals: object) -> str:
    if fmt == "string":
        return str(value)
    number = _number(value)
    precision = decimals if isinstance(decimals, int) else 2
    if fmt == "integer":
        return str(int(round(number)))
    return f"{number:.{precision}f}"


def _display_value(value: object) -> str:
    if value is None:
        return ""
    return str(value)


def _ordered_unique(values: Iterable[object]) -> list[object]:
    unique: list[object] = []
    for value in values:
        if value not in unique:
            unique.append(value)
    return unique


def _resolve_project_dir(project_dir: str) -> Path:
    try:
        return Path(project_dir).expanduser().resolve(strict=True)
    except FileNotFoundError as exc:
        raise ToolExecutionError(
            "CHATQ_VISUALIZATION_PROJECT_DIR_NOT_FOUND",
            "Current agent project directory was not found",
            detail={"project_dir": project_dir},
        ) from exc


def _resolve_input_file(project_dir: Path, file_path: str) -> Path:
    candidate = Path(file_path).expanduser()
    if not candidate.is_absolute():
        candidate = project_dir / candidate
    try:
        resolved = candidate.resolve(strict=True)
    except FileNotFoundError as exc:
        raise ToolExecutionError(
            "CHATQ_VISUALIZATION_FILE_NOT_FOUND",
            "Visualization spec file was not found",
            detail={"file": file_path},
        ) from exc
    if not resolved.is_file():
        raise ToolExecutionError(
            "CHATQ_VISUALIZATION_FILE_NOT_FOUND",
            "Visualization spec file is not a regular file",
            detail={"file": str(resolved)},
        )
    if not resolved.is_relative_to(project_dir):
        raise ToolExecutionError(
            "CHATQ_VISUALIZATION_FILE_OUTSIDE_PROJECT",
            "Visualization spec file must be under the current project directory",
            detail={"file": str(resolved), "project_dir": str(project_dir)},
        )
    return resolved


def _resolve_output_file(project_dir: Path, output_file: str) -> Path:
    candidate = Path(output_file).expanduser()
    if not candidate.is_absolute():
        candidate = project_dir / candidate
    resolved = candidate.resolve(strict=False)
    if not resolved.is_relative_to(project_dir):
        raise ToolExecutionError(
            "CHATQ_VISUALIZATION_OUTPUT_OUTSIDE_PROJECT",
            "Output HTML file must be under the current project directory",
            detail={"output_file": str(resolved), "project_dir": str(project_dir)},
        )
    if resolved.suffix.lower() != ".html":
        raise ToolExecutionError(
            "CHATQ_VISUALIZATION_OUTPUT_TYPE_INVALID",
            "Output file must use .html extension",
            detail={"output_file": _relative_to_project(project_dir, resolved)},
        )
    return resolved


def schema_for_kind(kind: str) -> VisualizationSpec:
    schemas: dict[str, VisualizationSpec] = {
        "chart": {
            "kind": "chart",
            "title": "股票K线",
            "subtitle": "近两个交易日示例",
            "source": "a_stock_daily_price / 前复权",
            "type": "candlestick",
            "data": {
                "columns": ["date", "open", "close", "low", "high"],
                "rows": [
                    ["2026-08-21", 101.2, 103.5, 100.8, 104.1],
                    ["2026-08-24", 103.7, 102.9, 101.6, 104.4],
                ],
            },
            "x": {"field": "date"},
            "series": [
                {
                    "name": "价格",
                    "fields": {
                        "open": "open",
                        "close": "close",
                        "low": "low",
                        "high": "high",
                    },
                }
            ],
        },
        "table": {
            "kind": "table",
            "title": "交易明细",
            "subtitle": "行情数据示例",
            "source": "a_stock_daily_price",
            "data": {
                "columns": ["date", "close", "volume"],
                "rows": [["2026-08-21", 103.5, 1203400]],
            },
        },
        "card": {
            "kind": "card",
            "title": "核心指标",
            "subtitle": "最近交易日摘要",
            "source": "a_stock_daily_price",
            "cards": [
                {
                    "label": "最新收盘价",
                    "value": 103.5,
                    "unit": "元",
                    "format": "number",
                    "decimals": 2,
                }
            ],
        },
        "report": {
            "kind": "report",
            "title": "市场分析报告",
            "subtitle": "近10个交易日走势与关键指标",
            "source": "a_stock_daily_price / 前复权",
            "layout": {"columns": 2},
            "cards": [{"label": "最新收盘价", "value": 103.5, "unit": "元"}],
            "charts": [
                {
                    "title": "收盘价趋势",
                    "type": "line",
                    "data": {
                        "columns": ["date", "close"],
                        "rows": [["2026-08-21", 103.5], ["2026-08-24", 102.9]],
                    },
                    "x": {"field": "date"},
                    "series": [{"name": "收盘价", "field": "close"}],
                }
            ],
            "tables": [],
        },
    }
    return schemas[kind]


def format_cli_payload(payload: ToolPayload, *, as_json: bool) -> str:
    if as_json:
        return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
    if not payload.get("ok"):
        message = str(payload.get("message") or "visualization command failed")
        return _format_cli_error(message, payload)
    summary = str(payload.get("summary") or "Visualization command completed.")
    data = payload.get("data")
    lines = [summary]
    if isinstance(data, dict):
        for key in ("file", "kind", "output_file", "iframe_url", "asset_base_url"):
            if key in data:
                lines.append(f"{key}: {data[key]}")
    else:
        lines.append(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))
    return "\n".join(lines)


def _format_cli_error(message: str, detail: object | None = None) -> str:
    lines = [f"Error: {message}"]
    if detail:
        lines.append(json.dumps(detail, ensure_ascii=False, indent=2, sort_keys=True))
    return "\n".join(lines)


def _success(
    operator: str,
    data: object,
    *,
    summary: str | None = None,
    artifacts: list[ToolArtifact] | None = None,
) -> ToolPayload:
    payload: ToolPayload = {"ok": True, "operator": operator, "data": data}
    if summary:
        payload["summary"] = summary
    if artifacts:
        payload["artifacts"] = artifacts
    return payload


def _error_payload(
    error_code: str,
    message: str,
    detail: JsonObject | None = None,
    *,
    operator: object = None,
) -> ToolPayload:
    payload: ToolPayload = {
        "ok": False,
        "operator": operator,
        "error_code": error_code,
        "message": message,
    }
    if detail:
        payload["detail"] = detail
    return payload


def _operator(args: argparse.Namespace) -> str:
    if getattr(args, "command", None):
        return f"{args.command_group} {args.command}"
    if getattr(args, "kind", None) and args.command_group == "schema":
        return f"schema {args.kind}"
    return str(args.command_group)


def _error_detail(exc: ToolExecutionError) -> JsonObject:
    return {"error_code": exc.error_code, **exc.detail}


def _relative_to_project(project_dir: Path, path: Path) -> str:
    return str(path.resolve(strict=False).relative_to(project_dir))


def _jsonable(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, tuple | list):
        return [_jsonable(item) for item in value]
    if value is None or isinstance(value, str | int | float | bool):
        return value
    return str(value)
