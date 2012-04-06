from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from leadr.browser.models import Entry, Tag, Example
from os.path import join
from settings import MEDIA_ROOT
import settings
import datetime

from leadr.browser.forms import RegistrationForm, LoginForm, EntryForm, RegistrationModalForm, LoginModalForm


def home(request):
    """Home page functionality."""
    date = datetime.datetime.now()

    if request.user.is_authenticated():
        return HttpResponseRedirect("/browser/")

    else:
        registration_form = RegistrationForm()
        login_form = LoginForm()
        context = RequestContext(request, {'registration_form':registration_form, 'login_form':login_form, 'media_root':MEDIA_ROOT, 'date':date})
        return render_to_response('home.html', context)


def register(request):
    """Registration functionality."""
    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            new_user = registration_form.save(commit=False)
            
            #sets username to email etc.
            email = registration_form.cleaned_data['email']
            password = registration_form.cleaned_data['password']
            username = email
            new_user.email = email
            new_user.username = username

            #first and last name logic
            name = registration_form.cleaned_data['first_name']
            names = name.split(' ')
            new_user.first_name = names[0]
            if len(names)>1:
                new_user.last_name = names[1]
            
            new_user.set_password(password)
            if not User.objects.filter(username=username):
                new_user.save()
                new_user = authenticate(username=username, password=password)
                if new_user:
                    login(request, new_user)
                    return HttpResponseRedirect('/browser/')
            else:
                return HttpResponseRedirect("/")
        else:
            login_form = LoginForm()
            registration_form = RegistrationForm()
            context = RequestContext(request, {'registration_form':registration_form, 'login_form':login_form})
            return render_to_response('home.html', context)
    else:
        return HttpResponseRedirect("/")


