import requests
from api.conf.config import Config
import logging

config = Config()

logging.basicConfig(level=config.logging_level, format='%(asctime)s - %(levelname)s - %(message)s')


class NamesiloApi:
    def __init__(self):
        self.api_key = config.namesilo_api_key
        self.api_url = 'https://www.namesilo.com/api/'

    def get_domain_list(self):
        url = self.api_url + 'listDomains?version=1&type=xml&key=' + self.api_key
        response = requests.get(url)
        logging.info("获取域名列表成功")
        return response.text

    def get_dns_list(self, domain):
        url = self.api_url + 'dnsListRecords?version=1&type=xml&key=' + self.api_key + '&domain=' + domain
        response = requests.get(url)
        logging.info("获取DNS列表成功")
        print(response.text)
        return response.text

    def add_dns_record(self, domain, host, record_type, value, ttl=3600, distance=None):
        if record_type == 'MX' and distance is None:
            distance = 10
        url = self.api_url + 'dnsAddRecord?version=1&type=xml&key=' + self.api_key + '&domain=' + domain + '&rrhost=' + host + '&rrtype=' + record_type + '&rrvalue=' + value + '&rrttl=' + str(
            ttl) + '&rrdistance=' + str(distance)
        response = requests.get(url)
        logging.info(response.text)
        return response.text

    def update_dns_record(self, domain, host, record_id, record_type, value, ttl=3600, distance=None):
        if record_type == 'MX' and distance is None:
            distance = 10
        url = self.api_url + 'dnsUpdateRecord?version=1&type=xml&key=' + self.api_key + '&domain=' + domain + '&rrid=' + str(
            record_id) + '&rrhost=' + host + '&rrtype=' + record_type + '&rrvalue=' + value + '&rrttl=' + str(
            ttl) + '&rrdistance=' + str(distance)
        response = requests.get(url)
        logging.info(response.text)
        return response.text

    def delete_dns_record(self, domain, record_id):
        url = self.api_url + 'dnsDeleteRecord?version=1&type=xml&key=' + self.api_key + '&domain=' + domain + '&rrid=' + str(
            record_id)
        response = requests.get(url)
        logging.info(response.text)
        return response.text


if __name__ == '__main__':
    api = NamesiloApi()
    #api.get_dns_list('yserver.top')
    print(api.get_domain_list())
