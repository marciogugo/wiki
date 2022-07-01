from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, HTML, Row # Div, HTML, Button, Row, 
from crispy_forms.bootstrap import FormActions

from django.template.loader import render_to_string

class EntryForm(forms.Form):
    formTitle = forms.CharField(
        label="Title", 
        max_length=30, 
        help_text="Enter entry title here in markdown format.",
        required=False,
    )

    formContent = forms.CharField( 
        label="Content", 
        help_text="Enter entry content here in markdown format.",
        required=False,
        widget=forms.Textarea(),
        initial = ""
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)     

        self.helper = FormHelper()       
        self.helper.form_id = 'id-formEntry'
        self.helper.form_class = 'EntryForm'
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Field('formTitle', type='text', name='formTitle', css_class='input-xlarge'),
            Field('formContent', rows='6', name='formContent', css_class='input-xlarge'),
            FormActions(
                Submit('cancel', 'Cancel', css_class="btn-primary"),
                Submit('save', 'Save changes', css_class="btn-primary"),
            )
        )
    
class EditEntryForm(forms.Form):
    formTitle = forms.CharField(
        label="Title", 
        max_length=30, 
        help_text="Enter entry title here in markdown format.",
        required=False,
    )

    formContent = forms.CharField( 
        label="Content", 
        help_text="Enter entry content here in markdown format.",
        required=False,
        widget=forms.Textarea(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)     

        self.helper = FormHelper()
        self.helper.form_id = 'id-formEntry'
        self.helper.form_class = 'EditEntryForm'
        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            Field('formTitle', type='text', name='formTitle', css_class='input-xlarge', value=kwargs['initial']['formTitle']),
            Field('formContent', rows='10', name='formContent', css_class='input-xlarge', template='text-area.html'),
            FormActions(
                Submit('cancel', 'Cancel', css_class="btn-primary"),
                Submit('save', 'Save changes', css_class="btn-primary"),
            )
        )
