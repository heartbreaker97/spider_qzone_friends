import operator as op
class CalRelationship:
    #得到txt文件内容
    def get_content(self,txtfile):
        file = open(txtfile, encoding='UTF-8')
        content = file.read()
        file.close()
        return content

    #计算关系值的基础方法
    def cal_relationship(self,name1,name2,value):
        global relationships

        # 设置两个好友同时是否存在于三元组的标志
        flag = False

        for relationship in relationships:
            # 如果两个人都在那么改变其关系值，并改变标记值
            if name1 in relationship and name2 in relationship:
                #存储关系图在三元组 [ [name1,name2,value], [name3,name4,vaule]....]
                relationship[2] += value
                flag = True
        # 如果两好友中一者或都不在三元组内，那么添加
        if flag == False and op.eq(name1, name2) == False:
            # 第一次进去就有个初值
            relationships.append([name1, name2, value])


    #通过评论和点赞计算关系值
    def cal_relationship_by_data(self,datas,value):
        count = 0
        data_list = datas.split('\n')
        for element in data_list:
            count += 1
            data = element.split('$|$')
            #最后一个是空
            if data[0] == '':
                return 0
            self.cal_relationship(data[0],data[1],value)
            print('已经分析了 '+ str(count)+' 行数据')


    #开始入口
    def start(self):

        comments = self.get_content('../comment.txt')
        likes = self.get_content('../like.txt')
        #开始计算
        #评论好友关系+3,点赞好友关系+1
        self.cal_relationship_by_data(comments,3)
        self.cal_relationship_by_data(likes,1)

if __name__ == '__main__':
    # 将关系设置为全局变量以供方便调用
    relationships = []
    cal = CalRelationship()
    cal.start()
    #将计算好的关系值写入txt
    file = open('relationship.txt', 'w', encoding='UTF-8')
    for relationship in relationships:
        file.write(relationship[0] + '$|$' + relationship[1] + '$|$' + str(relationship[2]) + '\n')
    file.close()

