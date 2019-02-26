from django.conf.urls import url, include
from . import views 


urlpatterns = [
    #login and registeration urls
    url(r'^$', views.index), 
    url(r'^register$', views.register), 
    url(r'^login$', views.login), 
    url(r'^home$', views.home),
    url(r'^quote_index$', views.added_quotes_index), 

    url(r'^logout$', views.logout),
    #quote dash app urls
    url(r'^myaccount/(?P<account_id>\d+)$', views.my_account),
    url(r'^updatedaccount/(?P<updated_account_id>\d+)$$', views.my_updated_account),
    
    url(r'^user/(?P<quote_view_id>\d+)$$', views.quote_view),

]
