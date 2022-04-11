from typing import Union

import requests

from api.api_base import ApiBase
from models.bear import Bear
from utils.dataclass_json_encoder import DataclassJsonEncoder


class AlaskaBearsApi(ApiBase):
    BASE_URL = 'http://localhost:8091'
    BEAR_ENDPOINT_URL = BASE_URL + '/bear'
    BEAR_ID_ENDPOINT_URL = BASE_URL + '/bear/{id}'

    def __init__(self, base_url: str = None):
        if base_url is not None:
            self.BASE_URL = base_url
        super().__init__()

    def get_bear(self, bear_id: Union[int, str]):
        return self._get(self.BEAR_ID_ENDPOINT_URL.format(id=bear_id))

    def get_bears_list(self):
        return self._get(self.BEAR_ENDPOINT_URL)

    def create_bear(self, bear_model: Bear):
        payload = DataclassJsonEncoder.encode(bear_model)
        return self._post(self.BEAR_ENDPOINT_URL, data=payload)

    def update_bear(self, bear_model: Bear):
        payload = DataclassJsonEncoder.encode(bear_model)
        return requests.put(self.BEAR_ID_ENDPOINT_URL.format(id=bear_model.bear_id), data=payload)

    def delete_all_bears(self):
        return self._delete(self.BEAR_ENDPOINT_URL)

    def delete_bear(self, bear_id: Union[int, str]):
        return self._delete(self.BEAR_ID_ENDPOINT_URL.format(id=bear_id))
