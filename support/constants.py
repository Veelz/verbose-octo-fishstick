class ResponseMessages:
    SUCCESS = 'OK'
    EMPTY = 'EMPTY'


class BearType:
    POLAR = 'POLAR'
    BROWN = 'BROWN'
    BLACK = 'BLACK'
    GUMMY = 'GUMMY'


class CreateValidBearData:
    BEAR_TYPE = BearType.BLACK
    BEAR_NAME = 'mikhail'
    BEAR_AGE = 17.5


class UpdateBearData:
    BEAR_TYPE = BearType.BROWN
    BEAR_NAME = 'test_name'
    BEAR_AGE = 1.5
