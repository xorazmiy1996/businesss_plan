from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import *
from datetime import datetime, timedelta
from django.http.response import HttpResponse, JsonResponse
from django.core.paginator import Paginator


def answer(request):
    return render(request, 'myApp/answer.html')


def about(request):
    obj = Team.objects.all()
    context = {'object_list': obj}
    return render(request, 'myApp/interface/about.html', context)


def contact(request):
    return render(request, 'myApp/interface/contact.html')


def payme(request):
    return render(request, 'myApp/interface/payme.html')


def reyting(request):
    return render(request, 'myApp/operator/reyting.html')


def bouns(request):
    return render(request, 'myApp/operator/bouns.html')


def admin_reyting(request):
    return render(request, 'myApp/admin/reyting_admin.html')


def grant_project_front(request):
    obj = GrantProject.objects.all()
    context = {'object_list': obj}
    return render(request, 'myApp/interface/grant_project_for_operator.html', context)


class BusinessPlanAdd(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = BusinessPlan
    form_class = BusinessForm
    template_name = 'myApp/admin/business_plan_add.html'
    success_url = reverse_lazy('business_admin_list_url')

    def test_func(self):
        return 'admin' == self.request.user.role


# Business Plan List
class BusinessPlanList(ListView):
    paginate_by = 9
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
    # template_name = "myApp/operator/order_list.html"
    template_name = "myApp/operator/order_list.html"

    def test_func(self):
        return 'Worker' == self.request.user.role or 'Operator' == self.request.user.role

    def get_queryset(self):
        queryset = super().get_queryset()
        # print(self.request.GET.get('search', ''))
        return queryset.filter(Q(phone_number__contains=self.request.GET.get('search', ''), operator_field=None))


class OperatorList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    paginate_by = 10
    model = Order
    template_name = "myApp/operator/operator_list.html"

    def test_func(self):
        return 'Worker' == self.request.user.role or 'Operator' == self.request.user.role

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(Q(payme__isnull=False, operator_field__isnull=False), worker_field=self.request.user,
                               status='False')


class OrderUpdate(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm

    template_name = 'myApp/operator/order_update.html'
    success_url = reverse_lazy('order_list_url')

    def post(self, request, *args, **kwargs):
        instance = Order.objects.get(id=kwargs['pk'])
        instance.operator_field = request.user
        instance.petition_type = 'site'

        instance.save()
        form = OrderForm(data=request.POST, instance=instance)
        #
        print('salom')
        print('salom')
        print('salom')
        print('salom')
        print(request.GET)
        print(request.POST)
        # print(form.cleaned_data)

        if form.is_valid():
            form.save()
            return redirect('/order_list/')
        return render(request, self.template_name, {'form': form})


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
        return 'Operator' == self.request.user.role

    def get_queryset(self):
        queryset = super().get_queryset()
        # return queryset.filter(Q(operator_field__isnull=False) and Q(payme__isnull=False) , worker_field=None)
        return queryset.filter(Q(operator_field__isnull=False, payme__isnull=False),
                               first_name__contains=self.request.GET.get('search', ''), worker_field=None)


class WorkerUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Order

    # fields = ['add_phone_number', 'first_name', 'last_name', 'business_name', 'price']
    fields = '__all__'
    template_name = 'myApp/worker/worker_update.html'
    success_url = reverse_lazy('operator_list_url')

    def test_func(self):
        return 'Worker' == self.request.user.role or 'Operator' == self.request.user.role

    def post(self, request, *args, **kwargs):
        instance = Order.objects.get(id=kwargs['pk'])
        instance.worker_field = request.user
        instance.save()

        # form = OrderForm(data=request.POST, instance=instance)
        #
        # if form.is_valid():
        #     form.save()
        return redirect('/paid_orders/')
        # return render(request, self.template_name, {'form': form})


class WorkerOrderUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Order
    form_class = WorkerOrderUpdate
    template_name = 'myApp/worker/worker_order_update.html'
    success_url = reverse_lazy('worker_order_list_url')

    def test_func(self):
        return 'Worker' == self.request.user.role


class WorkerOrderList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    paginate_by = 10
    model = Order
    template_name = "myApp/worker/worker_order_listl.html"

    def test_func(self):
        return 'Worker' == self.request.user.role

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            Q(operator_field__isnull=False, payme__isnull=False, worker_field__isnull=False, status=False),
            Q(first_name__contains=self.request.GET.get("search", '')))


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
    template_name = "myApp/admin/grant_project_list.html"

    def test_func(self):
        return 'admin' == self.request.user.role


# User List
class UserList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    paginate_by = 10
    model = User
    template_name = "myApp/admin/user_list.html"

    def test_func(self):
        return 'admin' == self.request.user.role

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(Q(first_name__contains=self.request.GET.get('search', '')))


class BusinessPlanDetail(DetailView):
    model = BusinessPlan
    template_name = 'myApp/business_plan_detail.html'


class BusinessPlanDelete(DeleteView):
    model = BusinessPlan
    template_name = 'myApp/admin/business_plan_delete.html'
    success_url = reverse_lazy("business_admin_list_url")


class FinalOrdersList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    paginate_by = 10
    model = Order
    template_name = 'myApp/admin/final_order_list.html'

    def test_func(self):
        return 'admin' == self.request.user.role

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            Q(operator_field__isnull=False, payme__isnull=False, worker_field__isnull=False, status=True),
            Q(first_name__contains=self.request.GET.get("search", '')))


