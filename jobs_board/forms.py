from flask.ext.wtf import Form
from wtforms_alchemy import model_form_factory

ModelForm = model_form_factory(Form)
