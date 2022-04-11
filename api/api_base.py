import logging
from abc import ABC
from typing import Any, Union

import requests
from requests import Response


class ApiBase(ABC):

    def _get(self, uri: Union[str, bytes]) -> Response:
        logging.log(logging.INFO, f"Send GET-request: {uri}")
        return requests.get(uri)

    def _post(self, uri: Union[str, bytes], data: Any) -> Response:
        logging.log(logging.INFO, f"Send POST-request: {uri}, data: {data}")
        return requests.post(uri, data=data)

    def _put(self, uri: Union[str, bytes], data: Any) -> Response:
        logging.log(logging.INFO, f"Send PUT-request: {uri}, data: {data}")
        return requests.put(uri, data=data)

    def _delete(self, uri: Union[str, bytes]) -> Response:
        logging.log(logging.INFO, f"Send DELETE-request: {uri}")
        return requests.delete(uri)
