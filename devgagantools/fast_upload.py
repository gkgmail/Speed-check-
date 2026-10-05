import os
from pathlib import Path


async def fast_upload(client, file_path, reply=None, name=None, progress_bar_function=None, user_id=None, **kwargs):
    """
    Minimal compatibility implementation for projects that import
    `from devgagantools import fast_upload`

    This function uploads a local file using the active Telegram client.
    It is intentionally simple and safe for compatibility.
    """
    if not file_path or not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    filename = name or Path(file_path).name

    # Prefer Telethon-style client methods if available
    if hasattr(client, "send_file"):
        target = user_id if user_id is not None else (reply.chat_id if reply is not None else None)
        if target is None:
            raise ValueError("No valid target chat/user id provided for fast_upload()")

        result = await client.send_file(
            target,
            file=file_path,
            force_document=True,
            file_name=filename,
        )
        return result

    # Fallback for Pyrogram-like clients
    if hasattr(client, "send_document"):
        target = user_id if user_id is not None else (reply.chat_id if reply is not None else None)
        if target is None:
            raise ValueError("No valid target chat/user id provided for fast_upload()")

        result = await client.send_document(
            chat_id=target,
            document=file_path,
            file_name=filename,
        )
        return result

    raise RuntimeError("Unsupported client object for fast_upload().")
