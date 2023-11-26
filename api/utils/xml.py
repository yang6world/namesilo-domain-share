from xml.dom.minidom import parse
import xml.dom.minidom


def get_domain_list_xml(value):
    domtree = xml.dom.minidom.parseString(value)
    collection = domtree.documentElement
    domains = collection.getElementsByTagName("domain")
    domain_list = []
    for domain in domains:
        domain_list.append(domain.childNodes[0].data)
    return domain_list


def get_dns_list_xml(value):
    domtree = xml.dom.minidom.parseString(value)
    collection = domtree.documentElement
    records = collection.getElementsByTagName("resource_record")
    record_list = []
    for record in records:
        record_dict = {}
        record_dict['record_id'] = record.getElementsByTagName('record_id')[0].childNodes[0].data
        record_dict['host'] = record.getElementsByTagName('host')[0].childNodes[0].data
        record_dict['type'] = record.getElementsByTagName('type')[0].childNodes[0].data
        record_dict['value'] = record.getElementsByTagName('value')[0].childNodes[0].data
        record_dict['ttl'] = record.getElementsByTagName('ttl')[0].childNodes[0].data
        record_dict['distance'] = record.getElementsByTagName('distance')[0].childNodes[0].data
        record_list.append(record_dict)
    return record_list


def get_modify_status_xml(value):
    domtree = xml.dom.minidom.parseString(value)
    collection = domtree.documentElement
    code = collection.getElementsByTagName("code")[0].childNodes[0].data
    return code


def get_record_id_xml(value):
    domtree = xml.dom.minidom.parseString(value)
    collection = domtree.documentElement
    record_id = collection.getElementsByTagName("record_id")[0].childNodes[0].data
    return record_id
