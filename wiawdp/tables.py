from wiawdp.models import Contract
import django_tables2 as tables

class ContractTable(tables.Table):
    pk = tables.Column(verbose_name='RecId')
    full_name = tables.Column(accessor='client.full_name', order_by=('client__first_name', 'client__last_name'))

    class Meta:
        model = Contract
        template_name = 'django_tables2/bootstrap.html'
        fields = ('pk', 'full_name', 'workforce', 'end_date', 'performance')

class ContractTableEditable(tables.Table):
    pk = tables.Column(verbose_name='RecId')
    full_name = tables.Column(accessor='client.full_name', order_by=('client__first_name', 'client__last_name'))
    actions = tables.TemplateColumn("""
<form method="GET" action="{% url 'wiawdp:modify_contract' %}">
    <input type="hidden" name="contract_id" value="{{ record.id }}">
    <input type="submit" value="Edit" class="btn btn-info">
</form>
    """, orderable=False)

    class Meta:
        model = Contract
        template_name = 'django_tables2/bootstrap.html'
        fields = ('pk', 'full_name', 'workforce', 'end_date', 'performance')