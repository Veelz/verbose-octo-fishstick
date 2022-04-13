from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(init=True, eq=True)
class Bear:
    bear_id: int
    bear_type: str
    bear_name: str
    bear_age: float
