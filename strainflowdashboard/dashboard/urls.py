from dashboard import views
from django.conf import settings
from django.views.static import serve
from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static



urlpatterns = [
    path('index/', views.IndexView.as_view(), name='plot')
]