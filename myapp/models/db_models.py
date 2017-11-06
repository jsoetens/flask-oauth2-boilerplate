import random
import string

from sqlalchemy.sql import func
from flask_login import UserMixin

from myapp.models.db_orm import db

from myapp.utils.argon2 import generate_argon2_hash, check_argon2_hash


# TODO: review if indexes are created with PK, add others if needed as well
# TODO: add naming conventions using metadata
# http://docs.sqlalchemy.org/en/latest/core/constraints.html#configuring-constraint-naming-conventions  # noqa

# Relationships
# One to One (1:1) - For example, one employee is assigned one employee id
# One to Many (1:M) - one department contains many employees
# Many to Many (M:M) - many employees take many training courses
# We are using SQLAlchemy lazy='dynamic' with returns a query object
# instead of firing the query.

# We are using SQLAlchemy's server_default / onupdate / server_onupdate
# for our timestamps. On the frontend it needs some handling.
# Another common way is using datetime.utcnow


class User(UserMixin, db.Model):

    """
    Maps subclass of declarative_base() to a Python class
    to table users_oauth2.
    UserMixin provides default implementations for the methods that Flask-Login
    expects user objects to have:
    is_active, is_authenticated, is_anonymous, get_id
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer)
    provider = db.Column(db.String, nullable=False)
    social_id = db.Column(db.String, nullable=False)
    email_address = db.Column(db.String)
    username = db.Column(db.String)
    password_hash = db.Column(db.String)
    created_date = db.Column(db.DateTime(
        timezone=True), server_default=func.now())
    updated_date = db.Column(db.DateTime(
        timezone=True), onupdate=func.now())
    stores = db.relationship('Store', backref='user', lazy='dynamic')

    # __table_args__ value must be a tuple, dict, or None
    __table_args__ = (
        db.PrimaryKeyConstraint('id', name='pk_users'),
        db.UniqueConstraint(
            'provider', 'social_id',
            name='uq_users_1'))

    def generate_social_id(size=20, chars=string.digits):
        """
        Generates a social_id that can be used for local myapp users.
        It's big enough so that it should be unique.

        Returns:
            social_id
        """
        return ''.join(
            random.SystemRandom().choice(chars) for _ in range(size))

    @property
    def password(self):
        """
        The password property will call generate_argon2_hash and
        write the result to the password_hash field.
        Reading this property will return an error.
        """
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_argon2_hash(password)

    def verify_password(self, password):
        """
        Verifies the password against the hashed version stored
        in the User model.
        """
        return check_argon2_hash(password, self.password_hash)

    def to_dict(self):
        """ Convert the model to a dictionary that can go into a JSON """
        return {
            # id is unnecessary
            'provider': self.provider,
            'social_id': self.social_id,
            'email_address': self.email_address,
            'username': self.username,
            'created_date': self.created_date,
            'updated_date': self.updated_date
        }


class Country(db.Model):

    """
    Maps subclass of declarative_base() to a Python class
    to table countries
    """

    __tablename__ = 'countries'

    # Country Code in ISO-ALPHA 2
    # http://country.io/data/
    country_code = db.Column(db.String(2))
    country_name = db.Column(db.String)

    # __table_args__ value must be a tuple, dict, or None
    __table_args__ = (
        db.PrimaryKeyConstraint(
            'country_code', 'country_name', name='pk_countries'),
        db.UniqueConstraint(
            'country_code', name='uq_countries_1'))

    def get_all():
        """ Returns all countries ordered by country_code """
        return Country.query.order_by('country_code').all()

    def to_dict(self):
        """ Convert the model to a dictionary that can go into a JSON """
        return {
            'country_code': self.country_code,
            'country_name': self.country_name
        }


class DistributionCenter(db.Model):

    """
    Maps subclass of declarative_base() to a Python class
    to table distribution_centers
    """

    __tablename__ = 'distribution_centers'

    id = db.Column(db.Integer)
    country_code = db.Column(db.String(2), nullable=False)  # unique
    number = db.Column(db.Integer, nullable=False)  # unique
    name = db.Column(db.String, nullable=False)  # unique
    tag = db.Column(db.String)
    created_date = db.Column(db.DateTime(
        timezone=True), server_default=func.now())
    updated_date = db.Column(db.DateTime(
        timezone=True), onupdate=func.now())
    stores = db.relationship('Store', backref='dc', lazy='dynamic')

    # __table_args__ value must be a tuple, dict, or None
    __table_args__ = (
        db.PrimaryKeyConstraint('id', name='pk_distribution_centers'),
        db.ForeignKeyConstraint(['country_code'], ['countries.country_code']),
        db.UniqueConstraint(
            'country_code',
            'number',
            name='uq_distribution_centers_1'))

    def get_id(country_code, number):
        """
        Returns id (pk) based on country_code and number.
        Some countries (like LU) have no DC, it needs to be handled in imports.
        """
        # In table distribution_centers we can use the unique
        # country_code, number
        dc = DistributionCenter.query.filter_by(
            country_code=country_code,
            number=number
            ).first()
        return dc.id

    def get_name(id):
        """
        Returns name based on id (pk).
        """
        dc = DistributionCenter.query.filter_by(id=id).first()
        return dc.name

    def get_all():
        """
        Returns all distribution centers ordered by country_code, number
        """
        return DistributionCenter.query.order_by(
            'country_code', 'number').all()

    def to_dict(self):
        """ Convert the model to a dictionary that can go into a JSON """
        return {
            # id is unnecessary
            'country_code': self.country_code,
            'number': self.number,
            'name': self.name,
            'tag': self.tag,
            'created_date': self.created_date,
            'updated_date': self.updated_date
        }


class StoreStatus(db.Model):

    """
    Maps subclass of declarative_base() to a Python class
    to table store_statuses
    """

    __tablename__ = 'store_status'

    id = db.Column(db.Integer)
    sequence = db.Column(db.Integer, nullable=False)  # unique
    name = db.Column(db.String, nullable=False)  # unique
    description = db.Column(db.String)
    stores = db.relationship('Store', backref='status', lazy='dynamic')

    # __table_args__ value must be a tuple, dict, or None
    __table_args__ = (
        db.PrimaryKeyConstraint('id', name='pk_store_status'),
        db.UniqueConstraint(
            'sequence',
            'name',
            name='uq_store_status_1'))

    def get_name(id):
        """
        Returns name based on id (pk).
        """
        status = StoreStatus.query.filter_by(id=id).first()
        return status.name

    def get_all():
        """ Returns all store statuses ordered by sequence """
        return StoreStatus.query.order_by('sequence').all()

    def to_dict(self):
        """ Convert the model to a dictionary that can go into a JSON """
        return {
            'sequence': self.sequence,
            'name': self.name,
            'description': self.description
        }


class Store(db.Model):

    """
    Maps subclass of declarative_base() to a Python class
    to table stores
    """

    __tablename__ = 'stores'

    id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, nullable=False)
    country_code = db.Column(db.String(2), nullable=False)
    dc_id = db.Column(db.Integer, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    status_id = db.Column(db.Integer, nullable=False)
    # TODO: move address data to its own tables
    street_number = db.Column(db.String)
    street_name = db.Column(db.String)
    postal_code = db.Column(db.String)
    city = db.Column(db.String)
    created_date = db.Column(db.DateTime(
        timezone=True), server_default=func.now())
    updated_date = db.Column(db.DateTime(
        timezone=True), onupdate=func.now())

    # __table_args__ value must be a tuple, dict, or None
    __table_args__ = (
        db.PrimaryKeyConstraint('id', name='pk_stores'),
        db.ForeignKeyConstraint(['user_id'], ['users.id']),
        db.ForeignKeyConstraint(['country_code'], ['countries.country_code']),
        db.ForeignKeyConstraint(['dc_id'], ['distribution_centers.id']),
        db.ForeignKeyConstraint(['status_id'], ['store_status.id']),
        # db.ForeignKeyConstraint(['id'], ['distribution_centers.id']),
        db.UniqueConstraint(
            'country_code',
            'number',
            name='uq_stores_1'))

    def get_id(country_code, number):
        """ Returns id (pk) based on country_code and number """

        # We need to find the store_id first to link the components
        # In table stores we can use the unique country_code, number
        store = Store.query.filter_by(
            country_code=country_code,
            number=number
            ).first()
        return store.id

    def get(country_code, number):
        """ Returns a store by country_code, number """
        return Store.query.filter_by(
            country_code=country_code, number=number).first()

    def get_user_id(country_code, number):
        """ Returns Store.user_id by country_code, number """
        store = Store.query.filter_by(
            country_code=country_code,
            number=number
            ).first()
        return store.user_id

    def get_dc_id(country_code, number):
        """ Returns Store.dc_id by country_code, number """
        store = Store.query.filter_by(
            country_code=country_code,
            number=number
            ).first()
        return store.dc_id

    def get_status_id(country_code, number):
        """ Returns Store.status_id by country_code, number """
        store = Store.query.filter_by(
            country_code=country_code,
            number=number
            ).first()
        return store.status_id

    def get_all():
        """
        Returns all stores ordered by country_code, number.
        """
        return Store.query.order_by('country_code', 'number').all()

    def to_dict(self):
        """
        Convert the model to a dictionary that can go into a JSON.
        TODO: it should return a non pk for dc, status
        """
        return {
            # id is unnecessary
            'country_code': self.country_code,
            #
            'dc_id': self.dc_id,
            'number': self.number,
            'name': self.name,
            'status_id': self.status_id,
            'street_name': self.street_name,
            'street_number': self.street_number,
            'postal_code': self.postal_code,
            'city': self.city,
            'created_date': self.created_date,
            'updated_date': self.updated_date
        }


class StoreComponent(db.Model):

    """
    Maps subclass of declarative_base() to a Python class
    to table store_components
    """

    __tablename__ = 'store_components'

    id = db.Column(db.Integer)
    # MAJOR TODO: need to retrieve correct store_id
    store_id = db.Column(db.Integer, nullable=False)
    # TODO: move component_type data to its own tables
    component_type = db.Column(db.String, nullable=False)
    hostname = db.Column(db.String, nullable=False)  # unique
    # MAJOR TODO: use conversion functions or the postgresql datatype for ip
    ip_address = db.Column(db.String)  # unique
    created_date = db.Column(db.DateTime(
        timezone=True), server_default=func.now())
    updated_date = db.Column(db.DateTime(
        timezone=True), onupdate=func.now())

    # __table_args__ value must be a tuple, dict, or None
    __table_args__ = (
        db.PrimaryKeyConstraint('id', name='pk_store_components'),
        # 1:M - one store can have many components
        db.ForeignKeyConstraint(['store_id'], ['stores.id']),
        db.UniqueConstraint(
            'store_id',
            'hostname',
            name='uq_store_components_1'))

    def get_all_by_type(store_id, component_type):
        """ Returns store components based on store_id and component_type """
        components = StoreComponent.query.filter_by(
            store_id=store_id,
            component_type=component_type
            ).all()
        return components

    def to_dict(self):
        """ Convert the model to a dictionary that can go into a JSON """
        return {
            # id is unnecessary
            # MAJOR TODO: rewrite store_id to something readable
            'store_id': self.store_id,
            'component_type': self.component_type,
            'hostname': self.hostname,
            'ip_address': self.ip_address,
            'created_date': self.created_date,
            'updated_date': self.updated_date
        }
