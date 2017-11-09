"""
    Copyright (c) 2013, Los Alamos National Security, LLC
    All rights reserved.

    Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
    following conditions are met:

    * Redistributions of source code must retain the above copyright notice, this list of conditions and the following
      disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
      following disclaimer in the documentation and/or other materials provided with the distribution.
    * Neither the name of Los Alamos National Security, LLC nor the names of its contributors may be used to endorse or
      promote products derived from this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
    INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
    WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
    THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient


ACCESS_TOKEN_URL = 'https://api.yelp.com/oauth2/token'

SEARCH_API_URL = 'https://api.yelp.com/v3/businesses/search'
PHONE_SEARCH_API_URL = 'https://api.yelp.com/v3/businesses/search/phone'
BUSINESS_MATCH_BEST_API_URL = 'https://api.yelp.com/v3/businesses/matches/best'
BUSINESS_MATCH_LOOKUP_API_URL = 'https://api.yelp.com/v3/businesses/matches/best'
TRANSACTION_SEARCH_API_URL = 'https://api.yelp.com/v3/transactions/{}/search'
BUSINESS_API_URL = 'https://api.yelp.com/v3/businesses/{}'
REVIEWS_API_URL = 'https://api.yelp.com/v3/businesses/{}/reviews'
AUTOCOMPLETE_API_URL = 'https://api.yelp.com/v3/autocomplete'
GRAPHQL_API_URL = 'https://api.yelp.com/v3/graphql'


class YelpAPI(object):

    """
        This class implements the complete Yelp Fusion API. It offers access to the following APIs:

            * Search API - https://www.yelp.com/developers/documentation/v3/business_search
            * Phone Search API - https://www.yelp.com/developers/documentation/v3/business_search_phone
            * Transaction Search API - https://www.yelp.com/developers/documentation/v3/transactions_search
            * Business API - https://www.yelp.com/developers/documentation/v3/business
            * Reviews API - https://www.yelp.com/developers/documentation/v3/business_reviews
            * Autocomplete API - https://www.yelp.com/developers/documentation/v3/autocomplete

        It is simple and completely extensible since it dynamically takes arguments. This will allow it to continue working even
        if Yelp changes the spec. The only thing that should cause this to break is if Yelp changes the URL scheme.
    """

    class YelpAPIError(Exception):

        """
            This class is used for all API errors. Currently, there is no master list of all possible errors, but
            there is an open issue on this: https://github.com/Yelp/yelp-fusion/issues/95
        """
        pass

    def __init__(self, client_id, client_secret):
        self._yelp_session = OAuth2Session(client=BackendApplicationClient(client_id=client_id))
        self._yelp_session.fetch_token(token_url=ACCESS_TOKEN_URL, client_id=client_id, client_secret=client_secret)

    def search_query(self, **kwargs):
        """
            Query the Yelp Search API. Visit https://www.yelp.com/developers/documentation/v3/business_search
            for documentation on the parameters and response body.
        """
        return self._query(SEARCH_API_URL, **kwargs)

    def phone_search_query(self, **kwargs):
        """
            Query the Yelp Phone Search API. Visit https://www.yelp.com/developers/documentation/v3/business_search_phone
            for documentation on the parameters and response body.

            NOTE: A mandatory phone number (parameter 'phone') must be provided.
        """
        if 'phone' not in kwargs or not kwargs['phone']:
            raise ValueError('A valid phone number (parameter "phone") must be provided.')

        return self._query(PHONE_SEARCH_API_URL, **kwargs)

    def business_match_query(self, **kwargs):
        """
            Query the Yelp Business Match API. Visit https://www.yelp.com/developers/documentation/v3/business_match
            for documentation on the parameters and response body.

            NOTE: Mandatory parameters "name", "city", and "state" must be provided.
            NOTE: Defaults to type using the "best" search method. Can be set to "lookup" for the top 10 results.
        """
        if 'name' not in kwargs or not kwargs['name']:
            raise ValueError('Valid business name (parameter "name") must be provided.')

        if 'city' not in kwargs or not kwargs['city']:
            raise ValueError('Valid city (parameter "city") must be provided.')

        if 'state' not in kwargs or not kwargs['state']:
            raise ValueError('Valid state (parameter "state") must be provided.')

        if 'country' not in kwargs or not kwargs['country']:
            kwargs['country'] = 'US'

        if 'type' not in kwargs or not kwargs['type']:
            kwargs['type'] = 'best'

        if kwargs['type'] not in ('best', 'lookup'):
            raise ValueError('Valid match type(parameter "type") must be provided. Accepted values: "best" or "lookup".')

        if kwargs['type'] is 'best':
            match_url = BUSINESS_MATCH_BEST_API_URL
        elif kwargs['type'] is 'lookup':
            match_url = BUSINESS_MATCH_LOOKUP_API_URL

        return self._query(match_url.format(id), **kwargs)

    def transaction_search_query(self, transaction_type, **kwargs):
        """
            Query the Yelp Transaction Search API. Visit https://www.yelp.com/developers/documentation/v3/transactions_search
            for documentation on the parameters and response body.

            NOTE: A mandatory transaction type (parameter "transaction_type") must be provided.
        """
        if not transaction_type:
            raise ValueError('A valid transaction type (parameter "transaction_type") must be provided.')

        return self._query(TRANSACTION_SEARCH_API_URL.format(transaction_type), **kwargs)

    def business_query(self, id, **kwargs):
        """
            Query the Yelp Business API. Visit https://www.yelp.com/developers/documentation/v3/business
            for documentation on the parameters and response body.

            NOTE: A mandatory business ID (parameter "id") must be provided.
        """
        if not id:
            raise ValueError('A valid business ID (parameter "id") must be provided.')

        return self._query(BUSINESS_API_URL.format(id), **kwargs)

    def reviews_query(self, id, **kwargs):
        """
            Query the Yelp Reviews API. Visit https://www.yelp.com/developers/documentation/v3/business_reviews
            for documentation on the parameters and response body.

            NOTE: A mandatory business ID (parameter "id") must be provided.
        """
        if not id:
            raise ValueError('A valid business ID (parameter "id") must be provided.')

        return self._query(REVIEWS_API_URL.format(id), **kwargs)

    def autocomplete_query(self, **kwargs):
        """
            Query the Yelp Autocomplete API. Visit https://www.yelp.com/developers/documentation/v3/autocomplete
            for documentation on the parameters and response body.

            NOTE: Mandatory search text (parameter "text") must be provided.
        """
        if 'text' not in kwargs or not kwargs['text']:
            raise ValueError('Valid text (parameter "text") must be provided.')

        return self._query(AUTOCOMPLETE_API_URL, **kwargs)

    def graphql_query(self, query, **kwargs):
        """
            Query the Yelp GraphQL API. Visit https://www.yelp.com/developers/graphql/guides/intro
            for documentation on the parameters and response body.
        """
        if not query:
            raise ValueError('A graphQL query must be provided.')

        response = self._yelp_session.post(GRAPHQL_API_URL, headers={'Content-Type': 'application/graphql'}, data=query)

        if not response.ok:
            raise YelpAPI.YelpAPIError(response.text)

        response_json = response.json()

        if 'error' in response_json:
            raise YelpAPI.YelpAPIError('{}: {}'.format(response_json['error']['code'], response_json['error']['description']))

        return response_json

    @staticmethod
    def _get_clean_parameters(kwargs):
        """
            Clean the parameters by filtering out any parameters that have a None value.
        """
        return dict((k, v) for k, v in kwargs.items() if v is not None)

    def _query(self, url, **kwargs):
        """
            All query methods have the same logic, so don't repeat it! Query the URL, parse the response as JSON,
            and check for errors. If all goes well, return the parsed JSON.
        """
        parameters = YelpAPI._get_clean_parameters(kwargs)
        response = self._yelp_session.get(url, params=parameters)
        response_json = response.json()  # it shouldn't happen, but this will raise a ValueError if the response isn't JSON

        # Yelp can return one of many different API errors, so check for one of them.
        # The Yelp Fusion API does not yet have a complete list of errors, but this is on the TODO list; see
        # https://github.com/Yelp/yelp-fusion/issues/95 for more info.
        if 'error' in response_json:
            raise YelpAPI.YelpAPIError('{}: {}'.format(response_json['error']['code'], response_json['error']['description']))

        # we got a good response, so return
        return response_json
