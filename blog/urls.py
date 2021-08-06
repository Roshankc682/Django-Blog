from django.contrib import admin
from django.urls import path
from components import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index_page),
    path('register/', views.register),
    path('register_add', views.register_add),
    path('login/', views.login),
    path('logout', views.logout_view, name='logined'),
    path('login_data', views.login_data_check),
    path('dashboard', views.dashboard_user,name='dashboard'),
    path('settings/', views.dashboard_user, name='settings'),
    path('write_a_blog/', views.dashboard_user, name='write_a_blog'),
    path('edit_blog/', views.dashboard_user, name='edit_blog'),
    path('blog_saved', views.blog_user_saved, name='blog_saved_by_user'),
    path('Read', views.Read_more_by_user, name='Read_more_by_user'),
    path('upload_profile_pic', views.upload_profile_pic, name='upload_profile_pic'),
    path('Delete', views.Delete, name='Delete'),
    path('Edit', views.Edit, name='Edit'),
    path('finally_edited', views.finally_edited, name='finally_edited'),
    path('media/', views.dashboard_user, name='Media'),
    path('upload_profile_media', views.upload_profile_media, name='upload_profile_media'),
    path('delete_image', views.delete_image, name='delete_image'),
    path('readmore_details_blog', views.readmore_details_blog, name='readmore_details_blog'),
]

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
