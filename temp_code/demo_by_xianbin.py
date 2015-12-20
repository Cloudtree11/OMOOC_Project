# -*- coding:utf-8 -*-
#encoding = utf-8
from bottle import Bottle, get, post, request

import MySQLdb

import sae.const

import hashlib

import xml.etree.ElementTree as ET

MYSQL_DB=sae.const.MYSQL_DB
MYSQL_USER=sae.const.MYSQL_USER
MYSQL_PASS=sae.const.MYSQL_PASS
MYSQL_HOST_M=sae.const.MYSQL_HOST
MYSQL_HOST_S=sae.const.MYSQL_HOST_S
MYSQL_PORT=int(sae.const.MYSQL_PORT)

app=Bottle()

@app.route('/', method=['GET'])
def check_signature():
    signature=request.GET.get('signature',None)
    timestamp=request.GET.get('timestamp',None)
    nonce=request.GET.get('nonce',None)
    echostr=request.GET.get('echostr',None)
    token='shuyou'
    tmplist=[token,timestamp,nonce]
    tmplist.sort()
    tmpstr=''.join(tmplist)
    hashstr=hashlib.sha1(tmpstr).hexdigest()
    if hashstr == signature:
        return echostr
    else:
        return None

@app.route('/',method='POST')
def lib():
    data=request.body.read()
    root=ET.fromstring(data)
    mydict={child.tag:child.text for child in root}
    d=mydict['Content']
    if d.startswith('d '):
        connection=MySQLdb.connection(host=MYSQL_HOST_M, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASS)
        connection.select_db(MYSQL_DB)
        sql_insert="""insert into MYSQL_diary(datetime, content) VALUES (CURRENT_TIMESTAMP,'"""+d[2:]+"""')"""
        connection.query(sql_insert)

    elif d in ['l','list']:
        connection=MySQLdb.connection(host=MYSQL_HOST_M, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASS)
        connection.select_db(MYSQL_DB)
        cursor=connection.cursor()
        cursor.execute('SELECT * FROM MYSQL_diary')
        rows=[item[2] for item in cursor.fetchall()]
        data=''.join(rows)
        myxml = '''\
    <xml>
    <ToUserName><![CDATA[{}]]></ToUserName>
    <FromUserName><![CDATA[{}]]></FromUserName>
    <CreateTime>12345678</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[{}]]></Content></xml>
    '''.format(mydict['FromUserName'],mydict['ToUserName'],data)
        return myxml

    elif d in ['?', 'h', 'help']:
        helpinfo='''usage:
        d+space write and save
        ?|h|help help info.
        l|list reload all historic msg
        '''
        myxml = '''\
    <xml>
    <ToUserName><![CDATA[{}]]></ToUserName>
    <FromUserName><![CDATA[{}]]></FromUserName>
    <CreateTime>12345678</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[{}]]></Content></xml>
    '''.format(mydict['FromUserName'],mydict['ToUserName'],helpinfo)
        return myxml

    #demo-by-xianbin
    elif d.startswith('b '):
        connection=MySQLdb.connection(host=MYSQL_HOST_M, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASS)
        #以字典形式返回数据行
        cursor = connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)    
        connection.select_db(user_table)         
        #查询包含用户ID的行，若该ID已注册，user_table中只存在一行记录符合查询要求              
        cursor.execute("""SELECT username FROM user_table WHERE openid=%s""", (mydict['FromUserName'],)) 
        #返回查询结果（字典形式），其中user_name['username']是该行记录中的username字段的值 
        user_name = cursor.fetchall()
        #用户还没注册，执行if中的代码
        if user_name['username'] == null:
            myxml = '''\
            <xml>
            <ToUserName><![CDATA[{}]]></ToUserName>
            <FromUserName><![CDATA[{}]]></FromUserName>
            <CreateTime>12345678</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[{}]]></Content></xml>
            '''.format(mydict['FromUserName'],mydict['ToUserName'],'''请输入你的用户名，让我们认识你！''')
        #用户已注册，执行else中的代码
        else:
            connection.select_db(book_table)
            #获取用户输入的书名
            book_name = (d.split(' '))[1]
            #在book_table中插入一条新纪录
            cursor.execute("""INSERT INTO book_table(datetime, bookname, username) VALUES (%s,%s,%s)""", (CURRENT_TIMESTAMP, book_name, user_name['username']))
            myxml = '''\
            <xml>
            <ToUserName><![CDATA[{}]]></ToUserName>
            <FromUserName><![CDATA[{}]]></FromUserName>
            <CreateTime>12345678</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[{}]]></Content></xml>
            '''.format(mydict['FromUserName'],mydict['ToUserName'],'''您的图书已添加成功''')

        return myxml
