from dataclasses import dataclass
import datetime


@dataclass(eq=True, frozen=True)
class TweetsDto:
    """
    parameters
        text: str 
        datetime: 
    exaple
        text: "ニーズを内包するテキストデータだよ"
        datetime: "2020/11/18 00:00:00" 
    """

    text: str
    datetime_jst: datetime.datetime
    label: int
    negative: float
    positive: float
