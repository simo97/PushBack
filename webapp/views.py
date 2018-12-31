from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


#  -------------- core models-------------------
from core.models import Application

# --------------- forms ----------------
from .forms import CreateApplicationForm

# Create your views here.


class ApplicationListView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'webapp/application/list.html'
    context_object_name = 'application_list'

    def get_queryset(self):
        """
        Only return application related to the current user
        :return:
        """
        return Application.objects.filter(account=self.request.user.account)


class ApplicationCreateView(LoginRequiredMixin, CreateView):
    model = Application
    form_class = CreateApplicationForm
    template_name = 'webapp/application/create.html'
    success_url = reverse_lazy('webapp:application-list')

    def get_initial(self):
        """
        Should be use to generate default form data such as the account, it should be hidden
        :return:
        """
        return {
            'account': self.request.user.account  # the current connected user's account
        }


class ApplicationDetailView(LoginRequiredMixin, DetailView):
    model = Application
    template_name = 'webapp/application/detail.html'
    context_object_name = 'application'

    def get_context_data(self, **kwargs):
        ctx = super(ApplicationDetailView, self).get_context_data(**kwargs)
        ctx['notifications'] = self.object.notifications.all()
        ctx['clients'] = self.object.client_set.all()
        return ctx


class ApplicationDeleteView(LoginRequiredMixin, DeleteView):
    model = Application
    success_url = reverse_lazy('webapp:application-list')
    template_name = 'webapp/application/confirm_delete.html'
