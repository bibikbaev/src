from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', MainPage.as_view(), name='home'),
    path('update/', update, name='update'),
    path('<slug:company_slug>/', SendStar.as_view(), name='main'),
    path('<slug:company_slug>/addreview/', AddReview.as_view(), name='add_review'),
    path('<slug:company_slug>/review/', Review.as_view(), name='review'),
]