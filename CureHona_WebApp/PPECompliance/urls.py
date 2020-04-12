from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from django.views.generic import RedirectView

urlpatterns = [

    path('',RedirectView.as_view(url='PPECompliance/upload-image/'),name="home_page_ppe"),
    path('PPECompliance/upload-image/',views.UploadImage.as_view(),name="upload_Image_ppe"),
    path('PPECompliance/show-images/',views.ShowAllImages, name="show_all_images_ppe"),
    path('PPECompliance/del-image-list/<int:id>/<str:url>/',views.delete_image_list, name="delete_image_list_ppe"),
    path('PPECompliance/del-all-images/',views.delete_all_image, name="delete_all_image_ppe"),
    path('PPECompliance/gallery/',views.gallery, name='gallery_ppe'),

    # SnUsers login view
    path('register/',views.user_register,name='register'),
    path('login/',views.user_login,name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Controlling success url after login using default view
    path('accounts/profile/',RedirectView.as_view(url='/PPECompliance/upload-image/')),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
