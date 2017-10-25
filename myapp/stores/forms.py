from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from myapp.models.db_models import Store
from myapp.models.db_models import Country
from myapp.models.db_models import DistributionCenter
from myapp.models.db_models import StoreStatus


# Query Factories - they need to return queries, not results
def callback_countries():
    return Country.query.order_by('country_code')


def callback_distribution_centers():
    return DistributionCenter.query.order_by('country_code', 'number')


def callback_store_status():
    return StoreStatus.query.order_by('sequence')


class StoreForm(FlaskForm):

    country_code = StringField('Country')
    dc = StringField('DC')
    status = StringField('Status')
    number = IntegerField('Store Number')
    name = StringField('Name')
    street_number = StringField('Street Number')
    street_name = StringField('Street')
    postal_code = StringField('Postal Code')
    city = StringField('City')


# Bootstrap 4 Beta has issues with invalid-feedback,
# for now only visual validation
# TODO: fix detailed feedback on missing fields
class AddStoreForm(FlaskForm):

    country_code = QuerySelectField(
        'Country',
        query_factory=callback_countries,
        get_label='country_name'
        )
    dc = QuerySelectField(
        'DC',
        query_factory=callback_distribution_centers,
        get_label='name'
        )
    status = QuerySelectField(
        'Status',
        query_factory=callback_store_status,
        get_label='name'
        )
    number = IntegerField('Store Number')
    name = StringField('Name')
    street_number = StringField('Street Number')
    street_name = StringField('Street')
    postal_code = StringField('Postal Code')
    city = StringField('City')

    # Methods with prefix validate_ are custom validators that are
    # automatically invoked in addition to other validators.
    def validate_country_code_number(self, field):
        """
        Verify if country_code and number for newly added store do not already
        exist.
        """
        if Store.query.filter_by(
                country_code=field.country_code).filter_by(
                number=field.number):
            print('Store {} {} already exists.'.format(
                field.country_code, field.number))
        raise ValidationError('Store already exists.')


class EditStoreForm(FlaskForm):

    country_code = QuerySelectField(
        'Country',
        query_factory=callback_countries,
        get_label='country_name'
        )
    dc = QuerySelectField(
        'DC',
        query_factory=callback_distribution_centers,
        get_label='name',
        )
    status = QuerySelectField(
        'Status',
        query_factory=callback_store_status,
        get_label='name'
        )
    number = IntegerField('Store Number')
    name = StringField('Name')
    street_number = StringField('Street Number')
    street_name = StringField('Street')
    postal_code = StringField('Postal Code')
    city = StringField('City')


class DeleteStoreForm(FlaskForm):

    """ DeleteStoreForm has no elements at the moment """
    pass
