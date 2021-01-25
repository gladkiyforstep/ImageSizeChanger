from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.image_upload_view),
    path('home/', views.home_page_view),
    path('changing_page/<int:pk>', views.changing_page_view)
]