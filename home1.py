from django.core.management import execute_from_command_line
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import path
from django.conf import settings

import this
from random import choice
import importlib

# URL
# https://docs.python.org # /3/library/index.html path

settings.configure(
    DEBUG=True,
    ROOT_URLCONF=__name__,
    SECRET_KEY='l1SdwXef42cXGspXsQnSh3pPbdgjLGLK6yumM5XYcX52rFBOZDmnCALjxMOiKqBs'
)


def handler(request):
    text = ''.join(this.d.get(c, c) for c in this.s)
    title, _, *quotes = text.splitlines()

    template = f"""
    <!DOCTYPE html>
    <html>
     <head>
      <title>{title}</title>
     </head>
     <body>
      <h1>{choice(quotes)}</h1>
     </body>
    </html>
    """
    return HttpResponse(template)


def mod_handler(request, mod_name):
    try:
        my_module = importlib.import_module(mod_name)
    except:
        return HttpResponseNotFound('404')

    links = [
        f'<a href="{name}">{name}</a><br>' for name in dir(my_module) if not name.startswith('_')
    ]

    template = f"""
        <!DOCTYPE html>
        <html>
         <head>
          <title>{mod_name}</title>
         </head>
         <body>
          <h1>Objects for {mod_name}</h1>
          {''.join(links)}
         </body>
        </html>
        """
    return HttpResponse(template)


def obj_handler(request, mod_name, obj_name):
    try:
        my_module = importlib.import_module(mod_name)
        my_object = getattr(my_module, obj_name)
    except:
        return HttpResponseNotFound('404')

    return HttpResponse(f'<pre>{my_object.__doc__}</pre>')


urlpatterns = [
  path('', handler),
  path('doc/<mod_name>/', mod_handler),
  path('doc/<mod_name>/<obj_name>', obj_handler),
]


if __name__== '__main__':
    execute_from_command_line()
