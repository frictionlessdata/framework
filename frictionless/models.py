from typing import Any, Dict, Optional

from pydantic import BaseModel


class PublishResult(BaseModel):
    url: Optional[str]
    context: Dict[str, Any] = {}
