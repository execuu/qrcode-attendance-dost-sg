from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    path('', views.home, name='home'),
    path('members/', views.memberList, name='members'),
    path('members/<int:id>/', views.viewMember, name='viewMember'),
    path('add_member/', views.addMember, name='addMember'),
    path('edit_member/<int:id>/', views.editMember, name='editMember'),
    path('delete_member/<int:id>/', views.deleteMember, name='deleteMember'),
]