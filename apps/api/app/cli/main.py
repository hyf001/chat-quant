from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(prog="chatq")
    subcommands = parser.add_subparsers(dest="module", required=True)
    artifact_parser = subcommands.add_parser("artifact")
    artifact_subcommands = artifact_parser.add_subparsers(dest="command", required=True)

    save_code = artifact_subcommands.add_parser("save-code")
    save_code.add_argument("--conversation-id", required=True)
    save_code.add_argument("--type", required=True)
    save_code.add_argument("--entrypoint", required=True)
    save_code.add_argument("--title", default="Agent 生成代码")
    save_code.add_argument("--user-id", default="u_dev")
    save_code.add_argument("--project-id", default="default")
    save_code.add_argument("--agent-run-id")
    save_code.add_argument("--source-message-id")
    save_code.add_argument("--tool-use-id")
    save_code.add_argument("--metadata-json", default="{}")
    save_code.add_argument("--file", action="append", required=True)

    save_files = artifact_subcommands.add_parser("save-files")
    save_files.add_argument("--conversation-id", required=True)
    save_files.add_argument("--source-base-dir")
    save_files.add_argument("--parent-artifact-id")
    save_files.add_argument("--user-id", default="u_dev")
    save_files.add_argument("--project-id", default="default")
    save_files.add_argument("--agent-run-id")
    save_files.add_argument("--source-message-id")
    save_files.add_argument("--tool-use-id")
    save_files.add_argument("--metadata-json", default="{}")
    save_files.add_argument("--file-role", required=True)
    save_files.add_argument("--file", action="append", required=True)

    get_artifact = artifact_subcommands.add_parser("get")
    get_artifact.add_argument("--artifact-id", required=True)

    args = parser.parse_args()
    api_base_url = os.environ.get("CHATQ_API_BASE_URL", "http://localhost:8000")

    if args.module == "artifact" and args.command == "save-code":
        payload = _save_code_payload(args)
        data = _post_json(f"{api_base_url}/api/artifacts/code", payload)
        print(
            json.dumps(
                {
                    "code_artifact_id": data["artifact_id"],
                    "entrypoint": data["entrypoint"],
                    "version": data["version"],
                    "checksum": data["checksum"],
                },
                ensure_ascii=False,
            )
        )
        return 0

    if args.module == "artifact" and args.command == "save-files":
        payload = _save_files_payload(args)
        print(
            json.dumps(
                _post_json(f"{api_base_url}/api/artifacts/files", payload),
                ensure_ascii=False,
            )
        )
        return 0

    if args.module == "artifact" and args.command == "get":
        print(
            json.dumps(
                _get_json(f"{api_base_url}/api/artifacts/{args.artifact_id}"),
                ensure_ascii=False,
            )
        )
        return 0

    parser.error("unsupported command")
    return 2


def _save_code_payload(args: argparse.Namespace) -> dict[str, object]:
    return {
        "chat_session_id": args.conversation_id,
        "user_id": args.user_id,
        "project_id": args.project_id,
        "source_sdk_session_id": args.agent_run_id,
        "source_sdk_message_uuid": args.source_message_id,
        "source_sdk_tool_use_id": args.tool_use_id,
        "artifact_type": args.type,
        "title": args.title,
        "entrypoint": args.entrypoint,
        "metadata": _json_object(args.metadata_json),
        "files": [
            {
                "relative_path": relative_path,
                "content": source.read_text(encoding="utf-8"),
                "file_role": args.type,
            }
            for relative_path, source in (_parse_file_arg(item) for item in args.file)
        ],
    }


def _save_files_payload(args: argparse.Namespace) -> dict[str, object]:
    parsed_files = [_parse_file_arg(item) for item in args.file]
    source_base_dir = args.source_base_dir
    if source_base_dir is None:
        source_base_dir = os.path.commonpath(
            [str(source.parent.resolve()) for _, source in parsed_files]
        )
    return {
        "chat_session_id": args.conversation_id,
        "user_id": args.user_id,
        "project_id": args.project_id,
        "source_sdk_session_id": args.agent_run_id,
        "source_sdk_message_uuid": args.source_message_id,
        "source_sdk_tool_use_id": args.tool_use_id,
        "parent_artifact_id": args.parent_artifact_id,
        "source_base_dir": source_base_dir,
        "metadata": _json_object(args.metadata_json),
        "files": [
            {
                "source_path": str(source.resolve().relative_to(Path(source_base_dir).resolve())),
                "file_role": args.file_role,
            }
            for _, source in parsed_files
        ],
    }


def _parse_file_arg(raw_value: str) -> tuple[str, Path]:
    relative_path, separator, source = raw_value.partition("=@")
    if separator == "":
        raise SystemExit("--file must use relative/path=@/absolute/source format")
    return relative_path, Path(source)


def _json_object(raw_value: str) -> dict[str, object]:
    value = json.loads(raw_value)
    if not isinstance(value, dict):
        raise SystemExit("--metadata-json must be a JSON object")
    return value


def _post_json(url: str, payload: dict[str, object]) -> object:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    return _request_json(request)


def _get_json(url: str) -> object:
    return _request_json(urllib.request.Request(url, method="GET"))


def _request_json(request: urllib.request.Request) -> object:
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        message = exc.read().decode("utf-8")
        raise SystemExit(f"chatq request failed: {exc.code} {message}") from exc


if __name__ == "__main__":
    sys.exit(main())
