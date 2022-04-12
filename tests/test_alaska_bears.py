from http import HTTPStatus

import allure
import pytest
from hamcrest import assert_that, equal_to, not_none, is_in, empty

from models.bear import Bear
from tests.assertion_steps import assert_status_code_is_equal, assert_response_is_in_json_format, \
    assert_response_body_is_equal
from utils.custom_assertions import dataclass_equals
import support.constants as constants
import support.test_data as test_data


class TestAlaskaBears:
    @allure.title("1. Создать запись о медведе")
    @pytest.mark.test_id(1)
    @pytest.mark.parametrize('bear_type', (constants.BearType.BLACK, constants.BearType.BROWN,
                                           constants.BearType.GUMMY, constants.BearType.POLAR))
    def test_create_bear(self, api_object, bear_type):
        with allure.step(f'1. Отправить POST-запрос на эндпоинт {api_object.BEAR_ENDPOINT_URL}'):
            bear_model = Bear(bear_type=bear_type,
                              bear_name=test_data.ValidBearData.BEAR_NAME,
                              bear_age=test_data.ValidBearData.BEAR_AGE,
                              bear_id=None)
            response = api_object.create_bear(bear_model)
            bear_id = int(response.text) if response.text.isnumeric() else None
            assert_status_code_is_equal(response.status_code, HTTPStatus.OK)
            assert_that(bear_id, not_none(), 'Response should contain bear_id')

        with allure.step(f'2. Отправить GET-запрос на эндпоинт {api_object.BEAR_ENDPOINT_URL}'):
            bear_model.bear_id = bear_id
            response = api_object.get_bears_list()
            actual = [Bear(**entry) for entry in response.json()]
            assert_status_code_is_equal(response.status_code, HTTPStatus.OK)
            assert_that(bear_model, is_in(actual), f'Response should contain the Bear but wasn\'t: {bear_model}')

    @allure.title("2. Получить запись о медведе")
    @pytest.mark.test_id(2)
    def test_get_bear(self, api_object, create_bear_with_valid_data):
        bear_id = create_bear_with_valid_data.bear_id
        with allure.step(f'1. Отправить GET-запрос на эндпоинт {api_object.BEAR_ID_ENDPOINT_URL.format(id=bear_id)}'):
            response = api_object.get_bear(bear_id)
            assert_status_code_is_equal(response.status_code, HTTPStatus.OK)
            assert_response_is_in_json_format(response)
            actual = Bear(**response.json())
            assert_that(actual.bear_id, equal_to(bear_id), 'Response returned bear with incorrect bear_id')

    @allure.title("3. Обновить запись о медведе")
    @pytest.mark.test_id(3)
    @pytest.mark.parametrize('bear_type', (constants.BearType.BLACK, constants.BearType.BROWN,
                                           constants.BearType.GUMMY, constants.BearType.POLAR))
    def test_update_bear(self, api_object, create_bear_with_valid_data, bear_type):
        bear_id = create_bear_with_valid_data.bear_id
        with allure.step(f'1. Отправить PUT-запрос на эндпоинт {api_object.BEAR_ID_ENDPOINT_URL.format(id=bear_id)}'):
            bear_model = Bear(bear_type=bear_type,
                              bear_name=test_data.ValidBearData.BEAR_NAME,
                              bear_age=test_data.ValidBearData.BEAR_AGE,
                              bear_id=bear_id)
            response = api_object.update_bear(bear_model)
            assert_status_code_is_equal(response.status_code, HTTPStatus.OK)
            assert_response_body_is_equal(response.text, constants.ResponseMessages.SUCCESS)

        with allure.step(f'2. Отправить GET-запрос на эндпоинт {api_object.BEAR_ID_ENDPOINT_URL.format(id=bear_id)}'):
            response = api_object.get_bear(bear_model.bear_id)
            actual = Bear(**response.json())
            assert_status_code_is_equal(response.status_code, HTTPStatus.OK)
            assert_that(actual, dataclass_equals(bear_model), f'Response should contain the Bear but wasn\'t: {bear_model}')

    @allure.title("4. Удалить записи о всех медведях")
    @pytest.mark.test_id(4)
    def test_delete_all_bears(self, api_object):
        with allure.step(f'1. Отправить DELETE-запрос на эндпоинт {api_object.BEAR_ENDPOINT_URL}'):
            response = api_object.delete_all_bears()
            assert_status_code_is_equal(response.status_code, HTTPStatus.OK)
            assert_response_body_is_equal(response.text, constants.ResponseMessages.SUCCESS)

        with allure.step(f'2. Отправить GET-запрос на эндпоинт {api_object.BEAR_ENDPOINT_URL}'):
            response = api_object.get_bears_list()
            assert_status_code_is_equal(response.status_code, HTTPStatus.OK)
            assert_that(response.json(), empty(), 'Response body is incorrect')

    @allure.title("5. Удалить запись о медведе")
    @pytest.mark.test_id(5)
    def test_delete_bear(self, api_object, create_bear_with_valid_data):
        bear_id = create_bear_with_valid_data.bear_id
        with allure.step(f'1. Отправить DELETE-запрос на эндпоинт {api_object.BEAR_ID_ENDPOINT_URL.format(id=bear_id)}'):
            response = api_object.delete_bear(bear_id)
            assert_status_code_is_equal(response.status_code, HTTPStatus.OK)
            assert_response_body_is_equal(response.text, constants.ResponseMessages.SUCCESS)

        with allure.step(f'2. Отправить GET-запрос на эндпоинт {api_object.BEAR_ENDPOINT_URL}'):
            response = api_object.get_bears_list()
            actual = [Bear(**entry) for entry in response.json()]
            assert_status_code_is_equal(response.status_code, HTTPStatus.OK)
            assert_that([bear for bear in actual if bear.bear_id == bear_id], empty(),
                        f'Response contains bear with id "{bear_id}" but should\'nt')

    @allure.title("6. Получить несуществующую запись о медведе")
    @pytest.mark.test_id(6)
    def test_get_not_existing_bear(self, api_object, not_existing_bear_id):
        with allure.step(f'1. Отправить GET-запрос на эндпоинт {api_object.BEAR_ID_ENDPOINT_URL.format(id=not_existing_bear_id)}'):
            response = api_object.get_bear(not_existing_bear_id)
            assert_status_code_is_equal(response.status_code, HTTPStatus.OK)
            assert_response_body_is_equal(response.text, constants.ResponseMessages.EMPTY)

    @allure.title("8. Обновить запись несуществующего медведя")
    @pytest.mark.test_id(8)
    def test_update_not_existing_bear(self, api_object, not_existing_bear_id):
        with allure.step(f'1. Отправить PUT-запрос на эндпоинт {api_object.BEAR_ID_ENDPOINT_URL.format(id=not_existing_bear_id)}'):
            bear_model = Bear(bear_id=not_existing_bear_id,
                              bear_type=test_data.ValidBearData.BEAR_TYPE,
                              bear_name=test_data.ValidBearData.BEAR_NAME,
                              bear_age=test_data.ValidBearData.BEAR_AGE)
            response = api_object.update_bear(bear_model)
            assert_status_code_is_equal(response.status_code, HTTPStatus.NOT_FOUND)

    @allure.title("9. Удалить запись несуществующего медведя")
    @pytest.mark.test_id(9)
    def test_delete_not_existing_bear(self, api_object, not_existing_bear_id):
        with allure.step(f'1. Отправить DELETE-запрос на эндпоинт {api_object.BEAR_ID_ENDPOINT_URL.format(id=not_existing_bear_id)}'):
            response = api_object.delete_bear(not_existing_bear_id)
            assert_status_code_is_equal(response.status_code, HTTPStatus.OK)
            assert_response_body_is_equal(response.text, constants.ResponseMessages.SUCCESS)
