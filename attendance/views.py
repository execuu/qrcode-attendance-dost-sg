from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.db import IntegrityError
from django.urls import reverse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from .models import Event, Attendance
from .forms import AttendanceForm
from members.models import Members



# Create your views here.
def attendanceList(request):
    return render(request, 'attendance/attendanceList.html', ({'events': Event.objects.all()}))

def viewEvent(request, id):
    event = Event.objects.get(pk=id)
    return HttpResponseRedirect(reverse('attendance:attendanceList'))

def addEvent(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                event = form.save(commit=False)
                event.save()
                messages.success(request, f"Event: {event.eventName} Dated: {event.created_at} has been added successfully!")
            except IntegrityError:
                messages.error(request, 'Failed to add event.')
            return redirect('attendance:attendanceList')
    else:
        form = AttendanceForm()

    return render(request, 'attendance/addEvent.html', {'form': form})

def editEvent(request, id):
    event = Event.objects.get(pk=id)
    if request.method == 'POST':
        form = AttendanceForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, f"Event: {event.eventName} has been updated successfully!")
            return redirect('attendance:attendanceList')
    else:
        form = AttendanceForm(instance=event)

    context = {
        'form': form,
        'event': event
    }

    html_form = render_to_string('attendance/editEvent.html', context, request=request)
    return JsonResponse({'html_form': html_form})

def deleteEvent(request, id):
    if request.method == 'POST':
        event = Event.objects.get(pk=id)
        event.delete()
        messages.success(request, f"event: {event.eventName} has been deleted successfully!")
    return HttpResponseRedirect(reverse('attendance:attendanceList'))

def eventDetail(request, id):
    event = Event.objects.get(pk=id)
    attendances = Attendance.objects.filter(event=event)
    
    member = request.GET.get('member')
    return render(request, 'attendance/eventDetail.html', {
        'event': event,
        'attendances': attendances,
        'member': member,  
    })
# Redirect users to the attendance confirmation page based on the scanned QR code
def qr_redirect(request, studentNumber):
    try:
        member = Members.objects.get(studentNumber=studentNumber)
    except Members.DoesNotExist:
        return HttpResponseRedirect('/not-found/')
    
    # Redirect to the member's specific attendance confirmation page
    return HttpResponseRedirect(f'/scan-member/{studentNumber}/')

# Handle scanning of the member's QR code
def scan_member(request, studentNumber):
    try:
        member = Members.objects.get(studentNumber=studentNumber)
    except Members.DoesNotExist:
        return render(request, 'attendance/member_not_found.html')

    # Fetch all events so the user can choose one
    events = Event.objects.all()
    return render(request, 'attendance/select_event.html', {
        'member': member,
        'events': events
    })

# Confirm the attendance for the selected event and member
def confirm_attendance(request, event_id, member_id):
    event = get_object_or_404(Event, id=event_id)
    member = get_object_or_404(Members, id=member_id)

    # Check if attendance already exists
    attendance_exists = Attendance.objects.filter(member=member, event=event).exists()

    if attendance_exists:
        # Display an error message if attendance already recorded
        messages.error(request, f'{member.firstName} {member.lastName} has already been recorded for this event.')
    else:
        # Record the attendance if it doesn't already exist
        Attendance.objects.create(member=member, event=event)
        messages.success(request, f'{member.firstName} {member.lastName} has been successfully recorded for {event.eventName}.')

    return redirect('attendance:eventDetail', id=event_id)


# Record the member's attendance
def record_attendance(request, event_id, member_id):
    event = get_object_or_404(Event, id=event_id)
    member = get_object_or_404(Members, id=member_id)

    # Create attendance record if not already recorded
    Attendance.objects.get_or_create(member=member, event=event)

    return redirect('attendance:eventDetail', id=event_id)

