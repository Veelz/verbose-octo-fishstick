from typing import Union

from requests import Response

from api.api_base import ApiBase
from models.bear import Bear


class AlaskaBearsApi(ApiBase):
    BASE_URL = 'http://localhost:8091'
    BEAR_ENDPOINT_URL = '/bear'
    BEAR_ID_ENDPOINT_URL = '/bear/{id}'
    __FULL_BEAR_URL = BASE_URL + BEAR_ENDPOINT_URL
    __FULL_BEAR_ID_URL = BASE_URL + BEAR_ID_ENDPOINT_URL

    def __init__(self, base_url: str = None):
        if base_url is not None:
            self.BASE_URL = base_url
        super().__init__()

    def get_bear(self, bear_id: Union[int, str]) -> Response:
        return self._get(self.__FULL_BEAR_ID_URL.format(id=bear_id))

    def get_bears_list(self) -> Response:
        return self._get(self.__FULL_BEAR_URL)

    def create_bear(self, bear_model: Bear) -> Response:
        payload = bear_model.to_json()
        return self._post(self.__FULL_BEAR_URL, data=payload)

    def update_bear(self, bear_model: Bear) -> Response:
        payload = bear_model.to_json()
        return self._put(self.__FULL_BEAR_ID_URL.format(id=bear_model.bear_id), data=payload)

    def delete_all_bears(self) -> Response:
        return self._delete(self.__FULL_BEAR_URL)

    def delete_bear(self, bear_id: Union[int, str]) -> Response:
        return self._delete(self.__FULL_BEAR_ID_URL.format(id=bear_id))
