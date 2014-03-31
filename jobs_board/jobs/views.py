from flask import Blueprint, current_app, redirect, render_template, request, url_for
from flask.ext.security import current_user
from ..core import db
from .models import Company, Job
from .forms import CompanyForm, EditJobForm, NewJobForm

blueprint = Blueprint('jobs', __name__, template_folder='templates')

# TODO: this is standard CRUD stuf
# should be able to be generalize it
# possibly flask-classy?

@blueprint.route('/')
def index():
    return redirect(url_for('.job_list'))

@blueprint.route('/jobs/', methods=['GET', 'POST'])
def job_list():
    jobs = Job.query.active()
    form = NewJobForm()
    form.company.query = current_user.companies
    if form.validate_on_submit():
        job = Job(poster=current_user)
        form.populate_obj(job)
        db.session.commit()
        return redirect('/')
    return render_template('jobs/job-list.html', form=form, jobs=jobs)

@blueprint.route('/jobs/<int:job_id>/', methods=['GET', 'POST'])
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    form = EditJobForm(obj=job)
    return render_template('jobs/job-detail.html', form=form, job=job)

@blueprint.route('/companies/', methods=['GET', 'POST'])
def company_list():
    companies = Company.query.approved()
    form = CompanyForm()
    if form.validate_on_submit():
        company = Company(creator=current_user)
        form.populate_obj(company)
        company.admins.append(current_user)
        db.session.commit()
        return redirect('/')
    return render_template('jobs/company-list.html', form=form, companies=companies)

@blueprint.route('/companies/<int:company_id>/', methods=['GET', 'POST'])
def company_detail(company_id):
    company = Company.query.get_or_404(company_id)
    form = CompanyForm(obj=company)
    return render_template('jobs/company-detail.html', form=form, company=company)
