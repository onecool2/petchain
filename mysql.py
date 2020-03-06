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

def mysql_list_task(executor, task_id):
    sql = "select * from task where taskid='%s' and executor='%s'" %(task_id, executor)
    print (sql)
    task_list = ""
    ret = cursor.execute(sql)
    result = cursor.fetchall()
    for k in result:
        task_list = task_list + "\n"+ "%s %s %s %s %s %d %s " %(k["taskid"], k["content"], k["executor"],k["reviewer"], k["summary"] ,k["score"], k["feedback_media"])
        #print ("nick:", k['nick'], "point:", k["point"], 'rank:', k["rank"])
    return task_list
    
def mysql_score_task(executor, task_id, score, summary):
    #update task set score=20, summary='123' where taskid=123468 and executor='lzz12347'
    sql = "update task set score=%s, summary='%s' where taskid='%s' and executor='%s'" %(score, summary, task_id, executor)
    print ("SQL:", sql)
    cursor.execute(sql)
    conn.commit()
    return mysql_list_task(executor, task_id)
    
def mysql_put_task_feedback_media(taskid, executor, feedback_media):
    sql = "select feedback_media from task where taskid='%s' and executor='%s'" %(taskid, executor)
    print ("SQL:", sql)
    ret = cursor.execute(sql)
    if ret > 1:
        return "结果不止一个，应该仅匹配一个"
        print("结果不止一个，应该仅匹配一个")
    elif ret < 1:
        print("没有找到匹配记录")
        return "没有找到匹配记录"
    else: 
        result = cursor.fetchone()
        print("result", result)
        print ("result:", result['feedback_media'])
        new_feedback_media = feedback_media + " "+ result["feedback_media"]
        sql = "update task set feedback_media='%s' where taskid='%s' and executor='%s'" %(new_feedback_media, taskid, executor)
        print ("SQL:", sql)
        cursor.execute(sql)
        conn.commit()