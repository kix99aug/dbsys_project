from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.core import serializers
from .models import *
from django.views.decorators.csrf import csrf_exempt
import hashlib
import json,string,random
import requests


def hash_code(s, salt='ivan'):  # 密碼加密
    h = hashlib.sha256()
    s = s + salt
    h.update(s.encode())
    return h.hexdigest()

def index(request):
    nickname = "訪客"
    logged = False
    if 'nickname' in request.session:
        nickname = request.session['nickname']
        logged = True
    return render(request, 'index.html', {'nickname': nickname, 'logged': logged})

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def search(request):
    nickname = "訪客"
    logged = False
    if 'nickname' in request.session:
        nickname = request.session['nickname']
        logged = True
    return render(request, 'search.html', {'nickname': nickname, 'logged': logged, 'value': request.GET['value']})


def logout(request):
    request.session.flush()
    return JsonResponse({'result': True})


def login(request):
    return render(request, 'login.html')


def register(request):
    return render(request, 'register.html')


def comment(request):
    with connection.cursor() as c:
        m = Merchandise.objects.raw("SELECT model,id from Merchandise WHERE id={}".format(request.GET['id']))
        mm = m[0].model
        mId = m[0].id
        u = User.objects.raw("SELECT id from User")
        userId = u[0].id
        d = Discuss.objects.raw("SELECT id,uid,content from Discuss")
        return render(request, 'comment.html', {'Mmodel': mm, 'D': d})


@csrf_exempt
def api_search(req):
    if req.method == 'POST':
        result = []
        merchs = Merchandise.objects.raw(
            'SELECT * FROM merchandise WHERE model LIKE "%{0}%"'.format(req.POST['value']))
        for merch in merchs:
            crawlinf = CrawlInf.objects.raw(
                'SELECT * FROM crawl_inf WHERE mid="{0}" AND price>=(SELECT AVG(price) FROM crawl_inf WHERE mid="{0}") ORDER BY price'.format(merch.id))
            data = []
            for eachinf in crawlinf:
                data.append({
                    'url': eachinf.url,
                    'title': eachinf.title,
                    'price': eachinf.price,
                    'image_url': eachinf.image_url,
                })
            result.append({
                'mid': merch.id,
                'model': str(merch.model).upper(),
                'data': data
            })
        return JsonResponse({'result': result})

#data['result'].length == 0

@csrf_exempt
def api_login(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST['email'])
            if (user.password == hash_code(request.POST['password'])):
                request.session['email'] = user.email
                request.session['nickname'] = user.nickname
                return JsonResponse({'result': True})
            else:
                return JsonResponse({'result': False})
        except:
            return JsonResponse({'result': False})

@csrf_exempt
def oauth_callback(request):
    social = SocialAuthUsersocialauth.objects.raw('SELECT * from social_auth_usersocialauth where user_id="{0}"'.format(request.session['_auth_user_id']))
    if not User.objects.filter(email = social[0].uid).exists():
        r = json.loads(social[0].extra_data)
        if social[0].provider == "google-oauth2":
            authorization_header = {"Authorization": "OAuth %s" % r['access_token']}
            url = "https://www.googleapis.com/oauth2/v3/userinfo"
        else:
            authorization_header = {"Authorization": "token %s" % r['access_token']}
            url = "https://api.github.com/user"
        res = requests.get(url,
                headers=authorization_header)
        data = res.json()
        User.objects.create(email=social[0].uid, password=randomString(), nickname=data['name'])
    user = User.objects.get(email=social[0].uid)
    request.session['email'] = user.email
    request.session['nickname'] = user.nickname
    return HttpResponseRedirect('/')


@csrf_exempt
def api_register(request):
    if request.method == "POST":
        try:
            if not User.objects.filter(email=request.POST['email']).exists():
                if (request.POST['nickname'] == ''):
                    raise Exception()
                if (request.POST['password'] == ''):
                    raise Exception()
                if (request.POST['password'] != request.POST['password_check']):
                    raise Exception()
                r = User.objects.create(email=request.POST['email'], password=hash_code(
                    request.POST['password']), nickname=request.POST['nickname'])
                request.session['email'] = request.POST['email']
                request.session['nickname'] = request.POST['nickname']
                return JsonResponse({'success': True})
            else:
                raise Exception()
        except:
            return JsonResponse({'success': False})


@csrf_exempt
def api_comment_add(request):
    if request.method == "POST":
        with connection.cursor() as cursor:
            content = request.POST['content']
            userId = User.objects.raw(
                'SELECT * FROM User WHERE email="{0}"'.format(request.session['email']))[0].id
            cursor.execute("INSERT INTO Discuss(uid, mid, content) VALUES ('{0}','{1}','{2}')".format(
                userId, 40, content))
            discuss = Discuss.objects.raw(
                "SELECT id,uid,mid,content FROM Discuss")
            result = []
            for comment in discuss:
                result.append(
                    {'id': comment.id, 'uid': comment.uid, 'mid': comment.mid, 'content':  comment.content})
            return JsonResponse(result, safe=False, json_dumps_params={'ensure_ascii': False})



@csrf_exempt
def api_comment_update(req):
    if req.method == 'POST':
        with connection.cursor() as cursor:
            discuss = Discuss.objects.raw(
                'SELECT * FROM discuss WHERE id="{0}"'.format(req.POST['id']))[0]
            if discuss.uid != User.objects.raw('SELECT * FROM User WHERE email="{0}"'.format(req.session['email']))[0].id:
                return JsonResponse({'result': False})
            cursor.execute(
                'UPDATE discuss SET content=\'{0}\' WHERE id="{1}"'.format(req.POST['content'], req.POST['id']))
            return JsonResponse({'result': True})


@csrf_exempt
def api_comment_delete(req):
    if req.method == 'POST':
        with connection.cursor() as cursor:
            discuss = Discuss.objects.raw(
                'SELECT * FROM discuss WHERE id="{0}"'.format(req.POST['id']))[0]
            if discuss.uid != User.objects.raw('SELECT * FROM User WHERE email="{0}"'.format(req.session['email']))[0].id:
                return JsonResponse({'result': False})
            cursor.execute(
                'DELETE FROM discuss WHERE id="{0}"'.format(req.POST['id']))
            return JsonResponse({'result': True})
