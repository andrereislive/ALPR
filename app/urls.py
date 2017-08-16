import sys
sys.path.append("C:\Web Services\Web Service - ALPR\ALPR\cntk_api")

from django.conf.urls import url
from app import views

urlpatterns = [
    # Projeto Intelligent Promoter
    url(r'^alpr/$', views.plateRecognition),



    # essas duas URLS podem ser usadas por qualquer projeto
    url(r'^online/$', views.online),
    url(r'^index/$', views.index),
    
  

]