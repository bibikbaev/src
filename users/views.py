from django.db.models import Avg
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django_filters.views import FilterView

from .forms import ProfileUserForm
from evaluation.models import Companies, Stars
# Create your views here.


class LoginUser(LoginView):
    template_name = 'login.html'
    authentication_form = ProfileUserForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LoginUser, self).get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

    def get_success_url(self):
        return reverse_lazy('profile')


def logout_user(request):
    logout(request)
    return redirect('login')


# @login_required
# def ShowProfile(request):
#     return render(request, 'profile.html')


class ShowProfile(LoginRequiredMixin, ListView):
    template_name = 'profile.html'
    context_object_name = 'reviews'
    model = Companies
    login_url = 'login'

    def get_queryset(self):
        c = Companies.objects.filter(owner=self.request.user)
        print(c)
        s = Stars.objects.filter(company__in=c).order_by('-company','-time')
        print(s)

        return s

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ShowProfile, self).get_context_data(**kwargs)
        context['title'] = 'Личный кабинет'
        c = Companies.objects.filter(owner=self.request.user)

        return context


class AllReviews(LoginRequiredMixin, ListView):
    template_name = 'allreviews.html'
    context_object_name = 'reviews'
    model = Companies
    paginate_by = 4
    login_url = 'login'

    def get_queryset(self):
        c = Companies.objects.filter(owner=self.request.user)
        queryset = Stars.objects.filter(company__in=c).order_by('-time')

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AllReviews, self).get_context_data(**kwargs)
        context['title'] = 'Все отзывы'
        c = Companies.objects.filter(owner=self.request.user)
        context['companies'] = c
        return context


class CompanyReviews(LoginRequiredMixin, ListView):
    template_name = 'companyreviews.html'
    context_object_name = 'reviews'
    model = Companies
    paginate_by = 4
    login_url = 'login'

    def get_queryset(self):
        c = Companies.objects.get(slug=self.kwargs.get("company_slug"))
        s = Stars.objects.filter(company=c).order_by('-time')
        print(s)
        return s

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CompanyReviews, self).get_context_data(**kwargs)
        c = Companies.objects.filter(owner=self.request.user)
        context['companies'] = c
        print(context['companies'])
        context['company_slug'] = self.kwargs.get("company_slug")

        return context


class ProfileExample(TemplateView):
    template_name = "profile-example.html"

