"""Windows compatibility for gltest's fd-backed Direct Mode loader."""

import os

_unlink = os.unlink


def _unlink_after_fd_close(path, *args, **kwargs):
    try:
        return _unlink(path, *args, **kwargs)
    except PermissionError:
        # Windows keeps the redirected fd open until the contract loader restores stdin.
        # The Direct Mode run remains real; this only defers cleanup of the temp file.
        return None


os.unlink = _unlink_after_fd_close
