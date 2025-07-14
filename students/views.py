

# Create your views here.
from django.shortcuts import render, redirect,get_object_or_404
from django.db import models
from .models import Student
from .forms import StudentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q



# List all students
@login_required
def student_list(request):
    query = request.GET.get('q')
    if query:
        students = Student.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(course__icontains=query)
        )
    else:
        students = Student.objects.all()
    
    return render(request, 'students/student_list.html', {'students': students})


# Add new student
@login_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Student added successfully!")
            return redirect('student_list')
    else:
        form = StudentForm()
    
    students = Student.objects.all()
    return render(request, 'students/student_list.html', {
        'form': form,
        'students': students
    })



# Edit student detilas
@login_required
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully!")
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/edit_student.html', {'form': form, 'student': student})



# DELETE student
@login_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'students/delete_confirm.html', {'student': student})

#  Add Export View 
import csv
from django.http import HttpResponse

@login_required
def export_students_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'

    writer = csv.writer(response)
    writer.writerow(['First Name', 'Last Name', 'Roll No', 'Email', 'Branch', 'Contact', 'Admission Date'])

    students = Student.objects.all()
    for student in students:
        writer.writerow([
            student.first_name,
            student.last_name,
            student.email,
            student.course,
            student.contact_number,
            student.created_at,
        ])

    return response

