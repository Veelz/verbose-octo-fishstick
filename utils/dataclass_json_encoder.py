import json
from typing import Any


class DataclassJsonEncoder:
    @staticmethod
    def encode(obj: Any) -> str:
        to_encode = {key: value for key, value in obj.__dict__.items() if value is not None}
        return json.dumps(to_encode)
