"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django_project import settings
from django.urls import path, include
from django.conf.urls.static import static
from users.views import ShowProfile, LoginUser, logout_user, ProfileExample, AllReviews, CompanyReviews
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from evaluation.views import CustomPasswordChangeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profile-example/', ProfileExample.as_view(), name='profile-example'),
    path('profile/edit/', CustomPasswordChangeView.as_view(), name='profile-edit'),
    path('profile/', ShowProfile.as_view(), name='profile'),
    path('reviews/all/', AllReviews.as_view(), name='all-reviews'),
    path('reviews/<slug:company_slug>/', CompanyReviews.as_view(), name='company-reviews'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('qr_code/', include('qr_code.urls', namespace="qr_code")),
    path('', include('evaluation.urls')),
]
