from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..forms import ModelForm
from .models import Company, Job

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        only = ('name', 'description')

class NewJobForm(ModelForm):
    company = QuerySelectField()

    class Meta:
        model = Job

class EditJobForm(ModelForm):
    class Meta:
        model = Job
