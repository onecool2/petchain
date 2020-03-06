# -*- coding: utf-8 -*-
import random
import time
import os
import shutil
import json
import requests


##########################  WeChatDownLoadDecoder  #####################################
import re

class WechatImageDecoder:
    def __init__(self, dat_file):
        dat_file = dat_file.lower()

        decoder = self._match_decoder(dat_file)
        decoder(dat_file)
        
    def get_image_file(self):
        return self.img_file

    def _match_decoder(self, dat_file):
        decoders = {
            r'.+\.dat$': self._decode_pc_dat,
            r'cache\.data\.\d+$': self._decode_android_dat,
            None: self._decode_unknown_dat,
        }

        for k, v in decoders.items():
            if k is not None and re.match(k, dat_file):
                return v
        return decoders[None]

    def _decode_pc_dat(self, dat_file):
        
        def do_magic(header_code, buf):
            return header_code ^ list(buf)[0] if buf else 0x00
        
        def decode(magic, buf):
            return bytearray([b ^ magic for b in list(buf)])
            
        def guess_encoding(buf):
            headers = {
                'jpg': (0xff, 0xd8),
                'png': (0x89, 0x50),
                'gif': (0x47, 0x49),
            }
            for encoding in headers:
                header_code, check_code = headers[encoding] 
                magic = do_magic(header_code, buf)
                _, code = decode(magic, buf[:2])
                if check_code == code:
                    return (encoding, magic)
            print('Decode failed')
            sys.exit(1) 
        
        with open(dat_file, 'rb') as f:
            buf = bytearray(f.read())
        file_type, magic = guess_encoding(buf)

        self.img_file = re.sub(r'.dat$', '.' + file_type, dat_file)
        with open(self.img_file, 'wb') as f:
            new_buf = decode(magic, buf)
            f.write(new_buf)
        print ("000000000000" + self.img_file)
        
    def _decode_android_dat(self, dat_file):
        with open(dat_file, 'rb') as f:
            buf = f.read()

        last_index = 0
        for i, m in enumerate(re.finditer(b'\xff\xd8\xff\xe0\x00\x10\x4a\x46', buf)):
            if m.start() == 0:
                continue

            imgfile = '%s_%d.jpg' % (dat_file, i)
            with open(imgfile, 'wb') as f:
                f.write(buf[last_index: m.start()])
            last_index = m.start()

    def _decode_unknown_dat(self, dat_file):
        raise Exception('Unknown file type')

###############################################################
inittext = [\
    '最近很忙吗？', \
    '吃了没呀？', \
    '你是不是很忙啊？', \
    '要不要一起去看电影？', \
    '我爱北京天安门' , \
    '今天天气好热啊！', \
]

exceptid = ['newsapp', \
"weixin", \
"qqmail", \
"filehelper", \
"fmessage", \
"tmessage", \
"qmessage", \
"lbsapp", \
"qqsync", \
"floatbottle", \
"shakeapp", \
"medianote", \
"newsapp", \
"weibo", \
"weixinguanhaozhushou", \
"feedsapp", \
"qqsafe", \
"mphelper", \
"cmb4008205555", \
"meituanwx"]

replytime = random.randint(1000, 2000)



message_dict={}
DATA_DIR = "C:\\Users\\Public\\nfs\\data\\langan"
BLOCKCHAIN_SERVER = "39.99.225.124"

HELLO_WORDS = "老师您好！我是公证员，负责把咱们的有效信息上传到区块链上。群里另一位是宠医助手，您有任何问题都可以随时联系她！"

#系统io操作函数
#------------------------------------------------------------------------------------------- 
def modify_path(path):
    return "\"" + path + "\""
    #return path.replace('WeChat Files', '\"WeChat Files\"')
    
def wait_exist(file):
    while os.path.exists(file) is False:
        print("wait file exist:" + file)
        time.sleep(0.3)
    time.sleep(3)   #等三秒是为了等待文件即使存在，可能正在被写入的情况，没有写完。TODO 应该判断两次间隔时间的文件大小    
    
def mkdir(path):
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print (path + '创建成功')
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print (path + '目录已存在')
        
def get_type(a):
    if isinstance(a, str):       # 判断是否为字符串类型
        print("It's str.")
    elif isinstance(a, list):     # 判断是否为列表
        print("It's list.")
    elif isinstance(a, tuple):     # 判断是否为元组
        print("It's tuple.")
    elif isinstance(a, dict):     # 判断是否为字典
        print("It's dict.")
    elif isinstance(a, set):     # 判断是否为集合
        print("It's set.")

#message相关操作函数
#------------------------------------------------------------------------------------------- 
def put_message_dict(room_wxid, message):
    print ("@@@@@@@@@@@@@@@@@@", room_wxid, message)
    message_dict.setdefault(room_wxid,{})['message'] = message
   
