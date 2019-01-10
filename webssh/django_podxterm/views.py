from django.shortcuts import render, HttpResponse,render_to_response
from django.http import JsonResponse
from django_webssh.tools import tools
import json
from .forms import ContainerForm
from .models import Container

from django_webssh.tools.k8sclient import K8SClient
from django.views.decorators.csrf import csrf_exempt

def index(request):
    if request.method == 'GET':
        return render(request, 'podxterm.html')

    elif request.method == 'POST':
        success = {'code': 0, 'message': None, 'error': None}

        try:
            post_data = request.POST.get('data')
            data = json.loads(post_data)


           # unique = tools.unique()
           # data['unique'] = unique
           # print("unique"+unique)
            valid_data=ContainerForm(data)
            if valid_data.is_valid():
                record = valid_data.save()
                success['message'] = str(record.id)
                print("id="+str(record.id))
            else:
                error_json = valid_data.errors.as_json()
                success['code'] = 1
                success['error'] = error_json

            return JsonResponse(success)
        except Exception as e:
            print(e)
            success['code'] = 1
            success['error'] = '发生未知错误'
            return JsonResponse(success)
'''
https://www.jianshu.com/p/a178f08d9389
不进行验证csrf
'''
@csrf_exempt
def getpodlogs(request,podid):
    success = {'code': 0, 'message': None, 'error': None}
    try:
        container = Container.objects.get(pk=podid)
        if container:
            k8s = K8SClient()
            podname=container.podname
            namespace=container.namespace
            logs = k8s.readlogs(podname=podname,namespace=namespace)
            success['code'] = 0
            success['data'] = logs
            if request.method =='POST':
                return JsonResponse(success)
            else:
                return render_to_response('podlogs.html', {'logs':logs})

        else:
            success['code'] = 1
            success['error'] = 'container not found'
            return JsonResponse(success)
    except Exception as e:
        print(e)
        success['code'] = 1
        success['error'] = '发生未知错误'
        return JsonResponse(success)