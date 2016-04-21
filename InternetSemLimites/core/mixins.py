from django.contrib.auth.models import User
from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string
from django.views.generic import CreateView


class EmailAdminCreateMixin:

    email_to = None
    email_context_name = None
    email_template_name = None
    email_from = settings.DEFAULT_FROM_EMAIL
    email_subject = ''

    def send_mail(self):

        subject = self.email_subject
        from_ = self.email_from
        to = self.get_email_to()
        template_name = self.get_email_template_name()
        context = self.get_email_context_data()

        body = render_to_string(template_name, context)
        return mail.send_mail(subject, body, from_, to)

    def get_email_template_name(self):
        if self.email_template_name:
            return self.email_template_name
        return '{}/{}_email.txt'.format(self.object._meta.app_label,
                                        self.object._meta.model_name)

    def get_email_context_data(self, **kwargs):
        context = dict(kwargs)
        context.setdefault(self.get_email_context_name(), self.object)
        return context

    def get_email_context_name(self):
        if self.email_context_name:
            return self.email_context_name
        return self.object._meta.model_name

    def get_email_to(self):
        for user in User.objects.exclude(email=''):
            yield user.email


class EmailAdminCreateView(EmailAdminCreateMixin, CreateView):

    def form_valid(self, form):
        response = super().form_valid(form)
        self.send_mail()
        return response
