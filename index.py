#coding=utf8
import itchat
import requests
import pickle
from random import choice
import hashlib

#去图灵机器人自己申请一个key
KEY = ''
def getTulingRes(msg):
    print ("getTulingRes {}".format(msg))
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    :  KEY,
        'info'   :  msg,
        'userid' : 'l-wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        return r.get('text')
    except:
        return '你说什么了，系统崩了。。。'
def whatFL(userid):
    print ("whatFL {}".format(userid))
    f = open('contact_list.txt','rb')
    contact = pickle.load(f)
    f.close()
    if contact and (userid in contact.keys()):
        print ("lunch all {}".format(contact[userid]))
        return choice(contact[userid])
    else:
        return '请输入用以下格式输入新增食物 eg：新增食物 肉夹馍-炸酱面-麻辣烫'
def setFood(userid,msg):
    print ("whatFL {} {}".format(userid,msg))
    foods = msg.split('-')
    try:
        f = open('contact_list.txt','rb')
        contact = pickle.load(f)
    except EOFError:
        contact = {}
    f.close()
    f = open('contact_list.txt','wb')  
    if userid in contact.keys():
        userData = contact[userid]
    else:
        userData = []
    newlists = list(set(userData+foods))
    contact[userid] = newlists
    pickle.dump(contact,f)
    f.close()
    return "设置成功"

@itchat.msg_register([itchat.content.TEXT,itchat.content.PICTURE,itchat.content.RECORDING])
def print_content(msg):
    if msg['FromUserName'] == '@': 
        print ("本人")
        return
    if msg['Type'] == 'Text':
        userid = 'key'+ msg['FromUserName']
        print ("userid: {}".format(userid))
        try:
            if msg['Text'] == '今天吃什么':
                itchat.send(whatFL(userid),msg['FromUserName'])
            elif msg['Text'].find('新增食物')> -1 :
                itchat.send(setFood(userid,msg['Text'].replace('新增食物',''.strip())),msg['FromUserName'])
            else:
                itchat.send(getTulingRes(msg['Text']),msg['FromUserName'])
        except:
            itchat.send("你说了什么，系统崩掉了",msg['FromUserName'])
    else:
        itchat.send("不识别该种消息类型。。。",msg['FromUserName'])

itchat.auto_login(hotReload=True)
itchat.run()
