#from Crypto.Util.Padding import pad, unpad
#from Crypto.Cipher import AES
#from Crypto.Random import get_random_bytes
#import hashlib

def encode(replay):
    return
#打开需要加密的文件并将内容赋值给data
#in_file = open("/root/work/study/ransomware/source.txt", "rb") 
#data = in_file.read() 
#in_file.close()
#print('source content %s from source.txt' %data)
#使用随机字符生成AES相关的参数
    key = get_random_bytes(32)
    iv = get_random_bytes(16)
    data=replay
    cipher1 = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher1.encrypt(pad(data, 16))
    md5get = hashlib.md5(b'abc')
    return
#使用AES.MODE_CBC对data进行加密并赋值给ct

    #print ('encrypted content is %s rewrite to source.txt ' %ct)
#将加密后的数据回写至文件source.txt,得到加密后的source.txt
    out_file = open("/root/work/study/ransomware/source.txt", "wb")
    out_file.write(ct)
    out_file.close()
    #秘钥和向量IV没动过，所以使用秘钥进行解密并解密回target.txt
    cipher2 = AES.new(key, AES.MODE_CBC, iv)
    #解密文件
    pt = unpad(cipher2.decrypt(ct), 16)
    print('decrypt content %s to target.txt' %pt)
    out_file = open("/root/work/study/ransomware/target.txt", "wb") 
    out_file.write(pt)
    out_file.close()