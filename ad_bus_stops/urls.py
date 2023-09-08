from django.urls import path

from .views_folder import account_view, analytics_views, app_explorer_view, authentication_views
from .views_folder import book_view, book_confirm_view, cart_view, dashboard_view, index_view
from .views_folder import message_views, staff_actions_view, start_views,  stops_view

urlpatterns = [
    
    path('', start_views.viewport, name = 'viewport'), 
    path("account", account_view.account, name="account"),
    path('app_explorer',app_explorer_view.app_explorer, name = 'app_explorer'),
    path('book',book_view.book, name = 'book'),
    path('book_confirm/<int:stop_id>/<int:order_id>/<str:stops_id_paginated>',book_confirm_view.book_confirm, name = 'book_confirm'),
    path("bus_stops/<str:city>/<int:num_page>/<str:letters>", stops_view.bus_stops, name="bus_stops"),
    path('cancel_order', staff_actions_view.cancel_order , name = 'cancel_order'),
    path('cart/<str:city>/<int:num_page>/<str:letters>', cart_view.cart, name = 'cart'),
    path('change_current_date',app_explorer_view.change_current_date, name = 'change_current_date'),
    path('checkout/<str:city>/<int:num_page>/<str:letters>', cart_view.checkout, name = 'checkout'),
    path('confirmation/<int:user_id>',authentication_views.confirmation, name = 'confirmation'),
    path("dashboard/<str:message>", dashboard_view.dashboard, name="dashboard"),
    path('edit_setUp', staff_actions_view.edit_setUp, name = 'edit_setUp'),
    path('enter_app_explorer',app_explorer_view.enter_app_explorer, name = 'enter_app_explorer'),
    path("guidance", index_view.guidance, name="guidance"),
    path('hide_study_message/<str:template_name>',app_explorer_view.hide_study_message ,
            name='hide_study_message'),
    path("index", index_view.index, name="index"),
    path("login", authentication_views.login_view, name="login"),
    path("logout", authentication_views.logout_view, name="logout"),
    path('order_page/<int:order_id>/<str:action>', analytics_views.order_page, name = 'order_page'),
    path('order_query',analytics_views.order_query, name = 'order_query'),
    path("payment_verification", dashboard_view.payment_verification, name="payment_verification"),
    path("placement_verification", dashboard_view.placement_verification, name="placement_verification"),
    path('prepare_cancel', staff_actions_view.prepare_cancel , name = 'prepare_cancel'),
    path('preset_db',app_explorer_view.preset_db_view, name = 'preset_db'),
    path("register", authentication_views.register, name="register"),
    path('register_app_explorer',app_explorer_view.register_app_explorer, 
            name = 'register_app_explorer'),
    path("removal_verification", dashboard_view.removal_verification, name="removal_verification"),        
    path('start',start_views.start, name = 'start'),   
    path('<path:x>',message_views.message, name = 'message'),  
]

