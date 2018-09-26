import urllib.parse
from abc import ABC, abstractmethod


class BaseMessage(ABC):

    def __init__(self, payload: str):
        values = payload.split('\r\n')

        headers_index = values.index('')
        self._headers = {}
        for item in values[1: headers_index]:
            key, val = item.split(':', 1)
            self._headers[str(key).lower()] = str(val).strip()
        self._body = ''.join(values[headers_index + 1:])

    @property
    @abstractmethod
    def http_version(self):
        pass

    @property
    def headers(self):
        return self._headers

    @property
    def body(self):
        return self._body


class RequestMessage(BaseMessage):

    def __init__(self, payload: str):
        values = payload.split('\r\n')
        self._request_method, self._request_uri, self._http_version = values[0].split(' ')
        BaseMessage.__init__(self, payload)

    @property
    def request_method(self):
        return self._request_method

    @property
    def request_uri(self):
        return self._request_uri

    @property
    def http_version(self):
        return self._http_version


class ResponseMessage(BaseMessage):

    def __init__(self, payload: str):
        values = payload.split('\r\n')
        self._http_version, self._status_code, self._status_message = values[0].split(' ')
        BaseMessage.__init__(self, payload)

    @property
    def http_version(self):
        return self._http_version

    @property
    def status_code(self):
        return self._status_code

    @property
    def status_message(self):
        return self.status_message


def is_url(message: BaseMessage) -> bool:
    return 'content-type' in message.headers and 'urlencoded' in message.headers['content-type']


def parse_url_encoding(message: BaseMessage):
    body = message.body

    if is_url(message):
        body = {}
        encoded_url = urllib.parse.unquote(message.body)
        for item in encoded_url.split('&'):
            k, v = item.split('=', 1)
            body[k] = v

    return body
