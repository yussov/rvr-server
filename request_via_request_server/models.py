from typing import Any, Dict, Optional

from pydantic import BaseModel


class Proxy(BaseModel):
    proxy_url: str
    port: int


class RequestGet(BaseModel):
    url: str
    answer_type: str
    proxy_server: Optional[Proxy] = None


class RequestPost(BaseModel):
    url: str
    answer_type: str
    data: Dict[str, Any]
    proxy_server: Optional[Proxy] = None


class Doh(BaseModel):
    domain: str
    doh_server: str
