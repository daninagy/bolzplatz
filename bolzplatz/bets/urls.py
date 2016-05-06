from django.conf.urls import include, url, patterns

urlpatterns = patterns('',
                       url(r'^$', 'bets.views.home', name='bets_home'),)


