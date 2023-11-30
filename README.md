# Namesilo-Domain-Share
## 介绍
本项目可用用于在NameSilo域名注册商上购买域名后通过调用NameSiloAPI
实现域名共享,该项目仅支持OIDC认证，可配合原有的认证系统使用
## 使用方法
### 1.获取APIKEY
在[NameSilo](https://www.namesilo.com/)上获取APIKEY
### 2.使用Docker部署
#### 2.1.获取镜像
```shell
docker build -t namesilo-domain-share .
```
#### 2.2.运行容器
```shell
docker run -d --name=namesoil -p 127.0.0.1:5000:5000 -v /root/config/namesilo/:/app/data namesilo-domain-share
```
#### 2.3.配置
 第一次启动后容器会自动生成配置文件，并退出，你需要完善配置文件后再次启动容器
```shell
docker start namesilo
```

