from django.conf.urls import  url
from myblog import views



urlpatterns = [

    url(r'^$',views.index,name='index'),
    url(r'^archive/$',views.archive,name='archive'),
    url(r'^article/$',views.article,name='article'),
    url(r'^comment/post/$',views.comment_post,name='comment_post'),
    url(r'^logout/$',views.do_logout,name='logout'),
    url(r'^reg/$',views.do_reg,name='reg'),
    url(r'^login/$',views.do_login,name='login'),
    url(r'^category/$',views.category,name='category'),
    url(r'^tag/$',views.tag,name='tag'),

]
