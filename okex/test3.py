# -*- coding: utf-8 -*-
import requests
import json

def get_mom(syb):
	url = 'https://www.okex.com/api/spot/v3/instruments/{}-usdt/candles?granularity=3600'.format(syb)
	result = requests.get(url).json()
	
	print(result)

syb = input('请输入想要查询的币种:')

get_price(syb)	




















