# spider_qzone_friends
# qq空间爬虫生成好友关系网
使用方法：

1.将cookie.py按照提示修改后运行，生成cookie

2.运行spider.py爬取数据并初步分析将结果生成txt文件保存至本地

3.将show_relation中的relation.php按照其中提示修改第二部得到的txt文件的路径，再将整文件夹放置本地搭建的web服务器下，并在http://echarts.baidu.com/download.html下载echarts插件，放在该文件夹下在浏览器上打开relation.php

爬取数据和分析数据同时进行，分析数据的算法有待改善，效率太慢，代码还在持续修改中
