# core/management/commands/cleanup_duplicate_emails.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone


class Command(BaseCommand):
    help = 'Clean up duplicate email addresses in User model'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without actually making changes',
        )
        parser.add_argument(
            '--auto-fix',
            action='store_true',
            help='Automatically fix duplicates by appending timestamp to email',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        auto_fix = options['auto_fix']

        self.stdout.write(self.style.WARNING('Checking for duplicate emails...'))

        # Find duplicate emails (excluding empty emails)
        duplicate_emails = User.objects.values('email').annotate(
            count=Count('email')
        ).filter(count__gt=1, email__isnull=False).exclude(email='')

        if not duplicate_emails.exists():
            self.stdout.write(self.style.SUCCESS('No duplicate emails found!'))
            return

        self.stdout.write(
            self.style.ERROR(f'Found {duplicate_emails.count()} email addresses with duplicates:')
        )

        total_affected_users = 0

        for dup in duplicate_emails:
            email = dup['email']
            count = dup['count']
            total_affected_users += count

            users = User.objects.filter(email=email).order_by('date_joined')

            self.stdout.write(f"\nEmail: '{email}' ({count} users)")

            for i, user in enumerate(users):
                status = "KEEP (oldest)" if i == 0 else "NEEDS FIX"
                self.stdout.write(
                    f"  - ID: {user.id}, Username: {user.username}, "
                    f"Joined: {user.date_joined}, Status: {status}"
                )

                # Auto-fix duplicates (except the oldest one)
                if auto_fix and i > 0:
                    if not dry_run:
                        # Append timestamp to make email unique
                        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
                        new_email = f"{email.split('@')[0]}_{timestamp}@{email.split('@')[1]}"

                        user.email = new_email
                        user.save()

                        self.stdout.write(
                            self.style.SUCCESS(f"    → Fixed: Changed to {new_email}")
                        )
                    else:
                        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
                        new_email = f"{email.split('@')[0]}_{timestamp}@{email.split('@')[1]}"
                        self.stdout.write(
                            self.style.WARNING(f"    → Would change to: {new_email}")
                        )

        self.stdout.write(f"\nTotal users affected: {total_affected_users}")

        if dry_run:
            self.stdout.write(
                self.style.WARNING('\nThis was a dry run. No changes were made.')
            )
            self.stdout.write(
                'Run with --auto-fix to automatically fix duplicates, or manually fix them.'
            )
        elif not auto_fix:
            self.stdout.write(
                self.style.WARNING('\nManual action required:')
            )
            self.stdout.write('1. Contact users to use different email addresses, OR')
            self.stdout.write('2. Run with --auto-fix to automatically append timestamps, OR')
            self.stdout.write('3. Manually update duplicate emails in Django admin')
        else:
            self.stdout.write(
                self.style.SUCCESS('\nDuplicate emails have been fixed!')
            )
            self.stdout.write('You can now run the add_email_unique_constraint command.')

# Contoh penggunaan:
# python manage.py cleanup_duplicate_emails --dry-run
# python manage.py cleanup_duplicate_emails --auto-fix