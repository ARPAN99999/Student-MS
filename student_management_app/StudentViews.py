from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.db.models import Avg
import datetime
from .models import CustomUser, Staffs, Courses, Subjects, Students, Attendance, AttendanceReport, LeaveReportStudent, FeedBackStudent, StudentResult

def student_home(request):
    try:
        student_obj = Students.objects.get(admin=request.user.id)
        total_attendance = AttendanceReport.objects.filter(student_id=student_obj).count()
        attendance_present = AttendanceReport.objects.filter(
            student_id=student_obj,
            status=True,
        ).count()
        attendance_absent = AttendanceReport.objects.filter(
            student_id=student_obj,
            status=False,
        ).count()

        total_subjects = 0
        subject_name = []
        data_present = []
        data_absent = []

        attendance_percentage = 0
        leave_pending = 0
        leave_approved = 0
        feedback_count = 0
        feedback_replied = 0
        result_subject_count = 0
        result_average = 0
        recent_attendance = []
        recent_feedback = []

        leave_data = LeaveReportStudent.objects.filter(student_id=student_obj)
        leave_pending = leave_data.filter(leave_status=0).count()
        leave_approved = leave_data.filter(leave_status=1).count()

        feedback_data = FeedBackStudent.objects.filter(student_id=student_obj)
        feedback_count = feedback_data.count()
        feedback_replied = feedback_data.exclude(feedback_reply="").count()
        recent_feedback = feedback_data.order_by('-created_at')[:4]

        results = StudentResult.objects.filter(student_id=student_obj)
        result_subject_count = results.count()
        result_average = results.aggregate(avg_total=Avg('subject_exam_marks'))['avg_total']
        if result_average is None:
            result_average = 0
        result_average = round(result_average, 1)

        recent_attendance = AttendanceReport.objects.filter(student_id=student_obj).select_related(
            'attendance_id',
            'attendance_id__subject_id',
        ).order_by('-attendance_id__attendance_date')[:6]

        if total_attendance > 0:
            attendance_percentage = round((attendance_present / total_attendance) * 100, 1)

        if student_obj.course_id:
            total_subjects = Subjects.objects.filter(course_id=student_obj.course_id).count()
            subject_data = Subjects.objects.filter(course_id=student_obj.course_id)
            for subject in subject_data:
                attendance = Attendance.objects.filter(subject_id=subject.id)
                attendance_present_count = AttendanceReport.objects.filter(
                    attendance_id__in=attendance,
                    status=True,
                    student_id=student_obj.id,
                ).count()
                attendance_absent_count = AttendanceReport.objects.filter(
                    attendance_id__in=attendance,
                    status=False,
                    student_id=student_obj.id,
                ).count()
                subject_name.append(subject.subject_name)
                data_present.append(attendance_present_count)
                data_absent.append(attendance_absent_count)

        context = {
            "total_attendance": total_attendance,
            "attendance_present": attendance_present,
            "attendance_absent": attendance_absent,
            "attendance_percentage": attendance_percentage,
            "total_subjects": total_subjects,
            "subject_name": subject_name,
            "data_present": data_present,
            "data_absent": data_absent,
            "leave_pending": leave_pending,
            "leave_approved": leave_approved,
            "feedback_count": feedback_count,
            "feedback_replied": feedback_replied,
            "result_subject_count": result_subject_count,
            "result_average": result_average,
            "recent_attendance": recent_attendance,
            "recent_feedback": recent_feedback,
        }
        return render(request, "student_template/student_home_template.html", context)
    except Students.DoesNotExist:
        messages.error(request, "Student profile not found. Please contact administrator.")
        return redirect('home')
    except Exception as e:
        messages.error(request, f"Error loading dashboard: {str(e)}")
        return redirect('home')


def student_view_attendance(request):
    try:
        student = Students.objects.get(admin=request.user.id)
        subjects = Subjects.objects.none()
        if student.course_id:
            subjects = Subjects.objects.filter(course_id=student.course_id)

        context = {
                "subjects": subjects
        }
        return render(request, "student_template/student_view_attendance.html", context)
    except Students.DoesNotExist:
        messages.error(request, "Student profile not found. Please contact administrator.")
        return redirect('student_home')


def student_view_attendance_post(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('student_view_attendance')
    else:
        # Getting all the Input Data
        subject_id = request.POST.get('subject')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Parsing the date data into Python object
        start_date_parse = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_parse = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

        # Getting all the Subject Data based on Selected Subject
        subject_obj = Subjects.objects.get(id=subject_id)
        
        # Getting Logged In User Data
        user_obj = CustomUser.objects.get(id=request.user.id)
        
        # Getting Student Data Based on Logged in Data
        stud_obj = Students.objects.get(admin=user_obj)

        # Now Accessing Attendance Data based on the Range of Date
        # Selected and Subject Selected
        attendance = Attendance.objects.filter(attendance_date__range=(start_date_parse,
                                                                       end_date_parse),
                                               subject_id=subject_obj)
        # Getting Attendance Report based on the attendance
        # details obtained above
        attendance_reports = AttendanceReport.objects.filter(attendance_id__in=attendance,
                                                             student_id=stud_obj)

        
        context = {
            "subject_obj": subject_obj,
            "attendance_reports": attendance_reports
        }

        return render(request, 'student_template/student_attendance_data.html', context)
       

def student_apply_leave(request):
    student_obj = Students.objects.get(admin=request.user.id)
    leave_data = LeaveReportStudent.objects.filter(student_id=student_obj)
    context = {
        "leave_data": leave_data
    }
    return render(request, 'student_template/student_apply_leave.html', context)


def student_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('student_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        student_obj = Students.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStudent(student_id=student_obj,
                                              leave_date=leave_date,
                                              leave_message=leave_message,
                                              leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('student_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('student_apply_leave')


def student_feedback(request):
    student_obj = Students.objects.get(admin=request.user.id)
    feedback_data = FeedBackStudent.objects.filter(student_id=student_obj)
    context = {
        "feedback_data": feedback_data
    }
    return render(request, 'student_template/student_feedback.html', context)


def student_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('student_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        student_obj = Students.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackStudent(student_id=student_obj,
                                           feedback=feedback,
                                           feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('student_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('student_feedback')


def student_profile(request):
    try:
        user = CustomUser.objects.get(id=request.user.id)
        student = Students.objects.get(admin=user)

        context = {
            "user": user,
            "student": student
        }
        return render(request, 'student_template/student_profile.html', context)
    except Students.DoesNotExist:
        messages.error(request, "Student profile not found. Please contact administrator.")
        return redirect('student_home')


def student_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('student_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            student = Students.objects.get(admin=customuser.id)
            student.address = address
            student.save()
            
            messages.success(request, "Profile Updated Successfully")
            return redirect('student_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('student_profile')


def student_view_result(request):
    try:
        student = Students.objects.get(admin=request.user.id)
        student_result = StudentResult.objects.filter(student_id=student.id)
        context = {
            "student_result": student_result,
        }
        return render(request, "student_template/student_view_result.html", context)
    except Students.DoesNotExist:
        messages.error(request, "Student profile not found. Please contact administrator.")
        return redirect('student_home')
