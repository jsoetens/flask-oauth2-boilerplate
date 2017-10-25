from flask import jsonify, render_template

from . import api

from myapp.models.db_models import User
from myapp.models.db_models import Country
from myapp.models.db_models import DistributionCenter
from myapp.models.db_models import StoreStatus
from myapp.models.db_models import Store
from myapp.models.db_models import StoreComponent


# http://localhost:5000/api
@api.route('/')
def overview():
    """
    This endpoint is publicly available.
    """
    return render_template('api/api.html', title='API Overview')


# Countries

# Collection resource is /api/users
@api.route('/users', methods=['GET'])
def get_users():
    """
    The endpoint is for now publicly available.
    Returns:
        JSON of all users
    """
    users = User.query  # no need to order
    users_data = [user.to_dict() for user in users.all()]
    return jsonify(users=users_data)


# Collection resource is /api/countries
@api.route('/countries', methods=['GET'])
def get_countries():
    """
    The endpoint is for now publicly available.
    Returns:
        JSON of all countries.
    """
    countries = Country.query  # no need to order
    countries_data = [country.to_dict() for country in countries.all()]
    return jsonify(countries=countries_data)


# Instance resource is /api/countries/country_code
@api.route('/countries/<country_code>', methods=['GET'])
def get_country_by_country_code(country_code):
    """
    The endpoint is for now publicly available.
    Returns:
        JSON of all countries using using country_code.
    """
    # string is default converter for dynamic routes
    # get_or_404() is like get() but aborts with 404 if not found
    # instead of returning None.
    return jsonify(Country.query.get_or_404(country_code).to_dict())


# Distribution Centers

# Collection resource is /api/distribution_centers
@api.route('/distribution_centers', methods=['GET'])
def get_distribution_centers():
    """
    The endpoint is for now publicly available.
    Returns:
        JSON of all distribution centers.
    """
    dcs = DistributionCenter.query  # no need to order
    dcs_data = [dc.to_dict() for dc in dcs.all()]
    return jsonify(distribution_centers=dcs_data)


# Instance resource is /api/distribution_centers/country_code
@api.route('/distribution_centers/<country_code>', methods=['GET'])
def get_distribution_center_by_country_code(country_code):
    """

    The endpoint is for now publicly available.
    Returns:
        JSON of all distribution centers using country_code.
    """
    return jsonify(DistributionCenter.query.get_or_404(country_code).to_dict())


# Store Statuses

# Collection resource is /api/store_status
@api.route('/store_status', methods=['GET'])
def get_store_status():
    """
    The endpoint is for now publicly available.
    Returns:
        JSON of all store statuses.
    """
    statuses = StoreStatus.query  # no need to order
    status_data = [status.to_dict() for status in statuses.all()]
    return jsonify(store_status=status_data)


# Stores

# Collection resource is /api/stores
@api.route('/stores', methods=['GET'])
def get_stores():
    """
    The endpoint is for now publicly available.
    Returns:
        JSON of all stores.
    """
    stores = Store.query  # no need to order
    stores_data = [store.to_dict() for store in stores.all()]
    return jsonify(stores=stores_data)


# Instance resource is /api/stores/number
@api.route('/stores/<int:number>', methods=['GET'])
def get_store_by_number(number):
    """

    The endpoint is for now publicly available.
    Returns:
        JSON of store using number.
    """
    result_store = Store.query.filter(Store.number == number)
    store_data = [
        store.to_dict() for store in result_store.all()]
    return jsonify(store=store_data)


# Instance resource is /api/stores/country_code
@api.route('/stores/<country_code>', methods=['GET'])
def get_store_by_country(country_code):
    """

    The endpoint is for now publicly available.
    Returns:
        JSON of all stores using country_code.
    """
    result_stores = Store.query.filter(Store.country_code == country_code)
    stores_data = [
        store.to_dict() for store in result_stores.all()]
    return jsonify(stores=stores_data)


# Store Components

# Collection resource is /api/store_components
@api.route('/store_components', methods=['GET'])
def get_store_components():
    """
    The endpoint is for now publicly available.
    Returns:
        JSON of all store components.
    """
    store_components = StoreComponent.query  # no need to order
    store_components_data = [
        component.to_dict() for component in store_components.all()]
    return jsonify(store_components=store_components_data)


# Instance resource is /api/store_components/type
@api.route('/store_components/<type>', methods=['GET'])
def get_store_component(type):
    """
    The endpoint is for now publicly available.
    Returns:
        JSON of all store components using type.
    """
    store_components = StoreComponent.query.filter(
        StoreComponent.component_type == type)  # no need to order
    store_components_data = [
        component.to_dict() for component in store_components.all()]
    return jsonify(store_components=store_components_data)
