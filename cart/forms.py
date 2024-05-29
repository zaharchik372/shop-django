from django import forms
from cart.models import ServiceExecution
from cart.models import Order


class ServiceExecutionForm(forms.ModelForm):
    class Meta:
        model = ServiceExecution
        fields = ['note', 'employee']


class CreateServiceExecutionForm(forms.ModelForm):
    order = forms.ModelChoiceField(queryset=Order.objects.all(), label='Заказ')

    class Meta:
        model = ServiceExecution
        fields = ['order', 'execution_date', 'note', 'employee']
        widgets = {
            'execution_date': forms.DateInput(attrs={'type': 'date'}),
        }
