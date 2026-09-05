import pymysql
import os
try:
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password=os.environ.get('MYSQL_ROOT_PASSWORD', 'your_password'),
                                 database='tcm_health')
    print("连接成功！")
    connection.close()
except Exception as e:
    print(f"连接失败：{e}")