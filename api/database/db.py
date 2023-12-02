import sqlite3
import os

file_path = os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data'),
                         'database.db')


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(file_path, check_same_thread=False)

    # 初始化数据库
    def init_tables(self):
        sql_user = '''
        CREATE TABLE IF NOT EXISTS user 
        (
            id VARCHAR(64) PRIMARY KEY,
            username VARCHAR(64) NOT NULL,
            email VARCHAR(64) NOT NULL,
            role VARCHAR(64) NOT NULL DEFAULT 'user',
            last_login_time DATETIME,
            status VARCHAR(64) NOT NULL DEFAULT 'enable' 
        )
        '''
        self.conn.execute(sql_user)
        self.conn.commit()
        sql_domain = '''
        CREATE TABLE IF NOT EXISTS domain_record
        (
            domain VARCHAR(64) NOT NULL,
            record_id VARCHAR(64) PRIMARY KEY,
            host VARCHAR(64) NOT NULL ,
            type VARCHAR(64) NOT NULL,
            value VARCHAR(64) NOT NULL,
            ttl VARCHAR(64) NOT NULL,
            distance VARCHAR(64) NOT NULL
            )
        '''
        self.conn.execute(sql_domain)
        self.conn.commit()
        sql_record = '''
        CREATE TABLE IF NOT EXISTS record
        (
            record_id VARCHAR(64) UNIQUE,
            id VARCHAR(64),
            host VARCHAR(64),
            add_user VARCHAR(64) DEFAULT 'system',
            record_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (record_id) REFERENCES domain_record(record_id) ON DELETE CASCADE ON UPDATE CASCADE
        )
        '''
        self.conn.execute(sql_record)
        sql_domain_list = '''
        CREATE TABLE IF NOT EXISTS domain_list
        (
            domain VARCHAR(64) PRIMARY KEY,
            record_time DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        '''
        self.conn.execute(sql_domain_list)
        self.conn.commit()

    # 对域名列表进行操作
    def insert_domain_record(self, domain, record_id, host, type, value, ttl, distance):
        sql = '''
        INSERT INTO domain_record (domain, record_id, host, type, value, ttl, distance) VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        self.conn.execute(sql, (domain, record_id, host, type, value, ttl, distance))
        self.conn.commit()


    def modify_domain_record(self, value, ttl, distance, record_id, old_record_id):
        sql = '''
        UPDATE domain_record SET value = ?, ttl = ?, distance = ?, record_id =? WHERE record_id = ?
        '''
        self.conn.execute(sql, (value, ttl, distance, record_id, old_record_id))
        self.conn.commit()

    def clear_table(self, tb_name):
        sql = f'''
        DELETE FROM {tb_name}
        '''
        self.conn.execute(sql)
        self.conn.commit()

    # 对用户列表进行操作
    def add_user(self, id, username, email, role='user'):
        sql = '''
        INSERT INTO user (id, username, email, role) VALUES (?, ?, ?, ?)
        '''
        self.conn.execute(sql, (id, username, email, role))
        self.conn.commit()

    def record_login_time(self, id):
        sql = '''
        UPDATE user SET last_login_time = CURRENT_TIMESTAMP WHERE id = ?
        '''
        self.conn.execute(sql, (id,))
        self.conn.commit()

    def get_user(self):
        sql = '''
        SELECT id FROM user 
        '''
        cursor = self.conn.execute(sql)
        user_lists = cursor.fetchall()
        user_list = []
        for user in user_lists:
            user_list.append(user[0])
        return user_list

    def change_user_status(self, id, status):
        sql = '''
        UPDATE user SET status = ? WHERE id = ?
        '''
        self.conn.execute(sql, (status, id))
        self.conn.commit()

    def get_all_user(self):
        sql = '''
        SELECT id, username, email, role, last_login_time, status FROM user
        '''
        cursor = self.conn.execute(sql)
        user_lists = cursor.fetchall()
        user_dict = {}
        for i, user in enumerate(user_lists, 1):
            user_dict[i] = user
        return user_dict

    def get_disabled_user(self):
        sql = '''
        SELECT id FROM user WHERE status = 'disable'
        '''
        cursor = self.conn.execute(sql)
        user_lists = cursor.fetchall()
        user_list = []
        for user in user_lists:
            user_list.append(user[0])
        return user_list


    # 对域名-用户关系表进行操作
    def insert_record(self, record_id, id, host):
        sql = '''
        INSERT INTO record (record_id, id, host) VALUES (?, ?, ?)
        '''
        self.conn.execute(sql, (record_id, id, host))
        self.conn.commit()

    def get_all_record(self):
        sql = '''
        SELECT record_id, host, type, value, ttl, distance 
        FROM domain_record
        '''
        cursor = self.conn.execute(sql)
        record_list = cursor.fetchall()
        data_dist = {}
        for i, record in enumerate(record_list, 1):
            data_dist[i] = record
        return data_dist

    def get_record(self, uid):
        sql = '''
        SELECT record_id, host, type, value, ttl, distance 
        FROM domain_record
        WHERE host IN (SELECT host FROM record WHERE id = ?)
        '''
        cursor = self.conn.execute(sql, (uid,))
        record_list = cursor.fetchall()
        data_dist = {}
        for i, record in enumerate(record_list, 1):
            data_dist[i] = record
        return data_dist

    def get_record_domain(self):
        sql = '''
        SELECT host
        FROM record
        '''
        cursor = self.conn.execute(sql)
        record_list = cursor.fetchall()
        data_list = []
        for record in record_list:
            data_list.append(record[0])
        return data_list

    def get_record_by_domain(self, domain):
        sql = '''
        SELECT host, type FROM domain_record WHERE host = ?
        '''
        cursor = self.conn.execute(sql, (domain,))
        record_list = cursor.fetchall()
        data_list = []
        return record_list

    def get_admin_record(self):
        sql = '''
        SELECT host FROM record WHERE add_user = 'admin'
        '''
        cursor = self.conn.execute(sql)
        record_list = cursor.fetchall()
        data_list = []
        for record in record_list:
            data_list.append(record[0])
        return data_list

    def set_record_owner(self, record_id, id, add_user='admin'):
        sql = '''
        UPDATE record SET id = ?, add_user = ? WHERE record_id = ?
        '''
        self.conn.execute(sql, (id, add_user, record_id))
        self.conn.commit()

    def get_record_by_id(self, record_id, username):
        sql = '''
        SELECT host FROM record WHERE record_id = ? AND id = ?
        '''
        cursor = self.conn.execute(sql, (record_id, username))
        record_list = cursor.fetchone()
        return record_list

    # 删除用户-域名关系并清除记录
    def delete_domain_record(self, record_id):
        sql = '''
        DELETE FROM domain_record WHERE record_id = ?
        '''
        self.conn.execute(sql, (record_id,))
        sql = '''
        DELETE FROM record WHERE record_id = ?
        '''
        self.conn.execute(sql, (record_id,))
        self.conn.commit()

    # 对域名列表进行操作
    def get_domain(self):
        sql = '''
        SELECT domain FROM domain_list
        '''
        cursor = self.conn.execute(sql)
        domain_list = cursor.fetchall()
        data_dist = {}
        for i, domain in enumerate(domain_list, 1):
            data_dist[i] = domain[0]
        return data_dist

    def insert_domain_list(self, domain):
        sql = '''
        INSERT INTO domain_list (domain) VALUES (?)
        '''
        self.conn.execute(sql, (domain,))
        self.conn.commit()


if __name__ == '__main__':
    db = Database()
    #db.set_record_owner('e3c1482d5ead908bd6155a143fc0ab33', 'yzr')
    # print(db.get_domain_id('blog.yserver.top', 'A'))
