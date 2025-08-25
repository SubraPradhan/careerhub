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


# Dashboard
@login_required
def dashboard(request):
    if request.user.user_type == "employer":
        jobs = Job.objects.filter(employer=request.user)
        return render(request, "employer_dashboard.html", {"jobs": jobs})
    else:  # job seeker
        jobs = Job.objects.all()
        return render(request, "candidate_dashboard.html", {"jobs": jobs})






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



