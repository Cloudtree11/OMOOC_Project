    #demo-by-xianbin
    elif d.startswith('b '):
        try:
            connection=MySQLdb.connection(host=MYSQL_HOST_M, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASS)
            #以字典形式返回数据行
            cursor = connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)    
            connection.select_db(user_table)         
            #查询包含用户ID的行，若该ID已注册，user_table中只存在一行记录符合查询要求              
            cursor.execute("SELECT username FROM user_table WHERE openid=%s", (mydict['FromUserName'],)) 
            #返回查询结果（字典形式），其中user_name['username']是该行记录中的username字段的值 
            user_name = cursor.fetchone()
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
                cursor.execute("INSERT INTO book_table(datetime, bookname, username) VALUES (%s,%s,%s)", (CURRENT_TIMESTAMP, book_name, user_name['username']))
                myxml = '''\
                <xml>
                <ToUserName><![CDATA[{}]]></ToUserName>
                <FromUserName><![CDATA[{}]]></FromUserName>
                <CreateTime>12345678</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[{}]]></Content></xml>
                '''.format(mydict['FromUserName'],mydict['ToUserName'],'''您的图书已添加成功''')
            return myxml

        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0],e.args[1])
            myxml = '''\
            <xml>
            <ToUserName><![CDATA[{}]]></ToUserName>
            <FromUserName><![CDATA[{}]]></FromUserName>
            <CreateTime>12345678</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[{}]]></Content></xml>
            '''.format(mydict['FromUserName'],mydict['ToUserName'],'''系统错误''')
            return myxml

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
