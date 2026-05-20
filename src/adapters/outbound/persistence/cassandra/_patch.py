"""Monkey-patch cassandra-driver for Python 3.12+ (asyncore removed).

Replaces the module-level connection class detection to use AsyncioConnection
instead of relying on the removed asyncore module. This runs BEFORE any
import of cassandra.cluster.

Also overrides AsyncioConnection.initialize_reactor on Windows to use
SelectorEventLoop instead of the default ProactorEventLoop, because
ProactorEventLoop (IOCP) can hang with Docker Desktop port-forwarded sockets.
"""
import os
import sys
import types
from pathlib import Path

_PATCHED = False


def patch_cassandra_cluster():
    global _PATCHED
    if _PATCHED:
        return
    _PATCHED = True

    # If cluster is already loaded, skip
    if "cassandra.cluster" in sys.modules:
        return

    try:
        import cassandra
    except ImportError:
        return

    cluster_path = Path(cassandra.__path__[0]) / "cluster.py"
    if not cluster_path.exists():
        return

    source = cluster_path.read_text(encoding="utf-8")

    # Add the asyncio import function
    asyncio_fn = """
def _try_asyncio_import():
    try:
        from cassandra.io.asyncioreactor import AsyncioConnection
        return (AsyncioConnection, None)
    except Exception as e:
        return (None, e)
"""

    old_func = """def _try_asyncore_import():
    try:
        from cassandra.io.asyncorereactor import AsyncoreConnection
        return (AsyncoreConnection,None)
    except DependencyException as e:
        return (None, e)"""

    new_func = asyncio_fn + """def _try_asyncore_import():
    return _try_asyncio_import()"""

    if old_func not in source:
        return

    source = source.replace(old_func, new_func)

    code = compile(source, str(cluster_path), "exec")
    module = types.ModuleType("cassandra.cluster")
    module.__file__ = str(cluster_path)
    module.__package__ = "cassandra"
    module.__path__ = [str(cluster_path.parent)]
    sys.modules["cassandra.cluster"] = module
    exec(code, module.__dict__)


def patch_asyncio_reactor():
    """On Windows, use SelectorEventLoop instead of ProactorEventLoop
    to avoid IOCP hangs with Docker Desktop forwarded sockets."""
    if sys.platform != "win32":
        return
    try:
        import asyncio
        from cassandra.io.asyncioreactor import AsyncioConnection
        from threading import Thread

        @classmethod
        def _patched_initialize_reactor(cls):
            with cls._lock:
                if cls._pid != os.getpid():
                    cls._loop = None
                if cls._loop is None:
                    cls._loop = asyncio.SelectorEventLoop()
                    asyncio.set_event_loop(cls._loop)
                if not cls._loop_thread:
                    cls._loop_thread = Thread(
                        target=cls._loop.run_forever,
                        daemon=True,
                        name="asyncio_thread"
                    )
                    cls._loop_thread.start()

        AsyncioConnection.initialize_reactor = _patched_initialize_reactor
    except ImportError:
        pass


def patch_asyncio_push_msg():
    """Fix _push_msg broken syntax for Python 3.8+.

    cassandra-driver 3.29.1 uses 'with await self._write_queue_lock:'
    which was valid in Python <= 3.7 (asyncio.Lock had __await__).
    Python 3.8+ requires 'async with lock' or 'await lock.acquire()'.
    This silently breaks the handshake because the OPTIONS message
    never gets queued, causing OperationTimedOut.
    """
    try:
        from cassandra.io.asyncioreactor import AsyncioConnection

        _orig_push_msg = AsyncioConnection._push_msg

        async def _patched_push_msg(self, chunks):
            async with self._write_queue_lock:
                for chunk in chunks:
                    self._write_queue.put_nowait(chunk)

        AsyncioConnection._push_msg = _patched_push_msg
    except ImportError:
        pass


# Run patches at import time (before cassette.cluster is imported externally)
patch_cassandra_cluster()
patch_asyncio_reactor()
patch_asyncio_push_msg()
