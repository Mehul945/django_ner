from django.urls import path,include
from . import views
handler404 = 'invoice_ner.views.custom_404'

urlpatterns = [
    path('', views.home,name='home'),
    path('upload_file', views.invoice_extract,name='upload'),
    path('change_values',views.update_data,name='home'),
    path('download',views.download_json,name='download_json'),
    path('download_txt',views.download_txt,name='download_txt'),
    path('login',views.login,name='login'),
    path('signup',views.signup,name='signup'),
    path('logout',views.logout,name='logout'),
]
 