import pymysql
from faker import Faker
import random

# 数据库配置，从你的 DATABASES 中提取
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'db': 'postal_savings',
    'port': 3306,
    'charset': 'utf8mb4'
}

# 初始化 Faker
fake = Faker()

# 连接数据库
conn = pymysql.connect(**DB_CONFIG)
cursor = conn.cursor()

# 确保表存在（如果不存在则创建）
create_table_query = """
CREATE TABLE IF NOT EXISTS `books` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `author` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
"""
cursor.execute(create_table_query)

# 插入数据的 SQL
insert_query = "INSERT INTO books (title, author) VALUES (%s, %s)"

# 生成 5000 条数据
data_count = 5000
books_data = []

for _ in range(data_count):
    # 生成随机书名和作者名，确保不超过 100 字符
    title = fake.sentence(nb_words=4)[:-1][:100]  # 截取前 100 字符
    author = fake.name()[:100]  # 截取前 100 字符
    books_data.append((title, author))

try:
    # 批量插入数据
    cursor.executemany(insert_query, books_data)
    # 提交事务
    conn.commit()
    print(f"成功插入 {data_count} 条数据！")
except Exception as e:
    # 如果出错，回滚事务
    conn.rollback()
    print(f"插入数据失败：{e}")
finally:
    # 关闭游标和连接
    cursor.close()
    conn.close()