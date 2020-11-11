from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('profilo/<str:user>/<int:id>', views.profilo, name='profilo')
]
