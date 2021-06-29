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
weekday = datetime.datetime.now().isoweekday()
api_key,secret_key=api_key_list[weekday-1],secret_key_list[weekday-1]
logtime = time.strftime('%Y-%m-%d %H:%M:%S')
spotAPI = spot.SpotAPI(api_key, secret_key, passphrase, False)

def log(content):
	log = open('log.txt','a',encoding='utf-8')
	log.write(str(content)+'\n')
	log.close()


def trade_check():
	# 币币API
	#result = spotAPI.get_account_info()
	#result = spotAPI.get_coin_account_info('USDT')

	# 公共-获取K线数据
	result = spotAPI.get_kline(instrument_id='BTC-USDT', granularity='3600')
	mom_btc = float('%0.2f' % (float(result[0][1])/float(result[-32][1])))
	
	result = spotAPI.get_kline(instrument_id='ETH-USDT', granularity='3600')
	mom_eth = float('%0.2f' % (float(result[0][1])/float(result[-32][1])))

	result = spotAPI.get_kline(instrument_id='XLM-USDT', granularity='3600')
	mom_xlm = float('%0.2f' % (float(result[0][1])/float(result[48][1])))

	result = spotAPI.get_kline(instrument_id='ZEC-USDT', granularity='3600')
	mom_zec = float('%0.2f' % (float(result[0][1])/float(result[48][1])))

	result = spotAPI.get_kline(instrument_id='ADA-USDT', granularity='3600')
	mom_ada = float('%0.2f' % (float(result[0][1])/float(result[48][1])))

	result = spotAPI.get_kline(instrument_id='DOT-USDT', granularity='3600')
	mom_dot = float('%0.2f' % (float(result[0][1])/float(result[48][1])))
	
	result = spotAPI.get_kline(instrument_id='UNI-USDT', granularity='3600')
	mom_uni = float('%0.2f' % (float(result[0][1])/float(result[48][1])))

	result = spotAPI.get_kline(instrument_id='ETC-USDT', granularity='3600')
	mom_etc = float('%0.2f' % (float(result[0][1])/float(result[48][1])))


	list1 = [(mom_eth,'ETH-USDT'),(mom_xlm,'XLM-USDT'),(mom_zec,'ZEC-USDT'),(mom_ada,'ADA-USDT'),(mom_dot,'DOT-USDT'),(mom_uni,'UNI-USDT'),(mom_etc,'ETC-USDT')]
	list1 = sorted(list1)

	cal1 = list1[-1][0]
	cal2 = list1[-2][0]

	global pairlist,holdlist
	pairlist=[[0,''],[0,''],[0,list1[-1][1]],[0,list1[-2][1]]]
	

	if mom_btc > mom_eth and mom_btc>=1:
		pairlist[0][1] = 'BTC-USDT'
		pairlist[0][0] = 1
		if mom_eth>=1:
			pairlist[1][1] = 'ETH-USDT'
			pairlist[1][0] = 1
		else:
			pairlist[1][1] = 'BTC-USDT'
			pairlist[1][0] = 1

	if mom_btc < mom_eth and mom_eth>=1:
		pairlist[0][1] = 'ETH-USDT'
		pairlist[0][0] = 1
		if mom_btc>=1:
			pairlist[1][1] = 'BTC-USDT'
			pairlist[1][0] = 1
		else:
			pairlist[1][1] = 'ETH-USDT'
			pairlist[1][0] = 1

	if mom_btc >= 1 or cal1 >= 1:
		if mom_btc > cal1:
			pairlist[2][1] = 'BTC-USDT'
		pairlist[2][0] = 1

	if mom_btc >= 1 or cal2 >= 1:
		if mom_btc > cal2:
			pairlist[3][1] = 'BTC-USDT'
		pairlist[3][0] = 1



	holdlist=[]
	for i in pairlist:
		if i[0]:
			holdlist.append(i[1])

	log('今日持仓币对:')
	log(holdlist)


def trade_status():
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

	log('上周持仓:')
	log(lasthold)


