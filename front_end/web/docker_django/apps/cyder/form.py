from __future__ import division
from django.forms import ModelForm, Textarea
import models as m
from bootstrap3_datetime.widgets import DateTimePicker
from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab, Div
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset


class ProjectDescriptionForm(ModelForm):

    class Meta:
        model = m.Project
        fields = ('name', 'description')
        widgets = {
          'description': Textarea(attrs={'rows':2, 'cols':20}),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectDescriptionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'description-id'
        self.helper.form_method = 'post'
        self.helper.form_action = "/my_project_settings/" + str(self.instance.id) + '/'
        self.helper.add_input(Submit('submit', 'Update', css_class="pull-right"))
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Field('name', placeholder="Project name"),
            Field('description', placeholder="Project description"))


class ProjectCreationForm(ModelForm):

    class Meta:
        model = m.Project
        fields = ('name', 'description')
        widgets = {
          'description': Textarea(attrs={'rows':2, 'cols':20}),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectCreationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'description-id'
        self.helper.form_method = 'post'
        self.helper.form_action = "/create_project/"
        self.helper.add_input(Submit('submit', 'Create', css_class="pull-right"))
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Field('name', placeholder="Project name"),
            Field('description', placeholder="Project description"))


class ElectricVehicleScenarioForm(ModelForm):

    class Meta:
        model = m.ElectricVehicleScenario
        fields = ('nb_vehicles', 'is_active')
        labels = {'nb_vehicles': 'Number of electric vehicles',
                  'is_active': 'Toggle influence of electric vehicles'}

    def __init__(self, *args, **kwargs):
        super(ElectricVehicleScenarioForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'description-id'
        self.helper.form_method = 'post'
        self.helper.form_action = "/my_project_model_scenarios/" + str(self.instance.project_model.id) + '/'
        self.helper.add_input(Submit('submit', 'Save', css_class="pull-right"))
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-6'
        self.helper.layout = Layout(
            Field('nb_vehicles', placeholder="Number of vehicles to simulate"),
            Field('is_active', placeholder="Toggle electric vehicle loads"))


# widgets = {
#   'description': Textarea(attrs={'rows':2, 'cols':20}),
#   'simulation_date': DateTimePicker(
#         options={"format": "YYYY-MM-DD HH:mm",
#                  "pickSeconds": False},
#         attrs={'placeholder': 'ex: 2016-06-17 23:50'}
#     )
# }