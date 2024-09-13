from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError
from django.template.loader import render_to_string
from .models import Members
from .forms import MembersForm
from attendance.models import Attendance


# Create your views here.

def home(request):
    return render(request, 'home.html')

def memberList(request):
    return render(request, 'members/memberList.html', {'members': Members.objects.all()})

from attendance.models import Attendance

def viewMember(request, id):
    member = Members.objects.get(pk=id)
    events_attended = Attendance.objects.filter(member=member)
    return render(request, 'members/viewMember.html', {
        'member': member,
        'events_attended': events_attended,
    })

def addMember(request):
    if request.method == 'POST':
        form = MembersForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                member = form.save(commit=False)
                member.save()
                messages.success(request, f"Member: {member.firstName} {member.lastName} has been added successfully!")
            except IntegrityError:
                messages.error(request, 'Failed to add member.')
            return redirect('members:members')
    else:
        form = MembersForm()

    return render(request, 'members/addMember.html', {'form': form})
    
def editMember(request, id):
    member = Members.objects.get(pk=id)
    if request.method == 'POST':
        form = MembersForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, f"Member: {member.firstName} {member.middleName} {member.lastName} has been updated successfully!")
            return redirect('members:members')
    else:
        form = MembersForm(instance=member)

    context = {
        'form': form,
        'member': member
    }

    html_form = render_to_string('members/editMember.html', context, request=request)
    return JsonResponse({'html_form': html_form})

def deleteMember(request, id):
    if request.method == 'POST':
        member = Members.objects.get(pk=id)
        member.delete()
        messages.success(request, f"Member: {member.firstName} {member.middleName} {member.lastName} has been deleted successfully!")
    return HttpResponseRedirect(reverse('members:members'))

