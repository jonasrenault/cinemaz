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

    def get_movie(self, code, profile='large'):
        """
        Sends a request to fetch movie information.
        :param code:  identifiant du film (entier)
        :param profile: (optionnel) degré d'informations renvoyées (valeurs possibles : small, medium, large)
        :return:
        """
        params = [('code', code),
                  ('profile', profile),
                  ('format', 'json')]

        request = self.build_request('movie', params)

        session = requests.Session()
        response = session.send(request)

        return response

    def get_theaters(self, zip=None, profile='large', code=None, location=None, count=None, page=None):
        """
        Sends a request to fetch cinemas. One of zip, theater, or location is mandatory

        :param zip:
        :param profile: (optionnel) degré d'informations renvoyées (valeurs possibles : small, medium, large)
        :param code:
        :param location:
        :param count:
        :param page:
        :return:
        """
        params = [('format', 'json'), ('profile', profile)]
        if zip is not None:
            params.append(('zip', zip))
        if code is not None:
            params.append(('theater', code))
        if location is not None:
            params.append(('location', location))
        if count is not None:
            params.append(('count', count))
        if page is not None:
            params.append(('page', page))

        request = self.build_request('theaterlist', params)

        session = requests.Session()
        response = session.send(request)

        return response

    def get_showtimes(self, zip=None, theaters=None, location=None, movie=None, date=None, count=None, page=None):
        """
        Sends a request to fetch movie showtimes. One of theaters, zip, or location is mandatory

        :param zip: code postal de la ville
        :param theaters: liste de codes de cinémas (séparé par une virgule, exemple: P0728,P0093)
        :param location:
        :param movie: (optionnel) identifiant du film (si non précisé, affiche tous les films)
        :param date: (optionnel) date au format YYYY-MM-DD (si non précisé, date du jour)
        :return:
        """
        params = [('format', 'json'),]
        if zip is not None:
            params.append(('zip', zip))
        if theaters is not None:
            params.append(('theaters', theaters))
        if location is not None:
            params.append(('location', location))
        if movie is not None:
            params.append(('movie', movie))
        if date is not None:
            params.append(('date', date))
        if count is not None:
            params.append(('count', count))
        if page is not None:
            params.append(('page', page))

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

