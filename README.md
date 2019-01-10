```

fork 自：https://github.com/huyuan1999/django-webssh 感谢作者。
作者blog：http://blog.51cto.com/hongchen99/2336087

增加k8s 中 pod 的 webssh 登录部分,及使用kubernetes api 获取日志


开发环境:
    deepin 15
    python 3.6

	
安装:(Centos 7 环境)
	git clone https://github.com/huyuan1999/django-webssh.git
	yum -y install epel-release gcc
	yum -y install python36 python36-devel
	curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
	python3.6 get-pip.py
	python3.6 -m pip install Django==2.0.6 paramiko==2.4.1 channels==2.1.5
	
	
启动:
	cd django-webssh/webssh/
	python3.6 manage.py makemigrations django_webssh
	python3.6 manage.py migrate django_webssh
	python3.6 manage.py runserver 0.0.0.0:8000

```	

<br><br><br><br>

demo:<br><br>

登录pod<br>
![webssh](https://github.com/zhailibao/django-webssh/blob/master/demo/podlogin.png)
<br><br><br>
命令行操作界面<br>
![webssh](https://github.com/zhailibao/django-webssh/blob/master/demo/podwebssh.png)
<br><br><br>
日志查看页面<br>

![webssh](https://github.com/zhailibao/django-webssh/blob/master/demo/podlogs.png)
<br><br><br>

登录<br>
![webssh](https://github.com/huyuan1999/django-webssh/blob/master/demo/ssh.png)
<br><br><br>
命令行界面<br>
![webssh](https://github.com/huyuan1999/django-webssh/blob/master/demo/ssh1.png)
![webssh](https://github.com/huyuan1999/django-webssh/blob/master/demo/ssh4.png)
<br><br><br>
top交互式命令行界面<br>
![webssh](https://github.com/huyuan1999/django-webssh/blob/master/demo/ssh2.png)
![webssh](https://github.com/huyuan1999/django-webssh/blob/master/demo/ssh3.png)
<br><br><br>
vim命令行界面<br>
![webssh](https://github.com/huyuan1999/django-webssh/blob/master/demo/ssh5.png)
![webssh](https://github.com/huyuan1999/django-webssh/blob/master/demo/ssh6.png)
