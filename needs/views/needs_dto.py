from dataclasses import dataclass
import datetime


@dataclass(eq=True, frozen=True)
class NeedsEntity:
    nid: int
    sentence: str
    date: datetime.datetime
    label: int