class UnFinishedOrdersList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    paginate_by = 10
    model = Order
    template_name = 'myApp/admin/unfinished_orders_list.html'

    def test_func(self):
        return 'admin' == self.request.user.role

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            Q(operator_field__isnull=False, payme__isnull=False, worker_field__isnull=False, status=False),
            Q(first_name__contains=self.request.GET.get("search", '')))


class UnSeenOrdersList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    paginate_by = 10
    model = Order
    template_name = 'myApp/admin/unseen_orders_list.html'

    def test_func(self):
        return 'admin' == self.request.user.role

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            Q(operator_field__isnull=True),
            Q(first_name__contains=self.request.GET.get("search", '')))


class NotInterestedList(ListView):
    paginate_by = 10
    model = Order
    template_name = 'myApp/admin/not_interested_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            Q(operator_field__isnull=False, business_type='qiziqmadi'))


class AcceptedOrdersList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    paginate_by = 10
    model = Order
    template_name = 'myApp/admin/accepted_orders_list.html'

    def test_func(self):
        return 'admin' == self.request.user.role

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            Q(operator_field__isnull=False, worker_field__isnull=True)).exclude(payme=0)


# yangi qo'shimchalar
class UserInformation(View):
    def get(self, request, *args, **kwargs):
        obj = User.objects.get(id=kwargs['pk'])
        date = self.request.GET.get('qalendar')
        if date not in [None, '']:
            try:
                valid_date = datetime.strptime(date, '%Y-%m-%d').date()
            except ValueError:
                raise ValidationError({"detail": "invalid params"})
        else:
            valid_date = datetime.today()
        orders = obj.orders.filter(updated_at__gte=valid_date)
        total_all_profit = obj.all_profit.filter(updated_at__gte=valid_date).aggregate(sum_price=Sum('price'))[
            'sum_price']
        total_projects = obj.all_orders.filter(updated_at__gte=valid_date).count()

        total_grant = obj.grant_count.filter(updated_at__gte=valid_date).count()
        total_teo = obj.teo_count.filter(updated_at__gte=valid_date).count()
        total_business = obj.business_count.filter(updated_at__gte=valid_date).count()

        total_boshqa = obj.boshqa_count.filter(updated_at__gte=valid_date).count()
        total_unpaid = obj.unpaid.filter(updated_at__gte=valid_date).count()
        total_payme25 = obj.payme25.filter(updated_at__gte=valid_date).count()
        total_payme50 = obj.payme50.filter(updated_at__gte=valid_date).count()
        total_payme75 = obj.payme75.filter(updated_at__gte=valid_date).count()
        total_order_count = obj.order_count.filter(updated_at__gte=valid_date).count()

        if obj.role == 'Worker':
            return render(request, 'myApp/admin/worker_information.html', context={"object": obj, "orders": orders,
                                                                                   'total_order_count': total_order_count,
                                                                                   'total_projects': total_projects,
                                                                                   'total_grant': total_grant,
                                                                                   'total_teo': total_teo,
                                                                                   'total_business': total_business,
                                                                                   'total_boshqa': total_boshqa,
                                                                                   'total_unpaid': total_unpaid,
                                                                                   'total_payme25': total_payme25,
                                                                                   'total_payme50': total_payme50,
                                                                                   'total_payme75': total_payme75,
                                                                                   'total_all_profit': total_all_profit})
        elif obj.role == 'Operator':
            return render(request, 'myApp/admin/operator_information.html', context={"object": obj, "orders": orders,
                                                                                     'total_projects': total_projects,
                                                                                     'total_grant': total_grant,
                                                                                     'total_teo': total_teo,
                                                                                     'total_business': total_business,
                                                                                     'total_boshqa': total_boshqa,
                                                                                     'total_unpaid': total_unpaid,
                                                                                     'total_payme25': total_payme25,
                                                                                     'total_payme50': total_payme50,
                                                                                     'total_payme75': total_payme75,
                                                                                     'total_all_profit': total_all_profit})
        else:
            return HttpResponse("hato")


