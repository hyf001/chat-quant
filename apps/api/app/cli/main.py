from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import NoReturn

from pydantic import ValidationError

from app.domain.strategies.models import StrategyCopyMode, StrategyPackage
from app.domain.strategies.service import StrategyError, strategy_service


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="chatq")
    subparsers = parser.add_subparsers(dest="resource", required=True)
    strategy_parser = subparsers.add_parser("strategy")
    strategy_subparsers = strategy_parser.add_subparsers(dest="action", required=True)

    create_parser = strategy_subparsers.add_parser("create")
    create_parser.add_argument("--conversation-id", required=True)
    create_parser.add_argument("--package-file", required=True)
    create_parser.add_argument("--user-id", default="demo-user")
    create_parser.add_argument("--project-id", default="default-project")
    create_parser.add_argument("--agent-run-id")
    create_parser.add_argument("--source-message-id")
    create_parser.add_argument("--source-tool-use-id")

    version_parser = strategy_subparsers.add_parser("version-create")
    version_parser.add_argument("--strategy-id", required=True)
    version_parser.add_argument("--parent-version-id")
    version_parser.add_argument("--package-file", required=True)
    version_parser.add_argument("--change-summary")
    version_parser.add_argument("--agent-run-id")
    version_parser.add_argument("--source-message-id")
    version_parser.add_argument("--source-tool-use-id")

    validate_parser = strategy_subparsers.add_parser("validate")
    validate_parser.add_argument("--strategy-version-id", required=True)

    get_parser = strategy_subparsers.add_parser("get")
    get_parser.add_argument("--strategy-version-id", required=True)

    copy_parser = strategy_subparsers.add_parser("copy")
    copy_parser.add_argument("--strategy-version-id", required=True)
    copy_parser.add_argument(
        "--mode",
        choices=[mode.value for mode in StrategyCopyMode],
        required=True,
    )
    copy_parser.add_argument("--conversation-id")
    copy_parser.add_argument("--user-id", default="demo-user")
    copy_parser.add_argument("--project-id", default="default-project")

    args = parser.parse_args(argv)

    try:
        result = _dispatch(args)
    except (StrategyError, ValidationError, ValueError) as error:
        return _fail(error)

    print(result.model_dump_json(indent=2))
    return 0


def _dispatch(args: argparse.Namespace):
    if args.resource != "strategy":
        raise ValueError("unsupported resource")

    if args.action == "create":
        package = _read_package(args.package_file)
        return strategy_service.create_strategy(
            user_id=args.user_id,
            project_id=args.project_id,
            chat_session_id=args.conversation_id,
            package=package,
            source_sdk_session_id=args.agent_run_id,
            source_sdk_message_uuid=args.source_message_id,
            source_sdk_tool_use_id=args.source_tool_use_id,
        )

    if args.action == "version-create":
        package = _read_package(args.package_file)
        return strategy_service.create_strategy_version(
            args.strategy_id,
            package=package,
            parent_version_id=args.parent_version_id,
            change_summary=args.change_summary,
            source_sdk_session_id=args.agent_run_id,
            source_sdk_message_uuid=args.source_message_id,
            source_sdk_tool_use_id=args.source_tool_use_id,
        )

    if args.action == "validate":
        return strategy_service.validate_version(args.strategy_version_id)

    if args.action == "get":
        return strategy_service.get_version(args.strategy_version_id)

    if args.action == "copy":
        return strategy_service.copy_strategy_version(
            args.strategy_version_id,
            mode=StrategyCopyMode(args.mode),
            user_id=args.user_id,
            project_id=args.project_id,
            target_chat_session_id=args.conversation_id,
        )

    raise ValueError("unsupported strategy action")


def _read_package(package_file: str) -> StrategyPackage:
    payload = json.loads(Path(package_file).read_text(encoding="utf-8"))
    return StrategyPackage.model_validate(payload)


def _fail(error: Exception) -> int:
    if isinstance(error, StrategyError):
        payload = {"error_code": error.error_code, "message": error.message}
    elif isinstance(error, ValidationError):
        payload = {"error_code": "STRATEGY_PACKAGE_INVALID", "message": str(error)}
    else:
        payload = {"error_code": "STRATEGY_CLI_ERROR", "message": str(error)}
    print(json.dumps(payload, ensure_ascii=False), flush=True)
    return 1


def run() -> NoReturn:
    raise SystemExit(main())


if __name__ == "__main__":
    run()
