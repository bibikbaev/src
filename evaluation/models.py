import datetime

from django.db import models
from django.db.models import Avg, Count
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django import template
import pytz

register = template.Library()
TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))


class Companies(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=500, verbose_name='Название компании', blank=True, null=True)
    slug = models.SlugField(max_length=500, unique=True, verbose_name="URL")
    greeting = models.CharField(max_length=1000, verbose_name='Приветствие', blank=True, null=True, default='Оцените нас, пожалуйста')
    timezone = models.IntegerField(default=0, verbose_name='Часов относительно Москвовского времени', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('company', kwargs={'company_slug': self.slug})

    def get_absolute_url_reviews(self):
        return f'/reviews/{self.slug}/'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Компания (Филиал)'
        verbose_name_plural = 'Компании (Филиалы)'

    @property
    def calc_avg(self):
        a = Stars.objects.filter(company=self).aggregate(Avg('count'))['count__avg']
        avg = float('{:.1f}'.format(a))
        avg = str(avg).replace(",", ".")
        return avg

    @property
    def calc_count(self):
        cnt = Stars.objects.filter(company=self).count()
        return cnt

    @property
    def calc_five(self):
        score_count = Stars.objects.filter(company=self, count=5).count()
        return score_count

    @property
    def calc_four(self):
        score_count = Stars.objects.filter(company=self, count=4).count()
        return score_count

    @property
    def calc_three(self):
        score_count = Stars.objects.filter(company=self, count=3).count()
        return score_count

    @property
    def calc_two(self):
        score_count = Stars.objects.filter(company=self, count=2).count()
        return score_count

    @property
    def calc_one(self):
        score_count = Stars.objects.filter(company=self, count=1).count()
        return score_count

    @property
    def get_max(self):
        max_value = max(self.calc_one, self.calc_two, self.calc_three, self.calc_four, self.calc_five)
        return max_value

    @property
    def get_clicked(self):
        clicked_by_site = {}
        company_sites = CompanySites.objects.filter(company=self)
        print(company_sites)
        for cs in company_sites:
            clicked_by_site[cs.site.title] = cs.clicked
        print(clicked_by_site)
        return clicked_by_site


class Sites(models.Model):
    title = models.CharField(max_length=500, verbose_name='Название сайта', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Площадка'
        verbose_name_plural = 'Названия площадок'


class CompanySites(models.Model):
    company = models.ForeignKey(Companies, on_delete=models.SET_NULL, null=True)
    site = models.ForeignKey(Sites, on_delete=models.SET_NULL, null=True)
    link = models.CharField(max_length=2000, verbose_name='Ссылка', blank=True, null=True)
    clicked = models.IntegerField(default=0, verbose_name='Количество переходов', blank=True, null=True)

    class Meta:
        verbose_name = 'Площадка компании'
        verbose_name_plural = 'Площадки компаний'

    def __str__(self):
        return self.company.title + " на " + self.site.title


class Stars(models.Model):
    company = models.ForeignKey(Companies, on_delete=models.SET_NULL, null=True, verbose_name='Компания (Филиал)')
    count = models.CharField(max_length=4, verbose_name='Количество', blank=True, null=True)
    time = models.DateTimeField(default=timezone.now, verbose_name='Оставлено')
    message = models.CharField(max_length=2000, verbose_name='Отзыв', blank=True, null=True)
    contact_info = models.CharField(max_length=200, verbose_name='Контактная информация', blank=True, null=True)
    name = models.CharField(max_length=100, verbose_name='Имя', blank=True, null=True)

    def __str__(self):
        return self.count + " для " + self.company.title + " в " + self.time.strftime('%H:%M %d.%m.%Y')

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки пользователей'

    @property
    def get_time(self):
        time_with_tz = self.time + datetime.timedelta(hours=self.company.timezone)
        return time_with_tz


class People(models.Model):
    telegram_id = models.CharField(max_length=20, verbose_name='Айди')
    first_name = models.CharField(max_length=200, verbose_name='Имя', default='no first-name', null=True, blank=True)
    username = models.CharField(max_length=200, verbose_name='Никнейм', default='no nickname', null=True, blank=True)

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Человек'
        verbose_name_plural = 'Люди'


class PeopleCompany(models.Model):
    company = models.ForeignKey(Companies, on_delete=models.SET_NULL, null=True, verbose_name='Компания (Филиал)')
    person = models.ForeignKey(People, on_delete=models.SET_NULL, null=True, verbose_name='Человек')

    def __str__(self):
        return self.person.__str__() + " от " + self.company.__str__()

    class Meta:
        verbose_name = 'Получатель сообщений от компании'
        verbose_name_plural = 'Получатели сообщений от компаний'