import sys
sys.path.append("D:/Django-Workspace/RestServer/cntk_api")

from django.conf.urls import url
from app import views

urlpatterns = [
    # Projeto Intelligent Promoter
    url(r'^intelligent_promoter/image/$', views.supermercado),



    # essas duas URLS podem ser usadas por qualquer projeto
    url(r'^online/$', views.online),
    url(r'^index/$', views.index),
    
    # Projeto Identificador de Fungos - Gabriel
    # Coloquem suas Urls aqui abaixo
    #\/ \/ \/ \/ \/ \/ 
 
    # Projeto Identificador de Fungos - Gabriel
    # Coloquem suas Urls aqui abaixo
    #\/ \/ \/ \/ \/ \/ 
    url(r'^agricultura/image/$', views.agricultura)

]