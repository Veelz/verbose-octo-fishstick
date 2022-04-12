import json

from hamcrest import assert_that, calling, is_not, raises, equal_to


def assert_response_is_in_json_format(response):
    assert_that(calling(response.json), is_not(raises(json.decoder.JSONDecodeError)),
                "Response returned non-json body")


def assert_status_code_is_equal(actual_status_code, expected_status_code):
    assert_that(actual_status_code, equal_to(expected_status_code), 'Status code is incorrect')


def assert_response_body_is_equal(actual_body, expected_body):
    assert_that(actual_body, equal_to(expected_body), 'Response body is incorrect')
