from wiawdp.models import Contract
import django_tables2 as tables


class ContractTable(tables.Table):
    pk = tables.Column(verbose_name='RecId')
    client = tables.Column()
    actions = tables.TemplateColumn(template_name="wiawdp/contract_table_actions.html", orderable=False)

    def render_client(self, value):
        return f'{value.first_name} {value.last_name} ({value.pk})'

    class Meta:
        model = Contract
        template_name = 'django_tables2/bootstrap.html'
        fields = ('pk', 'client', 'workforce', 'end_date', 'performance')
