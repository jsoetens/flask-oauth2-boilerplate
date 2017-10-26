from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError

from myapp.models.db_orm import db

from . import stores
from .forms import StoreForm
from .forms import AddStoreForm
from .forms import EditStoreForm
from .forms import DeleteStoreForm

from myapp.models.db_models import Country
from myapp.models.db_models import DistributionCenter
from myapp.models.db_models import StoreStatus
from myapp.models.db_models import Store
from myapp.models.db_models import StoreComponent


# http://localhost:5000/stores
@stores.route('/')
def index():
    """
    This endpoint is publicly available.
    """
    # Retrieve and do a join to retrieve relevant name values for store FKs.
    # Use labels because columns can have same names in multiple tables.
    stores = db.session.query(
        Store.country_code,
        DistributionCenter.tag.label('dc_tag'),
        Store.number,
        Store.name,
        StoreStatus.name.label('store_status'),
        Store.street_name,
        Store.street_number,
        Store.postal_code,
        Store.city).join(
        DistributionCenter, Store.dc_id == DistributionCenter.id).join(
        StoreStatus, Store.status_id == StoreStatus.id).order_by(
        Store.country_code, Store.number).all()

    return render_template(
        'stores/stores.html',
        stores=stores
        )


# http://localhost:5000/stores/<country_code>/<number>/components
@stores.route(
    '/<country_code>/<int:number>/components',
    methods=['GET'])
def components(country_code, number):

    # Retrieve store details
    store_id = Store.get_id(country_code, number)
    store = Store.get(country_code, number)

    # Retrieve and set name values for the store FKs
    current_dc = DistributionCenter.get_name(store.dc_id)
    current_status = StoreStatus.get_name(store.status_id)
    store.dc_id = current_dc
    store.status_id = current_status

    form = StoreForm()

    # Retrieve components
    backoffice = StoreComponent.get_all_by_type(
        store_id=store_id, component_type='backoffice')
    network_routers = StoreComponent.get_all_by_type(
        store_id=store_id, component_type='network_routers')
    network_switches = StoreComponent.get_all_by_type(
        store_id=store_id, component_type='network_switches')
    network_access_points = StoreComponent.get_all_by_type(
        store_id=store_id, component_type='network_access_points')

    return render_template(
        'stores/components.html',
        store=store,
        backoffice=backoffice,
        network_routers=network_routers,
        network_switches=network_switches,
        network_access_points=network_access_points,
        form=form
        )


# http://localhost:5000/stores/add-store
@stores.route(
    '/add-store',
    methods=['GET', 'POST'])
@login_required
def add_store():
    """
    A store can be created when the user is signed in.
    """

    form = AddStoreForm()

    # HTTP POST
    # validate_on_submit returns True if the form has been both submitted
    # (HTTP POST or PUT) and validated.
    if form.validate_on_submit():
        # Save the new store
        # Required fields are user_id, country_code, dc, number, name
        # Conversion of user_id is required because current_user.get_id()
        # returns unicode
        new_store = Store(
            user_id=int(current_user.get_id()),
            country_code=form.country_code.data.country_code,
            dc_id=form.dc.data.id,
            number=form.number.data,
            name=form.name.data,
            status_id=form.status.data.id,
            street_number=form.street_number.data,
            street_name=form.street_name.data,
            postal_code=form.postal_code.data,
            city=form.city.data
            )
        # Keep an informative store_name for feedback
        store_name = ('{} - {} {}'.format(
            form.country_code.data.country_code,
            form.number.data,
            form.name.data)
            )
        try:
            db.session.add(new_store)
            db.session.commit()
            print('Created store {}'.format(store_name))
            flash('Thank you for adding store {}'.format(store_name), 'info')
        except IntegrityError:
            db.session.rollback()
            print('Country {} already has a store with number {}.'.format(
                form.country_code.data.country_code, form.number.data))
            flash('Country {} already has a store with number {}.'.format(
                form.country_code.data.country_code, form.number.data),
                'error')
        # Return back to Stores Index
        return redirect(url_for('.index'))

    # HTTP GET
    return render_template('stores/add-store.html', form=form)


# http://localhost:5000/stores/<country_code>/<int:number>/edit-store
@stores.route(
    '/<country_code>/<int:number>/edit-store',
    methods=['GET', 'POST'])
