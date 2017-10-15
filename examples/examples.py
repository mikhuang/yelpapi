#!/usr/bin/env python

"""
    Example call:
        ./examples.py --client_id="[CLIENT ID]" --client_secret="[CLIENT SECRET]"
"""

from yelpapi import YelpAPI
import argparse
from pprint import pprint

argparser = argparse.ArgumentParser(description='Example Yelp queries using yelpapi. Visit https://www.yelp.com/developers/v3/manage_app to get the necessary API keys.')
argparser.add_argument('--client_id', type=str, help='Yelp Fusion API client ID')
argparser.add_argument('--client_secret', type=str, help='Yelp Fusion API client secret')
args = argparser.parse_args()

yelp_api = YelpAPI(args.client_id, args.client_secret)


"""
    Example search by location text and term. 
    
    Search API: https://www.yelp.com/developers/documentation/v3/business_search
"""
print('***** 5 best rated ice cream places in Austin, TX *****\n{}\n'.format("yelp_api.search_query(term='ice cream', location='austin, tx', sort_by='rating', limit=5)"))
response = yelp_api.search_query(term='ice cream', location='austin, tx', sort_by='rating', limit=5)
pprint(response)
print('\n-------------------------------------------------------------------------\n')


"""
    Example search by centroid and category.
    
    all Yelp categories: https://www.yelp.com/developers/documentation/v3/all_category_list
    centroid: https://www.flickr.com/places/info/2487956
"""
print('***** 5 bike rentals in San Francisco *****\n{}\n'.format("yelp_api.search_query(categories='bikerentals', longitude=-122.4392, latitude=37.7474, limit=5)"))
response = yelp_api.search_query(categories='bikerentals', longitude=-122.4392, latitude=37.7474, limit=5)
pprint(response)
print('\n-------------------------------------------------------------------------\n')


"""
    Example phone search query.
    
    Phone Search API: https://www.yelp.com/developers/documentation/v3/business_search_phone
"""
print('***** search for business by phone number *****\n{}\n'.format("yelp_api.phone_search_query(phone='+13193375512')"))
response = yelp_api.phone_search_query(phone='+13193375512')
pprint(response)
print('\n-------------------------------------------------------------------------\n')

"""
    Example business match query with the 'best' type.
    
    Business Match API: https://www.yelp.com/developers/documentation/v3/business_match
"""
print('***** search for business best match *****\n{}\n'.format("yelp_api.business_match_query(name='Splash Cafe', city='Pismo Beach', state='CA')"))
response = yelp_api.business_match_query(name='Splash Cafe', city='Pismo Beach', state='CA')
pprint(response)
print('\n-------------------------------------------------------------------------\n')

"""
    Example business match query with the 'lookup' type.
    
    Business Match API: https://www.yelp.com/developers/documentation/v3/business_match
"""
print('***** search for business best match *****\n{}\n'.format("yelp_api.business_match_query(name='Splash Cafe', city='Pismo Beach', state='CA')"))
response = yelp_api.business_match_query(name='Splash Cafe', city='Pismo Beach', state='CA', type='lookup')
pprint(response)
print('\n-------------------------------------------------------------------------\n')


"""
    Example transaction search query.
    
    Transaction Search API: https://www.yelp.com/developers/documentation/v3/transactions_search
"""
print("***** businesses in Dallas supporting delivery transactions *****\n{}\n".format("yelp_api.transaction_search_query(transaction_type='delivery', location='dallas, tx')"))
response = yelp_api.transaction_search_query(transaction_type='delivery', location='dallas, tx')
pprint(response)
print('\n-------------------------------------------------------------------------\n')


"""
    Example business query.
    
    Business API: https://www.yelp.com/developers/documentation/v3/business
"""
print("***** business information for Amy's on 6th St. *****\n{}\n".format("yelp_api.business_query(id='amys-ice-creams-austin-3')"))
response = yelp_api.business_query(id='amys-ice-creams-austin-3')
pprint(response)
print('\n-------------------------------------------------------------------------\n')


"""
    Example reviews query.
    
    Reviews API: https://www.yelp.com/developers/documentation/v3/business_reviews
"""
print("***** selected reviews for Amy's on 6th St. *****\n{}\n".format("yelp_api.reviews_query(id='amys-ice-creams-austin-3')"))
response = yelp_api.reviews_query(id='amys-ice-creams-austin-3')
pprint(response)
print('\n-------------------------------------------------------------------------\n')


"""
    Example autocomplete query.
    
    Autocomplete API: https://www.yelp.com/developers/documentation/v3/autocomplete
    centroid: https://www.flickr.com/places/info/2427422
"""
print("***** autocomplete results for 'Hambur' in Iowa City *****\n{}\n".format("yelp_api.autocomplete_query(text='Hambur', longitude=-91.5327, latitude=41.6560)"))
response = yelp_api.autocomplete_query(text='Hambur', longitude=-91.5327, latitude=41.6560)
pprint(response)
print('\n-------------------------------------------------------------------------\n')


"""
    Example erroneous search query.
"""
print('***** sample erroneous search query *****\n{}\n'.format("yelp_api.search_query(term='ice cream', location='austin, tx', sort_by='BAD_SORT')"))
try:
    # sort can only take on values "best_match", "rating", "review_count", or "distance"
    yelp_api.search_query(term='ice cream', location='austin, tx', sort_by='BAD_SORT')
except YelpAPI.YelpAPIError as e:
    print(e)
print('\n-------------------------------------------------------------------------\n')


"""
    Example erroneous business query.
"""
print('***** sample erroneous business query *****\n{}\n'.format("yelp_api.business_query(id='fake-business')"))
try:
    yelp_api.business_query(id='fake-business')
except YelpAPI.YelpAPIError as e:
    print(e)
