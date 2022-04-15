from django.urls import path
from django.contrib.auth.views import PasswordChangeView

# importing views from views.py
from .views import *

urlpatterns = [

    path('', BusinessPlanList.as_view(), name='home_url'),

    path('business/', BusinessPlanAdd.as_view(), name='business_plan_add_url'),

    path('answer/', answer, name='answer_url'),

    path('answer/', answer, name='answer_url'),

    path('about/', about, name='about_url'),

    path('contact/', contact, name='contact_url'),

    path('payme/', payme, name='payme_url'),

    path('reyting/', reyting, name='reyting_url'),

    path('bouns/', bouns, name='bouns_url'),

    # path('admin_reyting/', admin_reyting, name='admin_reyting_url'),

    path('grant_front_list/', grant_project_front, name='grant_front_list_url'),

    path('paid_orders/', PaidOrders.as_view(), name='paid_orders_url'),



    path('grant/', GrantProjectsAdd.as_view(), name='grant_add_url'),

    path('petitions_operator_add/', PetitionOperatorAdd.as_view(), name='petitions_operator_add_url'),

    path('individual_order_create/', IndividualOrderCreate.as_view(), name='individual_order_create_url'),

    # path('orders_site_create/', OrdersFromSiteCreate.as_view(), name='orders_site_create_url'),

    path('team/', TeamCreate.as_view(), name='team_add_url'),

    path('register/', RegisterPage.as_view(), name='register_url'),

    path('petition/', PetitiontAdd.as_view(), name='petition_add_url'),

    path('employee_order_list/', EmployeeOrdersList.as_view(), name='employee_order_list_url'),

    path('orders_site_list/', OrdersFromSiteList.as_view(), name='orders_site_list_url'),

    path('team_list/', TeamList.as_view(), name='team_list_url'),

    path('business_admin_list/', BusinessPlanAdminList.as_view(), name='business_admin_list_url'),

    path('grant_list/', GrantProjectList.as_view(), name='grant_list_url'),

    path('accepted_orders_list/', AcceptedOrdersList.as_view(), name='accepted_orders_list_url'),

    path('not_ordered/', NotOrdered.as_view(), name='not_ordered_url'),

    path('order_list/', OrderList.as_view(), name='order_list_url'),

    # team_detail

    path('team_detail/<pk>/', TeamDetail.as_view(), name='team_detail_url'),

    path('team_detail_front/<pk>/', TeamDetailFront.as_view(), name='team_detail_front_url'),

    path('operator_grant/<pk>', UserGrant.as_view(), name='user_grant_list_url'),

    path('operator_teo/<pk>', UserTEO.as_view(), name='user_teo_list_url'),

    path('operator_business/<pk>', UserBusiness.as_view(), name='user_business_list_url'),

    path('operator_boshqa/<pk>', UserBoshqa.as_view(), name='user_boshqa_list_url'),

    # path('petition_list/', PetitionList.as_view(), name='petition_list_url'),

    path('search/', OrderSearch.as_view(), name='search_list_url'),

    path('unseen_orders_list/', UnSeenOrdersList.as_view(), name='un_seen_order_list_url'),

    path('no_interested_list/', NotInterestedList.as_view(), name='no_interested_list_url'),

    path('final_order_list/', FinalOrdersList.as_view(), name='final_order_list_url'),

    path('my_end_project_list/', MyEndProjectsList.as_view(), name='my_end_project_list_url'),

    path('unfinal_order_list/', UnFinishedOrdersList.as_view(), name='un_final_order_list_url'),

    path('user_list/', UserList.as_view(), name='user_list_url'),

    # path('worker_order_list/', WorkerOrderList.as_view(), name='worker_order_list_url'),

    path('operator_list/', OperatorList.as_view(), name='operator_list_url'),

    # path('worker_list/', WorkerList.as_view(), name='worker_list_url'),

    path('user_information/<pk>/', UserInformation.as_view(), name='user_information_url'),

    path('user/<pk>/', UserDetail.as_view(), name='user_detail_url'),



    path('grant/<pk>', GrantProjectDelete.as_view(), name='grant_delete_url'),

    path('order_detail/<pk>/', OrderDetail.as_view(), name='order_detail_url'),

    path('team_delete/<pk>', TeamDelete.as_view(), name='team_delete_url'),

    path('business/<pk>/', BusinessPlanDetail.as_view(), name='business_plan_detail_url'),

    path('business/<pk>', BusinessPlanDelete.as_view(), name='business_delete_url'),

    path('pre_order_individual/<color>/', PreOrderColorIndividual.as_view(), name='pre_order_individual_url'),

    path('admin_pre_order_individual/<color>/', AdminPreOrderColorIndividual.as_view(), name='admin_pre_order_individual_url'),

    path('pre_order_site/<color>/', PreOrderColorSite.as_view(), name='pre_order_site_url'),

    path('admin_pre_order_site/<color>/', AddminPreOrderColorSite.as_view(), name='admin_pre_order_site_url'),

    path('ajax/load-cities/', load_cities, name='ajax_load_cities'),  # AJAX

    path('status/<pk>/update', StatusUpdates.as_view(), name='status_update_url'),

    path('pre_order/<pk>/update', PreOrderUpdate.as_view(), name='pre_order_update_url'),

    path('grant/<pk>/update', GrandUpdate.as_view(), name='grant_update_url'),

    path('site_order/<pk>/update', SiteOrderUpdate.as_view(), name='site_order_update_url'),

    path('user/<pk>/update/', UserUpdate.as_view(), name='user_update_url'),

    path('order/<pk>/update/', OrderUpdate.as_view(), name='order_update_url'),

    path('worker/<pk>/update/', WorkerUpdate.as_view(), name='worker_update_url'),

    path('worker_orders_site_update/<pk>/update/', WorkerOrderSiteUpdate.as_view(), name='worker_orders_site_update_url'),

    path('worker_orde_update/<pk>/update/', WorkerOrderUpdate.as_view(), name='worker_order_update_url'),

    path('chart/', chart_rating, name='chart_raating_url'),

    path('admin_chart/', admin_chart_rating, name='admin_chart_rating_url'),



    path('statistika/', AdminStatistika.as_view(), name='statistika_url'),



]
