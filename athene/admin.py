from django.contrib import admin
from django.urls import path

from seekers.admin_site import SeekersAdminSiteMixin
from events.admin_site import EventsAdminSiteMixin

class AtheneAdminSite(SeekersAdminSiteMixin, EventsAdminSiteMixin, admin.AdminSite):
    site_header = "SeekHealing"
    site_title = "SeekHealing Seekers Database"
    site_url = None
    index_title = "Seekers Database"
    