def stop_check():
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

sellall_err=[]
trade_err_mesg=[]
stop_order_errmesg=[]
def sell_all():
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
	global usdt		
	result = spotAPI.get_coin_account_info('USDT')
	result = float(result['available'])
	usdtlist =[str(result*0.4)[0:5],str(result*0.3)[0:5],str(result*0.2)[0:5],str(result*0.1)[0:5]] 
	usdt = result

	for i in range(4):
		pairlist[i].append(usdtlist[i])

	if sellall_err:
		log('全部卖出失败!错误日志:')
		log(sellall_err)
	else:
		log('全部卖出成功!交易明细:')
		log(sellall_mesg)
	#print(pairlist)

def balance_check():
	result = spotAPI.get_coin_account_info('USDT')
	global usdt
	usdt =result
	return result	


def trade():
	global trade_err_mesg
	trade_err_mesg=[]
	trade_mesg=[]
	for i in pairlist:
		if i[0]:
			result = spotAPI.take_order(instrument_id=i[1], side='buy', type='market', order_type='0', notional=i[2])
			if not result['result']:
				trade_err_mesg.append({'timestamp':time.strftime('%m-%d %H:%M:%S'),'currency':i[1],'error_code':result['error_code'],'err_mesg':result['error_message']})
			else:
				result = spotAPI.get_orders_list(instrument_id=i[1], state='2')
				result = result[0][0]
				trade_mesg.append({'timestamp':time.strftime('%m-%d %H:%M:%S'),'currency':i[1],'type':'buy','status':'ok','balance':result['filled_size'],'price':'$'+result['price_avg'],'notional':result['notional']+'usdt'})

	if trade_err_mesg:
		log('买入失败!错误日志:')
		log(trade_err_mesg)
	if trade_mesg:
		log('买入成功!交易明细:')
		log(trade_mesg)


def hold_check():
	holdcheck=[]
	global stop_price
	stop_price=[]
	global hold_status
	hold_status=''
	for i in holdlist:
		result = spotAPI.get_coin_account_info(i[0:3])
		holdcheck.append((i[0:3],result['balance']))
	holdcheck = list(set(holdcheck))

	for i in holdcheck:
		result = spotAPI.get_orders_list(instrument_id=i[0]+'-USDT', state='2')
		result = '%0.2f'%(float(result[0][0]['price_avg'])*0.9)
		stop_price.append((i[0]+'-USDT',i[1],result))

	for i in holdcheck:
		hold_status+=str(i)+';'
	hold_status= hold_status.replace('(','').replace(')','').replace(',','').replace("'",'').replace(';','\n')[0:-1]


def stop_order():
	stop_order_list=[]
	global stop_order_errmesg
	stop_order_errmesg=[]

	for i in stop_price:
		result = spotAPI.take_order_algo(instrument_id=i[0], mode='1', order_type='1', size=i[1], side='sell', trigger_price=i[2], algo_price='',algo_type='2')
		if not result['result']:
			stop_order_errmesg.append({'timestamp':time.strftime('%m-%d %H:%M:%S'),'type':'stop_order','status':False,'instrument_id':result['instrument_id'],'error_code':result['error_code'],'error_message':result['error_message']})
		else:
			stop_order_list.append({'timestamp':time.strftime('%m-%d %H:%M:%S'),'type':'stop_order','status':True,'instrument_id':result['instrument_id'],'algo_id':result['algo_id'],'order_type':result['order_type']})

	if stop_order_errmesg:
		log('止损设置失败!错误日志:')
		log(stop_order_errmesg)

	if stop_order_list:
		log('止损设置成功!')
		log(stop_order_list)

