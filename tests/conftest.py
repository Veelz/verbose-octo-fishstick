import random

import pytest

import config
from api.alaska_bears_api import AlaskaBearsApi
from models.bear import Bear
from support.constants import BEAR_AGE_MIN, BEAR_AGE_RANGE, BearType
from utils.datetime_utils import DatetimeUtils


def pytest_addoption(parser):
    parser.addoption("--hostname", action="store", default=config.BASE_URL)


@pytest.fixture(scope="class")
def api_object(request):
    hst = request.config.getoption("--hostname")
    yield AlaskaBearsApi(hst)


@pytest.fixture(scope="class", autouse=True)
def clear_all_data_before_test_run(api_object):
    _ = api_object.delete_all_bears()


@pytest.fixture(scope='function')
def create_bear_with_valid_data(api_object):
    name = f'test_name_{DatetimeUtils.timestamp()}'
    age = BEAR_AGE_MIN + BEAR_AGE_RANGE * random.random()
    bear_type = random.choice([getattr(BearType, attr) for attr in dir(BearType) if not attr.startswith('__')])
    bear_model = Bear(bear_type=bear_type, bear_name=name, bear_age=age, bear_id=None)
    response = api_object.create_bear(bear_model)
    if not response.text.isnumeric():
        raise ValueError('Bear was not created')
    bear_model.bear_id = int(response.text)
    yield bear_model


@pytest.fixture(scope='function')
def not_existing_bear_id(api_object):
    response = api_object.get_bears_list()
    existing_ids = [Bear(**entry).bear_id for entry in response.json()]
    yield 1 + max(existing_ids, default=1)
