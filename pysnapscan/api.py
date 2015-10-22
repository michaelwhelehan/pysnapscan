'''
Created on 22 Oct 2015

@author: michaelwhelehan
'''
import urllib
import json

import requests


class APIError(Exception):
    pass


class SnapScan(object):
    BASE_URL = 'https://pos.snapscan.io'
    BASE_API_URL = '%s/merchant/api/v1' % BASE_URL

    def __init__(self, snapcode=None, api_key=None):
        self.snapcode = snapcode
        self.api_key = api_key

    def set_snapcode(self, snapcode):
        self.snapcode = snapcode

    def set_api_key(self, api_key):
        self.api_key = api_key

    def _get(self, endpoint, page=None, per_page=None, offset=None):
        if self.api_key is None:
            raise APIError(
                "Please call 'set_api_key' first to use this method")
        url = '%s/%s' (self.BASE_API_URL, endpoint)
        pagination = {}
        if page is not None:
            pagination['page'] = page
        if per_page is not None:
            pagination['perPage'] = per_page
        if offset is not None:
            pagination['offset'] = offset
        response = requests.get(
            url, params=pagination, auth=(self.api_key, ''))
        if 200 <= response.status_code < 300:
            try:
                return response.json()
            except ValueError:
                raise APIError('There was an error decoding the response JSON')
        elif 400 <= response.status_code < 500:
            try:
                raise APIError(response.json()['message'])
            except (ValueError, KeyError):
                raise APIError('Error in data submitted')
        elif 500 <= response.status_code < 600:
            try:
                raise APIError(response.json()['message'])
            except (ValueError, KeyError):
                raise APIError('Server error')

    def _post(self, endpoint, data):
        if self.api_key is None:
            raise APIError(
                "Please call 'set_api_key' first to use this method")
        url = '%s/%s' (self.BASE_API_URL, endpoint)
        response = requests.post(
            url, data=json.dumps(data), auth=(self.api_key, ''))
        if 200 <= response.status_code < 300:
            try:
                return response.json()
            except ValueError:
                raise APIError('There was an error decoding the response JSON')
        elif 400 <= response.status_code < 500:
            try:
                raise APIError(response.json()['message'])
            except (ValueError, KeyError):
                raise APIError('Error in data submitted')
        elif 500 <= response.status_code < 600:
            try:
                raise APIError(response.json()['message'])
            except (ValueError, KeyError):
                raise APIError('Server error')

    def generate_qr_code_url(self, uid=None, amount=None, strict=False,
                             snap_code_size=125, img_type='.png'):
        if self.snapcode is None:
            raise APIError(
                "Please call 'set_snapcode' first to use this method")
        url = '%s/qr/%s%s' % (self.BASE_URL, self.snapcode, img_type)
        params = {
            'snap_code_size': snap_code_size,
        }
        if uid is not None:
            params['id'] = uid
        if amount is not None:
            params['amount'] = amount * 100
        if strict:
            params['strict'] = 'true'
        url += '?%s' % urllib.urlencode(params)
        return url

    def create_cash_up_period(self, timestamp, ref):
        data = {
            'date': timestamp.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'reference': ref
        }
        return self._post('cash_ups', data)

    def get_cash_ups(self, page=None, per_page=None, offset=None):
        return self._get('cash_ups', page, per_page, offset)

    def get_cash_up_payments(self, ref, page=None, per_page=None, offset=None):
        return self._get(
            'payments/cash_ups/%s' % ref,
            page,
            per_page,
            offset)

    def get_payments(self, page=None, per_page=None, offset=None):
        return self._get('payments', page, per_page, offset)

    def get_payment(self, payment_id):
        return self._get('payments/%i' % payment_id)
