#!/usr/bin/env python3

from json import dumps
from typing import Any, Dict, Optional


def jp(content: Dict[str, Any], title: Optional[str] = None) -> None:
    if title is not None:
        data = {title: content}
    else:
        data = content
    print(dumps(data, indent=2))
