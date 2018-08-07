# spider_qzone_friends
# qq空间爬虫生成好友关系网
使用方法：

1.将cookie.py的chromedriver的地址修改成自己的（设置了环境变量的可不设置），账号密码按照提示修改后运行，生成cookie

2.运行spider.py爬取数据并初步分析将结果生成txt文件保存至本地

3.运行show_relation下的analysis.py，得到好友关系值文件

4.将show_relation中的relation.php按照其中提示修改第三步得到的txt文件的路径，再将整文件夹放置本地搭建的web服务器下，并在http://echarts.baidu.com/download.html 下载echarts插件，放在该文件夹下在浏览器上打开relation.php

爬虫太慢，代码还在持续修改重构中，针对没有搭建本地web服务器的显示结果
