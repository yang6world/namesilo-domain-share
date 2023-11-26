from database.db import Database
from utils import namesilo
import utils.xml as xml

import re


def sync_db_domain_record():
    db = Database()
    api = namesilo.NamesiloApi()
    db.clear_table('domain_record')
    for own_domain in xml.get_domain_list_xml(api.get_domain_list()):
        domains = xml.get_dns_list_xml(api.get_dns_list(own_domain))
        for domain in domains:
            db.insert_domain_record(own_domain, domain['record_id'], domain['host'], domain['type'],
                                    domain['value'], domain['ttl'], domain['distance'])


def sync_db_record():
    db = Database()
    user_list = db.get_user()
    record_list = db.get_all_record()
    db.clear_table('record')
    print(record_list)
    for user in user_list:
        for i, record in record_list.items():
            if re.match(".*" + user, record[1]):
                db.insert_record(record[0], user, record[1])


def sync_db_domain_list():
    db = Database()
    api = namesilo.NamesiloApi()
    db.clear_table('domain_list')
    for domain in xml.get_domain_list_xml(api.get_domain_list()):
        db.insert_domain_list(domain)


if __name__ == '__main__':
    sync_db_domain_record()
    sync_db_record()
    sync_db_domain_list()
