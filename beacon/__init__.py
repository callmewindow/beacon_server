import pymysql
pymysql.version_info = (1, 4, 0, "final", 0)
pymysql.install_as_MySQLdb()  # 告诉django用pymysql代替mysqldb连接数据库