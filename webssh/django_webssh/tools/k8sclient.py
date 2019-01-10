from kubernetes import config
from kubernetes.client import Configuration
from kubernetes.client.apis import core_v1_api
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream


from django.conf import settings

from threading import Thread
import json
'''
https://github.com/kubernetes-client/python-base/blob/master/stream/ws_client.py
https://github.com/kubernetes-client/python/blob/master/examples/exec.py
'''


class K8SClient:
    def __int__(self):
        print('K8sclient init start')
    def new(self):
        config.load_kube_config(settings.K8S_CONFIG)
        c= Configuration()
        c.assert_hostname = False
        Configuration.set_default(c)
        self.k8s = core_v1_api.CoreV1Api()
        print('K8sclient init end')


    def connect(self,namespace, podname,containername,socketer,pty_width=80, pty_height=24):
        config.load_kube_config(settings.K8S_CONFIG)
        self.command=''
        self.socketer = socketer
        self.new()
        print('K8sclient init end')
        #command = ['/bin/bash']
        #print(podname)
        #print(namespace)
        command = [
            "/bin/sh",
            "-c",
            'TERM=xterm-256color; export TERM; [ -x /bin/bash ] '
            '&& ([ -x /usr/bin/script ] '
            '&& /usr/bin/script -q -c "/bin/bash" /dev/null || exec /bin/bash) '
            '|| exec /bin/sh']

        container_stream = stream(
            self.k8s.connect_get_namespaced_pod_exec,
            name=podname,
            namespace=namespace,
            command=command,
            stderr=True, stdin=True,
            stdout=True, tty=True,
            _preload_content=False
        )
        self.container_stream=container_stream
        return container_stream

    def write(self,command):
        print("write" + command)
#       self.container_stream.write_stdin(self.command)
        message = {}
        message['status'] = 0
        message['message'] = command
        socket_message = json.dumps(message)
        self.socketer.send(socket_message)
        if command =="\r":
#            print("receive rn")
            self.container_stream.write_stdin(self.command+"\n")
            self.command=''
        else:
            self.command=self.command+command
    def read(self):
        while self.container_stream.is_open():
            self.container_stream.update(timeout=1)
            if self.container_stream.peek_stdout():
                str=self.container_stream.read_stdout()
                message={}
                message['status']=0
                message['message']=str
                socket_message=json.dumps(message)
                print('stdout'+socket_message)
                self.socketer.send(socket_message)


    def shell(self,command):
        Thread(target=self.write, args=(command,)).start()
        Thread(target=self.read).start()

    def close(self):
        self.socketer.close()
        self.container_stream.close()

    def resize_pty(self,cols, rows):
        RESIZE_CHANNEL = 4
        print('resize_pty')
        self.container_stream.write_channel(RESIZE_CHANNEL,json.dumps({"Height": int(rows),
                                                                  "Width": int(cols)}))


    def readlogs(self,podname,namespace):
        self.new()
        try:
            logs = self.k8s.read_namespaced_pod_log(name=podname,namespace=namespace,tail_lines=100)
            return logs
        except ApiException as e:
            print("Exception when calling CoreV1Api->read_namespaced_pod_log: %s\n" % e)
