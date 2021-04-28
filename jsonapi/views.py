from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
import threading
import requests
import queue
import json
import io
from urllib.request import urlopen
from rest_framework.decorators import api_view
from rest_framework.response import Response


def ping(request):
    successResponse = {"success": 'true'}
    return JsonResponse(successResponse,status = 200)


def multithreading(url_queue, responses):
    queue_full = True
    while queue_full:

        try:            
            url = url_queue.get(False)
            data = urlopen(url).read()
            
            fix_bytes_value = data.replace(b"'", b'"')
            my_json = json.load(io.BytesIO(fix_bytes_value)) 
            responses.append(my_json["posts"])
            
        except queue.Empty:
            queue_full = False


def posts(request):
    if 'tags' in request.GET:
        tags = request.GET["tags"]
    else:
        errorResponse = {"error" : 'Tags parameter is required' }
        return JsonResponse(errorResponse)

    sortList = ['id','likes']
    if "sortBy" in request.GET:
        sortBy = request.GET["sortBy"]
        if sortBy not in sortList:
            errorResponse = {"error" : 'sortBy parameter is invalid' }
            return JsonResponse(errorResponse, status=400)
    else:
        sortBy = 'id'
    
    directionList = ['asc','desc']
    if 'direction' in request.GET:
        direction = request.GET["direction"]
        if direction not in directionList:
            errorResponse = {"error" : 'direction parameter is invalid' }
            return JsonResponse(errorResponse, status=400)
    else:
        direction = 'asc'

    tags = tags.split(',')
    
    if direction == 'desc':
        value =True
    else:
        value = False

    apis =[]
    
    for tag in tags:
        apis.append('https://api.hatchways.io/assessment/blog/posts?tag='+tag)
    
    wait_list = queue.Queue()
    
    for api in apis:
        wait_list.put(api)

    responses = []
    for i in range(len(tags)):
        t = threading.Thread(target=multithreading, args = ( wait_list, responses))
        t.start()
        t.join()

    output=[]
    for i in responses:
        output+=i

    output.sort(key = lambda json: json[sortBy], reverse= value)
    unique = { each['id'] : each for each in output }.values()
    unique1=list(unique)
    responseData = {"posts":unique1}
    return JsonResponse(responseData, status=200, safe=False)
      


