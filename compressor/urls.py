from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.image_upload_view),
    path('home', views.home),
    path('changing_page/<int:pk>', views.change)
]