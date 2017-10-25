import json
import random

from myapp.models.db_orm import db

from myapp.models.db_models import User
from myapp.models.db_models import Country
from myapp.models.db_models import DistributionCenter
from myapp.models.db_models import StoreStatus
from myapp.models.db_models import Store
from myapp.models.db_models import StoreComponent


# For demo purposes we are only generating about 10 stores:
#   -   distribution center is randomly assigned to the existing 4 dcs
#       (range 1 to 3), 4 is for country LU.
#   -   status will be randomly assigned (range 1 to 3)
#   -   store numbers are simply increased and assigned.
#   -   store components are randomly generated.


# randomly to a distribution center, status will also be
def load_users_from_json():
    """
    Importing JSON data to table users
    """
    json_filename = 'db/json/users.json'
    with open(json_filename, 'r', encoding='utf-8') as f:
        json_object = json.load(f)
        users = []
        for user in json_object['users']:
            # Each user is a dict
            users.append(User(
                provider='myapp',
                social_id=User.generate_social_id(),
                email_address=user.get('email_address'),
                password=user.get('password'))
                )
    # Add data to users
    db.session.add_all(users)
    # Flush the remaining changes and commit the transaction
    db.session.commit()
    # Close the Session
    db.session.close()


def load_countries_from_json():
    """
    Importing JSON data to table stores
    """
    json_filename = 'db/json/countries.json'
    with open(json_filename, 'r', encoding='utf-8') as f:
        json_object = json.load(f)
        countries = []
        for country in json_object['countries']:
            countries.append(Country(
                country_code=country.get('country_code'),
                country_name=country.get('country_name'))
                )
    db.session.add_all(countries)
    db.session.commit()
    db.session.close()


def load_distribution_centers_from_json():
    """
    Importing JSON data to table distribution_centers
    """
    json_filename = 'db/json/distribution_centers.json'
    with open(json_filename, 'r', encoding='utf-8') as f:
        json_object = json.load(f)
        dcs = []
        for dc in json_object['distribution_centers']:
            dcs.append(DistributionCenter(
                country_code=dc.get('country_code'),
                number=dc.get('number'),
                name=dc.get('name'),
                tag=dc.get('tag'))
                )
    db.session.add_all(dcs)
    db.session.commit()
    db.session.close()


def load_stores_status_from_json():
    """
    Importing JSON data to table store_status
    """
    json_filename = 'db/json/store_status.json'
    with open(json_filename, 'r', encoding='utf-8') as f:
        json_object = json.load(f)
        statuses = []
        for status in json_object['store_status']:
            statuses.append(StoreStatus(
                sequence=status.get('sequence'),
                name=status.get('name'),
                description=status.get('description'))
                )
    db.session.add_all(statuses)
    db.session.commit()
    db.session.close()


def load_stores_from_json():
    """
    Importing JSON data to table stores.
    Table dependencies: countries, distribution_centers
    """
    json_filename = 'db/json/stores.json'
    with open(json_filename, 'r', encoding='utf-8') as f:
        json_object = json.load(f)
        stores = []
        number = 0

        # Use default iterators/operators, no need for .keys()
        for key in json_object.get('stores'):

            # Default value for user_id will be 1, as there should always
            # be a default user.
            user_id = 1

            # Retrieve country_code
            country_code = json_object.get(
                'stores').get(key).get('store').get('country_code')

            # Retrieve dc_id using country_code and the exported dc number
            # dc_number = json_object.get(
            #     'stores').get(key).get('store').get('dc_number')
            if country_code == 'LU':
                dc_number = 4
            else:
                dc_number = random.randint(1, 3)

            # Some countries can have no DC, so we change it to the
            # relevant parent country.
            # if country_code == 'LU':
            #     dc_id = DistributionCenter.get_id('BE', dc_number)
            # else:
            #     dc_id = DistributionCenter.get_id(country_code, dc_number)

            # Retrieve store number
            # number = json_object.get(
            #     'stores').get(key).get('store').get('number')
            number += 1

            # Add the fields to the store
            stores.append(Store(
                user_id=user_id,
                country_code=country_code,
                dc_id=dc_number,
                number=int(key),
                name=json_object.get(
                    'stores').get(key).get('store').get('name'),
                status_id=random.randint(1, 3),
                street_name=json_object.get(
                    'stores').get(key).get('store').get('street_name'),
                street_number=json_object.get(
                    'stores').get(key).get('store').get('street_number'),
                postal_code=json_object.get(
                    'stores').get(key).get('store').get('postal_code'),
                city=json_object.get(
                    'stores').get(key).get('store').get('city'),
            ))

    db.session.add_all(stores)
    db.session.commit()
    db.session.close()


def load_store_components_from_json():
    """
    Importing JSON data to table store_components.
    We only load components for stores with status Open (sequence 2).
    """
    json_filename = 'db/json/stores.json'
    with open(json_filename, 'r', encoding='utf-8') as f:
        json_object = json.load(f)

        backoffices = []
        network_routers = []
        network_switches = []
        access_points = []

        # Use default iterators/operators, no need for .keys()
        for key in json_object.get('stores'):

            # backoffice
            i = 1
            while i <= random.randint(1, 2):
                country_code = json_object.get(
                    'stores').get(key).get('store').get('country_code')
                number = int(key)
                bo_hostname = 'Backoffice {}'.format(i)
                backoffices.append(StoreComponent(
                    store_id=Store.get_id(country_code, number),
                    component_type='backoffice',
                    hostname=bo_hostname,
                    ip_address='127.0.0.1')
                    )
                i += 1

            # network_routers
            i = 1
            while i <= random.randint(1, 3):
                country_code = json_object.get(
                    'stores').get(key).get('store').get('country_code')
                number = int(key)
                nr_hostname = 'Network Router {}'.format(i)
                network_routers.append(StoreComponent(
                    store_id=Store.get_id(country_code, number),
                    component_type='network_routers',
                    hostname=nr_hostname,
                    ip_address='127.0.0.1')
                    )
                i += 1

            # network_switches
            i = 1
            while i <= random.randint(1, 2):
                country_code = json_object.get(
                    'stores').get(key).get('store').get('country_code')
                number = int(key)
                ns_hostname = 'Network Switch {}'.format(i)
                network_switches.append(StoreComponent(
                    store_id=Store.get_id(country_code, number),
                    component_type='network_switches',
                    hostname=ns_hostname,
                    ip_address='127.0.0.1')
                )
                i += 1

            # network_access_points
            i = 1
            while i <= random.randint(1, 5):
                country_code = json_object.get(
                    'stores').get(key).get('store').get('country_code')
                number = int(key)
                ap_hostname = 'Network Access Point {}'.format(i)
                access_points.append(StoreComponent(
                    store_id=Store.get_id(country_code, number),
                    component_type='network_access_points',
                    hostname=ap_hostname,
                    ip_address='127.0.0.1')
                )
                i += 1

        db.session.add_all(backoffices)
        db.session.add_all(network_routers)
        db.session.add_all(network_switches)
        db.session.add_all(access_points)
        db.session.commit()
        db.session.close()
