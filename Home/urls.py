from django.contrib import admin
from django.urls import path
from Home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'), #views.about is your funcation name in urls file, thn about is path of your site, name is idk
    path('songs', views.songs, name='songs')
    # path('services', views.services, name='services'),

]

admin.site.site_header = "Admin Panel"
admin.site.site_title = "Ubtohts"
admin.site.index_title = "Lets check the user searching data"