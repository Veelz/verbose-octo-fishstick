from datetime import datetime


class DatetimeUtils:
    @staticmethod
    def timestamp() -> str:
        return str(int(datetime.utcnow().timestamp()))