def get_message_dict(room_wxid):
    return message_dict[room_wxid]['message']

def clear_message_dict(room_wxid):
    message_dict.setdefault(room_wxid,{})['message'] = ""
    
#------------------------------------------------------------------------------------------- 
#保存附件操作函数 
def get_object_dir(msg):
    action = msg["action"]
    dir = ""
    if action == 'reportPicMessage':
        dir = msg["data"]["msg"]["fileIndex"]
    elif action == 'reportVideoMessage':
        dir = msg["data"]["msg"]["videoIndex"]
    elif action == 'reportVoiceMessage':
        dir = msg["data"]["msg"]["voiceIndex"]
    return  dir 
    
def save_text_file(FileDir, text):
    print ("text *********" + text)
    print ("FileDir *********" + FileDir)
    
    target_file = time.strftime("%H-%M-%S", time.localtime()) + ".txt"
    with open(FileDir + target_file, 'wt') as f:
        f.write(text)
    
    return target_file # 返回的是文件名，没有路径，如果需要返回文件所在本机完整路径，返回target_file 
    
def save_video_file(FileDir, object_dir):
    print ("source file *********" + object_dir)
    print ("targer file *********" + FileDir)
    wait_exist(object_dir)
    file_name = object_dir.split('\\'); 
    target_file = FileDir + file_name[-1]
    shutil.copyfile(object_dir, target_file)
    return file_name[-1] # 返回的是文件名，没有路径，如果需要返回文件所在本机完整路径，返回target_file 
    
def save_voice_file(FileDir, object_dir):
    print ("source file *********" + object_dir)
    print ("target dir *********" + FileDir)
    wait_exist(object_dir)
    
    object_dir = modify_path(object_dir)  #增加”“给 WeChat Files => "WeChat Files"
    file_name = object_dir.split('\\')    # 取文件名
    file_name_without_suffix = file_name[-1].split('.') #取没有扩展名的文件名  
    target_file = FileDir + file_name_without_suffix[0] + ".wav" #组合新的目标文件名，换成目标路径+源文件名+wav
    cmd = "QQSlk2Wav.exe " + object_dir + " " + target_file + " -quiet"
    print(cmd)
    os.system(cmd)
    #shutil.copyfile(object_dir, target_file)
    return file_name_without_suffix[0] + ".wav" # 返回的是文件名，没有路径，如果需要返回文件所在本机完整路径，返回target_file    
    
def save_pic_file(FileDir, object_dir):
    print ("source file *********" + object_dir)
    print ("targer file *********" + FileDir)
    #object_dir = 'c:\\users\\administrator\\documents\\wechat files\\wangrui_rw24\\filestorage\\image\\2020-02\\cf22f99ce154ac10be6682e3b3f8bc1a.dat'
   
    wait_exist(object_dir)
    wechatimage = WechatImageDecoder(object_dir)
    new_file = wechatimage.get_image_file()
    file_name = new_file.split('\\'); 
    target_file = FileDir + file_name[-1]
    print ("targer file *********" + target_file)
    
    shutil.copyfile(new_file, target_file)
    return file_name[-1] # 返回的是文件名，没有路径，如果需要返回文件所在本机完整路径，返回target_file
    
#区块链相关函数
def user_to_blockchain_put_broker(json_data):
    print ("user_to_blockchain broker:")
    print(json.dumps(json_data, sort_keys=True, indent=4, separators=(', ', ': ')))
    r = requests.post("http://" + BLOCKCHAIN_SERVER + ":6666/put_broker", json=json_data)
    return r;
    
def user_to_blockchain_put_task(json_data):
    print ("user_to_blockchain task:")
    print(json.dumps(json_data, sort_keys=True, indent=4, separators=(', ', ': ')))
    r = requests.post("http://" + BLOCKCHAIN_SERVER + ":6666/put_task", json=json_data)
    return r;
    
def user_to_blockchain_put_media(json_data):
    print ("user_to_blockchain media:")
    print(json.dumps(json_data, sort_keys=True, indent=4, separators=(', ', ': ')))
    r = requests.post("http://" + BLOCKCHAIN_SERVER + ":6666/put_task", json=json_data)
    return r;

#回答的任务相关函数
task_dic={}
def get_user_task(user_id):
    #current_time = time.strftime("%Y-%m-%d", time.localtime())
    
    task_id = ""
    
    if user_id in task_dic:
        task_id = task_dic[user_id]['Task_id']
    print ("get task***************************", task_id, user_id)
    return task_id

def set_user_task(user_id, task_id):
    print ("set task========================", task_id, user_id)
    task_dic.setdefault(user_id,{})['Task_id'] = task_id
    return task_id
