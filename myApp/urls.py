from django.urls import path

# importing views from views.py
from .views import *

urlpatterns = [
    path('answer/', answer, name='answer_url'),


    path('answer/', answer, name='answer_url'),

    path('about/', about, name='about_url'),

    path('contact/', contact, name='contact_url'),

    path('payme/', payme, name='payme_url'),

    path('grant_operator_list/', grant_project_for_operator, name='grant_operator_list_url'),

    path('grant/', GrantProjectsAdd.as_view(), name='grant_add_url'),

    path('grant/<pk>', GrantProjectDelete.as_view(), name='grant_delete_url'),

    path('register/', RegisterPage.as_view(), name='register_url'),

    path('petition/', PetitiontAdd.as_view(), name='petition_add_url'),

    path('grant_list/', GrantProjectList.as_view(), name='grant_list_url'),

    path('order_list/', OrderList.as_view(), name='order_list_url'),

    path('order_admin_list/', OrderListAdmin.as_view(), name='order_admin_list_url'),

    path('petition_list/', PetitionList.as_view(), name='petition_list_url'),

    path('user_list/', UserList.as_view(), name='user_list_url'),

    path('worker_order_list/', WorkerOrderList.as_view(), name='worker_order_list_url'),

    path('operator_list/', OperatorList.as_view(), name='operator_list_url'),

    path('worker_list/', WorkerList.as_view(), name='worker_list_url'),

    path('order/<pk>/', OrderDetailView.as_view(), name='order_detail_url'),

    path('order/<pk>/update/', OrderUpdate.as_view(), name='order_update_url'),

    path('worker/<pk>/update/', WorkerUpdate.as_view(), name='worker_update_url'),

]
