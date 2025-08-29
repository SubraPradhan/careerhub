from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from jobs.models import Job   # ✅ import Job model


# ----------------------------
# Register View
# ----------------------------
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Go directly to dashboard
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


# ----------------------------
# Dashboard View
# ----------------------------
@login_required
def dashboard(request):
    if request.user.user_type == "employer":
        # ✅ Fetch only jobs created by this employer
        jobs = Job.objects.filter(employer=request.user)
        return render(request, 'users/employer_dashboard.html', {"jobs": jobs})
    else:
        return render(request, 'users/candidate_dashboard.html')



from django.shortcuts import get_object_or_404
from .forms import forms

@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, posted_by=request.user)
    if request.method == "POST":
        form = forms(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = forms(instance=job)
    return render(request, "jobs/edit_job.html", {"form": form})


@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, posted_by=request.user)
    if request.method == "POST":
        job.delete()
        return redirect("dashboard")
    return render(request, "jobs/confirm_delete.html", {"job": job})
