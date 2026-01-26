from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    """
    Base admin class for all models in the project.
    """

    readonly_fields = ("date_created", "date_updated")
    list_per_page = 25
