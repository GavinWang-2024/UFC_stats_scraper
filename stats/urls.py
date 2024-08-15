from django.urls import path
from . import views
urlpatterns=[
    path("home",views.home,name='home'),
    path("fighters",views.all_fighters,name="all_fighters"),
    path("fighter/<str:first_name>/<str:last_name>",views.fighter_detail,name="fighter_detail"),
    path("fighter/search",views.search_fighter,name="search_fighter"),
    path('events/', views.display_events, name='display_events'),
]