import os
import django

# set up django environment for standalone scripts
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')
django.setup()

from rango.models import Category, Page


def add_cat(name, views=0, likes=0):
    cat, created = Category.objects.get_or_create(name=name)
    cat.views = views
    cat.likes = likes
    cat.save()
    return cat


def add_page(cat, title, url, views=0):
    page, created = Page.objects.get_or_create(category=cat, title=title)
    page.url = url
    page.views = views
    page.save()
    return page


def populate():
    # Python category
    python_cat = add_cat('Python', views=128, likes=64)
    add_page(python_cat, 'Official Python Tutorial', 'http://docs.python.org/3/', views=50)
    add_page(python_cat, 'How to Think like a Computer Scientist', 'http://www.greenteapress.com/thinkpython/', views=30)
    add_page(python_cat, 'Learn Python in 10 Minutes', 'http://www.korokithakis.net/tutorials/python/', views=20)

    # Django category
    django_cat = add_cat('Django', views=64, likes=32)
    add_page(django_cat, 'Official Django Tutorial', 'https://docs.djangoproject.com/en/2.2/intro/tutorial01/', views=40)
    add_page(django_cat, 'Django Rocks', 'http://www.djangorocks.com/', views=25)
    add_page(django_cat, 'How to Tango with Django', 'http://www.tangowithdjango.com/', views=30)

    # Other frameworks
    other_cat = add_cat('Other Frameworks', views=32, likes=16)
    add_page(other_cat, 'Bottle', 'http://bottlepy.org/docs/dev/', views=10)
    add_page(other_cat, 'Flask', 'http://flask.pocoo.org', views=15)

    print("Population complete!")


if __name__ == '__main__':
    populate()
