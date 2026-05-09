"""
pytest configuration for OMPA tests.

On Windows, SQLite holds an exclusive file lock until the connection is
explicitly closed. Ompa.close() / KnowledgeGraph.close() handle this, but
TemporaryDirectory cleanup can still race the garbage collector. Setting
ignore_cleanup_errors=True on TemporaryDirectory prevents spurious
PermissionError teardown failures on Windows without hiding real test failures.
"""

import sys
import tempfile

if sys.platform == "win32":
    _OriginalTemporaryDirectory = tempfile.TemporaryDirectory

    class _WindowsSafeTemporaryDirectory(_OriginalTemporaryDirectory):
        def __init__(self, *args, **kwargs):
            kwargs.setdefault("ignore_cleanup_errors", True)
            super().__init__(*args, **kwargs)

    tempfile.TemporaryDirectory = _WindowsSafeTemporaryDirectory
