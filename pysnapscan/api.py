'''
Created on 22 Oct 2015

@author: michaelwhelehan
'''
import urllib
import json
import time

import requests


class APIError(Exception):
    """
    General API errors raised from the API.
    """


class APIError400(APIError):
    """
    Error raised when an HTTP 400 is returned from the API.
    """


class APIError500(APIError):
    """
    Error raised when an HTTP 500 is returned from the API.
    """


class SnapScan(object):
    """
    This class encapsulates all the functionality of the SnapScan REST API.

    Public methods:
        set_snapcode(snapcode<str>)

        set_api_key(api_key<str>)

        generate_qr_code_url([, uid<str>, amount<int,float>, strict<bool>,
                              snap_code_size<int>, img_type<str>])

        create_cash_up_period(timestamp<datetime>, ref<str>)

        get_cash_ups([, page<int>, per_page<int>, offset<int>])

        get_cash_up_payments(ref<str>[, page<int>, per_page<int>, offset<int>])

        get_payments([, page<int>, per_page<int>, offset<int>])

        get_payment(id<int>)


    Private methods:
        _get(endpoint<str>[, page<int>, per_page<int>, offset<int>])

        _post(endpoint<str>, data<dict>)
    """
    BASE_URL = 'https://pos.snapscan.io'
    BASE_API_URL = '%s/merchant/api/v1' % BASE_URL

    def __init__(self, snapcode=None, api_key=None):
        """
        Initialise the SnapScan object.

        Args:
            snapcode (str): SnapScan Merchant's SnapCode reference.
            api_key (str): SnapScan Merchant's API Key for GET and POST calls.
        """
        self.snapcode = snapcode
        self.api_key = api_key

    def set_snapcode(self, snapcode):
        """
        Setup the snapcode if not initiated.

        Args:
            snapcode (str): SnapScan Merchant's SnapCode reference.
        """
        self.snapcode = snapcode

    def set_api_key(self, api_key):
        """
        Setup the api_key if not initiated.

        Args:
            api_key (str): SnapScan Merchant's API Key for GET and POST calls.
        """
        self.api_key = api_key

    def _get(self, endpoint, page=None, per_page=None, offset=None):
        """
        Returns the JSON response from the REST API based on response code.

        Args:
            endpoint (str): The endpoint to make the GET request to.

        Kwargs:
            page (int): The page number for pagination.
            per_page (int): The amount of results to show per page.
            offset (int): The offset to start from.

        Returns:
            JSON response or raises APIError with a message.

            HTTP Status codes:

            2XX = Success
            4XX = Error in submitted data
            5XX = Server error
        """
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
                raise APIError400(response.json()['message'])
            except (ValueError, KeyError):
                raise APIError400('Error in data submitted')
        elif 500 <= response.status_code < 600:
            try:
                raise APIError500(response.json()['message'])
            except (ValueError, KeyError):
                raise APIError500('Server error')

    def _post(self, endpoint, data):
        """
        Creates a new record and returns the JSON response from the REST API
        based on response code.

        Args:
            endpoint (str): The endpoint to make the POST request to.
            data (dict): The data dictionary to submit.

        Returns:
            JSON response or raises APIError with a message.

            HTTP Status codes:

            2XX = Success
            4XX = Error in submitted data
            5XX = Server error
        """
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
                raise APIError400(response.json()['message'])
            except (ValueError, KeyError):
                raise APIError400('Error in data submitted')
        elif 500 <= response.status_code < 600:
            try:
                raise APIError500(response.json()['message'])
            except (ValueError, KeyError):
                raise APIError500('Server error')

    def generate_qr_code_url(self, uid=None, amount=None, strict=False,
                             snap_code_size=125, img_type='.png'):
        """
        Generates a QR Code image at a URL.

        Kwargs:
            uid (str): A unique identifier for tracking the payment.
            amount (int, float): Payment amount specified in Rands.
            strict (bool): Whether the payment amount is editable by the User.
            snap_code_size (int): Size of the QR Code image being generated.
                Range is 50 - 500.
            img_type (str): Extension of the QR Code image to return.

        Returns:
            A URL to generate the QR Code image.
        """
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
        """
        Marks the end of the current transaction period and the start of a
        new one.

        Args:
            timestamp (datetime): The timestamp for when to mark the end of the
                current transaction period.
            ref (str): A reference for this cash up period.

        Returns:
            A JSON object with a reference that marks the end of the current
            transaction period and the start of a new one.
        """
        data = {
            'date': timestamp.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'reference': ref
        }
        return self._post('cash_ups', data)

    def get_cash_ups(self, page=None, per_page=None, offset=None):
        """
        Get all cash up references that have been created.

        Kwargs:
            page (int): The page number for pagination.
            per_page (int): The amount of results to show per page.
            offset (int): The offset to start from.

        Returns:
            A paginated list of all cash up references that have been
            created. The references are ordered by descending date.
        """
        return self._get('cash_ups', page, per_page, offset)

    def get_cash_up_payments(self, ref, page=None, per_page=None, offset=None):
        """
        Get all cash up payments that have been created for a given reference.

        Args:
            ref (str): Reference for the cash up period.

        Kwargs:
            page (int): The page number for pagination.
            per_page (int): The amount of results to show per page.
            offset (int): The offset to start from.

        Returns:
            A list of all payments that were completed successfully in the
            specified cash up period. When a HTTP 500 is returned due to
            pending payments, we wait 5 seconds and then retry the request.
        """
        try:
            return self._get(
                'payments/cash_ups/%s' % ref,
                page,
                per_page,
                offset)
        except APIError500:
            time.sleep(5)
            return self.get_cash_up_payments(ref, page, per_page, offset)

    def get_payments(self, page=None, per_page=None, offset=None):
        """
        Get all payments for SnapScan merchant.

        Kwargs:
            page (int): The page number for pagination.
            per_page (int): The amount of results to show per page.
            offset (int): The offset to start from.

        Returns:
            A list of all payments.
        """
        return self._get('payments', page, per_page, offset)

    def get_payment(self, payment_id):
        """
        Get a specific payment for SnapScan merchant.

        Args:
            payment_id (int): The payment id to retrieve.

        Returns:
            A payment matching the identifier.
        """
        return self._get('payments/%i' % payment_id)