def email():
	mail_host = consts.mail_host
	mail_user = consts.mail_user
	mail_pwd = consts.mail_pwd
	mail_receiver = consts.mail_receiver

	date = time.strftime('%Y-%m-%d')
	mail_subject = '{} 交易简报 Trading{}'.format(date,weekday)

	if holdlist:
		status = str(holdlist).replace('[','').replace(']','').replace("'",'')
	else:
		status = '空仓'

	if lasthold:
		email_lasthold = str(lasthold).replace('[','').replace(']','').replace("'",'')
	else:
		email_lasthold = '<font color="red">空仓</font>'

	if not (sellall_err and trade_err_mesg and stop_order_errmesg):
		setup_status=' <font color="green">OK</font>'
	else:
		setup_status=' false</br>错误日志:</br>'+str(sellall_err)+'</br>'+str(trade_err_mesg)+'</br>'+str(stop_order_errmesg)

	if status == '空仓':
		setup_status = ' None'
		status = '<font color="red">空仓</font>'
	errmesg = []
	if sellall_err:
		errmesg.append('卖出错误!'+str(sellall_err)+'</br>')
	if trade_err_mesg:
		errmesg.append('买入错误!'+str(trade_err_mesg)+'</br>')
	if stop_order_errmesg:
		errmesg.append('止损设置错误!'+str(stop_order_errmesg)+'</br>')

	if errmesg:
		errmesg=str(errmesg).replace("'",'').replace('"','').replace('[','').replace(']','')
		setup_status+='</br>{}'.format(errmesg)
		br = ''
	else:
		br = '</br>'

	email_holdstatus = hold_status.replace('\n','</br>')

	if email_holdstatus:
		holdbr = '</br>'
	else:
		holdbr = ''
	mail_content = '''今日持仓:</br>{}</br>上周持仓:</br>{}</br></br>Trade Status:{}</br>{}持仓信息:</br>{}{}账户余额 {} usdt'''.format(status,email_lasthold,setup_status,br,email_holdstatus,holdbr,usdt['available'])

	msg = MIMEText(mail_content,'html','utf-8')
	msg['Subject'] = mail_subject
	msg['From'] = mail_user
	msg['To'] = mail_receiver
	client = smtplib.SMTP_SSL(mail_host,465) #得到smtp服务器的连接
	client.login(mail_user,mail_pwd) #登录
	client.send_message(msg)
	client.quit

def setup():
	log('---------------------------------------------------')
	datecontent = logtime+'   Trading '+str(weekday)
	log(datecontent)
	trade_check()
	trade_status()

	if lasthold:
		try:
			stop_check()
		except:
			pass

	if selllist:
		sell_all()
	else:
		usdt=balance_check()
		usdt = float(usdt['available'])
		usdtlist =[str(usdt*0.4)[0:5],str(usdt*0.3)[0:5],str(usdt*0.2)[0:5],str(usdt*0.1)[0:5]] 
		for i in range(4):
			pairlist[i].append(usdtlist[i])

	if holdlist:
		trade()

	try:
		hold_check()
	except:
		pass

	if stop_price:
		stop_order()

	log('持仓信息:')
	log(hold_status)
	usdt=balance_check()
	log('账户余额 %s usdt'%usdt['available'])

	email()

def clear():
	for i in zip(api_key_list,secret_key_list):
		spotAPI = spot.SpotAPI(i[0], i[1], passphrase, False)
		trade_status()
		if lasthold:
			try:
				stop_check()
			except:
				pass

		if selllist:
			sell_all()

if __name__ == '__main__':
	try:
		setup()
	except Exception as err:
		import smtplib #登录发送退出
		from email.mime.text import MIMEText
		mail_host = consts.mail_host
		mail_user = consts.mail_user
		mail_pwd = consts.mail_pwd
		mail_receiver = consts.mail_receiver

		mail_subject = '报警提醒!程序异常退出!'
		mail_content = '错误提示:</br>%s'%err
		msg = MIMEText(mail_content,'html','utf-8')
		msg['Subject'] = mail_subject
		msg['From'] = mail_user

		msg['To'] = mail_receiver
		client = smtplib.SMTP_SSL(mail_host,465) #得到smtp服务器的连接
		client.login(mail_user,mail_pwd) #登录
		client.send_message(msg)
		client.quit


