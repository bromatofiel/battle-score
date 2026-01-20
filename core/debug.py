from pprint import pprint as pp
from contextlib import ContextDecorator
from datetime import datetime as D, timedelta as T

from django.utils import timezone
from django.db import connection, close_old_connections
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


def ppd(*args):
    for arg in args:
        pp(arg if not hasattr(arg, "__dict__") else arg.__dict__)


pgsql_refresh = close_old_connections


def pgsql(query):
    from django.db import connection

    cursor = connection.cursor()
    start = timezone.now()
    cursor.execute(query)
    duration = (timezone.now() - start).total_seconds()
    results = None
    if cursor.description:
        rows = cursor.fetchall()
        if len(rows) == 1:
            results = rows[0]
        else:
            results = rows
    print("Executed in %.3fs" % duration)
    return results


class catch(ContextDecorator):
    def __enter__(self):
        self.exception = None
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.exception = exc_value
        return True  # Stop exception propagation

    def __str__(self):
        return str(self.exception)


class sql_breakpoint:
    def __enter__(self):
        def wrapper(execute, sql, params, many, context):
            print("\nSQL breakpoint triggered")
            print(sql)
            import ipdb

            ipdb.set_trace()
            return execute(sql, params, many, context)

        self._cm = connection.execute_wrapper(wrapper)
        self._cm.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._cm.__exit__(exc_type, exc_val, exc_tb)


def model_shortcut(model, search_fields=None):

    def wrapper(value=None, many=False, lookup="icontains", **kwargs):
        # Main selection
        if isinstance(value, int):
            qs = model.objects.filter(pk=value)
        elif isinstance(value, str) and search_fields:
            conds = Q()
            for field in search_fields:
                conds |= Q(**{f"{field}__{lookup}": value})
            qs = model.objects.filter(conds)
        else:
            assert value is None, f"Can't interpret {type(value)} value: {value}"
        # Optional filtering
        if kwargs:
            qs = qs.filter(**kwargs)
        # Formatting
        if many:
            return qs
        else:
            return qs.get()

    return wrapper


USER = model_shortcut(User, search_fields=["email", "uid", "public_id"])
