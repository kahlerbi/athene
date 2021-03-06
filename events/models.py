import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.core.exceptions import ValidationError
from django.template import Context, Template, loader
from django.utils.functional import cached_property
from django.utils.timezone import now
from multiselectfield import MultiSelectField

from . import google, twilio, mailgun

DAYS_OF_WEEK = [
    (0, 'Sunday'),
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday')
]

class Calendar(models.Model):
    calendar_id = models.CharField(max_length=250, primary_key=True)
    name = models.CharField(max_length=120, editable=False)
    inactive_date = models.DateField(blank=True, null=True)
    track_attendance = models.BooleanField(default=False)
    send_autotext_days = MultiSelectField(choices=DAYS_OF_WEEK, blank=True)
    autotext_days_in_advance = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    def clean(self):
        try:
            calendar_obj = google.calendar.get_calendar(self.calendar_id)
        except ValueError as e:
            raise ValidationError({'calendar_id', e.args[0]})
        else:
            self.name = calendar_obj['summary']
    

class HumanAttendance(models.Model):
    human = models.ForeignKey('seekers.Human', verbose_name='Attendee', on_delete=models.CASCADE)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    event_id = models.CharField(max_length=120, db_index=True)
    recurring_event_id = models.CharField(max_length=120, blank=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True)

    @cached_property
    def event(self):
        if not self.event_id:
            return {}
        try:
            event_obj = google.calendar.get_event(self.calendar.calendar_id, self.event_id)
        except ValueError:
            return {}
        return event_obj
    
    def __str__(self):
        return f'{self.human} went to {self.event.get("summary") or "Unknown event"}'
    
    class Meta:
        verbose_name = 'Event attendance'
        verbose_name_plural = 'Event attendance'
        unique_together = [('human', 'calendar', 'event_id')]

CONTACT_PREFERENCES = [
    (1, 'Email'),
    (2, 'SMS'),
    # (3, 'Facebook')
]

class HumanCalendarSubscription(models.Model):
    human = models.ForeignKey('seekers.Human', on_delete=models.CASCADE)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    contact_method = models.IntegerField(choices=CONTACT_PREFERENCES)

    def __str__(self):
        return f'{self.human} subscribed to {self.calendar}'

    def send_events_summary(self, events, extra_context=None, test=False):
        logger.debug(f'Sending to event summary to {self.human} via {self.get_contact_method_display()}')
        extra_context = extra_context or dict()
        context = dict(
            human=self.human,
            events=events,
            calendar=self.calendar,
            **extra_context
        )
        template_path = f'events/autotext/{self.get_contact_method_display().lower()}.txt'
        template_obj = loader.get_template(template_path)
        content = template_obj.render(context)
        if self.contact_method == 1: # email
            if not self.human.email:
                logger.warning(f'Human {self.human} is set to receive {self.calendar} via email but has no email address')
                return
            today = Template('{{ timestamp|date:"DATE_FORMAT" }}').render(
                Context(dict(timestamp=now()))
            )
            mailgun.send_email('info@seekhealing.org', self.human.email,
                                    f'Upcoming {self.calendar.name} - {today}',
                                    content, test=test)
        elif self.contact_method == 2: # sms
            if not self.human.phone_number:
                logger.warning(f'Human {self.human} is set to receive {self.calendar} via SMS but has no phone number')
                return
            twilio.sms.send_text(str(self.human.phone_number), content, test=test)

    class Meta:
        unique_together = [('human', 'calendar')]
        verbose_name = 'Calendar subscription'