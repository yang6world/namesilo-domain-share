import logging

from api.database import Database
from api.utils import namesilo
from api.utils import xml
import re

db = Database()
api = namesilo.NamesiloApi()


class User:
    def __init__(self, username, data):
        self.username = username
        self.data = data
        self.domain_list = xml.get_domain_list_xml(api.get_domain_list())
        for domain in self.domain_list:
            if self.data['action'] != 'add':
                self.record_id = db.get_domain_id(self.data['host'], self.data['type'])

                if re.match(".*" + domain, self.data['host']):
                    self.domain = domain
                data['host'] = self.data['host'].split('.' + domain)[0]
        logging.info(self.data)

    def action(self):
        if self.data['action'] == 'add':
            record_host = self.data['host'] + '.' + self.username + '.' + self.data['domain']
            xml_s = api.add_dns_record(self.data['domain'], self.data['host'] + '.' + self.username, self.data['type'],
                                       self.data['value'],
                                       self.data['ttl'], self.data['mx'])
            status = xml.get_modify_status_xml(xml_s)
            record_id = xml.get_record_id_xml(xml_s)
            if status == '300':
                db.insert_domain_record(self.data['domain'], record_id, record_host, self.data['type'],
                                        self.data['value'], self.data['ttl'], self.data['mx'])
                db.insert_record(record_id, self.username, record_host)
                return '添加成功'
            else:
                return '添加失败'
        if self.data['action'] == 'modify':
            xml_s = api.update_dns_record(self.domain, self.data['host'], self.record_id, self.data['type'],
                                          self.data['value'], self.data['ttl'], self.data['mx'])
            status = xml.get_modify_status_xml(xml_s)
            record_id = xml.get_record_id_xml(xml_s)
            if status == '300':
                db.modify_domain_record(self.data['value'], self.data['ttl'], self.data['mx'], record_id,
                                        self.record_id)
                return '更新成功'
            else:
                return '更新失败'
        if self.data['action'] == 'delete':
            status = xml.get_modify_status_xml(api.delete_dns_record(self.domain, self.record_id))
            if status == '300':
                db.delete_domain_record(self.record_id)
                return '删除成功'
            else:
                return '删除失败'

class Admin:
    def __init__(self, user, data):
        pass


if __name__ == '__main__':
    db.modify_domain_record('')
