from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    # Authentication endpoints
    path('auth/student/login/', views.StudentLoginView.as_view(), name='student_login'),
    path('auth/washerman/login/', views.WashermanLoginView.as_view(), name='washerman_login'),
    path('auth/student/signup/', views.StudentSignupView.as_view(), name='student_signup'),
    path('auth/washerman/signup/', views.WashermanSignupView.as_view(), name='washerman_signup'),
    
    # Order endpoints
    path('orders/create/', views.CreateOrderView.as_view(), name='create_order'),
    path('orders/student/<str:bag_no>/', views.StudentOrdersView.as_view(), name='student_orders'),
    path('orders/all/', views.AllOrdersView.as_view(), name='all_orders'),
    path('orders/pending/', views.PendingOrdersView.as_view(), name='pending_orders'),
    path('orders/<int:order_id>/status/', views.UpdateOrderStatusView.as_view(), name='update_order_status'),
    
    # Dashboard endpoints
    path('student/dashboard/<str:bag_no>/', views.StudentDashboardView.as_view(), name='student_dashboard'),
    path('washerman/dashboard/', views.WashermanDashboardView.as_view(), name='washerman_dashboard'),
]
