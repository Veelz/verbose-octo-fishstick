from dataclasses import dataclass


@dataclass(init=True, eq=True)
class BearModel:
    bear_id: int
    bear_type: str
    bear_name: str
    bear_age: float