@login_required
def edit_store(country_code, number):
    """
    A store can be edited when the user is signed in and created this store.
    """

    # Verify if current_user created this store
    user_id = Store.get_user_id(country_code, number)
    # Conversion is required because current_user.get_id() returns unicode
    if int(current_user.get_id()) != user_id:
        # Give some feedback
        print('You can only edit store {} {} if you created it!'.format(
            country_code, str(number)))
        flash('You can only edit store {} {} if you created it!'.format(
            country_code, str(number)), 'error')
        # Return back to Stores Index
        return redirect(url_for('.index'))

    # We need to provide query result objects to EditStoreForm
    # for default choices in QuerySelectField
    store_id = Store.get_id(country_code, number)
    current_store = Store.query.filter_by(id=store_id).first()
    current_country_code = Country.query.filter_by(
        country_code=current_store.country_code).first()
    current_dc = DistributionCenter.query.filter_by(
        id=current_store.dc_id).first()
    current_status = StoreStatus.query.filter_by(
        id=current_store.status_id).first()

    form = EditStoreForm(
        country_code=current_country_code,
        dc=current_dc,
        status=current_status
        )

    # HTTP POST
    if form.validate_on_submit():
        # Update the store
        # Keep an informative store_name for feedback
        store_name = ('{} - {} {}'.format(
            form.country_code.data.country_code,
            form.number.data,
            form.name.data)
            )
        try:
            db.session.query(Store).filter(Store.id == store_id).update(dict(
                country_code=form.country_code.data.country_code,
                dc_id=form.dc.data.id,
                number=form.number.data,
                name=form.name.data,
                status_id=form.status.data.id,
                street_number=form.street_number.data,
                street_name=form.street_name.data,
                postal_code=form.postal_code.data,
                city=form.city.data))
            db.session.commit()
            print('Store {} has been edited'.format(store_name))
            flash('Store {} has been edited'.format(store_name), 'info')
        except IntegrityError:
            db.session.rollback()
            print('Country {} already has a store with number {}.'.format(
                form.country_code.data.country_code, form.number.data))
            flash('Country {} already has a store with number {}.'.format(
                form.country_code.data.country_code, form.number.data),
                'error')
        # Return back to Stores Index
        return redirect(url_for('.index'))

    # HTTP GET
    store = Store.get(country_code, number)
    return render_template(
        'stores/edit-store.html',
        store=store,
        form=form
        )


# http://localhost:5000/stores/<country_code>/<number>/delete-store
@stores.route(
    '/<country_code>/<int:number>/delete-store',
    methods=['GET', 'POST'])
@login_required
def delete_store(country_code, number):
    """
    A store can be deleted when the user is signed in and created this store.
    """

    # Verify if current_user created this store
    user_id = Store.get_user_id(country_code, number)
    # Conversion is required because current_user.get_id() returns unicode
    if int(current_user.get_id()) != user_id:
        # Give some feedback
        print('You can only delete store {} {} if you created it!'.format(
            country_code, str(number)))
        flash('You can only delete store {} {} if you created it!'.format(
            country_code, str(number)), 'error')
        # Return back to Stores Index
        return redirect(url_for('.index'))

    form = DeleteStoreForm()

    # HTTP POST
    if form.validate_on_submit():
        # Retrieve store primary key
        store_id = Store.get_id(country_code, number)
        # Delete store components
        db.session.query(StoreComponent).filter(
            StoreComponent.store_id == store_id).delete()
        # Delete store
        db.session.query(Store).filter(
            Store.id == store_id).delete()
        # Commit the changes
        db.session.commit()
        # Give some feedback
        print('Deleted store {} {}'.format(country_code, str(number)))
        flash('You deleted store {} {}'.format(
            country_code, str(number)), 'info')
        # Return back to Stores Index
        return redirect(url_for('.index'))

    # HTTP GET
    # Return the confirmation page
    store = Store.get(country_code, number)
    return render_template(
        'stores/delete-store.html',
        store=store,
        form=form
        )


# http://localhost:5000/stores/<country_code>/<number>/
# components/backoffice-edit
@stores.route(
    '/<country_code>/<int:number>/components/backoffice-edit',
    methods=['GET', 'POST'])
def backoffice_edit(country_code, number):
    if request.method == 'POST':
        print('POST backoffice_edit')
    return render_template('stores/backoffice-edit.html')


# http://localhost:5000/stores/<country_code>/<number>/
# components/network-router-edit
@stores.route(
    '/<country_code>/<int:number>/components/network-router-edit',
    methods=['GET', 'POST'])
def network_router_edit(country_code, number):
    if request.method == 'POST':
        print('POST network_router_edit')
    return render_template('stores/network-router-edit.html')


# http://localhost:5000/stores/<country_code>/<number>/
# components/network-switch-edit
@stores.route(
    '/<country_code>/<int:number>/components/network-switch-edit',
    methods=['GET', 'POST'])
def network_switch_edit(country_code, number):
    if request.method == 'POST':
        print('POST network_switch_edit')
    return render_template('stores/network-switch-edit.html')


# http://localhost:5000/stores/<country_code>/<number>/
# components/network-ap-edit
@stores.route(
    '/<country_code>/<int:number>/components/network-ap-edit',
    methods=['GET', 'POST'])
def network_ap_edit(country_code, number):
    if request.method == 'POST':
        print('POST network_ap_edit')
    return render_template('stores/network-ap-edit.html')
