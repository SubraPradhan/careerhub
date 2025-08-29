from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from jobs.models import Job


class Command(BaseCommand):
    help = "Fix orphan jobs (with employer=None) by assigning them to a given employer"

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            type=str,
            required=True,
            help="Employer username to assign orphan jobs to",
        )

    def handle(self, *args, **options):
        User = get_user_model()
        username = options["username"]

        try:
            employer = User.objects.get(username=username, user_type="employer")
        except User.DoesNotExist:
            raise CommandError(f"Employer with username '{username}' not found.")

        updated = Job.objects.filter(employer__isnull=True).update(employer=employer)

        if updated:
            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ Fixed {updated} orphan job(s). Assigned to employer: {employer.username}"
                )
            )
        else:
            self.stdout.write(self.style.WARNING("No orphan jobs found."))
