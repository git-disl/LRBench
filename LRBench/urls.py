from django.urls import path
from LRBench import views

urlpatterns = [
	path('',views.lr_form_process,name='blog-form'),
    path('about/', views.about, name='blog-about'),
    path('', views.home, name='blog-home'),
    path('results/',views.results,name='blog-results'),
    path('visualize/',views.visualize,name='blog-visualize'),
    path('visualize/data/', views.pivot_data, name='pivot_data'),
    path('apply-lr-schedule/', views.apply_lr_schedule, name='apply-lr-schedule'),
]