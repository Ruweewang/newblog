#coding:utf-8
import logging
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.hashers import make_password #django内置密码加密
from django.conf import settings
from django.db import connection
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db.models import Count
from models import *
from forms import *
# Create your views here.

#使用自己定义的日志器
logger = logging.getLogger('myblog.views')


def global_setting(request):
    #站点基本信息
    SITE_DESC = settings.SITE_DESC
    WEIBO_SINA = settings.WEIBO_SINA
    WEIBO_TENCENT = settings.WEIBO_TENCENT
    PRO_RSS = settings.PRO_RSS
    PRO_EMAIL = settings.PRO_EMAIL
    SITE_NAME = settings.SITE_NAME
    #分类信息获取（导航数据）
    category_list = Category.objects.all()
    #文章归档数据
    archive_list = Article.objects.distinct_date()
    #广告数据
    ad_imgurl_list=Ad.objects.filter(status=True)
    article_click_list = Article.objects.all().order_by('-click_count')[:6]
    article_recommend_list = Article.objects.all().order_by('is_recommend')[:6]
    #标签云数据
    tag_list = Tag.objects.all()
    #友情链接数据
    links_list = Links.objects.all()
    #文章排行榜数据

    #评论排行
    comment_count_list = Comment.objects.values('article').annotate(comment_count=Count('article')).order_by('-comment_count') #聚合函数
    article_comment_list = [Article.objects.get(pk=comment['article']) for comment in comment_count_list][:6]
    #Article.objects.all().
    return locals()

#分页
def getPage(request,article_list):
    paginator = Paginator(article_list,5) #分页显示
    try:
        page = int(request.GET.get('page',1))  #获取当前的页码，否则返回第一页
        article_list = paginator.page(page)  #返回当前页的数据
    except (InvalidPage, EmptyPage, PageNotAnInteger):
        article_list = paginator.page(1) #输入不规范时，显示第一页
    return article_list

def index(request):
    try:
        #分类信息获取（导航数据）
        #category_list = Category.objects.all()

        #最新文章数据
        article_list = Article.objects.all()
        article_list = getPage(request,article_list)
        #文章归档
        #archive_list = Article.objects.distinct_date()

    except Exception as e:
        logger.error(e)
    return render(request, 'index.html',locals())

def archive(request):
    try:
        year = request.GET.get('year',None)
        month = request.GET.get('month',None)
        article_list = Article.objects.filter(date_publish__icontains=year+'-'+month) #根据发布日期做模糊查询
        article_list = getPage(request,article_list)
    except Exception as e:
        logger.error(e)

    return render(request, 'archive.html',locals())



#文章详情
def article(request):
    try:
        id = request.GET.get('id',None) #获取文章id
        try:
            article = Article.objects.get(pk=id)  #把用户传递的id用于文章查询
            article.click_count += 1
            article.save() #保存浏览次数
        except Article.DoesNotExist:
            return render(request,'failure.html',{'reason':'没有找到相应文章'})
        # 评论表单,初始化表单对象
        comment_form = CommentForm({'author': request.user.username,
                                    'email': request.user.email,
                                    'article': id} if request.user.is_authenticated() else{'article': id}) #登陆后初始化，否则只显示id
        #获取评论信息
        comments = Comment.objects.filter(article=article).order_by('id') #取出文章的评论
        commentsnum = len(comments)
        comment_list = [] #定义评论容器，存放评论
        for comment in comments:
            for item in comment_list:
                if not hasattr(item, 'children_comment'): #判断当前评论里是否有子评论
                    setattr(item, 'children_comment',[])  #添加子评论到当前评论
                if comment.pid == item: #判断当前评论是否有父级评论，若有，判断是否是当前评论的父评论
                    item.children_comment.append(comment) #添加当前评论的子评论到子评论列表
                    break
            if comment.pid is None:  #这个评论不是其它评论的子评论
                comment_list.append(comment)
    except Exception as e:
        logger.error(e)
    return render(request,'article.html',locals())

#发表评论，提交评论
def comment_post(request):
    try:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            #获取表单信息
            comment = Comment.objects.create(username=comment_form.cleaned_data['author'],  #创建评论对象进行初始化
                                             email = comment_form.cleaned_data['email'],
                                             content = comment_form.cleaned_data['comment'],
                                             article_id = comment_form.cleaned_data['article'],
                                             user = request.user if request.user.is_authenticated() else None

                                             )
            comment.save()
        else:
            return render(request,'failure.html',{'reason':comment_form.errors})
    except Exception as e:
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])

#注销
def do_logout(request):
    try:
        logout(request)
    except Exception as e:
        logger.error(e)
    return redirect(request.META['HTTP_REFERER'])

#注册
def do_reg(request):
    try:
        if request.method == 'POST':
            reg_form = RegForm(request.POST)
            if reg_form.is_valid():
                #注册
                user = User.objects.create(username=reg_form.cleaned_data['username'], #用模板表单的数据赋值
                                           email = reg_form.cleaned_data['email'],
                                           password = make_password(reg_form.cleaned_data['password']),
                                           )
                user.save()

                #登陆
                user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                login(request,user)
                return redirect(request.POST.get('source_url'))
            else:
                return render(request,'failure.html',{'reason':reg_form.errors})
        else:
            reg_form = RegForm() #通过get提交表单重新返回注册页面
    except Exception as e:
        logger.error(e)
    return render(request, 'reg.html',locals())


# 登录
def do_login(request):
    try:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                # 登录
                username = login_form.cleaned_data["username"] #得到用户提交的用户名
                password = login_form.cleaned_data["password"] #得到用户提交的密码
                user = authenticate(username=username, password=password)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                    login(request, user)
                else:
                    return render(request, 'failure.html', {'reason': '登录验证失败'})
                return redirect(request.POST.get('source_url'))  #根据source_url隐藏域跳转回源地址
            else:
                return render(request, 'failure.html', {'reason': login_form.errors})
        else:
            login_form = LoginForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'login.html', locals())


def category(request):
    try:
        # 先获取客户端提交的信息
        cid = request.GET.get('id', None)
        try:
            category = Category.objects.get(pk=cid)
        except Category.DoesNotExist:
            return render(request, 'failure.html', {'reason': '分类不存在'})
        article_list = category.article_set.all()
        article_list = getPage(request, article_list)
    except Exception as e:
        logger.error(e)
    return render(request, 'category.html', locals())



def tag(request):
    try:
        id = request.GET.get( "id", None)
        tag=Tag.objects.get(pk=id)
        tagarticle_list = tag.article_set.all()
        article_list=getpage(request,tagarticle_list)
    except Exception as e:
        logger.error(e)
    return render(request, 'tag_archive.html', locals())



























