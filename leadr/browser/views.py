from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext
from django.template.loader import render_to_string
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from leadr.browser.models import Entry, Tag, Example
from os.path import join
from base64 import b64encode, b64decode
from settings import MEDIA_ROOT
import settings
import datetime
import bitly_api

from leadr.browser.forms import RegistrationForm, LoginForm, EntryForm, RegistrationModalForm, LoginModalForm, EditForm, BookmarkletForm, LoginBookmarkletForm


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
    """If user is logged in, browser is loaded."""
    entry_form = EntryForm()
    edit_form = EditForm()
    date = datetime.datetime.now()

    #loads entries
    entries = request.user.entry_set.order_by('-created')
    for entry in entries:

        if not entry.short_link:
            #bitly link
            encoded_id = b64encode(str(entry.id))
            c = bitly_api.Connection('mleadr','R_b2577c8ead1cc2edc49ffb1b641db41d')
            if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
                link_dict = c.shorten(('http://127.0.0.1:8000/location/' + encoded_id))
            else:
                link_dict = c.shorten(('http://www.leadr.cc/location/' + encoded_id))
            entry.short_link = link_dict['url']
            entry.save()

        if entry.title:
            if len(entry.title) > 26:
                trunc_title = entry.title[0:27] + "..."
                entry.title = trunc_title
        if len(entry.raw_address) > 31:
            trunc_raw_address = entry.raw_address[0:32] + "..."
            entry.raw_address = trunc_raw_address
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
        entry.encoded_id = b64encode(str(entry.id))

    #loads examples
    examples = Example.objects.all().order_by('-created')
    for example in examples:

        if len(example.title) > 26:
            trunc_title = example.title[0:27] + "..."
            example.title = trunc_title
        if len(example.raw_address) > 34:
            trunc_raw_address = example.raw_address[0:35] + "..."
            example.raw_address = trunc_raw_address

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
    
    context = RequestContext(request, {'edit_form':edit_form, 'browser_user':request.user, 'entry_list':entries, 'entry_form':entry_form, 'date':date, 'example_list':examples})
    return render_to_response('browser.html', context)


@login_required
def edit_loc(request, id):
    """Edits an entry."""
    if request.method == 'POST':
        e = Entry.objects.get(id=id)
        edit_form = EditForm(request.POST, instance=e)
        tags = ((request.POST['tags']).replace(', ',',')).split(',')
        if edit_form.is_valid():
            edited_entry = edit_form.save(commit=False)
            
            #re-assigns user to entry
            edited_entry.user = request.user
            
            #tags logic
            lst = []
            for tag in tags:
                t = Tag.objects.create(user=request.user, tag=tag)
                lst.append(t)
            edit_form.tags = lst

            #manual save methods (both form and many-to-many needed)
            edited_entry.save()
            edit_form.save_m2m()

            return HttpResponseRedirect('/browser/')
        else:
            return HttpResponseRedirect('/browser/')
    else:
        return HttpResponseRedirect('/browser/')


@login_required
def delete_loc(request, id):
    """Deletes an entry."""
    if request.method == 'POST':
        e = Entry.objects.filter(id=id)
        e.delete()
        return HttpResponseRedirect('/browser/')
    else:
        return HttpResponseRedirect('/browser/')


@login_required
def new_location(request):
    """Adds a new location - uses modal form on browser."""
    if request.method == 'POST':
        entry_form = EntryForm(request.POST)
        tags = ((request.POST['tags']).replace(', ',',')).split(',')
        if entry_form.is_valid():
            e = Entry.objects.create(user=request.user, raw_address=entry_form.cleaned_data['raw_address'], title=entry_form.cleaned_data['title'])
            lst = []
            for tag in tags:
                t = Tag.objects.create(user=request.user, tag=tag)
                lst.append(t)
            e.tags = lst

            #bitly link
            encoded_id = b64encode(str(e.id))
            c = bitly_api.Connection('mleadr','R_b2577c8ead1cc2edc49ffb1b641db41d')
            if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
                link_dict = c.shorten(('http://127.0.0.1:8000/location/' + encoded_id))
            else:
                link_dict = c.shorten(('http://www.leadr.cc/location/' + encoded_id))
            e.short_link = link_dict['url']
            e.save()

        #saves a small txt file with entry info, for saving to dropbox
        dbfile =  open(MEDIA_ROOT + '/dropbox/' + encoded_id + '.txt','w')
        dbfile.write('name: ' + entry_form.cleaned_data['title'] + '\naddress: ' + entry_form.cleaned_data['raw_address'])
        dbfile.close()

        return HttpResponseRedirect('/browser/')
    else:
        return HttpResponseRedirect('/browser/') 


