from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.views import LoginView
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import *
from django.http.response import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView


def answer(request):
    return render(request, 'myApp/answer.html')


def about(request):
    return render(request, 'myApp/interface/about.html')


def contact(request):
    return render(request, 'myApp/interface/contact.html')


def payme(request):
    return render(request, 'myApp/interface/payme.html')


def grant_project_for_operator(request):
    obj = GrantProject.objects.all()
    context = {'object_list': obj}
    return render(request, 'myApp/interface/grant_project_for_operator.html', context)


class BusinessPlanAdd(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = BusinessPlan
    # form_class = BusinessForm
    template_name = 'myApp/admin/business_plan_add.html'
    fields = ['image', 'name_business', 'money_min', 'profit_year', 'profit_month', 'cost', 'text_min']
    success_url = reverse_lazy('business_admin_list_url')

    def test_func(self):
        return 'admin' == self.request.user.role


# Business Plan List
class BusinessPlanList(ListView):
    model = BusinessPlan
    template_name = 'myApp/index.html'


class BusinessPlanAdminList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    paginate_by = 10
    model = BusinessPlan
    template_name = 'myApp/admin/business_plan_list.html'

    def test_func(self):
        return 'admin' == self.request.user.role


class RegisterPage(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = AdminUserCreationForm
    success_url = reverse_lazy('login')
    template_name = "registration/registration.html"

    def test_func(self):
        return 'admin' == self.request.user.role

    def post(self, request, *args, **kwargs):
        if request.user.role != 'admin' or not request.user.is_superuser:
            raise PermissionError("You have not access to do this action")

        return super().post(request, *args, **kwargs)


class PetitiontAdd(CreateView):
    model = Petition
    form_class = PetitionForm
    template_name = 'myApp/petition_add.html'
    success_url = reverse_lazy('answer_url')


class PetitionList(ListView):
    model = Petition
    template_name = "myApp/petition_list.html"


class PetitionList(ListView):
    model = Petition
    template_name = 'myApp/petition_list.html'


class OrderList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    paginate_by = 10
    model = Order
    template_name = "myApp/operator/order_list.html"

    def test_func(self):
        return 'Operator' == self.request.user.role

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(operator_field=None)


class OperatorList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    paginate_by = 10
    model = Order
    template_name = "myApp/operator/operator_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(operator_field=self.request.user)

    def test_func(self):
        return 'Operator' == self.request.user.role


#
class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'myApp/order_detail.html'


class OrderUpdate(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'myApp/order_update.html'
    success_url = reverse_lazy('order_list_url')

    def post(self, request, *args, **kwargs):
        instance = Order.objects.get(id=kwargs['pk'])
        instance.operator_field = request.user
        instance.save()
        form = OrderForm(data=request.POST, instance=instance)

        if form.is_valid():
            form.save()
            return redirect('/order_list/')
        return render(request, self.template_name, {'form': form})

    # def post(self, request, *args, **kwargs):
    #
    #     if int(request.user.order_count()) < int(3):
    #         instance = Order.objects.get(id=kwargs['pk'])
    #         instance.operator_field = request.user
    #         instance.save()
    #         form = OrderForm(data=request.POST, instance=instance)
    #
    #         if form.is_valid():
    #             form.save()
    #             return redirect('/order_list/')
    #         return render(request, self.template_name, {'form': form})
    #     else:
    #         return HttpResponse("Iloji yo'q")


#
class UpdateOrderInOperator(LoginRequiredMixin, UpdateView):
    model = Order
    # specify the fields
    fields = ["first_name", "last_name", "province", "region", "business_name",
              "business_type", "payme"]
    success_url = reverse_lazy('operator_list_url')


class WorkerList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    paginate_by = 10
    model = Order
    template_name = "myApp/worker/worker_list.html"

    def test_func(self):
        return 'Worker' == self.request.user.role

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(Q(operator_field__isnull=False) and Q(payme__isnull=False), worker_field=None)


class WorkerUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'myApp/worker/worker_update.html'
    success_url = reverse_lazy('worker_list_url')

    def test_func(self):
        return 'Worker' == self.request.user.role

    def post(self, request, *args, **kwargs):
        if int(request.user.order_count()) < int(3):
            instance = Order.objects.get(id=kwargs['pk'])
            instance.worker_field = request.user
            instance.save()
            form = OrderForm(data=request.POST, instance=instance)

            if form.is_valid():
                form.save()
                return redirect('/worker_list/')
            return render(request, self.template_name, {'form': form})
        else:
            return render(request, 'myApp/worker/answer_worker.html')

    # def post(self, request, *args, **kwargs):
    #     instance = Order.objects.get(id=kwargs['pk'])
    #     instance.worker_field = request.user
    #     instance.save()
    #     form = OrderForm(data=request.POST, instance=instance)
    #
    #     if form.is_valid():
    #         form.save()
    #         return redirect('/worker_list/')
    #     return render(request, self.template_name, {'form': form})


class WorkerOrderUpdate(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Order
    form_class = WorkerOrderUpdate
    template_name = 'myApp/worker/worker_order_update.html'
    success_url = reverse_lazy('worker_order_list_url')

    def test_func(self):
        return 'Worker' == self.request.user.role

    def post(self, request, *args, **kwargs):
        instance = Order.objects.get(id=kwargs['pk'])
        if instance.status == 'bajarildi':
            pass
        #     request.user.worker_orders= request.user.order_count()-1
        #     instance.save()
        #     form = OrderForm(data=request.POST, instance=instance)
        #     if form.is_valid():
        #         form.save()
        #         return redirect('/order_list/')
        #     return render(request, self.template_name, {'form': form})
        # else:
        #     return HttpResponse(request.user.order_count())




class WorkerOrderList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    paginate_by = 10
    model = Order
    template_name = "myApp/worker/worker_order_listl.html"

    def test_func(self):
        return 'Worker' == self.request.user.role

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            Q(operator_field__isnull=False) and Q(payme__isnull=False) and Q(worker_field__isnull=False))


# Grant  Projects
class GrantProjectsAdd(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = GrantProject
    form_class = GrantForm
    template_name = 'myApp/admin/grant_project_create.html'
    success_url = reverse_lazy('grant_list_url')

    def test_func(self):
        return 'admin' == self.request.user.role


class GrantProjectDelete(DeleteView):
    model = GrantProject
    template_name = 'myApp/admin/grant_project_delete.html'
    success_url = reverse_lazy("grant_list_url")


# Grant Projects List
class GrantProjectList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    paginate_by = 10
    model = GrantProject
    template_name = "myApp/grant_project_list.html"

    def test_func(self):
        return 'admin' == self.request.user.role


# User List
class UserList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    paginate_by = 10
    model = User
    template_name = "myApp/admin/user_list.html"

    def test_func(self):
        return 'admin' == self.request.user.role

    # def get(self, request, *args, **kwargs):
    #     search_query = request.GET.get('search', '')
    #     if search_query:
    #         obj = User.objects.filter(Q(first_name__contains=search_query))
    #     else:
    #         obj = User.objects.all()
    #
    #     paginator = Paginator(obj, 4)
    #     page_number = request.GET.get('page', 1)
    #     page = paginator.get_page(page_number)
    #
    #     is_paginated = page.has_other_pages()
    #
    #     if page.has_previous():
    #         prev_url = '?page={}'.format(page.previous_page_number())
    #     else:
    #         prev_url = ''
    #     if page.has_next():
    #         next_url = '?page={}'.format(page.next_page_number())
    #     else:
    #         next_url = ''
    #     context = {
    #         'page_object': page,
    #         'next_url': next_url,
    #         'prev_url': prev_url,
    #         'is_paginated': is_paginated
    #     }
    #
    #     return render(request, 'myApp/user_list.html', context=context)


# Order Admin List
class OrderListAdmin(LoginRequiredMixin, UserPassesTestMixin, ListView):
    paginate_by = 3
    model = Order
    template_name = "myApp/admin/order_list_admin.html"

    # def get(self, request, *args, **kwargs):
    #     search_query = request.GET.get('search', '')
    #     if search_query:
    #         obj = Order.objects.filter(Q(first_name__contains=search_query))
    #     else:
    #         obj = Order.objects.all()
    #
    #     paginator = Paginator(obj, 4)
    #     page_number = request.GET.get('page', 1)
    #     page = paginator.get_page(page_number)
    #
    #     is_paginated = page.has_other_pages()
    #
    #     if page.has_previous():
    #         prev_url = '?page={}'.format(page.previous_page_number())
    #     else:
    #         prev_url = ''
    #     if page.has_next():
    #         next_url = '?page={}'.format(page.next_page_number())
    #     else:
    #         next_url = ''
    #     context = {
    #         'page_object': page,
    #         'next_url': next_url,
    #         'prev_url': prev_url,
    #         'is_paginated': is_paginated
    #     }
    #
    #     return render(request, '', context=context)

    def test_func(self):
        return 'admin' == self.request.user.role
