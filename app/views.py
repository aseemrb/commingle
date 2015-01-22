from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template import RequestContext, loader
from app.models import Users, Feeds, Comments
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
import json
import time
import cPickle

# Create your views here.
def index(request):
    try:
        if request.session['username']:
            feeds = Feeds.objects.order_by('-time')
            user = Users.objects.filter(username=request.session['username'])[0]
            users = Users.objects.all()
            struc = []

            for feed in feeds:
                usr = Users.objects.filter(username=feed.user)[0]
                struc.append({'feed': feed, 'usr': usr})

            favfeeds = cPickle.loads(user.favs)
            print favfeeds
            return render(request, 'users/index.html', {'struc': struc, 'user': user, 'favfeeds': favfeeds})
        else:
            return render(request, 'users/login.html')
    except KeyError:
        return render(request, 'users/login.html')

def register(request):
    context = RequestContext(request)
    errors = False
    if request.method == 'POST' and request.is_ajax():
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        college = request.POST['college']
        fname = request.POST['fname']
        lname = request.POST['lname']
        bio = request.POST['bio']
        query = Users.objects.filter(username=username)
        if query:
            errors = True
        else:
            dic = []
            dat = cPickle.dumps(dic)
            user = Users.objects.create(username=username, password=password, email=email, fname=fname, lname=lname, college=college, bio=bio, favs=dat)
            request.session['username']  = username
            request.session['password']  = password
            
        return HttpResponse(json.dumps({'errors': errors}),content_type='application/json')
    else:
        raise Http404


def user_login(request):
    try:
        if request.session['username']:
            return HttpResponseRedirect("/app")
    except KeyError:
        context = RequestContext(request)
        error = False
        if request.method == 'POST' and request.is_ajax():
            username = request.POST['username']
            password = request.POST['password']
            query = Users.objects.filter(username=username, password=password)
            # user = authenticate(username=username, password=password)
            if query:
                request.session['username']  = username
                request.session['password']  = password
                return HttpResponse(json.dumps({'errors': error}),content_type='application/json')
            else:
                error = True
                return HttpResponse(json.dumps({'errors': error}),content_type='application/json')
        return render(request, 'users/login.html')


def newfeed(request):
    try:
        if request.session['username']:
            context = RequestContext(request)
            if request.method == 'POST':
                username = request.session['username']
                verb = request.POST['verb']
                event = request.POST['event']
                place = request.POST['place']
                link = request.POST['link']
                feedtime = int(round(time.time() * 1000))
                user = Users.objects.filter(username=request.session['username'])[0]
                feed = Feeds.objects.create(user=username, verb=verb, event=event, place=place, link=link, time=feedtime, fname=user.fname, lname=user.lname)
        return HttpResponseRedirect("/app")

    except KeyError:
        return HttpResponseRedirect("/app")


def favorite(request, feed_id):
    try:
        if request.session['username']:
            
            username = request.session['username']
            feed = Feeds.objects.filter(id=feed_id)[0]
            user = Users.objects.filter(username=request.session['username'])[0]
            dic = cPickle.loads(user.favs)
            dic.append(feed)
            user.favs = cPickle.dumps(dic)
            user.save()

        return HttpResponseRedirect("/app")

    except KeyError:
        return HttpResponseRedirect("/app")

def unfavorite(request, feed_id):
    try:
        if request.session['username']:
            
            username = request.session['username']
            feed = Feeds.objects.filter(id=feed_id)[0]
            user = Users.objects.filter(username=request.session['username'])[0]
            dic = cPickle.loads(user.favs)
            dic.remove(feed)
            user.favs = cPickle.dumps(dic)
            user.save()

        return HttpResponseRedirect("/app")

    except KeyError:
        return HttpResponseRedirect("/app")


def starred(request):
    try:
        if request.session['username']:
            user = Users.objects.filter(username=request.session['username'])[0]
            feeds = cPickle.loads(user.favs)

            users = Users.objects.all()
            struc = []

            for feed in feeds:
                usr = Users.objects.filter(username=feed.user)[0]
                struc.append({'feed': feed, 'usr': usr})

            return render(request, 'users/favs.html', {'struc': struc, 'user': user})
        else:
            return HttpResponseRedirect("/app")
    except KeyError:
        return HttpResponseRedirect("/app")


@login_required
def change_password(request):
    error = 0
    if request.method == "POST":
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        user = authenticate(username=request.session['username'], password=old_password)
        if user is not None:
            query = User.objects.get(username=request.session['username'])
            query.set_password(new_password)
            query.save()
            error = 1
            t = loader.get_template('users/account.html')
            c = RequestContext(request, {'error': error})
            return HttpResponse(t.render(c))
        else:
            error = 2
            t = loader.get_template('users/account.html')
            c = RequestContext(request, {'error': error})
            return HttpResponse(t.render(c))
            

@login_required
def change_email(request):
    error = 3
    if request.method == "POST":
        email = request.POST['email']
        query = User.objects.get(username=request.session['username'])
        query.email = email
        query.save()
        error = 4
    t = loader.get_template('users/account.html')
    c = RequestContext(request, {'error': error})
    return HttpResponse(t.render(c))

def user_logout(request):
    try:
        if request.session['username']:
            del request.session['username']
            del request.session['password']
        return HttpResponseRedirect("/app")
    except KeyError:
        return HttpResponseRedirect("/app")

def account(request):
    try:
        if request.session['username']:
            user = Users.objects.filter(username=request.session['username'])[0]
            return render(request, 'users/account.html', {'user': user})
        else:
            return HttpResponseRedirect("/app")
    except KeyError:
        return HttpResponseRedirect("/app")

@login_required
def problems(request):
    problems = Problems.objects.order_by('id')
    return render(request, 'problems/index.html', {'problems': problems})

@login_required
def details(request, problem_id):
    prob = get_object_or_404(Problems, id=problem_id)
    try:
        solution = Solve.objects.get(username=request.session['username'], problem_id=prob.id)
    except Solve.DoesNotExist:
        solution = None
    status = False
    if solution:
        if solution.status==1:
            status = True
    return render(request, 'problems/details.html', {'prob': prob, 'status': status})