"""
Django-admin command to wait for the database to be available.
"""
from django.core.management.base import BaseCommand
from django.db.utils import OperationalError

from psycopg2 import OperationalError as Psycopg20Error

import time


class Command(BaseCommand):
    """https://docs.djangoproject.com/en/4.2/howto/custom-management-commands/"""
    help = "Django-admin command to wait for the database."


    def handle(self, *args, **options):
        """Entry point for the command."""
        self.stdout.write("Waiting for the database...")
        db_down = True

        while db_down:
            try:
                self.check(databases=["default"])
                db_down = False
            except (Psycopg20Error, OperationalError):
                self.stdout.write("Database unavailable waiting 1 second...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database available!"))
