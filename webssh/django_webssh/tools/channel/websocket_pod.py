from channels.generic.websocket import WebsocketConsumer
from django_webssh.tools.k8sclient import K8SClient
from django.http.request import QueryDict
from django_webssh import models
from django_podxterm.models import Container
from django.utils.six import StringIO
import json
import base64


class WebSSHPOD(WebsocketConsumer):
    message = {'status': 0, 'message': None}
    """
    status:
        0: ssh 连接正常, websocket 正常
        1: 发生未知错误, 关闭 ssh 和 websocket 连接

    message:
        status 为 1 时, message 为具体的错误信息
        status 为 0 时, message 为 ssh 返回的数据, 前端页面将获取 ssh 返回的数据并写入终端页面
    """

    def connect(self):
        message = {'status': 0, 'message': None}
        try:
            self.accept()
            query_string = self.scope['query_string']
            connet_argv = QueryDict(query_string=query_string, encoding='utf-8')
            unique = connet_argv.get('unique')
            width = connet_argv.get('width')
            height = connet_argv.get('height')

            width = int(width)
            height = int(height)
            print("unique"+unique)
            connect_info = Container.objects.get(pk=unique)

            #containername = connect_info.containername
            #namespace = connect_info.namespace
            #podname = connect_info.podname
            print('connect_info'+connect_info.podname)
           # connect_info.delete()
            namespace='default'
            podname='nginx-deployment-7f858f7f6f-x7ntb'
            containername='nginx-deployment-7f858f7f6f-x7ntb'
            k8sapi = K8SClient()
            self.k8sapi=k8sapi
            return k8sapi.connect(namespace,podname,containername,socketer=self)


        except Exception as e:
            print(e)
            print('112222222')
            self.message['status'] = 1
            self.message['message'] = str(e)
            message = json.dumps(self.message)
            self.send(message)
            self.close()

    def disconnect(self, close_code):
        try:
            self.k8sapi.close()
        except:
            pass

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        if type(data) == dict:
            status = data['status']
            if status == 0:
                data = data['data']
                #print('in receive data')
                #print(data)
                self.k8sapi.shell(data)
            else:
                cols = data['cols']
                rows = data['rows']
                self.k8sapi.resize_pty(cols=cols, rows=rows)
