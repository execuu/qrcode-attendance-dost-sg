from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('attendance/', views.attendanceList, name='attendanceList'),
    path('attendance/<int:id>/', views.viewEvent, name='viewEvent'),
    path('add_event/', views.addEvent, name='addEvent'),
    path('edit_event/<int:id>/', views.editEvent, name='editEvent'),
    path('delete_event/<int:id>/', views.deleteEvent, name='deleteEvent'),
    path('event/<int:id>/', views.eventDetail, name='eventDetail'),
    path('qr-redirect/<int:studentNumber>/', views.qr_redirect, name='qr_redirect'),
    path('record-attendance/<int:event_id>/<int:member_id>/', views.record_attendance, name='record_attendance'),
    path('scan-member/<int:studentNumber>/', views.scan_member, name='scan_member'),
    path('confirm-attendance/<int:event_id>/<int:member_id>/', views.confirm_attendance, name='confirm_attendance'),
]