class UserGrant(View):
    def get(self, request, *args, **kwargs):
        obj = User.objects.get(id=kwargs['pk'])
        return render(request, 'myApp/admin/operator_grant_list.html', context={"object": obj})


class UserTEO(View):
    def get(self, request, *args, **kwargs):
        obj = User.objects.get(id=kwargs['pk'])
        return render(request, 'myApp/admin/operator_teo.html', context={"object": obj})


class UserBusiness(View):
    def get(self, request, *args, **kwargs):
        obj = User.objects.get(id=kwargs['pk'])
        return render(request, 'myApp/admin/operator_business_list.html', context={"object": obj})


class UserBoshqa(View):
    def get(self, request, *args, **kwargs):
        obj = User.objects.get(id=kwargs['pk'])
        return render(request, 'myApp/admin/operator_boshqa_list.html', context={"object": obj})


# user detil
class UserDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = User
    template_name = "myApp/admin/user_detail.html"

    def test_func(self):
        return 'admin' == self.request.user.role


# user update
class UserUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'myApp/admin/user_update.html'
    fields = [
        "first_name",
        "last_name",
        "role",
        # "number_of_orders",

    ]

    def test_func(self):
        return 'admin' == self.request.user.role


#
class TeamCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'myApp/admin/team_create.html'
    success_url = reverse_lazy('team_list_url')

    def test_func(self):
        return 'admin' == self.request.user.role


class TeamList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Team
    template_name = 'myApp/admin/team_list.html'

    def test_func(self):
        return 'admin' == self.request.user.role


class TeamDetail(DetailView):
    model = Team
    template_name = 'myApp/admin/team_detail.html'


class TeamDelete(DeleteView):
    model = Team
    template_name = 'myApp/admin/team_delete.html'
    success_url = reverse_lazy("team_list_url")


class TeamDetailFront(DetailView):
    model = Team
    template_name = 'myApp/interface/team_detail_front.html'


class GrandUpdate(UpdateView):
    model = GrantProject
    form_class = GrantForm

    template_name = 'myApp/admin/grant_update.html'
    success_url = reverse_lazy("grant_list_url")


