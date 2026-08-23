from __future__ import annotations

import base64
from pathlib import Path

from supermind_mcp.config import JupyterConfig
from supermind_mcp.jupyter_ws import (
    _handle_message,
    _is_for_parent,
    build_kernel_ws_url,
)
from supermind_mcp.models import ExecutionResult


def test_build_kernel_ws_url_preserves_user_base_path() -> None:
    config = JupyterConfig(
        url="https://supermind.example/notebook/user/123",
        token="secret",
    )

    url = build_kernel_ws_url(config, "kernel-1")

    assert url == (
        "wss://supermind.example/notebook/user/123"
        "/api/kernels/kernel-1/channels?token=secret"
    )


def test_is_for_parent_filters_messages() -> None:
    assert _is_for_parent({"parent_header": {"msg_id": "abc"}}, "abc")
    assert not _is_for_parent({"parent_header": {"msg_id": "other"}}, "abc")


def test_handle_messages_collects_stream_result_error_and_image(tmp_path: Path) -> None:
    result = ExecutionResult()
    parent_header = {"msg_id": "abc"}
    png = base64.b64encode(b"png-bytes").decode("ascii")

    _handle_message(
        {
            "header": {"msg_type": "stream"},
            "parent_header": parent_header,
            "content": {"name": "stdout", "text": "hello\n"},
        },
        result,
    )
    _handle_message(
        {
            "header": {"msg_type": "execute_result"},
            "parent_header": parent_header,
            "content": {"data": {"text/plain": "42", "image/png": png}},
        },
        result,
        image_dir=tmp_path,
    )
    done = _handle_message(
        {
            "header": {"msg_type": "execute_reply"},
            "parent_header": parent_header,
            "content": {"status": "ok"},
        },
        result,
    )
    idle = _handle_message(
        {
            "header": {"msg_type": "status"},
            "parent_header": parent_header,
            "content": {"execution_state": "idle"},
        },
        result,
    )

    assert not done
    assert idle
    assert result.stdout == ["hello\n"]
    assert result.result == "42"
    assert len(result.images) == 1
    assert Path(result.images[0].path).read_bytes() == b"png-bytes"


def test_handle_messages_waits_for_idle_after_execute_reply() -> None:
    result = ExecutionResult()
    parent_header = {"msg_id": "abc"}

    done = _handle_message(
        {
            "header": {"msg_type": "execute_reply"},
            "parent_header": parent_header,
            "content": {"status": "ok"},
        },
        result,
    )
    _handle_message(
        {
            "header": {"msg_type": "stream"},
            "parent_header": parent_header,
            "content": {"name": "stdout", "text": "late stdout\n"},
        },
        result,
    )
    idle = _handle_message(
        {
            "header": {"msg_type": "status"},
            "parent_header": parent_header,
            "content": {"execution_state": "idle"},
        },
        result,
    )

    assert not done
    assert idle
    assert result.stdout == ["late stdout\n"]
