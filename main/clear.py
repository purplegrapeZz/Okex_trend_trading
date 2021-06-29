# -*- coding: utf-8 -*-
import okex.spot_api as spot
import json
import datetime
import time
import smtplib #登录发送退出
from email.mime.text import MIMEText
from main import consts

passphrase = consts.passphrase
api_key_list=consts.api_key_list
secret_key_list=consts.secret_key_list

def log(content):
	log = open('log.txt','a',encoding='utf-8')
	log.write(str(content)+'\n')
	log.close()

def trade_status(spotAPI):
	statuslist=[]
	# 币币API	
	result = spotAPI.get_coin_account_info('BTC')
	statuslist.append((float(result['balance'][0:6]),'BTC-USDT',result['balance']))

	result = spotAPI.get_coin_account_info('ETH')
	statuslist.append((float(result['balance'][0:5]),'ETH-USDT',result['balance']))

	result = spotAPI.get_coin_account_info('XLM')
	statuslist.append((float(result['balance'][0:4]),'XLM-USDT',result['balance']))

	result = spotAPI.get_coin_account_info('ZEC')
	statuslist.append((float(result['balance'][0:4]),'ZEC-USDT',result['balance']))

	result = spotAPI.get_coin_account_info('ADA')
	statuslist.append((float(result['balance'][0:4]),'ADA-USDT',result['balance']))

	result = spotAPI.get_coin_account_info('DOT')
	statuslist.append((float(result['balance'][0:4]),'DOT-USDT',result['balance']))

	result = spotAPI.get_coin_account_info('UNI')
	statuslist.append((float(result['balance'][0:4]),'UNI-USDT',result['balance']))

	result = spotAPI.get_coin_account_info('ETC')
	statuslist.append((float(result['balance'][0:4]),'ETC-USDT',result['balance']))

	global selllist,lasthold
	selllist=[]
	lasthold=[]
	for i in statuslist:
		if i[0]:
			selllist.append(i)

	for i in selllist:
		lasthold.append(i[1])

def stop_check(spotAPI):
	stop_check_errlist=[]
	for i in lasthold:
		result = spotAPI.get_order_algos(instrument_id=i, order_type='1', status='1')
		result = spotAPI.cancel_algos(instrument_id=i, algo_ids=list(result.values())[0][0]['algo_id'], order_type='1')
		if not result['result']:
			stop_check_errlist.append({'timestamp':time.strftime('%m-%d %H:%M:%S'),'currency':result['instrument_id'],'status':False,'err_code':result['error_code'],'err_mesg':result['error_message']})

	if stop_check_errlist:
		log('委托撤单失败!错误日志:')
		log(stop_check_errlist)
	else:
		log('委托撤单成功!')

def sell_all(spotAPI):
	global sellall_err
	sellall_err=[]
	sellall_mesg=[]
	for i in selllist:
		result = spotAPI.take_order(instrument_id=i[1], side='sell', type='market', size=i[2],order_type='0')
		if not result['result']:
			sellall_err.append({'timestamp':time.strftime('%m-%d %H:%M:%S'),'currency':i[1],'error_code':result['error_code'],'err_mesg':result['error_message']})
		else:
			result = spotAPI.get_orders_list(instrument_id=i[1], state='2')
			result = result[0][0]
			sellall_mesg.append({'timestamp':time.strftime('%m-%d %H:%M:%S'),'currency':i[1],'type':'sell','status':'ok','amount':result['size'],'price':'$'+result['price_avg'],'notional':result['filled_notional']+'usdt'})


	if sellall_err:
		log('全部卖出失败!错误日志:')
		log(sellall_err)
	else:
		log('全部卖出成功!交易明细:')
		log(sellall_mesg)

def clear():
	log('---------------------------------------------------')
	for i in zip(api_key_list,secret_key_list):
		spotAPI = spot.SpotAPI(i[0], i[1], passphrase, False)
		trade_status(spotAPI)
		if lasthold:
			try:
				stop_check(spotAPI)
			except:
				pass

		if selllist:
			sell_all(spotAPI)


			
