from datetime import datetime, timedelta
from flask import current_app
from flask.ext.sqlalchemy import BaseQuery
from ..core import db
from ..users.models import User

company_admins = db.Table(
    'company_admins',
    db.Column('company_id', db.Integer, db.ForeignKey('company.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
)


class CompanyQuery(BaseQuery):
    def approved(self):
        return self.filter(Company.approved == True)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    # This is nullable by design. The default will be null.
    # False means explicitly banned, and True means allowed.
    approved = db.Column(db.Boolean)

    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    creator = db.relationship('User', backref=db.backref('companies_created', lazy='dynamic'))
    admins = db.relationship(
        'User',
        secondary=company_admins,
        backref=db.backref('companies', lazy='dynamic'),
    )

    query_class = CompanyQuery

    def __str__(self):
        return self.name


class JobQuery(BaseQuery):
    def active(self):
        start = datetime.now() - timedelta(days=current_app.config['JOB_ACTIVE_DAYS'])
        return self.join(Company).filter(Company.approved == True).filter(Job.created >= start).order_by(Job.created.desc())


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)

    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    company = db.relationship('Company', backref=db.backref('jobs', lazy='dynamic'))
    poster_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    poster = db.relationship('User', backref=db.backref('jobs', lazy='dynamic'))

    query_class = JobQuery

    def __str__(self):
        return self.title
