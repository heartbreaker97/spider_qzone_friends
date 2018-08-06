import urllib
import requests
import json
import re
import threadpool
import time
import operator as op

class Qzone:

    #算出来gtk
    def get_gtk(self):
        p_skey = cookie['p_skey']
        h = 5381
        for i in p_skey:
            h += (h << 5) + ord(i)
            g_tk = h & 2147483647
        return g_tk

    #得到uin
    def get_uin(self):
        uin = cookie['ptui_loginuin']
        return uin


    def write_comment(self,m,qq,name):
        g_tk = self.get_gtk()
        if 'content' not in m.keys():
            return 0
        if m['content'] is None:
            return 0
        # 查看是否有评论
        if ('commentlist' in m.keys()):
            if m['commentlist'] is None:
                return 0
            for comment in m['commentlist']:
                # 计算
                #self.cal_relationship(comment['uin'],name,comment['name'],3)
                #判断共同好友,是的话则写入
                if comment['uin'] in qq_list:
                    file_comment.write(name+'$|$'+comment['name']+'\n')

            # 如果评论大于20条的话需要再进入新的界面，为了写入评论方便，所以在这里写
            # 正常来说说说评论都不超过40条，所以这里写的最多的就是40条了，懒得改了
            if m['cmtnum'] > 20:
                data_more_20 = {
                    'uin': qq,
                    'topicId': str(qq) + '_' + m['tid'],
                    'ftype': 0,
                    'sort': 0,
                    'order': 20,
                    'start': 20,
                    'num': 20,
                    't1_source': 'undefined',
                    'callback': '_preloadCallback',
                    'code_version': 1,
                    'format': 'jsonp',
                    'need_private_comment': 1,
                    'g_tk': g_tk,
                }
                url_more_20 = 'https://h5.qzone.qq.com/proxy/domain/taotao.qzone.qq.com/cgi-bin/emotion_cgi_getcmtreply_v6?'
                url_more_20 += urllib.parse.urlencode(data_more_20)
                res_more_20 = requests.get(url_more_20, headers=header, cookies=cookie)
                # 新的json格式解析,这里返回的json数据又不一样了，需要新的解析
                # print(url_more)
                # 匹配出_Callback之后的内容
                r_more_20 = re.findall('\((.*)\)', res_more_20.text)[0]
                m_more_20 = json.loads(r_more_20)
                # 得到的m_more_20的字典结构 dict_keys(['code', 'data', 'message', 'result', 'right', 'smoothpolicy', 'subcode'])
                data = m_more_20['data']
                if 'comments' not in data.keys():
                    return 0
                for comment in data['comments']:
                    # 判断共同好友,是的话则写入
                    if comment['poster']['id'] in qq_list:
                        file_comment.write(name + '$|$' + comment['poster']['name']+'\n')
            # self.cal_relationship(comment['poster']['id'], name, comment['poster']['name'], 3)'''

    #记录说说
    def write_like(self,m, qq, name):
        g_tk = self.get_gtk()
        uin = self.get_uin()
        global relationships
        url_like = 'https://user.qzone.qq.com/proxy/domain/users.qzone.qq.com/cgi-bin/likes/get_like_list_app?'
        if m['content'] is None:
            return 0
        tid = m['tid']
        # 如果说说是转发的，那么关系网可能会错误，因为得到的点赞列表是源说说的，那么可能会出现A,B都是自己的好友，而A,B他们不是好友，
        # A转发了一天烂大街的说说，然后几经转发后B也看到了，就点赞，误认为AB是好友那么直接跳过点赞
        if 'rt_uin' in m.keys() and 'rt_tid' in m.keys():
            return 0
        data_like = {
            'uin': uin,  # 注意这里的uin是自己的qq
            'unikey': 'http://user.qzone.qq.com/' + str(qq) + '/mood/' + str(tid) + '.1',
            'begin_uin': 0,
            'query_count': 60,
            'if_first_page': 1,
            'g_tk': g_tk
        }
        data_like_encode = urllib.parse.urlencode(data_like)
        url_like += data_like_encode
        res = requests.get(url_like, headers=header, cookies=cookie)

        # 踩坑，这里必须加不然会乱码！！！！çŸ³å®¶åº„å想这样子的乱码！
        res.encoding = 'UTF-8'
        r = re.findall('\((.*)\)', res.text, re.S)[0]
        # 将json数据变成字典格式
        r = json.loads(r)
        if 'data' not in r.keys():
            return 0
        if 'like_uin_info' not in r['data'].keys():
            return 0
        for like in r['data']['like_uin_info']:
            if like['fuin'] in qq_list:
                file_like.write(name + '$|$' + like['nick'] + '\n')

    #找到说说模块
    #pos是当前页面第一个说说的排序，一页20个
    def find_topic(self, qq, name):

        page = 1
        #conti循环的标志，当为false时退出循环
        conti = True
        pos = 0
        g_tk = self.get_gtk()
        uin = self.get_uin()
        while conti:
            #url必须在循环内，每次循环必须重置
            url = 'https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?'
            data = {
                'uin': qq,
                'pos': pos,
                'num': 20,
                'hostUin': uin,
                'replynum': 100,
                'callback': '_preloadCallback',
                'code_version': 1,
                'format': 'jsonp',
                'need_private_comment': 1,
                'g_tk': g_tk,
            }
            #下次翻页
            #下次翻页
            pos += 20
            #构造访问说说页面的HTTP报文内容
            url += urllib.parse.urlencode(data)
            res = requests.get(url,headers=header,cookies=cookie)
            print('读取 '+name+' 的第 '+str(page)+' 页说说成功')
            page += 1
            #匹配出_preloadCallback之后的内容
            if len(re.findall('\((.*)\)', res.text)) == 0:
                记录下没有权限的
                file_denied.write(name + ': ' + str(qq) + '\n')
                continue
            r = re.findall('\((.*)\)', res.text)[0]
            #将json数据变成字典格式
            msg = json.loads(r)

            #如果没有说说就返回
            if 'msglist' not in msg:
                return 0

            #这里爬说说结束，注意和上面的区别，一个是不存在键值，一个是存在键，但值类型为None
            if msg['msglist'] == None:
                print('\n'+name+'的空间无更多说说'+'\n')
                return 0

            #得到的说说相关内容都在msglist(list类型)里面，msglist[i]是字典类型，可利用keys方法查看结构
            #说说内容conlist[0]['con'],另外转发的说说在conlist[1/2/3....]
            #每一条说说就是m
            for m in msg['msglist']:

                #每一条说说下根据点赞计算关系值
                #self.cal_relationship_by_like(m, qq, name)
                #记录共同好友点赞记录
                self.write_like(m, qq, name)

                #如果评论数大于10，则需要点进查看全部评论
                if m['cmtnum'] < 10:
                    ##这里特殊，如果转发了说说并且没有配文字，而且原说说被删了，就会出现错误
                    if m['conlist'] is None:
                        continue
                    self.write_comment(m,qq, name)

                # 如果评论数大于10，则需要点进查看全部评论
                else:
                    data_more = {
                        'uin': qq,
                        'tid': m['tid'],
                        'ftype': 0,
                        'sort': 0,
                        'pos': 0,
                        'num': 20,
                        't1_source': 'undefined',
                        'callback': '_preloadCallback',
                        'code_version': 1,
                        'format': 'jsonp',
                        'need_private_comment': 1,
                        'g_tk': g_tk,
                    }
                    url_more = 'https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msgdetail_v6?'
                    url_more += urllib.parse.urlencode(data_more)
                    res_more = requests.get(url_more, headers=header, cookies=cookie)
                    # print(url_more)
                    # 匹配出_preloadCallback之后的内容
                    r_more = re.findall('\((.*)\)', res_more.text)[0]
                    # print(res_more.text)
                    m_more = json.loads(r_more)
                    # 写入txt文件
                    self.write_comment(m_more, qq, name)


    #得到好友qq
    def get_qq(self):
        qq_list = []
        friend_list = self.get_friend()
        for friend in friend_list:
            qq_list.append(friend[1])
        return qq_list


    #找出好友列表
    def get_friend(self):
        url_friend = 'https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_ship_manager.cgi?'
        g_tk = self.get_gtk()
        uin= self.get_uin()
        data = {
            'uin': uin,
            'do' : 1,
            'g_tk': g_tk
        }
        data_encode = urllib.parse.urlencode(data)
        url_friend += data_encode
        res = requests.get(url_friend, headers = header, cookies = cookie)
        friend_json = re.findall('\((.*)\)',res.text,re.S)[0]
        friend_dict = json.loads(friend_json)
        friend_result_list = []
        #循环将好友的姓名qq号存入字典中
        for friend in friend_dict['data']['items_list']:
            friend_result_list.append([friend['name'],friend['uin']])
        #得到的好友字典是{name: qqNum}格式的
        return friend_result_list

    def get(self, friend_list):
        self.find_topic(friend_list[1], friend_list[0])

    #开始
    def start(self):
        global relationships
        friend_list = self.get_friend()
        pool_size = 15
        pool = threadpool.ThreadPool(pool_size)
        # 创建工作请求，这里他自己会把list分开
        reqs = threadpool.makeRequests(self.get,friend_list)
        # 将工作请求放入队列
        [pool.putRequest(req) for req in reqs]
        # for req in requests:
        #    pool.putRequest(req)
        pool.wait()




if __name__ == '__main__':
    qzone = Qzone()

    #将关系设置为全局变量以供方便调用
    relationships = []
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0",
        "Accepted-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    with open('cookie_dict.txt','r') as f:
        cookie = json.load(f)

    #得到qq列表，
    qq_list = qzone.get_qq()
    # 记录设置空间权限的死鬼
    file_denied = open('denied_list.txt', 'w', encoding='UTF-8')
    #记录共同好友点赞和评论的记录
    file_comment = open('comment.txt','w',encoding='UTF-8')
    file_like = open('like.txt', 'w', encoding='UTF-8')
    qzone.start()
    file_denied.close()
    file_comment.close()
    file_like.close()
