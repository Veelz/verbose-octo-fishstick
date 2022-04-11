import json
import logging
from http import HTTPStatus

import pytest
from hamcrest import assert_that, equal_to, not_none, is_in, empty, calling, is_not, raises

from models.bear import Bear
from utils.custom_assertions import dataclass_equals
import support.constants as constants


class TestAlaskaBears:
    @pytest.mark.test_id(1)
    def test_create_bear(self, api_object):
        logging.log(logging.INFO, f'1. Отправить POST-запрос на эндпоинт {api_object.BEAR_ENDPOINT_URL}')
        bear_model = Bear(bear_type=constants.CreateValidBearData.BEAR_TYPE,
                          bear_name=constants.CreateValidBearData.BEAR_NAME,
                          bear_age=constants.CreateValidBearData.BEAR_AGE,
                          bear_id=None)
        response = api_object.create_bear(bear_model)
        bear_id = int(response.text) if response.text.isnumeric() else None
        assert_that(response.status_code, equal_to(HTTPStatus.OK), 'Status code is incorrect')
        assert_that(bear_id, not_none(), 'Response should contain bear_id')

        logging.log(logging.INFO, f'2. Отправить GET-запрос на эндпоинт {api_object.BEAR_ENDPOINT_URL}')
        bear_model.bear_id = bear_id
        response = api_object.get_bears_list()
        actual = [Bear(**entry) for entry in response.json()]
        assert_that(response.status_code, equal_to(HTTPStatus.OK), 'Status code is incorrect')
        assert_that(bear_model, is_in(actual), f'Response should contain the Bear but wasn\'t: {bear_model}')

    @pytest.mark.test_id(2)
    def test_get_bear_list(self, api_object):
        logging.log(logging.INFO, f'1. Отправить GET-запрос на эндпоинт {api_object.BEAR_ENDPOINT_URL}')
        response = api_object.get_bears_list()
        assert_that(response.status_code, equal_to(HTTPStatus.OK), 'Status code is incorrect')
        assert_that(calling(response.json), is_not(raises(json.decoder.JSONDecodeError)),
                    "Response returned non-json body")
        expected_content_ = response.text
        logging.log(logging.INFO, f'2. Отправить GET-запрос на эндпоинт {api_object.BEAR_ENDPOINT_URL}')
        response = api_object.get_bears_list()
        assert_that(response.status_code, equal_to(HTTPStatus.OK), 'Status code is incorrect')
        assert_that(calling(response.json), is_not(raises(json.decoder.JSONDecodeError)),
                    "Response returned non-json body")
        assert_that(response.text, equal_to(expected_content_), "Response returned incorrect body")

    @pytest.mark.test_id(3)
    def test_get_bear(self, api_object, create_bear_with_valid_data):
        bear_id = create_bear_with_valid_data.bear_id

        logging.log(logging.INFO, f'1. Отправить GET-запрос на эндпоинт {api_object.BEAR_ID_ENDPOINT_URL.format(id=bear_id)}')
        response = api_object.get_bear(bear_id)
        assert_that(response.status_code, equal_to(HTTPStatus.OK), 'Status code is incorrect')
        assert_that(calling(response.json), is_not(raises(json.decoder.JSONDecodeError)),
                    "Response returned non-json body")
        actual = Bear(**response.json())
        assert_that(actual.bear_id, equal_to(bear_id), 'Response returned bear with incorrect bear_id')
        expected_body = response.text

        logging.log(logging.INFO, f'2. Отправить GET-запрос на эндпоинт {api_object.BEAR_ID_ENDPOINT_URL.format(id=bear_id)}')
        response = api_object.get_bear(bear_id)
        assert_that(response.status_code, equal_to(HTTPStatus.OK), 'Status code is incorrect')
        assert_that(calling(response.json), is_not(raises(json.decoder.JSONDecodeError)),
                    "Response returned non-json body")
        assert_that(response.text, equal_to(expected_body), 'Response returned incorrect body')

    @pytest.mark.test_id(4)
    def test_update_bear(self, api_object, create_bear_with_valid_data):
        bear_id = create_bear_with_valid_data.bear_id

        logging.log(logging.INFO, f'1. Отправить PUT-запрос на эндпоинт {api_object.BEAR_ID_ENDPOINT_URL.format(id=bear_id)}')
        bear_model = Bear(bear_type=constants.UpdateBearData.BEAR_TYPE,
                          bear_name=constants.UpdateBearData.BEAR_NAME,
                          bear_age=constants.UpdateBearData.BEAR_AGE,
                          bear_id=bear_id)
        response = api_object.update_bear(bear_model)
        assert_that(response.status_code, equal_to(HTTPStatus.OK), 'Status code is incorrect')
        assert_that(response.text, equal_to(constants.ResponseMessages.SUCCESS), 'Response body is incorrect')

        logging.log(logging.INFO, f'2. Отправить GET-запрос на эндпоинт {api_object.BEAR_ID_ENDPOINT_URL.format(id=bear_id)}')
        response = api_object.get_bear(bear_model.bear_id)
        actual = Bear(**response.json())
        assert_that(response.status_code, equal_to(HTTPStatus.OK), 'Status code is incorrect')
        assert_that(actual, dataclass_equals(bear_model), f'Response should contain the Bear but wasn\'t: {bear_model}')

        logging.log(logging.INFO, f'3. Отправить PUT-запрос на эндпоинт {api_object.BEAR_ID_ENDPOINT_URL.format(id=bear_id)} с payload шага 1')
        response = api_object.update_bear(bear_model)
        assert_that(response.status_code, equal_to(HTTPStatus.CREATED), 'Status code is incorrect')
        assert_that(response.text, equal_to(constants.ResponseMessages.SUCCESS), 'Response body is incorrect')

        logging.log(logging.INFO, f'4. Отправить GET-запрос на эндпоинт {api_object.BEAR_ID_ENDPOINT_URL.format(id=bear_id)}')
        response = api_object.get_bear(bear_model.bear_id)
        actual = Bear(**response.json())
        assert_that(response.status_code, equal_to(HTTPStatus.OK), 'Status code is incorrect')
        assert_that(actual, dataclass_equals(bear_model), f'Response should contain the Bear but wasn\'t: {bear_model}')

    @pytest.mark.test_id(5)
    def test_delete_all_bears(self, api_object):
        logging.log(logging.INFO, f'1. Отправить DELETE-запрос на эндпоинт {api_object.BEAR_ENDPOINT_URL}')
        response = api_object.delete_all_bears()
        assert_that(response.status_code, equal_to(HTTPStatus.OK), 'Status code is incorrect')
        assert_that(response.text, equal_to(constants.ResponseMessages.SUCCESS), 'Response body is incorrect')

        logging.log(logging.INFO, f'2. Отправить GET-запрос на эндпоинт {api_object.BEAR_ENDPOINT_URL}')
        response = api_object.get_bears_list()
        assert_that(response.status_code, equal_to(HTTPStatus.OK), 'Status code is incorrect')
        assert_that(response.json(), empty(), 'Response body is incorrect')

        logging.log(logging.INFO, f'3. Отправить DELETE-запрос на эндпоинт {api_object.BEAR_ENDPOINT_URL}')
        response = api_object.delete_all_bears()
        assert_that(response.status_code, equal_to(HTTPStatus.OK), 'Status code is incorrect')
        assert_that(response.text, equal_to(constants.ResponseMessages.SUCCESS), 'Response body is incorrect')

        logging.log(logging.INFO, f'4. Отправить GET-запрос на эндпоинт {api_object.BEAR_ENDPOINT_URL}')
        response = api_object.get_bears_list()
        assert_that(response.status_code, equal_to(HTTPStatus.OK), 'Status code is incorrect')
        assert_that(response.json(), empty(), 'Response body is incorrect')

    @pytest.mark.test_id(6)
    def test_delete_bear(self, api_object, create_bear_with_valid_data):
        bear_id = create_bear_with_valid_data.bear_id

        logging.log(logging.INFO, f'1. Отправить DELETE-запрос на эндпоинт {api_object.BEAR_ID_ENDPOINT_URL.format(id=bear_id)}')
        response = api_object.delete_bear(bear_id)
        assert_that(response.status_code, equal_to(HTTPStatus.OK), 'Status code is incorrect')
        assert_that(response.text, equal_to(constants.ResponseMessages.SUCCESS), 'Response body is incorrect')

        logging.log(logging.INFO, f'2. Отправить GET-запрос на эндпоинт {api_object.BEAR_ENDPOINT_URL}')
        response = api_object.get_bears_list()
        actual = [Bear(**entry) for entry in response.json()]
        assert_that(response.status_code, equal_to(HTTPStatus.OK), 'Status code is incorrect')
        assert_that([bear for bear in actual if bear.bear_id == bear_id], empty(),
                    f'Response contains bear with id "{bear_id}" but should\'nt')
        saved_response_text = response.text

        logging.log(logging.INFO, f'3. Отправить DELETE-запрос на эндпоинт {api_object.BEAR_ID_ENDPOINT_URL.format(id=bear_id)}')
        response = api_object.delete_bear(bear_id)
        assert_that(response.status_code, equal_to(HTTPStatus.OK), 'Status code is incorrect')
        assert_that(response.text, equal_to(constants.ResponseMessages.SUCCESS), 'Response body is incorrect')

        logging.log(logging.INFO, f'4. Отправить GET-запрос на эндпоинт {api_object.BEAR_ENDPOINT_URL}')
        response = api_object.get_bears_list()
        assert_that(response.status_code, equal_to(HTTPStatus.OK), 'Status code is incorrect')
        assert_that(response.text, equal_to(saved_response_text), 'Response is incorrect')

    @pytest.mark.test_id(7)
    def test_get_not_existing_bear(self, api_object, not_existing_bear_id):
        logging.log(logging.INFO, f'1. Отправить GET-запрос на эндпоинт {api_object.BEAR_ID_ENDPOINT_URL.format(id=not_existing_bear_id)}')
        response = api_object.get_bear(not_existing_bear_id)
        assert_that(response.status_code, equal_to(HTTPStatus.OK), 'Status code is incorrect')
        assert_that(response.text, equal_to(constants.ResponseMessages.EMPTY), 'Response body is incorrect')

    @pytest.mark.test_id(9)
    def test_update_not_existing_bear(self, api_object, not_existing_bear_id):
        logging.log(logging.INFO, f'1. Отправить PUT-запрос на эндпоинт {api_object.BEAR_ID_ENDPOINT_URL.format(id=not_existing_bear_id)}')
        bear_model = Bear(bear_id=not_existing_bear_id,
                          bear_type=constants.UpdateBearData.BEAR_TYPE,
                          bear_name=constants.UpdateBearData.BEAR_NAME,
                          bear_age=constants.UpdateBearData.BEAR_AGE)
        response = api_object.update_bear(bear_model)
        assert_that(response.status_code, equal_to(HTTPStatus.NOT_FOUND), 'Status code is incorrect')

    @pytest.mark.test_id(10)
    def test_delete_not_existing_bear(self, api_object, not_existing_bear_id):
        logging.log(logging.INFO, f'1. Отправить DELETE-запрос на эндпоинт {api_object.BEAR_ID_ENDPOINT_URL.format(id=not_existing_bear_id)}')
        response = api_object.delete_bear(not_existing_bear_id)
        assert_that(response.status_code, equal_to(HTTPStatus.OK), 'Status code is incorrect')
        assert_that(response.text, equal_to(constants.ResponseMessages.SUCCESS), 'Response body is incorrect')
