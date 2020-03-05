import pymysql

conn = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='root',
    database='petchain',
    autocommit= 'True',
    charset='utf8'
)
cursor = conn.cursor(pymysql.cursors.DictCursor)


def mysql_put_broker(phone, name, introducer, address):
    sql = "insert into broker (phone, name, introducer, address) values(" + '\''+ phone + '\', '+ '\'' + name + '\', '+ '\'' + introducer + '\', '+ '\''+ address + '\''+")"
    
    ret = cursor.execute(sql)
    if ret != 1:
        print ("insert sql error" + ret + sql)
    conn.commit()

def mysql_put_task(taskid, executor, content):

    sql = "insert into task (taskid, executor, content) values(" + '\'' + taskid + '\'' + ', \''+ executor + '\'' + ', \''+content + '\''+")"
    print (sql)
    cursor.execute(sql)
    conn.commit()