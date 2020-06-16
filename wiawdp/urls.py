from django.urls import path
from wiawdp.views import IndexView, AddContractView, ReportView, ModifyContractView, ModifyContractLookupView, \
    ActiveContractView, SearchContractsView, CareerPathwayView

app_name = 'wiawdp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('active_contracts/', ActiveContractView.as_view(), name='active_contracts'),
    path('add_contract/', AddContractView.as_view(), name='add_contract'),
    path('view_report/', ReportView.as_view(), name='view_report'),
    path('search_contracts/', SearchContractsView.as_view(), name='search_contracts'),
    path('modify_contract_lookup/', ModifyContractLookupView.as_view(), name='modify_contract_lookup'),
    path('modify_contract/', ModifyContractView.as_view(), name='modify_contract'),
    path('career_pathways/', CareerPathwayView.as_view(), name='available_programs')
]
