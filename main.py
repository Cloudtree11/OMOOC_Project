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
def index():
    data=request.body.read()
    root=ET.fromstring(data)
    recv_con = {child.tag:child.text for child in root}
    d = recv_con['Content']
    ret_msg = 'error'

    if d.startswith('u '):
        row = None

        try:
            userid=recv_con['FromUserName']
            connection=MySQLdb.connect(host=MYSQL_HOST_M, port=MYSQL_PORT, \
                                       user=MYSQL_USER, passwd=MYSQL_PASS, \
                                       charset="utf8")
            connection.select_db(MYSQL_DB)

            cur = connection.cursor()
            sql_select="""SELECT * FROM user_table WHERE openid='"""+userid+"""'"""
            cur.execute(sql_select)
            row = cur.fetchone()

        except Exception, e:
            ret_msg = 'error: open_mysql_error' + e.__class__.__doc__
            myxml = '''\
            <xml>
            <ToUserName><![CDATA[{}]]></ToUserName>
            <FromUserName><![CDATA[{}]]></FromUserName>
            <CreateTime>12345678</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[{}]]></Content></xml>
            '''.format(recv_con['FromUserName'],recv_con['ToUserName'], ret_msg)
            return myxml
        

        if row is None:
            try:
                sql_insert="""insert into user_table(datetime, username, openid) VALUES (CURRENT_TIMESTAMP,'"""+d[2:]+"""','"""+userid+"""')"""
                cur.execute(sql_insert)

                connection.close()

                ret_msg = '您的用户名已经添加成功啦^_^ '
            except Exception, e:
                ret_msg = 'error: insert_error:' + e.__class__.__doc__
        else:
            ret_msg = '已经有你的名字喽^_^'

        myxml = '''\
        <xml>
        <ToUserName><![CDATA[{}]]></ToUserName>
        <FromUserName><![CDATA[{}]]></FromUserName>
        <CreateTime>12345678</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{}]]></Content></xml>
        '''.format(recv_con['FromUserName'],recv_con['ToUserName'], ret_msg)
        return myxml

    elif d.startswith('b '):
        row = None

        try:
            userid = recv_con['FromUserName']
            connection=MySQLdb.connect(host=MYSQL_HOST_M, port=MYSQL_PORT, \
                                       user=MYSQL_USER, passwd=MYSQL_PASS, \
                                       charset="utf8")
            connection.select_db(MYSQL_DB)

            cur = connection.cursor()
            sql_select="""SELECT * FROM user_table WHERE openid='"""+userid+"""'"""
            cur.execute(sql_select)
            row = cur.fetchone()

        except Exception, e:
            ret_msg = 'error: open_mysql_error' + e.__class__.__doc__
            myxml = '''\
             <xml>
             <ToUserName><![CDATA[{}]]></ToUserName>
             <FromUserName><![CDATA[{}]]></FromUserName>
             <CreateTime>12345678</CreateTime>
             <MsgType><![CDATA[text]]></MsgType>
             <Content><![CDATA[{}]]></Content></xml>
             '''.format(recv_con['FromUserName'],recv_con['ToUserName'], ret_msg)
            return myxml
        

        if row is not None:
            try:
                sql_insert="""insert into book_table(datetime, bookname, username, openid) VALUES (CURRENT_TIMESTAMP,'"""+d[2:]+"""','"""+row[2]+"""','"""+userid+"""')"""
                cur.execute(sql_insert)

                connection.close()
 
                ret_msg = '您的图书已经添加成功啦^_^'
            except Exception, e:
                ret_msg = 'error: insert_error:' + e.__class__.__doc__
        else:
            ret_msg = '要先添加用户名哦^_^'
 
        myxml = '''\
            <xml>
            <ToUserName><![CDATA[{}]]></ToUserName>
            <FromUserName><![CDATA[{}]]></FromUserName>
            <CreateTime>12345678</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[{}]]></Content></xml>
            '''.format(recv_con['FromUserName'],recv_con['ToUserName'], ret_msg)
        return myxml
    
    elif d in ['qu']:
        try:
            connection=MySQLdb.connect(host=MYSQL_HOST_M, port=MYSQL_PORT, \
                                       user=MYSQL_USER, passwd=MYSQL_PASS, \
                                       charset="utf8")
            connection.select_db(MYSQL_DB)

            cur = connection.cursor()

            sql_select = """SELECT * FROM user_table"""
            cur.execute(sql_select)

            ret_msg = ''
            for record in cur.fetchall():
                u=record[2].encode("utf-8")
                ret_msg = ret_msg + u + '\n'
        except Exception, e:
            ret_msg = 'error: insert_error:' + e.__class__.__doc__

        try:
            myxml = '''\
            <xml>
            <ToUserName><![CDATA[{}]]></ToUserName>
            <FromUserName><![CDATA[{}]]></FromUserName>
            <CreateTime>12345678</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[{}]]></Content></xml>
            '''.format(recv_con['FromUserName'],recv_con['ToUserName'], ret_msg)
            return myxml
        except Exception, e:
            ret_msg = ret_msg + e.__class__.__doc__

            myxml = '''\
            <xml>
            <ToUserName><![CDATA[{}]]></ToUserName>
            <FromUserName><![CDATA[{}]]></FromUserName>
            <CreateTime>12345678</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[{}]]></Content></xml>
            '''.format(recv_con['FromUserName'],recv_con['ToUserName'], ret_msg)
            return myxml

    elif d.startswith('qu '):
        try:
            connection=MySQLdb.connect(host=MYSQL_HOST_M, port=MYSQL_PORT, \
                                       user=MYSQL_USER, passwd=MYSQL_PASS, \
                                       charset="utf8")
            connection.select_db(MYSQL_DB)

            cur = connection.cursor()

            sql_select = """SELECT * FROM book_table"""
            cur.execute(sql_select)

            ret_msg = ''
            for record in cur.fetchall():
                if d[3:]==record[3]:
                    u=record[2].encode("utf-8")
                    ret_msg = ret_msg + u + '\n'
        except Exception, e:
            ret_msg = 'error: insert_error:' + e.__class__.__doc__

        try:
            myxml = '''\
            <xml>
            <ToUserName><![CDATA[{}]]></ToUserName>
            <FromUserName><![CDATA[{}]]></FromUserName>
            <CreateTime>12345678</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[{}]]></Content></xml>
            '''.format(recv_con['FromUserName'],recv_con['ToUserName'], ret_msg)
            return myxml
        except Exception, e:
            ret_msg = ret_msg + e.__class__.__doc__

            myxml = '''\
            <xml>
            <ToUserName><![CDATA[{}]]></ToUserName>
            <FromUserName><![CDATA[{}]]></FromUserName>
            <CreateTime>12345678</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[{}]]></Content></xml>
            '''.format(recv_con['FromUserName'],recv_con['ToUserName'], ret_msg)
            return myxml

    elif d in ['qb']:
        try:
            connection=MySQLdb.connect(host=MYSQL_HOST_M, port=MYSQL_PORT, \
                                       user=MYSQL_USER, passwd=MYSQL_PASS, \
                                       charset="utf8")
            connection.select_db(MYSQL_DB)

            cur = connection.cursor()

            sql_select = """SELECT * FROM book_table"""
            cur.execute(sql_select)

            ret_msg = ''
            for record in cur.fetchall():
                u=record[2].encode("utf-8")
                ret_msg = ret_msg + u + '\n'
        except Exception, e:
            ret_msg = 'error: insert_error:' + e.__class__.__doc__

        try:
            myxml = '''\
            <xml>
            <ToUserName><![CDATA[{}]]></ToUserName>
            <FromUserName><![CDATA[{}]]></FromUserName>
            <CreateTime>12345678</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[{}]]></Content></xml>
            '''.format(recv_con['FromUserName'],recv_con['ToUserName'], ret_msg)
            return myxml
        except Exception, e:
            ret_msg = ret_msg + e.__class__.__doc__

            myxml = '''\
            <xml>
            <ToUserName><![CDATA[{}]]></ToUserName>
            <FromUserName><![CDATA[{}]]></FromUserName>
            <CreateTime>12345678</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[{}]]></Content></xml>
            '''.format(recv_con['FromUserName'],recv_con['ToUserName'], ret_msg)
            return myxml
        
    elif d.startswith('qb '):
        try:
            connection=MySQLdb.connect(host=MYSQL_HOST_M, port=MYSQL_PORT, \
                                       user=MYSQL_USER, passwd=MYSQL_PASS, \
                                       charset="utf8")
            connection.select_db(MYSQL_DB)

            cur = connection.cursor()

            sql_select = """SELECT * FROM book_table"""
            cur.execute(sql_select)

            ret_msg = ''
            for record in cur.fetchall():
                if d[3:]==record[2]:
                    u=record[3].encode("utf-8")
                    ret_msg = ret_msg + u + '\n'
        except Exception, e:
            ret_msg = 'error: insert_error:' + e.__class__.__doc__

        try:
            myxml = '''\
            <xml>
            <ToUserName><![CDATA[{}]]></ToUserName>
            <FromUserName><![CDATA[{}]]></FromUserName>
            <CreateTime>12345678</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[{}]]></Content></xml>
            '''.format(recv_con['FromUserName'],recv_con['ToUserName'], ret_msg)
            return myxml
        except Exception, e:
            ret_msg = ret_msg + e.__class__.__doc__

            myxml = '''\
            <xml>
            <ToUserName><![CDATA[{}]]></ToUserName>
            <FromUserName><![CDATA[{}]]></FromUserName>
            <CreateTime>12345678</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[{}]]></Content></xml>
            '''.format(recv_con['FromUserName'],recv_con['ToUserName'], ret_msg)
            return myxml
        
    elif d in ['?', 'h', 'help']:
        helpinfo='''使用信息:
        0 ?|h|help 获取使用信息
        1 u+空格+用户名 记录用户名
        2 qu 查询所有用户
        3 qu+空格+用户名 查询特定用户的所有图书
        4 b+空格+书名 记录书名
        5 qb 查询所有图书
        6 qb+空格+图书名 查询特定图书的所有拥有者
        '''
        myxml = '''\
    <xml>
    <ToUserName><![CDATA[{}]]></ToUserName>
    <FromUserName><![CDATA[{}]]></FromUserName>
    <CreateTime>12345678</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[{}]]></Content></xml>
    '''.format(recv_con['FromUserName'],recv_con['ToUserName'],helpinfo)
        return myxml
    else:
        return None
