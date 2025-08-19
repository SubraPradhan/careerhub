from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import JobForm
from .models import Job

# Add Job (Employer only)
@login_required
def add_job(request):
    if request.user.user_type != "employer":   # <-- stick to user_type
        return redirect('dashboard')
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user  # must match Job model field
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
        jobs = Job.objects.filter(employer=request.user)  # consistent field
    else:  # job seeker
        jobs = Job.objects.all()
    return render(request, "dashboard.html", {"jobs": jobs})
