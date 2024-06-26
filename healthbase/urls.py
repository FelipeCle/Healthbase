"""
URL configuration for healthbase project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('registro/', views.registro, name='registro'),
    path('menu/', views.menu, name='menu'),
    path('conta/', views.conta, name='conta'),
    path('modificarcartao/', views.modificarcartao, name='modificarcartao'),
    path('modificarcartao/', views.modificarcartao, name='modificarcartao'),
    path('encomendar_indicadores/', views.encomendar_indicadores, name='encomendar_indicadores'),
    path('encomendar_sucesso/', views.encomendar_sucesso, name='encomendar_sucesso'),
    path('visualizar_cobrancas/', views.visualizar_cobrancas, name='visualizar_cobrancas'),
    path('meupainel/', views.meupainel, name='meupainel'),
    path('alterar_senha/', views.alterar_senha, name='alterar_senha'),
]



