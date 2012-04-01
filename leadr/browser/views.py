from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from leadr.browser.models import Entry, Tag
from os.path import join

from leadr.browser.forms import RegistrationForm, LoginForm, EntryForm


def home(request):
    """Home page functionality."""
    if request.user.is_authenticated():
        return HttpResponseRedirect("/browser/")

    else:
        registration_form = RegistrationForm()
        login_form = LoginForm()
        context = RequestContext(request, {'registration_form':registration_form, 'login_form':login_form})
        return render_to_response('home.html', context)


def register(request):
    """Registration functionality."""
    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            new_user = registration_form.save(commit=False)
            email = registration_form.cleaned_data['email']
            first_name = registration_form.cleaned_data['first_name']
            password = registration_form.cleaned_data['password']
            username = email
            #build logic here to populate first and last name fields
            new_user.email = email
            new_user.username = username
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
    
    context = RequestContext(request, {'browser_user':request.user, 'entry_list':entries, 'entry_form':entry_form})
    return render_to_response('browser.html', context)


@login_required
def new_location(request):
    if request.method == 'POST':
        entry_form = EntryForm(request.POST)
        tags = ((request.POST['tags']).replace(' ','')).split(',')
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

