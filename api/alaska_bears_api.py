import logging
import requests

from models.bear_model import BearModel
from utils.dataclass_json_encoder import DataclassJsonEncoder


class AlaskaBearsApi:
    BASE_URL = 'http://localhost:8091'
    BEAR_ENDPOINT_URL = BASE_URL + '/bear'
    BEAR_ID_ENDPOINT_URL = BASE_URL + '/bear/{id}'

    def __init__(self, base_url=None):
        if base_url is not None:
            self.BASE_URL = base_url

    def get_bear(self, bear_id):
        uri = self.BEAR_ID_ENDPOINT_URL.format(id=bear_id)
        logging.log(logging.INFO, f"Send GET-request: {uri}")
        return requests.get(uri)

    def get_bears_list(self):
        logging.log(logging.INFO, f"Send GET-request: {self.BEAR_ENDPOINT_URL}")
        return requests.get(self.BEAR_ENDPOINT_URL)

    def create_bear(self, bear_model: BearModel):
        payload = DataclassJsonEncoder.encode(bear_model)
        logging.log(logging.INFO, f"Send POST-request: {self.BEAR_ENDPOINT_URL}, data: {payload}")
        return requests.post(self.BEAR_ENDPOINT_URL, data=payload)

    def update_bear(self, bear_model: BearModel):
        uri = self.BEAR_ID_ENDPOINT_URL.format(id=bear_model.bear_id)
        payload = DataclassJsonEncoder.encode(bear_model)
        logging.log(logging.INFO, f"Send PUT-request: {uri}, data: {payload}")
        return requests.put(uri, data=payload)

    def delete_all_bears(self):
        logging.log(logging.INFO, f"Send DELETE-request: {self.BEAR_ENDPOINT_URL}")
        return requests.delete(self.BEAR_ENDPOINT_URL)

    def delete_bear(self, bear_id):
        uri = self.BEAR_ID_ENDPOINT_URL.format(id=bear_id)
        logging.log(logging.INFO, f"Send DELETE-request: {uri}")
        return requests.delete(self.BEAR_ID_ENDPOINT_URL.format(id=bear_id))
