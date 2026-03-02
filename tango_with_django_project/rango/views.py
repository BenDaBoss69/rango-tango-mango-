from urllib import request
from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm, PageForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.urls import reverse


def index(request):
    # grab the top five categories by likes and the top five pages by views
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    # Session handling for visit counts (do not pass visits in index context)
    session = request.session
    visits = session.get('visits', 0)
    last_visit_str = session.get('last_visit')

    now = datetime.now()

    if last_visit_str:
        try:
            last_visit_time = datetime.strptime(last_visit_str[:19], '%Y-%m-%d %H:%M:%S')
        except Exception:
            last_visit_time = now

        # if last visit was more than a day ago, increment
        if (now - last_visit_time).days >= 1:
            visits = visits + 1
            session['last_visit'] = str(now)
            session['visits'] = visits
        else:
            # update last_visit but don't increment
            session['last_visit'] = str(last_visit_time)
            session['visits'] = visits
    else:
        visits = 1
        session['last_visit'] = str(now)
        session['visits'] = visits

    context_dict = {
        'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!',
        'categories': category_list,
        'pages': page_list,
    }

    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    # ensure session counter has been initialised by index view
    session = request.session
    visits = session.get('visits', 0)
    context = {'visits': visits}
    return render(request, 'rango/about.html', context=context)


def add_category(request):
    # require login
    if not request.user.is_authenticated:
        return redirect(f"{reverse('rango:login')}?next={request.path}")

    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('rango:index')
    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        return redirect('rango:index')

    # require login
    if not request.user.is_authenticated:
        return redirect(f"{reverse('rango:login')}?next={request.path}")

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.save()
            return redirect('rango:show_category', category_name_slug=category_name_slug)
    return render(request, 'rango/add_page.html', {'form': form, 'category': category})


def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request, 'rango/category.html', context=context_dict)


def register(request):
    """Handle user registration."""

    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()

            registered = True
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


def user_login(request):
    """Simple login view used by tests (named `login` in urls)."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('rango:index')
        else:
            # invalid login details; re-render login page with error
            return render(request, 'rango/login.html', {'error': 'Invalid login details.'})
    else:
        return render(request, 'rango/login.html', {})


def user_logout(request):
    """Log out the user and redirect to index."""
    logout(request)
    return redirect('rango:index')


def restricted(request):
    """A view that requires login; redirects to login if unauthenticated."""
    if not request.user.is_authenticated:
        return redirect(f"{reverse('rango:login')}?next={request.path}")

    return render(request, 'rango/restricted.html', {})