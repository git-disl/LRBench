from django.urls import path, include
from LRBench import views

urlpatterns = [
	path('',views.lr_form_process,name='blog-form'),
    path('about/', views.about, name='blog-about'),
    path('', views.home, name='blog-home'),
    path('results/',views.results,name='blog-results'),

]




