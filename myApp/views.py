from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.views import LoginView
from .forms import AdminUserCreationForm, OrderForm, PetitionForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import *
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
    template_name = 'myApp/petition_list.html'


class OrderList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Order
    template_name = 'myApp/order_list.html'

    def test_func(self):
        return 'Operator' == self.request.user.role

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(operator_field=None)


class OperatorList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Order
    template_name = "myApp/operator_list.html"

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


#
class UpdateOrderInOperator(LoginRequiredMixin, UpdateView):
    model = Order
    # specify the fields
    fields = ["first_name", "last_name", "province", "region", "business_name",
              "business_type", "payme"]
    success_url = reverse_lazy('operator_list_url')


class WorkerList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Order
    template_name = "myApp/worker_list.html"

    def test_func(self):
        return 'Worker' == self.request.user.role

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(Q(operator_field__isnull=False) and Q(payme__isnull=False), worker_field=None)


class WorkerUpdate(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'myApp/worker_update.html'
    success_url = reverse_lazy('worker_list_url')

    def post(self, request, *args, **kwargs):
        instance = Order.objects.get(id=kwargs['pk'])
        instance.worker_field = request.user
        instance.save()
        form = OrderForm(data=request.POST, instance=instance)

        if form.is_valid():
            form.save()
            return redirect('/worker_list/')
        return render(request, self.template_name, {'form': form})


class WorkerOrderList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Order
    template_name = "myApp/worker_list.html"

    def test_func(self):
        return 'Worker' == self.request.user.role

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            Q(operator_field__isnull=False) and Q(payme__isnull=False) and Q(worker_field__isnull=False))
