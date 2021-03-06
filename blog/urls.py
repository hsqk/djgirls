from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.clothes_list, name='clothes_list'),

    url(r'^seller/$', views.seller_list, name='seller_list'),
    url(r'^seller/new/$', views.seller_new, name='seller_new'),
    url(r'^seller/(?P<pk>\d+)/edit/$', views.seller_edit, name='seller_edit'),
    url(r'^seller/(?P<pk>\d+)/remove/$', views.seller_remove, name='seller_remove'),
    
    url(r'^event_stats/$', views.event_stats, name='event_stats'),
    
    url(r'^clothes/new/$', views.clothes_new, name='clothes_new'),
    url(r'^clothes/(?P<pk>\d+)/edit/$', views.clothes_edit, name='clothes_edit'),
    url(r'^clothes/(?P<pk>\d+)/remove/$', views.clothes_remove, name='clothes_remove'),
    
    url(r'^sale/$', views.sale, name='sale'),
    url(r'^refund/$', views.refund, name='refund'),
    url(r'^transaction_details/$', views.transaction_details, name='transaction_details'),
    
    url(r'^recycle/$', views.recycle, name='recycle'),
    url(r'^return/$', views.return_to_owner, name='return'),
    
    url(r'^settlement/$', views.settlement, name='settlement'),
    url(r'^unsettled/$', views.unsettled, name='unsettled'),

]



"""
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),
"""
