from django.urls import path

from ads_app import views

urlpatterns = [
    path('index/', views.Home.as_view(), name='index'),
    path('my-ads/', views.MyAds.as_view(), name='my_ads'),
    path('add-ad/', views.AddAd.as_view(), name='add_ad'),
    path('edit-ad/<int:pk>/', views.UpdateAd.as_view(), name='edit_ad'),
    path('delete-ad/<int:pk>/', views.DeleteAd.as_view(), name='delete_ad'),
    path('offer/<int:pk>/', views.ExchangeOffer.as_view(), name='exchange_offer'),
    path('list-offers/', views.ExchangeOfferList.as_view(), name='list_offers'),
    path('offer/<int:pk>/action/', views.offer_action, name='offer_action'),
    path('my-list-offers/', views.MyExchangeProposalsList.as_view(), name='my_list_offers'),
    path('auth/login/', views.LoginUser.as_view(), name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
]
