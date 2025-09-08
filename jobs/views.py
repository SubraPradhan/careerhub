from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import JobForm, ApplicationForm
from .models import Job, Application


# Add Job (Employer only)
@login_required
def add_job(request):
    if request.user.user_type != "employer":   # only employers can add jobs
        return redirect('dashboard')
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user  # link job to employer
            job.save()
            return redirect('dashboard')
    else:
        form = JobForm()
    return render(request, 'jobs/add_job.html', {'form': form})


# Job List (open to all users)
@login_required
def job_list(request):
    jobs = Job.objects.all().order_by('-created_at')
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

# Job Detail
def job_detail(request, pk):
    job = get_object_or_404(Job, id=pk)
    return render(request, 'jobs/job_detail.html', {'job': job})


# Apply to a Job
@login_required
def apply_to_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            return redirect("job_detail", pk=job.id)  # ✅ fixed here
    else:
        form = ApplicationForm()
    return render(request, "jobs/apply_job.html", {"form": form, "job": job})

# Employer: View Applications for their Jobs
@login_required
def view_applications(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    applications = job.applications.all()
    return render(request, "jobs/view_applications.html", {
    "job": job,
    "applications": applications
})


@login_required
def update_application_status(request, app_id, status):
    application = get_object_or_404(Application, id=app_id, job__employer=request.user)
    if status in ["selected", "rejected"]:
        application.status = status
        application.save()
    return redirect("view_applications", job_id=application.job.id)


#Employer Dashboard View
@login_required
def employer_dashboard(request):
    # Only show jobs posted by this employer
    jobs = Job.objects.filter(employer=request.user)
    
    context = {
        'jobs': jobs
    }
    return render(request, 'employer_dashboard.html', context)






#Candidate Dashboard View
@login_required
def candidate_dashboard(request):
    # 1️⃣ All available jobs
    jobs = Job.objects.all()

    # 2️⃣ All applications by this candidate
    applications = Application.objects.filter(applicant=request.user)

    # 3️⃣ Jobs the candidate has applied to
    applied_jobs = Job.objects.filter(applications__applicant=request.user)

    # 4️⃣ Debug prints
    print(f"DEBUG: Candidate '{request.user.username}' sees {jobs.count()} total jobs")
    print(f"DEBUG: Candidate '{request.user.username}' applied to {applications.count()} jobs")
    print("DEBUG: Applied job titles:", [job.title for job in applied_jobs])

    context = {
        'jobs': jobs,
        'applications': applications,
        'applied_jobs': applied_jobs
    }

    return render(request, 'candidate_dashboard.html', context)

