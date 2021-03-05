from flask import Flask
from ..spy import WeChatSpy
from queue import Queue
from threading import Thread
from ..command import *
import requests


class SpyService(Flask):
    def __init__(self, import_name,
                 static_url_path=None,
                 static_folder="static",
                 static_host=None,
                 host_matching=False,
                 subdomain_matching=False,
                 template_folder="templates",
                 instance_path=None,
                 instance_relative_config=False,
                 root_path=None,
                 key=None):
        self.last_client_count = 0
        self.response_queue = Queue()
        self.client2pid = dict()
        self.client2wxid = dict()
        self.client2login = dict()
        self.client2user_logout = dict()
        self.client2account = dict()
        self.client2qrcode = dict()
        self.client2contacts = dict()
        self.spy = WeChatSpy(response_queue=self.response_queue, key=key)
        super().__init__(import_name,
                         static_url_path=static_url_path,
                         static_folder=static_folder,
                         static_host=static_host,
                         host_matching=host_matching,
                         subdomain_matching=subdomain_matching,
                         template_folder=template_folder,
                         instance_path=instance_path,
                         instance_relative_config=instance_relative_config,
                         root_path=root_path)
        t = Thread(target=self.parse)
        t.setDaemon(True)
        t.start()

    def parse(self):
        while True:
            data = self.response_queue.get()
            if data.type == WECHAT_CONNECTED:
                self.client2pid[data.port] = data.pid
                self.client2login[data.port] = "0"
            elif data.type == WECHAT_LOGIN:
                self.client2login[data.port] = "1"
            elif data.type == WECHAT_LOGOUT:
                self.client2login[data.port] = "0"
            elif data.type == ACCOUNT_DETAILS:
                self.client2account[data.port] = data.bytes
            elif data.type == LOGIN_QRCODE:
                self.client2qrcode[data.port] = data
            elif data.type == GET_CONTACTS_LIST and not data.code:
                self.client2contacts[data.port] = data
            elif data.type == CONTACTS_LIST:
                self.client2contacts[data.port] = data
            elif data.type == USER_LOGOUT:
                self.client2user_logout[data.port] = data.code

