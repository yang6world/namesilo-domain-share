from api.database.db import Database
from api.utils import namesilo
from api.utils import xml
from api.conf import config


import re

config = config.Config()

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
    db.clear_table('record WHERE add_user = "system"')
    for user in user_list:
        for i, record in record_list.items():
            if re.match(".*" + user, record[1]) and record[1] not in db.get_admin_record():
                db.insert_record(record[0], user, record[1])
    for i, record in record_list.items():
        if record[1] not in db.get_record_domain():
            db.insert_record(record[0], config.admin_name, record[1])


def sync_db_domain_list():
    db = Database()
    api = namesilo.NamesiloApi()
    db.clear_table('domain_list')
    for domain in xml.get_domain_list_xml(api.get_domain_list()):
        db.insert_domain_list(domain)


if __name__ == '__main__':
    #sync_db_domain_record()
    sync_db_record()
    #sync_db_domain_list()
