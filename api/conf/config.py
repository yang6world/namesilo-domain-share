import logging
import os
import yaml
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# 读取配置文件
class Config:
    def __init__(self):
        self.file_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
        # 通过读取环境变量获取或从config。yaml中获取
        self.namesilo_api_key = os.getenv('NAMESILO_API_KEY') or self.get_yaml_config('namesilo_api_key')
        self.admin_name = os.getenv('ADMIN_NAME') or self.get_yaml_config('admin_name')
        self.logging_level = os.getenv('LOGGING_LEVEL') or self.get_yaml_config('log_level')
        # OAuth2.0
        self.client_id = os.getenv('CLIENT_ID') or self.get_yaml_config('client_id')
        self.client_secret = os.getenv('CLIENT_SECRET') or self.get_yaml_config('client_secret')
        self.redirect_uri = os.getenv('REDIRECT_URI') or self.get_yaml_config('redirect_uri') +'/authr'
        self.token_url = os.getenv('TOKEN_URL') or self.get_yaml_config('token_url')
        self.user_url = os.getenv('USER_URL') or self.get_yaml_config('user_url')
        self.auth_url = os.getenv('AUTH_URL') or self.get_yaml_config('auth_url')
        self.issuer = os.getenv('ISSUER') or self.get_yaml_config('issuer')
        self.secret_key = os.getenv('SECRET_KEY') or self.get_yaml_config('secret_key')

    def get_yaml_config(self, key):
        try:
            with open(self.file_path) as f:
                config_temp = yaml.safe_load(f)
                return config_temp[key]
        except FileNotFoundError:
            return None

    def creat_base_config(self):
        base_config = {
            'namesilo_api_key': '',
            'admin_name': '',
            'client_id': '',
            'client_secret': '',
            'redirect_uri': '',
            'token_url': '',
            'user_url': '',
            'auth_url': '',
            'issuer': '',
            'log_level': 'INFO',
            'secret_key': ''

        }
        try:

            with open(self.file_path, 'w') as f:
                yaml.dump(base_config, f)
                logging.info('创建配置文件成功')
                exit(0)
        except IOError:
            logging.error('创建配置文件失败')
            exit(1)

    def modify_config(self, key, value):
        try:

            with open(self.file_path) as f:
                config_temp = yaml.safe_load(f)
                config_temp[key] = value
            with open(self.file_path, 'w') as f:
                yaml.dump(config_temp, f)
                logging.info('修改配置文件成功')
        except FileNotFoundError:
            logging.error('修改配置文件失败')

    def init_oidc_json(self):
        oidc_json = {
            "web": {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "redirect_uris": [
                    self.redirect_uri
                ],
                "auth_uri": self.auth_url,
                "token_uri": self.token_url,
                "issuer": self.issuer,
                "userinfo_uri": self.user_url,
                "userinfo_endpoint": self.user_url,
            }
        }

        try:
            file_path = os.path.join(os.path.dirname(__file__), 'client_secrets.json')
            with open(file_path, 'w') as f:
                json.dump(oidc_json, f)
                logging.info('创建OIDC配置文件成功')
                exit(0)
        except IOError:
            logging.error('创建OIDC配置文件失败')
            exit(1)


if __name__ == '__main__':
    config = Config()
    logging.info(config.namesilo_api_key)
    config.init_oidc_json()
