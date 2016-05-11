from health_check.backends.base import BaseHealthCheckBackend, ServiceUnavailable, ServiceReturnedUnexpectedResult
from health_check_db.models import TestModel
from django.db import DatabaseError, IntegrityError, transaction
from health_check.plugins import plugin_dir

class DjangoDatabaseBackend(BaseHealthCheckBackend):

    def description(self):
        return "Checks that the default database can be saved to and read from"

    def check_status(self):
        try:
            with transaction.atomic():
                obj = TestModel.objects.create(title="test")
                obj.title = "newtest"
                obj.save()
                obj.delete()
            return True
        except IntegrityError:
            raise ServiceReturnedUnexpectedResult("Integrity Error")
        except DatabaseError:
            raise ServiceUnavailable("Database error")

plugin_dir.register(DjangoDatabaseBackend)
