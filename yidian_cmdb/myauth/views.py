# -*- coding:utf8 -*-
# Author: Chenxc
# Email: chenxiaochen@yidian-inc.com
# Date: 2016-07-27
from django.views.generic import TemplateView, FormView, ListView, CreateView, UpdateView, DeleteView
from utils.mixins import MyPermissionRequiredMixin
from models import MyUser
from django.contrib.auth.models import Group
from forms import MyUserCreationForm, MyUserUpdateForm, MyAdminPasswordChangeForm, GroupForm
from django.core.urlresolvers import reverse_lazy


class CurrentUserDashboardView(TemplateView):
    """
    登录用户详细信息
    """
    template_name = "myauth/user_detail.html"


class UserListView(MyPermissionRequiredMixin, ListView):
    """
    用户列表
    """
    permission_required = 'myauth.read_user'

    model = MyUser
    ordering = '-date_joined'
    template_name = 'myauth/users.html'


class UserCreationView(MyPermissionRequiredMixin, CreateView):
    """
    创建用户
    """
    permission_required = 'myauth.add_user'

    model = MyUser
    form_class = MyUserCreationForm
    template_name = 'myauth/user_creation.html'

    def get_success_url(self):
        return reverse_lazy('myauth-user-update', kwargs={'user_id': self.object.id})


class UserUpdateView(MyPermissionRequiredMixin, UpdateView):
    """
    更新用户
    """
    permission_required = 'myauth.change_user'

    model = MyUser
    pk_url_kwarg = 'user_id'
    form_class = MyUserUpdateForm
    template_name = 'myauth/user_update.html'
    success_url = reverse_lazy('myauth-user-list')


class UserPasswordResetView(MyPermissionRequiredMixin, FormView):
    """
    管理员重置用户密码
    """
    permission_required = 'myauth.change_myuser'

    form_class = MyAdminPasswordChangeForm
    template_name = 'myauth/user_password_reset.html'
    success_url = reverse_lazy('myauth-user-list')

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request.user, **self.get_form_kwargs())


class UserDeletionView(MyPermissionRequiredMixin, DeleteView):
    """
    删除用户
    """
    permission_required = 'myauth.delete_myuser'

    model = MyUser
    pk_url_kwarg = 'user_id'
    success_url = reverse_lazy('myauth-user-list')


class GroupListView(MyPermissionRequiredMixin, ListView):
    """
    用户组列表
    """
    permission_required = 'auth.add_group'

    model = Group
    template_name = 'myauth/groups.html'


class GroupCreationView(MyPermissionRequiredMixin, CreateView):
    """
    创建用户组
    """
    permission_required = 'auth.add_group'

    model = Group
    form_class = GroupForm
    template_name = 'myauth/group_creation.html'
    success_url = reverse_lazy('myauth-group-list')


class GroupUpdateView(MyPermissionRequiredMixin, UpdateView):
    """
    更新用户组
    """
    permission_required = 'auth_change_group'

    model = Group
    form_class = GroupForm
    pk_url_kwarg = 'group_id'
    template_name = 'myauth/group_update.html'
    success_url = reverse_lazy('myauth-group-list')


class GroupDeletionView(MyPermissionRequiredMixin, DeleteView):
    """
    删除用户组
    """
    permission_required = 'auth.delete_group'

    model = Group
    pk_url_kwarg = 'group_id'
    success_url = reverse_lazy('myauth-group-list')