def single_loc(request, id):
    """Shows single location publicly."""
    registration_form = RegistrationModalForm()
    login_form = LoginModalForm()
    entry_id = int(b64decode(id))
    entry = Entry.objects.get(id=entry_id)

    if len(entry.title) > 26:
        trunc_title = entry.title[0:27] + "..."
        entry.title = trunc_title
    if len(entry.raw_address) > 34:
        trunc_raw_address = entry.raw_address[0:35] + "..."
        entry.raw_address = trunc_raw_address

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

    db_name = entry.title.lower().replace(" ","_")
    
    context = RequestContext(request, {'browser_user':request.user, 'registration_form':registration_form, 
        'login_form':login_form, 'entry':entry, 'dbfile_name':db_name, 'dbfile_id':id})
    return render_to_response('single_loc.html', context)


def add_single(request, id):
    """Adds public location if user is logged in. Used with single_loc view."""
    if request.method == 'POST':  
        entry = Entry.objects.get(id=id)
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
    else:
        return HttpResponseRedirect('/')


def add_example(request, id):
    """Adds example location to browser"""
    if request.method == 'POST':  
        example = Example.objects.get(id=id)
        date = datetime.datetime.now()

        e = Entry.objects.create(user=request.user, raw_address=example.raw_address, title=example.title, created=date)

        tags = [x[1] for x in example.tags.values_list()]
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

        #bitly link
        encoded_id = b64encode(str(e.id))
        c = bitly_api.Connection('mleadr','R_b2577c8ead1cc2edc49ffb1b641db41d')
        if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
            link_dict = c.shorten(('http://127.0.0.1:8000/location/' + encoded_id))
        else:
            link_dict = c.shorten(('http://www.leadr.cc/location/' + encoded_id))
        e.short_link = link_dict['url']
        e.save()

        return HttpResponseRedirect('/browser/')
    else:
        return HttpResponseRedirect('/')


def login_add(request, id):
    """Logs user in and adds single location to browser. Used with single_loc view."""
    entry = Entry.objects.get(id=id)
    date = datetime.datetime.now()

    """Login functionality."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return HttpResponseRedirect('/location/'+id)
    else:
        return HttpResponseRedirect("/")

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


def register_add(request, id):
    """Registers and logs in new user and adds single location to browser. Used with single_loc view."""
    entry = Entry.objects.get(id=id)
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
                return HttpResponseRedirect('/location/'+id)
        else:
            return HttpResponseRedirect('/location/'+id)
    else:
        return HttpResponseRedirect('/location/'+id)


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


def bookmarklet(request, random, address=None):
    """Loads bookmarklet javascript to launch form."""
    if address:
        bookmarklet_form = BookmarkletForm(initial={'raw_address':address})
    else:
        bookmarklet_form = BookmarkletForm()
    login_form = LoginBookmarkletForm()

    variables = {'bookmarklet_form':bookmarklet_form, 'login_form':login_form, 'user':request.user}
    resp = render_to_string('book.js', variables)
    return HttpResponse(resp, mimetype="text/javascript")


@csrf_exempt
def login_bookmarklet(request):
    if request.META['HTTP_REFERER']:
        url = request.META['HTTP_REFERER']
    else:
        url = 'http://www.leadr.cc'
        
    """Login functionality."""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return HttpResponseRedirect(url)
    else:
        return HttpResponseRedirect(url)

    #resp = render_to_string('book.js')
    return HttpResponseRedirect(url)


@login_required
@csrf_exempt
def bookmarklet_add(request):
    """Adds a new location using bookmarklet, redirects to current page."""
    if request.META['HTTP_REFERER']:
        url = request.META['HTTP_REFERER']
    else:
        url = 'http://www.leadr.cc'

    if request.method == 'POST':
        entry_form =  BookmarkletForm(request.POST)
        tags = ((request.POST['tags']).replace(', ',',')).split(',')
        if entry_form.is_valid():
            e = Entry.objects.create(user=request.user, raw_address=entry_form.cleaned_data['raw_address'], title=entry_form.cleaned_data['title'])
            lst = []
            for tag in tags:
                t = Tag.objects.create(user=request.user, tag=tag)
                lst.append(t)
            e.tags = lst

            #bitly link
            encoded_id = b64encode(str(e.id))
            c = bitly_api.Connection('mleadr','R_b2577c8ead1cc2edc49ffb1b641db41d')
            if settings.DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
                link_dict = c.shorten(('http://127.0.0.1:8000/location/' + encoded_id))
            else:
                link_dict = c.shorten(('http://www.leadr.cc/location/' + encoded_id))
            e.short_link = link_dict['url']
            e.save()

        return HttpResponseRedirect(url)
    else:
        return HttpResponseRedirect(url)










