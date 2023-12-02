import logging

from api.database import Database
from api.utils import namesilo
from api.utils import xml
from api.sync import sync_db_record, sync_db_domain_record, sync_db_domain_list
from api.conf import config
import re

db = Database()
api = namesilo.NamesiloApi()
config = config.Config()


# 检查是否符合域名记录规范
def check_repeat_domain(host, record_type):
    if re.search(r'[^a-z0-9\-\_\.\@]', host):
        logging.info('输入参数错误')
        return False
    for record_host in db.get_record_by_domain(host):
        if record_host[1] == record_type or record_host[1] == 'CNAME' or record_type == 'CNAME':
            logging.info('与已有记录冲突')
            return False
    return True


def check_record_exist(record_id, username):
    if username == config.admin_name:
        return True
    if db.get_record_by_id(record_id, username):
        return True
    else:
        return False


class User:
    def __init__(self, username, data):
        self.username = username
        self.data = data
        self.domain_list = xml.get_domain_list_xml(api.get_domain_list())
        for domain in self.domain_list:
            if self.data['action'] == 'modify' or self.data['action'] == 'delete' or self.data['action'] == 'deliverDomain':
                self.record_id = self.data['record_id']
                if re.match(".*" + domain, self.data['host']):
                    self.domain = domain
                data['host'] = self.data['host'].split('.' + domain)[0]
        logging.info(self.data)

    def action(self):
        if self.data['action'] == 'add':
            return self.add_record()
        elif self.data['action'] == 'modify':
            return self.modify_record()
        elif self.data['action'] == 'delete':
            return self.delete_record()
        else:
            return '404'

    def add_record(self):
        record_host = self.data['host'] + '.' + self.username + '.' + self.data['domain']
        if not check_repeat_domain(record_host, self.data['type']):
            return '400'
        xml_s = api.add_dns_record(self.data['domain'], self.data['host'] + '.' + self.username, self.data['type'],
                                   self.data['value'],
                                   self.data['ttl'], self.data['mx'])
        status = xml.get_modify_status_xml(xml_s)
        if status == '300':
            record_id = xml.get_record_id_xml(xml_s)
            db.insert_domain_record(self.data['domain'], record_id, record_host, self.data['type'],
                                    self.data['value'], self.data['ttl'], self.data['mx'])
            db.insert_record(record_id, self.username, record_host)
            logging.info('添加成功')
            return '200'
        else:
            logging.info('添加失败')
            return status

    def modify_record(self):
        if not check_record_exist(self.record_id, self.username):
            return '400'
        xml_s = api.update_dns_record(self.domain, self.data['host'], self.record_id, self.data['type'],
                                      self.data['value'], self.data['ttl'], self.data['mx'])
        status = xml.get_modify_status_xml(xml_s)
        if status == '300':
            record_id = xml.get_record_id_xml(xml_s)
            db.modify_domain_record(self.data['value'], self.data['ttl'], self.data['mx'], record_id,
                                    self.record_id)
            logging.info('更新成功')
            return '200'
        else:
            logging.info('更新失败')
            return status

    def delete_record(self):
        if not check_record_exist(self.record_id, self.username):
            return '400'
        status = xml.get_modify_status_xml(api.delete_dns_record(self.domain, self.record_id))
        if status == '300':
            db.delete_domain_record(self.record_id)
            logging.info('删除成功')
            return '200'
        else:
            logging.info('删除失败')
            return status


class Admin(User):

    def action(self):
        if self.data['action'] == 'add':
            return self.add_record()
        elif self.data['action'] == 'modify':
            return self.modify_record()
        elif self.data['action'] == 'delete':
            return self.delete_record()
        elif self.data['action'] == 'modifyUser':
            return self.change_user_status()
        elif self.data['action'] == 'deliverDomain':
            return self.set_record_owner()
        elif self.data['action'] == 'modify_setting':
            return self.modify_setting()
        elif self.data['action'] == 'sync_all':
            return self.sync_all()

    def add_record(self):
        record_host = self.data['host'] + '.' + self.data['domain']
        if not check_repeat_domain(record_host, self.data['type']):
            return '400'
        xml_s = api.add_dns_record(self.data['domain'], self.data['host'], self.data['type'],
                                   self.data['value'],
                                   self.data['ttl'], self.data['mx'])
        status = xml.get_modify_status_xml(xml_s)
        if status == '300':
            record_id = xml.get_record_id_xml(xml_s)
            db.insert_domain_record(self.data['domain'], record_id, record_host, self.data['type'],
                                    self.data['value'], self.data['ttl'], self.data['mx'])
            db.insert_record(record_id, self.username, record_host)
            logging.info('添加成功')
            return '200'
        else:
            logging.info('添加失败')
            return status

    def change_user_status(self):
        if self.data['user'] == config.admin_name:
            logging.info('不能修改管理员状态')
            return '400'
        if self.data['userStatus'] != 'enable' and self.data['userStatus'] != 'disable':
            logging.info('参数错误')
            return '400'
        db.change_user_status(self.data['user'], self.data['userStatus'])
        logging.info('修改成功')
        return '200'

    def set_record_owner(self):
        if self.data['user'] not in db.get_user():
            logging.info('用户不存在')
            return '400'
        db.set_record_owner(self.record_id, self.data['user'])
        logging.info('修改成功')
        return '200'

    def modify_setting(self):
        config.modify_config(self.data)
        logging.info('修改成功')
        return '200'

    def sync_all(self):
        sync_db_domain_list()
        sync_db_domain_record()
        sync_db_record()
        logging.info('同步成功')
        return '200'


if __name__ == '__main__':
    pass
