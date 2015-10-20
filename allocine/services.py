from hashlib import sha1
from urllib.parse import urlencode
from allocine.utils import AndroidUserAgentSelector
import datetime
import base64
import requests


class AllocineService:
    """
    Allocine API
    """
    def __init__(self):
        self.apiHostName = 'http://api.allocine.fr'
        self.apiBasePath = '/rest/v3/'
        self.apiPartner = '100043982026'
        self.apiSecretKey = b'29d185d98c984a359e6e6f26a0474269'
        self.imgBaseUrl = 'http://images.allocine.fr'
        self.userAgentSelector = AndroidUserAgentSelector()

    def get_movie(self, allocine_code, profile='small'):
        params = [('code', allocine_code),
                  ('profile', 'large'),
                  ('format', 'json')]
        request = self.build_request('movie', params)

        session = requests.Session()
        response = session.send(request)

        return response

    def get_theaters(self, zip):
        params = [('zip', zip), ('profile', 'large'), ('format', 'json')]
        request = self.build_request('theaterlist', params)

        session = requests.Session()
        response = session.send(request)

        return response

    def get_showtimes(self, zip=None, theaters=None, location=None, movie=None, date=None):
        params = [('format', 'json'),]
        if zip: params.append(('zip', zip))
        if theaters: params.append(('theaters', theaters))
        if location: params.append(('location', location))
        if movie: params.append(('movie', movie))
        if date: params.append(('date', date))

        request = self.build_request('showtimelist', params)

        session = requests.Session()
        response = session.send(request)

        return response

    def build_request(self, method, params=[]):
        """
        Builds a Prepared Request that will fetch the data requested
        """

        request_params = [('partner', '100043982026')]
        request_params.extend(params)

        #Add the timestamp to the params
        timestamp = datetime.datetime.now().strftime('%Y%m%d')
        request_params.append(("sed", timestamp))

        #URL encode the params
        message = urlencode(request_params).encode('utf-8')

        #Build the signature
        hashed_value = base64.b64encode(sha1(self.apiSecretKey + message).digest())
        print('base64encode=' + str(hashed_value, 'utf-8'))
        #hashed_value = quote_plus(hashed_value)
        #print('urlencoded=' + hashed_value)

        #Add the signature to the params
        request_params.append(('sig', hashed_value))

        headers = {
            'user-agent': self.userAgentSelector.get_user_agent(),
            'accept': "application/json"
        }
        request = requests.Request('GET', self.apiHostName + self.apiBasePath + method, params=request_params, headers=headers)
        prepared = request.prepare()

        self.pretty_print_prepared_request(prepared)
        return prepared

    def pretty_print_prepared_request(self, req):
        """
        Pretty prints a prepared request
        :param req:
        :return:
        """
        print('{}\n{}\n{}\n\n{}'.format(
            '-----------START-----------',
            req.method + ' ' + req.url,
            '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            req.body,
        ))