def login_view(request):
    """Login functionality."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/browser/')
        else:
            login_form = LoginForm()
            registration_form = RegistrationForm()
            context = RequestContext(request, {'login_form': login_form, 'registration_form': registration_form})
            return render_to_response('home.html', context)
    else:
        return HttpResponseRedirect("/")


def logout_view(request):
    """Logs user out."""
    logout(request)
    return HttpResponseRedirect("/")


@login_required
def browser(request):
    """Checks whether user is logged in, if so loads browser."""
    entry_form = EntryForm()
    date = datetime.datetime.now()

    entries = request.user.entry_set.order_by('-created')
    for entry in entries:
        tags = [x[1] for x in entry.tags.values_list()]
        if tags:
            entry.tag_lst = tags[0]
            if len(tags)>1:
                for i in range(1, len(tags)):
                    entry.tag_lst += (', ' + tags[i])
            if len(entry.tag_lst) > 40:
                trunc_tag_lst = entry.tag_lst[0:45] + "..."
                entry.tag_lst = trunc_tag_lst
        entry.split_address = ','.join(entry.raw_address.split(' '))

    examples = Example.objects.all().order_by('-created')
    for example in examples:
        tags = [x[1] for x in example.tags.values_list()]
        if tags:
            example.tag_lst = tags[0]
            if len(tags)>1:
                for i in range(1, len(tags)):
                    example.tag_lst += (', ' + tags[i])
            if len(example.tag_lst) > 40:
                trunc_tag_lst = example.tag_lst[0:45] + "..."
                example.tag_lst = trunc_tag_lst
        example.split_address = ','.join(example.raw_address.split(' '))
    
    context = RequestContext(request, {'browser_user':request.user, 'entry_list':entries, 'entry_form':entry_form, 'date':date, 'example_list':examples})
    return render_to_response('browser.html', context)


@login_required
def new_location(request):
    if request.method == 'POST':
        entry_form = EntryForm(request.POST)
        #fix tags here so spaces appear in multi-word tags
        tags = ((request.POST['tags']).replace(', ',',')).split(',')
        if entry_form.is_valid():
            e = Entry.objects.create(user=request.user, raw_address=entry_form.cleaned_data['raw_address'], title=entry_form.cleaned_data['title'])
            lst = []
            for tag in tags:
                t = Tag.objects.create(user=request.user, tag=tag)
                lst.append(t)
            e.tags = lst
        return HttpResponseRedirect('/browser/')
    else:
        return HttpResponseRedirect('/browser/') 


def single_loc(request, id):
    """Shows single location."""
    registration_form = RegistrationModalForm()
    login_form = LoginModalForm()
    entry = Entry.objects.get(id=id)

    tags = [x[1] for x in entry.tags.values_list()]
    if tags:
        entry.tag_lst = tags[0]
        if len(tags)>1:
            for i in range(1, len(tags)):
                entry.tag_lst += (', ' + tags[i])
        if len(entry.tag_lst) > 40:
            trunc_tag_lst = entry.tag_lst[0:45] + "..."
            entry.tag_lst = trunc_tag_lst
    entry.split_address = ','.join(entry.raw_address.split(' '))
    
    context = RequestContext(request, {'browser_user':request.user, 'registration_form':registration_form, 'login_form':login_form, 'entry':entry})
    return render_to_response('single_loc.html', context)



def add_single(request):
    uid = (request.META.get('HTTP_REFERER'))[-1:]
    entry = Entry.objects.get(id=uid)
    date = datetime.datetime.now()

    e = Entry.objects.create(user=request.user, raw_address=entry.raw_address, title=entry.title, created=date)

    tags = [x[1] for x in entry.tags.values_list()]
    if tags:
        tag_str = tags[0]
        if len(tags)>1:
            for i in range(1, len(tags)):
                tag_str += (', ' + tags[i])
    tags_add = (tag_str.replace(', ',',')).split(',')
    lst = []
    for tag in tags_add:
        t = Tag.objects.create(user=request.user, tag=tag)
        lst.append(t)
    e.tags = lst

    return HttpResponseRedirect('/browser/')


def login_add(request):
    uid = (request.META.get('HTTP_REFERER'))[-1:]
    entry = Entry.objects.get(id=uid)
    date = datetime.datetime.now()

    """Login functionality."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return HttpResponseRedirect('/location/'+uid)
    else:
        return HttpResponseRedirect("/")

    uid = (request.META.get('HTTP_REFERER'))[-1:]
    entry = Entry.objects.get(id=uid)
    date = datetime.datetime.now()

    e = Entry.objects.create(user=request.user, raw_address=entry.raw_address, title=entry.title, created=date)

    tags = [x[1] for x in entry.tags.values_list()]
    if tags:
        tag_str = tags[0]
        if len(tags)>1:
            for i in range(1, len(tags)):
                tag_str += (', ' + tags[i])
    tags_add = (tag_str.replace(', ',',')).split(',')
    lst = []
    for tag in tags_add:
        t = Tag.objects.create(user=request.user, tag=tag)
        lst.append(t)
    e.tags = lst

    return HttpResponseRedirect('/browser/')


def register_add(request):
    uid = (request.META.get('HTTP_REFERER'))[-1:]
    entry = Entry.objects.get(id=uid)
    date = datetime.datetime.now()

    """Registration functionality."""
    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            new_user = registration_form.save(commit=False)
            
            #sets username to email etc.
            email = registration_form.cleaned_data['email']
            password = registration_form.cleaned_data['password']
            username = email
            new_user.email = email
            new_user.username = username

            #first and last name logic
            name = registration_form.cleaned_data['first_name']
            names = name.split(' ')
            new_user.first_name = names[0]
            if len(names)>1:
                new_user.last_name = names[1]
            
            new_user.set_password(password)
            if not User.objects.filter(username=username):
                new_user.save()
                new_user = authenticate(username=username, password=password)
                if new_user:
                    login(request, new_user)
            else:
                return HttpResponseRedirect('/location/'+uid)
        else:
            return HttpResponseRedirect('/location/'+uid)
    else:
        return HttpResponseRedirect('/location/'+uid)


    e = Entry.objects.create(user=request.user, raw_address=entry.raw_address, title=entry.title, created=date)

    tags = [x[1] for x in entry.tags.values_list()]
    if tags:
        tag_str = tags[0]
        if len(tags)>1:
            for i in range(1, len(tags)):
                tag_str += (', ' + tags[i])
    tags_add = (tag_str.replace(', ',',')).split(',')
    lst = []
    for tag in tags_add:
        t = Tag.objects.create(user=request.user, tag=tag)
        lst.append(t)
    e.tags = lst

    return HttpResponseRedirect('/browser/')





























