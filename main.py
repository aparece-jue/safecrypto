#!/usr/bin/python3

import sys
import hashlib
import binascii
import base64
import time

def sh256(data):
    # 创建SHA-256对象
    sha256_hash = hashlib.sha256()
    # 更新哈希对象的输入数据
    sha256_hash.update(data)
    # 获取加密后的结果（以字节形式）
    encrypted_data = sha256_hash.digest()
    # 将加密结果转换为十六进制表示
    hex_encrypted_data = sha256_hash.hexdigest()
    return encrypted_data

def enp(password, salt, iterations=1000, key_length=6):
    # 使用hmac和hashlib库实现PBKDF2
    key = hashlib.pbkdf2_hmac('sha256', password, salt, iterations, key_length)
    # 将生成的密钥转换为十六进制表示
    hex_key = binascii.hexlify(key)
    #print(hex_key)
    return base64.a85encode(hex_key).decode()

def getsalt():
    timestamp = int(time.time() * 10000000)
    temp = hex(timestamp)[2:]
    temp = binascii.unhexlify(temp if len(temp)%2==0 else "0"+temp)
    return sh256(temp)

# 原密码，加密信息
data=sys.argv
n=len(data)-1
a1=""
# 都有
if n==2:
	passwd=data[1].encode()
	a1=data[2]
# 没有加密信息
elif n==1:
	passwd=data[1].encode()
	a1 = input("请输入加密信息salt(默认使用时间戳):")
# 没有密码
else:
	passwd = input("请输入基础密码:").encode()
	a1 = input("请输入加密信息(默认使用时间戳):")

salt = getsalt() if a1 == "" else sh256(a1.encode())

c = enp(passwd, salt, key_length=6)
#print("生成的密钥:", c, "密钥长度", len(c))
print("|"+passwd.decode()+"|"+a1+"|"+c+"|")