# class NotOrdered(LoginRequiredMixin, UserPassesTestMixin, ListView):
#     paginate_by = 10
#     model = Order
#     template_name = 'myApp/admin/not_ordered.html'
#
#     def test_func(self):
#         return 'Worker' == self.request.user.role or 'Operator' == self.request.user.role
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         return queryset.filter(
#             Q(operator_field__isnull=False, worker_field__isnull=True), business_type__contains='qiziqmadi')

class NotOrdered(LoginRequiredMixin, UserPassesTestMixin, View):

    def get(self, request):
        green_individual_count = Order.objects.all().filter(color_type__contains='green',
                                                            petition_type__contains='individual').filter(
            payme=0).count()
        yellow_individual_count = Order.objects.all().filter(color_type__contains='yellow',
                                                             petition_type__contains='individual').filter(
            payme=0).count()
        red_individual_count = Order.objects.all().filter(color_type__contains='red',
                                                          petition_type__contains='individual').filter(
            payme=0).count()

        green_site_count = Order.objects.all().filter(color_type__contains='green',
                                                      petition_type__contains='site').filter(payme=0).count()
        yellow_site_count = Order.objects.all().filter(color_type__contains='yellow',
                                                       petition_type__contains='site').filter(payme=0).count()
        red_site_count = Order.objects.all().filter(color_type__contains='red', petition_type__contains='site').filter(
            payme=0).count()

        context = {
            'green_individual_count': green_individual_count,
            'yellow_individual_count': yellow_individual_count,
            'red_individual_count': red_individual_count,

            'green_site_count': green_site_count,
            'yellow_site_count': yellow_site_count,
            'red_site_count': red_site_count,
        }

        return render(request, 'myApp/admin/not_ordered.html', context)

    def test_func(self):
        return 'Worker' == self.request.user.role or 'Operator' == self.request.user.role


# class PetitionOperatorAdd(LoginRequiredMixin, UserPassesTestMixin, CreateView):
#     model = Petition
#     form_class = PetitionForm
#     template_name = 'myApp/petitions_operator_add.html'
#     # success_url = reverse_lazy('answer_url')
#
#     site_orders = Order.objects.filter(Q(operator_field__isnull=True, worker_field__isnull=True)).count()
#
#     extra_context = {
#         'site_orders': site_orders
#     }
#
#     def test_func(self):
#         return 'Worker' == self.request.user.role or 'Operator' == self.request.user.role

class PetitionOperatorAdd(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request):
        site_orders = Order.objects.filter(Q(operator_field__isnull=True, worker_field__isnull=True)).count()

        context = {
            'site_orders': site_orders
        }
        return render(request, 'myApp/petitions_operator_add.html', context)

    def test_func(self):
        return 'Worker' == self.request.user.role or 'Operator' == self.request.user.role


class PaidOrders(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request):
        individual = Order.objects.all().filter(
            Q(operator_field__isnull=False, worker_field__isnull=True), petition_type__contains='individual').exclude(
            payme=0).count()
        site = Order.objects.all().filter(
            Q(operator_field__isnull=False, worker_field__isnull=True), petition_type__contains='site').exclude(
            payme=0).count()

        context = {
            'order_individual_count': individual,
            'order_site_count': site,
        }

        return render(request, 'myApp/operator/paid_orders.html', context)

    def test_func(self):
        return 'Worker' == self.request.user.role or 'Operator' == self.request.user.role


class IndividualOrderCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Order
    form_class = IndividualOrderForm
    template_name = 'myApp/operator/individual_order_create.html'
    success_url = reverse_lazy('petitions_operator_add_url')

    def test_func(self):
        return 'Worker' == self.request.user.role or 'Operator' == self.request.user.role

    # def post(self, request, *args, **kwargs):
    #     if request.method == 'POST':
    #         form = IndividualOrderForm(request.POST, request.FILES)
    #         if form.is_valid():
    #             form.save()
    #
    #
    #     return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.petition_type = 'individual'
        form.instance.operator_field = self.request.user
        form.save()
        return super(IndividualOrderCreate, self).form_valid(form)


# AJAX
def load_cities(request):
    province_id = request.GET.get('province_id')
    cities = Region.objects.filter(province_id=province_id)
    return render(request, 'myApp/city_dropdown_list_options.html', {'cities': cities})
    # return JsonResponse(list(cities.values('id', 'name')), safe=False)


class SiteOrderUpdate(UpdateView):
    model = Order
    fields = ['phone_number', 'add_phone_number', 'first_name', 'last_name', 'province', 'region', 'business_name',
              'business_type',
              'price', 'stat_date', 'end_date', 'payme', 'color_type']

    template_name = 'myApp/operator/site_order_update.html'

    success_url = reverse_lazy('answer_url')

    def form_valid(self, form):
        form.instance.petition_type = 'site'
        form.instance.operator_field = self.request.user

        form.save()
        return super(SiteOrderUpdate, self).form_valid(form)


class EmployeeOrdersList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    paginate_by = 15
    model = Order

    template_name = 'myApp/operator/employee_orders_list.html'

    def test_func(self):
        return 'Worker' == self.request.user.role or 'Operator' == self.request.user.role

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            Q(operator_field__isnull=False, worker_field__isnull=True), petition_type__contains='individual').exclude(
            payme=0)


class OrdersFromSiteList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    paginate_by = 10
    model = Order
    template_name = 'myApp/operator/orders_from_site_list.html'

    def test_func(self):
        return 'Worker' == self.request.user.role or 'Operator' == self.request.user.role

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            Q(operator_field__isnull=False, worker_field__isnull=True), petition_type__contains='site').exclude(
            payme=0)


