from django.shortcuts import render, redirect
from wiawdp.forms import FindStudentForm, ViewReportForm, ModifyContractLookupForm
from django.urls import reverse_lazy
from wiawdp.models import Contract, WIAWDP
from django.views.generic import TemplateView, FormView, CreateView, UpdateView, DeleteView, View
from datetime import datetime
from django.contrib.auth.mixins import PermissionRequiredMixin
from wiawdp.tables import ContractTable, WIAWDPTable
from django_tables2 import SingleTableView, SingleTableMixin


class IndexView(TemplateView):
    template_name = 'wiawdp/index.html'


class ActiveContractView(PermissionRequiredMixin, SingleTableView):
    permission_required = 'wiawdp.view_contract'
    template_name = 'wiawdp/active_contracts.html'
    model = Contract
    table_data = Contract.objects.filter(end_date__gte=datetime.today())
    table_class = ContractTable

    def get_table_kwargs(self):
        user = self.request.user
        if user.has_perms('wiawdp.change_contract') or user.has_perms('wiawdp.delete_contract'):
            return super(ActiveContractView, self).get_table_kwargs()
        return {'exclude': ('actions',)}


class AddContractView(PermissionRequiredMixin, CreateView):
    permission_required = 'wiawdp.add_contract'
    model = Contract
    template_name = 'wiawdp/add_contract_form.html'
    success_url = reverse_lazy('wiawdp:active_contracts')
    fields = ['client', 'workforce', 'end_date', 'performance']


class ReportView(PermissionRequiredMixin, FormView):
    permission_required = 'wiawdp.view_contract'
    template_name = 'wiawdp/view_report.html'
    form_class = ViewReportForm
    success_url = reverse_lazy('wiawdp:index')

    def form_valid(self, form):
        return render(self.request, 'wiawdp/report.html')


class FormTableView(SingleTableMixin, FormView):
    result_template_name = None

    def filter_table_data(self, form):
        return None

    def get_context_data(self, **kwargs):
        context = super(FormView, self).get_context_data(**kwargs)
        if 'form' not in context or not context['form'].is_valid():
            return context
        table = self.get_table(**self.get_table_kwargs())
        context[self.get_context_table_name(table)] = table
        return context

    def form_valid(self, form):
        self.table_data = self.filter_table_data(form)
        return render(self.request, self.result_template_name, context=self.get_context_data(form=form))


class SearchContractsView(PermissionRequiredMixin, FormTableView):
    permission_required = ('wiawdp.view_contract', 'wiawdp.view_person')
    template_name = 'wiawdp/search_contracts_form.html'
    result_template_name = 'wiawdp/search_contracts_results.html'
    form_class = FindStudentForm
    table_class = ContractTable

    def get_table_kwargs(self):
        return {
            'empty_text': 'No results matching query.'
        }

    def filter_table_data(self, form):
        print(Contract.objects.none())
        contract_list = Contract.objects
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        ssn = form.cleaned_data['ssn']
        email = form.cleaned_data['email']
        home_phone = form.cleaned_data['home_phone']
        cell_phone = form.cleaned_data['cell_phone']
        zipcode = form.cleaned_data['zipcode']

        if not any((first_name, last_name, ssn, email, home_phone, cell_phone, zipcode)):
            return Contract.objects.none()

        if first_name:
            contract_list = contract_list.filter(client__first_name__iexact=first_name)
        if last_name:
            contract_list = contract_list.filter(client__last_name__iexact=last_name)
        if ssn:
            contract_list = contract_list.filter(client__ssn__iexact=ssn)
        if email:
            contract_list = contract_list.filter(client__email__iexact=email)
        if home_phone:
            contract_list = contract_list.filter(client__homePhone=home_phone)
        if cell_phone:
            contract_list = contract_list.filter(client__cellPhone__iexact=cell_phone)
        if zipcode:
            contract_list = contract_list.filter(client__zipcode__iexact=zipcode)

        return contract_list


class ModifyContractView(PermissionRequiredMixin, UpdateView):
    permission_required = 'wiawdp.change_contract'
    model = Contract
    template_name = 'wiawdp/modify_contract_form.html'
    fields = ['workforce', 'end_date', 'performance']
    success_url = reverse_lazy('wiawdp:active_contracts')

    def get_object(self):
        return Contract.objects.get(pk=self.request.GET.get('contract_id'))


class ModifyContractLookupView(PermissionRequiredMixin, FormTableView):
    permission_required = 'wiawdp.change_contract'
    template_name = 'wiawdp/modify_contract_lookup_form.html'
    result_template_name = 'wiawdp/modify_contract_lookup_results.html'
    form_class = ModifyContractLookupForm
    table_class = ContractTable

    def get_table_kwargs(self):
        return {
            'empty_text': 'No results matching query.'
        }

    def filter_table_data(self, form):
        return Contract.objects.filter(client__pk__exact=form.cleaned_data['student_id'])


class WIAWDPView(SingleTableView):
    model = WIAWDP
    table_data = WIAWDP.objects.all()
    table_class = WIAWDPTable
    template_name = 'wiawdp/programs.html'


class DeleteContractView(DeleteView):
    model = Contract
    success_url = reverse_lazy('wiawdp:active_contracts')

    def get_object(self, queryset=None):
        return Contract.objects.get(pk=self.request.POST.get('pk'))