'''
def update_user_dic(task_id, user_id, message):
    user_dic.setdefault(user_id,{})['Task_id'] = task_id
    user_dic.setdefault(user_id,{})['Message'] = message
'''
#-------------------------------------------------------------------------------------------    
#消息操作函数
def get_msg_sender(msg):
    sender = msg["data"]["msg"]["nick"]
    print ("nick:" + sender)
    return sender

def get_msg_sender_wxid(msg):
    wxid = msg["data"]["msg"]["wxidFrom"]
    print ("wxid:" + wxid)
    return wxid
    
def get_msg_data(request_json):
    return request_json["data"]

def get_msg_action(msg_data):
    if "action" in msg_data.keys():
        return msg_data["action"]
    return "error"

def get_text_content(msg):
    action = msg["action"]
    if action == 'reportTextMessage':
        text = msg["data"]["msg"]["message"]
    return text
    
#-------------------------------------------------------------------------------------------    
#群操作函数
room_dict={}        #保存群的字典+列表结构

def contract_init():    #初始化群
    if not bool(room_dict):
        return 1
    return 0
    
def get_room_name(msg):
    room_wxid = msg["data"]["msg"]["roomWxid"]
    if room_wxid == "":      #如果没有room_wxid，说明不是群信息，跳过下面的更新
        return ""
    room_name = ""
    if room_wxid in room_dict:          #找到了，说明是已经存在的群
        room_name = room_dict[room_wxid]["nick"]
        print("get_room_name:" + room_name)
    else:
        update_room_dict_wxid(room_wxid)
        room_name =room_wxid
    return room_name

def get_room_wxid(msg):
    room_wxid = msg["data"]["msg"]["roomWxid"]
    if room_wxid in room_dict:          #找到了，说明是已经存在的群
        room_wxid = room_dict[room_wxid]["wxid"]
        print("get_room_wxid:" + room_wxid)
    return room_wxid
    
def get_room_wxid_by_nick(nick):    #获得群nick对应的wxid
    for k in room_dict: 
        print("room_wxid:" + k + "nick:" + room_dict[k]["nick"])
        if nick in room_dict[k]["nick"]:
            return room_dict[k]["wxid"]
    print("Can not find wxid by nick:" + nick)
    return ""

def get_all_room_nick_list(nick):   #获得群nick开头的所有群list
    print ("8888888888888888888888888888888888", nick)
    room_list = []
    for k in room_dict: 
        #print (k, room_dict[k])
        if nick in room_dict[k]["nick"]:
            print ("群名：%s   值：%s" % (room_dict[k]["nick"], room_dict[k]))
            room_list.append(room_dict[k]["nick"])
    return room_list 

def print_room_dict():
    room_list = []
    for k in  room_dict: 
        #print (k, room_dict[k])
        print ("群名：%s   值：%s" % (room_dict[k]["nick"], room_dict[k]))
        room_list.append(room_dict[k])
    return room_list
         
def update_room_dict(groupList):            #收到reportContact事件后调用的，可能在开始会被调用n次，因为微信端返回的慢，轮询的快
    for i in range(len(groupList)):
        #print ("序号：%s   值：%s" % (i + 1, groupList[i]))
        wxid = groupList[i]["wxid"]
 
        if "nick" in groupList[i]:
            room_dict.setdefault(wxid,{})['wxid'] = groupList[i]["wxid"]
            room_dict.setdefault(wxid,{})['nick'] = groupList[i]["nick"]
            room_dict.setdefault(wxid,{})['owner'] = groupList[i]["owner"]
            room_dict.setdefault(wxid,{})['userList'] = groupList[i]["userLists"]    #群成员的wxid列表
    print_room_dict()

def update_room_dict_wxid(wxid):            #收到新的信息后，如果群不存在则调用增加新的群到room_dict里
    room_dict.setdefault(wxid,{})['wxid'] = wxid
    room_dict.setdefault(wxid,{})['nick'] = wxid
    print_room_dict()
    
def update_room_dict_nick(wxid, nick):            #调用改名事件后，更新新的群昵称
    room_dict.setdefault(wxid,{})['wxid'] = wxid
    room_dict.setdefault(wxid,{})['nick'] = nick
    print_room_dict()

def process_ChatroomMessage_msg_data(msg_data):     #上报群相关系统消息
    message = msg_data["data"]["msg"]["message"]
    print ("得到了一个群系统消息:" + message)
    reply_msg = ""
    if "加入了群聊" in message:
        n = message.rfind('\"')
        k = message[:n].rfind('\"') +1
        new_people = message[k:n]
        reply_msg = new_people + HELLO_WORDS
    elif "修改群名为" in message:
        msg_array = message.split("修改群名为")
        room_name = msg_array[1]
        if "“" in room_name:
            room_name = room_name[1:-1]
        room_wxid = msg_data["data"]["msg"]["roomWxid"]
        update_room_dict_nick(room_wxid, room_name)
    return reply_msg, get_room_wxid(msg_data) 