class PreOrderColorIndividual(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        return 'Worker' == self.request.user.role or 'Operator' == self.request.user.role

    def get(self, request, color):
        search_query = request.GET.get('search', '')
        if search_query:
            obj = Order.objects.filter(Q(phone_number__contains=search_query)).filter(color_type__contains=color,
                                                                                      petition_type__contains='individual').filter(
                payme=0)
        else:
            obj = Order.objects.filter(color_type__contains=color, petition_type__contains='individual').filter(
                payme=0)

        paginator = Paginator(obj, 15)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)

        is_paginated = page.has_other_pages()

        if page.has_previous():
            prev_url = '?page={}'.format(page.previous_page_number())
        else:
            prev_url = ''
        if page.has_next():
            next_url = '?page={}'.format(page.next_page_number())
        else:
            next_url = ''
        context = {
            'page_obj': obj,
            'color_id': color,
            'page_object': page,
            'next_url': next_url,
            'prev_url': prev_url,
            'is_paginated': is_paginated
        }

        return render(request, 'myApp/operator/pre_order_color_individual.html', context)


class AdminPreOrderColorIndividual(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        return 'admin' == self.request.user.role

    def get(self, request, color):
        obj = Order.objects.all().filter(color_type__contains=color, petition_type__contains='individual').filter(
            payme=0)
        return render(request, 'myApp/admin/admin_pre_order_color_individual.html', context={'page_obj': obj})


class PreOrderColorSite(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        return 'Worker' == self.request.user.role or 'Operator' == self.request.user.role

    def get(self, request, color):

        search_query = request.GET.get('search', '')
        if search_query:
            obj = Order.objects.filter(Q(phone_number__contains=search_query)).filter(color_type__contains=color,
                                                                                      petition_type__contains='site').filter(
                payme=0)
        else:
            obj = Order.objects.filter(color_type__contains=color, petition_type__contains='site').filter(
                payme=0)

        paginator = Paginator(obj, 3)

        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)

        is_paginated = page.has_other_pages()

        if page.has_previous():
            prev_url = '?page={}'.format(page.previous_page_number())
        else:
            prev_url = ''
        if page.has_next():
            next_url = '?page={}'.format(page.next_page_number())
        else:
            next_url = ''
        context = {
            'page_obj': obj,
            'color_id': color,
            'page_object': page,
            'next_url': next_url,
            'prev_url': prev_url,
            'is_paginated': is_paginated
        }

        return render(request, 'myApp/operator/pre_order_color_site.html', context)


class AddminPreOrderColorSite(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        return 'admin' == self.request.user.role

    def get(self, request, color):
        obj = Order.objects.all().filter(color_type__contains=color, petition_type__contains='site').filter(
            payme=0)
        return render(request, 'myApp/admin/admin_pre_order_color_site.html', context={'page_obj': obj})


class StatusUpdates(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Order
    fields = ['status', 'comment_worker']
    template_name = 'myApp/operator/status_update.html'
    success_url = reverse_lazy('operator_list_url')

    def test_func(self):
        return 'Worker' == self.request.user.role or 'Operator' == self.request.user.role

    def form_valid(self, form):
        form.instance.order_finished_date = datetime.today()
        # form.instance.operator_field = self.request.user

        form.save()
        return super(StatusUpdates, self).form_valid(form)


class WorkerOrderSiteUpdate(UpdateView):
    model = Order
    fields = ['add_phone_number', 'first_name', 'last_name', 'business_name', 'business_type', 'price']
    template_name = 'myApp/worker/worker_order_site_update.html'


# class AdminChart(LoginRequiredMixin, UserPassesTestMixin, View):
#     def get(self, request):
#         user_names = []
#         user_order_price = []
#         oy = request.GET.get('oy')
#         yil = request.GET.get('yil')
#
#         if oy in [None, '']:
#             try:
#                 oy = datetime.today().month
#             except ValueError:
#                 raise ValidationError({"detail": "invalid params"})
#
#         if yil in [None, '']:
#             try:
#                 yil = datetime.today().year
#             except ValueError:
#                 raise ValidationError({"detail": "invalid params"})
#
#         if oy == '0' and yil != '0':
#             for user in User.objects.all().exclude(role='admin'):
#                 user_names.append(user.username)
#                 sm = 0
#
#                 for order in user.orders.filter(order_finished_date__year=int(yil)):
#                     sm += order.price
#                 user_order_price.append(sm)
#
#         elif oy != '0' and yil == '0':
#             for user in User.objects.all().exclude(role='admin'):
#                 user_names.append(user.username)
#                 sm = 0
#
#                 for order in user.orders.filter(order_finished_date__year=datetime.today().year).filter(
#                         order_finished_date__month=int(oy)):
#                     sm += order.price
#                 user_order_price.append(sm)
#
#         elif oy != '0' and yil != '0':
#             for user in User.objects.all().exclude(role='admin'):
#                 user_names.append(user.username)
#                 sm = 0
#
#                 for order in user.orders.filter(order_finished_date__year=int(yil)).filter(
#                         order_finished_date__month=int(oy)):
#                     sm += order.price
#                 user_order_price.append(sm)
#
#         context = {
#             'user_names': user_names,
#             'user_order_price': user_order_price
#         }
#         return render(request, 'myApp/admin/admin_chart_rating.html', context)


def admin_chart_rating(request):
    user_names = []
    user_order_price = []
    oy = request.GET.get('oy')
    yil = request.GET.get('yil')

    if oy in [None, '']:
        try:
            oy = datetime.today().month
        except ValueError:
            raise ValidationError({"detail": "invalid params"})

    if yil in [None, '']:
        try:
            yil = datetime.today().year
        except ValueError:
            raise ValidationError({"detail": "invalid params"})

    if oy == '0' and yil != '0':
        for user in User.objects.all().exclude(role='admin'):
            user_names.append(user.username)
            sm = 0

            for order in user.orders.filter(order_finished_date__year=int(yil)):
                sm += order.price
            user_order_price.append(sm)

    elif oy != '0' and yil == '0':
        for user in User.objects.all().exclude(role='admin'):
            user_names.append(user.username)
            sm = 0

            for order in user.orders.filter(order_finished_date__year=datetime.today().year).filter(
                    order_finished_date__month=int(oy)):
                sm += order.price
            user_order_price.append(sm)

    elif oy != '0' and yil != '0':
        for user in User.objects.all().exclude(role='admin'):
            user_names.append(user.username)
            sm = 0

            for order in user.orders.filter(order_finished_date__year=int(yil)).filter(
                    order_finished_date__month=int(oy)):
                sm += order.price
            user_order_price.append(sm)

    context = {
        'user_names': user_names,
        'user_order_price': user_order_price
    }
    return render(request, 'myApp/admin/admin_chart_rating.html', context)


# def chart_rating(request):
#     user_names = []
#     user_order_price = []
#
#     string1 = request.GET.get('oy')
#
#     if string1 == '1':
#         for user in User.objects.all().exclude(role='admin'):
#             user_names.append(user.username)
#             sm = 0
#
#             for order in user.orders.filter(order_finished_date__month=datetime.today().month):
#                 sm += order.price
#             user_order_price.append(sm)
#     elif string1 == '2':
#         for user in User.objects.all().exclude(role='admin'):
#             user_names.append(user.username)
#             sm = 0
#             last_day_of_prev_month = datetime.today().replace(day=1) - timedelta(days=1)
#             for order in user.orders.filter(order_finished_date__month=last_day_of_prev_month.month):
#                 sm += order.price
#             user_order_price.append(sm)
#
#     context = {
#         'user_names': user_names,
#         'user_order_price': user_order_price
#     }
#     return render(request, 'myApp/operator/reyting.html', context)


def chart_rating(request):
    user_names = []
    user_order_price = []

    user_names2 = []
    user_order_price2 = []

    # user_names3 = []
    # user_order_price3 = []

    string1 = request.GET.get('oy')

    if string1 == '1':
        for user in User.objects.all().exclude(role='admin'):
            user_names.append(user.username)
            sm = 0

            for order in user.orders.filter(order_finished_date__month=datetime.today().month):
                sm += order.price
            user_order_price.append(sm)

        for user in User.objects.all().exclude(role='admin'):
            user_names2.append(user.username)
            sm = 0

            for order in user.operator_orders.filter(order_finished_date__month=datetime.today().month):
                sm += order.price
            user_order_price2.append(sm)

        # for user in User.objects.all().exclude(role='admin'):
        #     user_names3.append(user.username)
        #     sm = 0
        #
        #     for order in user.operator_worker_orders.filter(order_finished_date__month=datetime.today().month):
        #         sm += order.price
        #     user_order_price3.append(sm)

    elif string1 == '2':
        for user in User.objects.all().exclude(role='admin'):
            user_names.append(user.username)
            sm = 0
            last_day_of_prev_month = datetime.today().replace(day=1) - timedelta(days=1)
            for order in user.orders.filter(order_finished_date__month=last_day_of_prev_month.month):
                sm += order.price
            user_order_price.append(sm)

        for user in User.objects.all().exclude(role='admin'):
            user_names2.append(user.username)
            sm = 0
            last_day_of_prev_month = datetime.today().replace(day=1) - timedelta(days=1)
            for order in user.operator_orders.filter(order_finished_date__month=last_day_of_prev_month.month):
                sm += order.price
            user_order_price2.append(sm)

        # for user in User.objects.all().exclude(role='admin'):
        #     user_names3.append(user.username)
        #     sm = 0
        #     last_day_of_prev_month = datetime.today().replace(day=1) - timedelta(days=1)
        #     for order in user.operator_worker_orders.filter(order_finished_date__month=last_day_of_prev_month.month):
        #         sm += order.price
        #     user_order_price3.append(sm)

    user_order_price3 = []
    for i in range(0, len(user_names)):
        user_order_price3.append(user_order_price[i] + user_order_price2[i])

    context = {
        'user_names': user_names,
        'user_order_price': user_order_price,

        'user_names2': user_names2,
        'user_order_price2': user_order_price2,

        'user_order_price3': user_order_price3,

    }
    return render(request, 'myApp/operator/reyting.html', context)


class PreOrderUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Order
    form_class = PreOrderUpdateForm
    template_name = 'myApp/operator/pre_order_update.html'
    success_url = reverse_lazy('not_ordered_url')

    def test_func(self):
        return 'Worker' == self.request.user.role or 'Operator' == self.request.user.role

    def form_valid(self, form):
        form.instance.operator_field = self.request.user

        form.save()
        return super(PreOrderUpdate, self).form_valid(form)


class OrderDetail(DetailView):
    model = Order
    template_name = 'myApp/order_detail.html'

    success_url = reverse_lazy('not_ordered_url')


class AdminStatistika(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        return 'admin' == self.request.user.role

    def get(self, request):
        return render(request, 'myApp/admin/admin_statistika.html')


class OrderSearch(View):
    def get(self, request):
        search_query = request.GET.get('search', '')
        if search_query:
            obj = Order.objects.filter(Q(phone_number__contains=search_query))
        else:
            obj = Order.objects.all()

        paginator = Paginator(obj, 15)

        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)

        is_paginated = page.has_other_pages()

        if page.has_previous():
            prev_url = '?page={}'.format(page.previous_page_number())
        else:
            prev_url = ''
        if page.has_next():
            next_url = '?page={}'.format(page.next_page_number())
        else:
            next_url = ''
        context = {
            'page_obj': obj,
            'page_object': page,
            'next_url': next_url,
            'prev_url': prev_url,
            'is_paginated': is_paginated
        }

        return render(request, 'myApp/operator/search_orders.html', context)


class MyEndProjectsList(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        return 'Worker' == self.request.user.role or 'Operator' == self.request.user.role

    def get(self, request):
        search_query = request.GET.get('search', '')
        if search_query:
            obj = Order.objects.filter(
                Q(operator_field__isnull=False, payme__isnull=False, worker_field__isnull=False, status=True,
                  worker_field=self.request.user),
                Q(phone_number__contains=self.request.GET.get("search", '')))
        else:
            obj = Order.objects.filter(
                Q(operator_field__isnull=False, payme__isnull=False, worker_field__isnull=False, status=True,
                  worker_field=self.request.user))

        paginator = Paginator(obj, 3)

        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)

        is_paginated = page.has_other_pages()

        if page.has_previous():
            prev_url = '?page={}'.format(page.previous_page_number())
        else:
            prev_url = ''
        if page.has_next():
            next_url = '?page={}'.format(page.next_page_number())
        else:
            next_url = ''
        context = {
            'page_obj': obj,
            'page_object': page,
            'next_url': next_url,
            'prev_url': prev_url,
            'is_paginated': is_paginated
        }
        return render(request, 'myApp/operator/my_end_project_list.html', context)


class MyOrderUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Order
    form_class = MyOrderUpdateForm
    template_name = 'myApp/operator/my_order_update.html'

    success_url = reverse_lazy('operator_list_url')

    def post(self, request, *args, **kwargs):
        print('Salom')
        print('Salom')
        print(request)

        return super().post(request, *args, **kwargs)

    def test_func(self):
        return 'Worker' == self.request.user.role or 'Operator' == self.request.user.role
