import base64
import hashlib
import hmac
import json
import requests
import time

from requests.auth import AuthBase
from config import *


class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key: str = API_KEY, secret_key: str = SECRET_KEY, passphrase: str = PASSPHRASE):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or '')
        sign = hmac.new(key=base64.b64decode(self.secret_key), msg=message.encode('utf-8'), digestmod=hashlib.sha256)
        signature_b64 = base64.b64encode(sign.digest())

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request

    def get_accounts(self):
        return requests.get(API_URL + f'accounts/{BTC_ID}', auth=self)

    def get_history(self):
        return requests.get(API_URL + f'accounts/{BTC_ID}/ledger', auth=self)

    def get_coinbase_accounts(self):
        return requests.get(API_URL + f'coinbase-accounts', auth=self)

    def get_margin_profile(self, product_id: str = 'BTC-EUR'):
        return requests.get(API_URL + f'margin/profile_information?&product_id={product_id}', auth=self)

    def get_products(self):
        return requests.get(API_URL + f'products', auth=self)

    def get_market_data_by_product_id(self, product_id: str = 'BTC-EUR', granularity: int = 3600):
        return requests.get(API_URL + f'products/{product_id}/candles?&granularity={granularity}', auth=self)


if __name__ == '__main__':
    auth = CoinbaseExchangeAuth()
    print(json.dumps(auth.get_market_data_by_product_id().json(), indent=2, sort_keys=True))
