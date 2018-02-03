# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
import json

def get_xr(coins_dict):
    api_dic = {'coinmarketcap':{'base_url':
        'https://api.coinmarketcap.com/v1/ticker/'},
    'nocks':{'base_url':'https://api.nocks.com/api/v2/trade-market/'},
    'poloniex':{'base_url':
        'https://poloniex.com/public?command=returnTradeHistory&currencyPair='}}
        
    xr = {}  
    
    # Coinmarketcap    
    coins = coins_dict['coinmarketcap']
    base_url = api_dic['coinmarketcap']['base_url']
    
    for quote, param in coins.items():
        url = '{}{}?convert=EUR'.format(base_url, param)
        request = requests.get(url)
        if not request.ok:
            xr[quote] = 'No JSON result for {} using {}'.format(quote, url)
        try:
            json_result = json.loads(request.content)
        
            xr[quote] = float(json_result[0]['price_eur'])
            print('..Successfully retrieved XR from {} for {}'.format(
                    'coinmarketcap', quote))
        except:
            print('Something went wrong with parsing the JSON from {}'.format(
                    quote))
        finally:
            request.close()
        
    # Nocks    
    coins = coins_dict['nocks']
    base_url = api_dic['nocks']['base_url']
    
    for quote, param in coins.items():
        url = '{}{}'.format(base_url, param)
        request = requests.get(url)
        if not request.ok:
            xr[quote] = 'No JSON result for {} using {}'.format(quote, url)
        try:
            json_result = json.loads(request.content)
        
            xr[quote] = float(json_result['data']['last']['amount'])
            print('..Successfully retrieved XR from {} for {}'.format(
                    'nocks', quote))            
        except:
            print('Something went wrong with parsing the JSON from {}'.format(
                    quote))
        finally:
            request.close()
        
    # Poloniex    
    coins = coins_dict['poloniex']
    base_url = api_dic['poloniex']['base_url']
    
    for quote, param in coins.items():
        url = '{}{}'.format(base_url, param)
        request = requests.get(url)
        if not request.ok:
            xr[quote] = 'No JSON result for {} using {}'.format(quote, url)
        try:
            json_result = json.loads(request.content)
        
            btc_xr = float(json_result[0]['rate'])
            xr[quote] = btc_xr * xr['BTC']
            print('..Successfully retrieved XR from {} for {}'.format(
                    'poloniex', quote))            
        except:
            print('Something went wrong with parsing the JSON from {}'.format(
                    quote))
        finally:
            request.close()      
    
    return xr


def main():
    # Example dictionary containing exchanges, tickers and API parameters
    coins_dict = {'coinmarketcap':{'BTC':'bitcoin'}, 'nocks':{'NLG':'NLG-EUR'},
                'poloniex':{'ETH':'BTC_ETH'}}
    # To open a JSON file containing the coins you'd want to look up the XR for
    # per exchange, uncomment the following lines)
    coins_dict_fp = input('Please prove a path to your coins saved in a JSON file:\n')
    if coins_dict_fp == "":
        coins_dict_fp = 'coins_dict.json'
    print(coins_dict_fp)
    
    try: 
        fh = open(coins_dict_fp, 'r')
        coins_dict = json.load(fh)
    finally:
        fh.close()
    
    xr = get_xr(coins_dict)
    quotes = []
    xrs = []
    for quote, xr in xr.items():
        print('{}: {}'.format(quote, xr))
        quotes.append(quote)
        xrs.append(xr)
        
    print('\nQuotes:')
    for quote in quotes:
        print(quote)
        
    print('\nXRs:')
    for xr in xrs:
        print(str(xr).replace('.',','))


if __name__ == '__main__':
    main()
    