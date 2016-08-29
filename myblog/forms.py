#coding:utf-8
from django import forms
from django.conf import settings
from django.db.models import Q  #对对象的复杂查询
from models import User
import re

#登陆form
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required",}),
                              max_length=50,error_messages={"required": "username不能为空",})
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required",}),
                              max_length=20,error_messages={"required": "password不能为空",})

#注册表单
class RegForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required",}),
                              max_length=50,error_messages={"required": "username不能为空",})
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "Email", "required": "required",}),
                              max_length=50,error_messages={"required": "email不能为空",})
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "required",}),
                              max_length=20,error_messages={"required": "password不能为空",})


#评论表单
class CommentForm(forms.Form):
    author = forms.CharField(widget=forms.TextInput(attrs={"id":"author","class":"comment_input",
                                                             "required":"required","size":"25","tabindex":"1"}),
                               max_length=50,error_messages={"required":"username不能为空",})
    email = forms.EmailField(widget=forms.TextInput(attrs={"id":"email","type":"email","class": "comment_input",
                                                           "required":"required","size":"25", "tabindex":"2"}),
                                 max_length=50, error_messages={"required":"email不能为空",})

    comment = forms.CharField(widget=forms.Textarea(attrs={"id":"comment","class": "message_input",
                                                           "required": "required", "cols": "25",
                                                           "rows": "5", "tabindex": "4"}),
                                                    error_messages={"required":"评论不能为空",})
    article = forms.CharField(widget=forms.HiddenInput())
