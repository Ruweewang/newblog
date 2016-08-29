#coding:utf-8

from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import os
import uuid
import json
import datetime as dt

@csrf_exempt
def upload_image(request,dir_name):
    #kindeditor图片上传返回数据格式说明
    #{'error':1,'message':'出错信息'}
    #{'error':'url':'图片地址'}
    result = {"error":1,"message":"上传出错"}
    files = request.FILES.get("imgFile",None)  #点击上传“浏览”后，name="imgFile"
    if files:
        result = image_upload(files,dir_name)
    return HttpResponse(json.dumps(result),content_type="application/json")

#创建目录
def upload_gengeration_dir(dir_name):
    today = dt.datetime.today()
    dir_name = dir_name + '/%d/%d/'%(today.year,today.month)
    if not os.path.exists(settings.MEDIA_ROOT + dir_name): #如果目录不存在
        os.makedirs(settings.MEDIA_ROOT + dir_name)
    return dir_name

def image_upload(files,dir_name):
    allow_suffix = ['jpg','png','jpeg','gif','bmp']  #允许上传的图片格式
    file_suffix = files.name.split(".")[-1]
    if file_suffix not in allow_suffix:
        return {"error":1, "message":"图片格式不正确"}
    relative_path_file = upload_gengeration_dir(dir_name)
    path = os.path.join(settings.MEDIA_ROOT,relative_path_file)
    if not os.path.exists(path): #如果目录不存在则创建目录
        os.makedirs(path)
    file_name = str(uuid.uuid1())+""+file_suffix  #对上传的文件做命名的修改，用uuid的方式保证它的唯一性
    path_file = os.path.join(path,file_name)
    file_url = settings.MEDIA_URL + relative_path_file + file_name
    open(path_file,'wb').write(files.file.read()) #以二进制的方式保存图片
    return {'error':0,'url':file_url} #kindeditor需要的格式