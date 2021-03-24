"""DjangoAppCenter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path

from DjangoAppCenter.settings import load_settings
from DjangoAppCenter.signals import restart

SETTINGS = load_settings()


def restart_server(request):
    restart.RELOAD_SIGNAL.send(sender="xxx")
    return HttpResponse("")


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('admin/restart', restart_server)
]

routers = SETTINGS.get('routers', [])

# {path: 'app/', model:'app', handler: 'app.api' }
# 动态导入包
for router in routers:
    # model = importlib.import_module(router['urls'])
    urlpatterns.append(
        path(router['path'], include(router['urls'])))
