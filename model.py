from dataclasses import dataclass,  field
from dataclasses_json import dataclass_json, config
from typing import TypeVar, Generic, Optional, List, Dict
from datetime import datetime

T = TypeVar('T')

def str_to_int(value: Optional[str]) -> Optional[int]:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except ValueError:
        return None

@dataclass_json
@dataclass
class MTeamResponse(Generic[T]):
    code: str
    data: Optional[T] = None
    message: Optional[str] = None

@dataclass_json
@dataclass
class DMMATag():
    count: Optional[str] = None
    id: Optional[str] = None
    keyword: Optional[str] = None
    lastModifiedDate: Optional[str] = None
    createdDate: Optional[str] = None

@dataclass_json
@dataclass
class DMMDetail():
    cntitle: Optional[str] = None
    collection: Optional[bool] = None
    count: Optional[int] = field(
        default=None,
        metadata=config(decoder=str_to_int)
    )
    lastModifiedDate: Optional[str] = None
    createdDate: Optional[str] = None
    entitle: Optional[str] = None
    id: Optional[int] = field(
        default=None,
        metadata=config(decoder=str_to_int)
    )

    note: Optional[str] = None
    notify: Optional[bool] = None
    pic: Optional[str] = None
    pic1: Optional[str] = None
    pic2: Optional[str] = None
    processed: Optional[bool] = None
    size: Optional[int] = field(
        default=None,
        metadata=config(decoder=str_to_int)
    )


@dataclass_json
@dataclass
class DMMListResponse(Generic[T]):
    aTags: List[DMMATag]
    detail: Optional[T] = None
    list: List[T] = None
    tTages: List[Dict]= None



