from django.urls import path

from ads_app import views

urlpatterns = [
    path('index/', views.Home.as_view(), name='index'),
    path('my-ads/', views.MyAds.as_view(), name='my_ads'),
    path('add-ad/', views.AddAd.as_view(), name='add_ad'),
    path('edit-ad/<int:pk>/', views.UpdateAd.as_view(), name='edit_ad'),
]
