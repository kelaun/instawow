from __future__ import annotations

import importlib.util
from typing import TYPE_CHECKING
import sys

if TYPE_CHECKING:
    import types


def __getattr__(name: str) -> types.ModuleType:
    """Defer importing own modules until attempting to access an attribute.

    Importing this in ``__init__`` will overwrite relative imports.
    """
    fullname = __package__ + '.' + name
    try:
        return sys.modules[fullname]
    except KeyError:
        spec = importlib.util.find_spec(fullname)
        sys.modules[fullname] = module = importlib.util.module_from_spec(spec)
        lazy_loader = importlib.util.LazyLoader(spec.loader)
        lazy_loader.exec_module(module)
        return module