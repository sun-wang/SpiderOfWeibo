#coding:utf8
import urllib
import rsa
import base64
import binascii
import re
#此函数将用户名用base64加密
def encrypt_user_name(original_user_name):
	#将用户名url编码
	user_name_temp = urllib.quote(original_user_name)
	#将编码后的用户名用base64加密
	encrypted_user_name = base64.encodestring(user_name_temp)[: -1]
	# print encrypted_user_name
	return encrypted_user_name
#此函数将用户密码加密，需要原始密码，servertime时间戳 ，nonce一次性随机码 ，公钥
def encrypt_user_password(original_user_password, server_time, nonce , pubkey):
	#将pubkey转换为整型数字
	rsa_public_key = int(pubkey, 16)
	#创建公钥
	key = rsa.PublicKey(rsa_public_key, 65537)#1001?
	#加入servertime , nonce , password
	#js中的方式
	message = str(server_time) + '\t' +str(nonce) + '\n' + str(original_user_password)
	#将连接后的字符串加密

	encrypted_user_password = rsa.encrypt(message, key)
	#将加密后的信息转化为16进制
	encrypted_user_password = binascii.b2a_hex(encrypted_user_password)
	return encrypted_user_password
#此函数将加密后的信息构成post数据
def post_encode(user_name, user_password, server_time, nonce, pubkey, rsakv):
	#调用encrypt_user_name函数
	get_encrypt_user_name = encrypt_user_name(user_name)
	get_encrypt_user_password = encrypt_user_password(user_password, server_time, nonce, pubkey)
	#构建post数据
	post_data = {
		        'entry': 'weibo',
		        'gateway': '1',
		        'from': '',
		        'savestate': '7',
		        'userticket': '1',
		        'ssosimplelogin': '1',
		        'vsnf': '1',
		        'vsnval': '',
		        'su': get_encrypt_user_name,
		        'service': 'miniblog',
		        'servertime': server_time,
		        'nonce': nonce,
		        'pwencode': 'rsa2',
		        'sp': get_encrypt_user_password,
		        'encoding': 'UTF-8',
		        'prelt': '115',
		        'rsakv': rsakv,     
		        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
		        'returntype': 'META'
	}
	#将post数据编码
	get_post_data = urllib.urlencode(post_data)
	return get_post_data