from django.views.generic import ListView, FormView
from evaluation.models import *
from .forms import StarsForm, MessageForm
from .models import Stars
from django.shortcuts import get_object_or_404
from django.contrib import messages
from evaluation.management.commands.telegramm import send_message, update_message
from django.http import JsonResponse
from json import dumps
from django.views.generic import TemplateView, UpdateView
import json
from django.urls import reverse_lazy
from .forms import ProfileUserForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin


class SendStar(FormView):
    template_name = 'main.html'
    form_class = StarsForm
    is_good = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SendStar, self).get_context_data(**kwargs)
        context['title'] = 'Оценить'
        context['company'] = Companies.objects.get(slug=self.kwargs.get("company_slug"))
        return context

    def get_object(self):
        return get_object_or_404(Companies, slug=self.kwargs.get("company_slug"))

    def form_valid(self, form):
        count_stars = form.cleaned_data.get("rating")

        c = Companies.objects.get(slug=self.kwargs.get("company_slug"))
        s = Stars.objects.create(company=c, count=count_stars)
        self.request.session['rew'] = s.id
        message = "На " + c.title + " поставили оценку " + str(count_stars)

        if int(count_stars) >= 4:
            self.is_good = True
        else:
            self.is_good = False
            message += " без комментария"   # добавлять текст без комментария только при плохой оценке

        p = PeopleCompany.objects.filter(company=c)  # выбор людей, которые получают отзывы от этой компании

        id_list = list()
        for i in range(len(p)):
            id_list.append(p[i].person.telegram_id)  # заполнение списка с id таких людей

        sent = send_message(message, id_list)

        dict_sent = {}
        for i in range(len(sent)):
            dict_sent[sent[i].chat.id] = sent[i].message_id

        self.request.session['dict_sent'] = dict_sent
        self.request.session['msg'] = message
        return super().form_valid(form)

    def get_success_url(self):
        success_url_for_good = 'add_review'
        success_url_for_bad = 'review'
        if self.is_good:
            return reverse(success_url_for_good, kwargs={'company_slug': self.kwargs.get("company_slug")})
        else:
            return reverse(success_url_for_bad, kwargs={'company_slug': self.kwargs.get("company_slug")})


class Review(FormView):
    template_name = 'review.html'
    form_class = MessageForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Review, self).get_context_data(**kwargs)
        context['title'] = 'Оценить'
        return context

    def get_object(self):
        return get_object_or_404(Companies, slug=self.kwargs.get("company_slug"))

    def form_valid(self, form):
        review_id = self.request.session.get('rew')
        dict_sent = self.request.session.get('dict_sent')

        review_text = form.cleaned_data.get("review_text")
        contact_info = form.cleaned_data.get("contact_info")
        name = form.cleaned_data.get("name")

        print("review_text")
        print(review_text)

        print("contact_info")
        print(contact_info)

        print("name")
        print(name)

        r = Stars.objects.get(pk=review_id)
        message = "На " + r.company.title + " поставили оценку " + str(r.count)

        if review_text:
            r.message = review_text
            r.save(update_fields=["message"])
            message += "\n\nОставили отзыв:\n" + review_text

        if contact_info:
            r.contact_info = contact_info
            r.save(update_fields=["contact_info"])
            message += "\n\nОставили контакты:\n" + contact_info

        if name:
            r.name = name
            r.save(update_fields=["name"])
            message += "\n\nИмя:\n" + name

        if review_text or contact_info or name:
            messages.success(self.request, 'Спасибо, ваш отзыв обязательно будет прочитан!')
            update_message(message, dict_sent)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('review', kwargs={'company_slug': self.kwargs.get("company_slug")})


class AddReview(ListView):
    model = CompanySites
    template_name = 'addreview.html'
    context_object_name = 'links'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AddReview, self).get_context_data(**kwargs)
        context['title'] = 'Выбор площадки'
        context['data'] = self.request.session.get('dict_sent')
        context['msg'] = self.request.session.get('msg')
        context['company_slug'] = self.kwargs.get("company_slug")
        return context

    def get_queryset(self):
        c = Companies.objects.get(slug=self.kwargs.get("company_slug"))
        return CompanySites.objects.filter(company=c)


def update(request):
    print("THIS IS REQUEST")
    if request.method == 'POST':
        dict_sent = request.POST

        print(dict_sent)
        res = request.POST['sended'].replace("\'", "\"")
        res = json.loads(res)

        msg = request.POST['message']
        msg += '. Гость перешёл нa ' + request.POST['site'] + ', возможно, скоро там появится новый отзыв :)'
        update_message(msg, res)

        s = CompanySites.objects.get(company__slug=request.POST['company'], site__title=request.POST['site'])
        s.clicked += 1
        s.save(update_fields=["clicked"])

    return JsonResponse({"success": True}, status=200)


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'edit_profile.html'
    success_url = reverse_lazy('profile-edit')
    login_url = 'login'

    def form_valid(self, form):
        messages.success(self.request, 'Пароль успешно изменён.')
        return super().form_valid(form)


class MainPage(TemplateView):
    template_name = 'home.html'
