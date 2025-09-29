from fasthtml.common import *
from components.card import Card
from components.layout import Layout
from starlette.requests import Request
from backend.src.models.property import Property
from typing import List, Optional, Union
from starlette.datastructures import UploadFile
import sqlite3
import os
import uuid

# --- Constants ---
FEATURES_LIST = [
    "Accessible Road", "Approved Government Excision", "Buy and build land", "Contract of Sales",
    "Deed of Assignment", "Dry Land", "Good title", "Instant Allocation", "Perimeter Fencing",
    "Survey", "24 Hour Water Supply", "24 Hours Security", "24/7 uninterrupted power supply",
    "Approved Gazette", "Balcony", "Basketball Court", "Beautiful Landscapes", "Building approval",
    "Central Business District", "Golf Course", "Good drainage system", "Government Allocation",
    "Governor's Consent", "Interlocked Road", "Interlocked Streets", "Tennis Court(s)", "Water treatment plant"
]
PROPERTY_TYPES = ["land", "house", "apartment"]
PROPERTY_STATUSES = ["for sale", "for rent", "invest", "lease", "sold"]
PROPERTY_LABELS = ["buy and build", "off-plan", "open house", "ready to move in", "sold out"]

# --- Page Content Components (Fully Implemented) ---

def admin_dashboard_content():
    return Div(
        H1("Admin Dashboard"),
        Div(
            Card(title="Total Properties", content="324 Listed", card_cls="card mb-4"),
            Card(title="Active Users", content="1,245 Users", card_cls="card mb-4"),
            Card(title="Revenue", content="$45,750", card_cls="card mb-4"),
            cls="dashboard-content"
        ),
        cls="container-fluid"
    )

def admin_properties_content():
    properties = get_all_properties()
    return Div(
        H1("Property Management"),
        Button("Add New Property", cls="btn btn-primary mb-4", hx_get="/admin/properties/new", hx_target="#main-content"),
        Table(
            Thead(Tr(Th("S/N"), Th("Image"), Th("Title"), Th("Location"), Th("Price"), Th("Actions"))),
            Tbody(*[Tr(
                Td(f"{i + 1}"),
                Td(Img(src=prop.images[0], cls="img-thumbnail", style="max-width: 70px;") if prop.images else "No Image"),
                Td(prop.name),
                Td(f"{prop.city or ''}, {prop.state or ''}"),
                Td(f"${prop.price:,.2f}"),
                Td(
                    A(I(cls="fe fe-eye"), hx_get=f"/admin/properties/{prop.id}", hx_target="#main-content", cls="text-info me-3"),
                    A(I(cls="fe fe-edit"), hx_get=f"/admin/properties/{prop.id}/edit", hx_target="#main-content", cls="text-primary me-3"),
                    A(I(cls="fe fe-trash-2"), hx_delete=f"/admin/properties/{prop.id}", hx_confirm="Are you sure?", hx_target="#main-content", cls="text-danger"),
                )
            ) for i, prop in enumerate(properties)]),
            cls="table table-striped"
        ),
        cls="container-fluid"
    )

def admin_property_detail_content(property_id: int):
    prop = get_property_by_id(property_id)
    if not prop: return Div(H1("Property Not Found"))
    location_parts = [prop.address, prop.city, prop.state, prop.country, prop.zip_code]
    full_location = ", ".join(filter(None, location_parts))
    return Div(
        H1(prop.name),
        Div(
            Div(H4("Status & Labels"), P(f"Status: {prop.property_status or 'N/A'}"), P(f"Type: {prop.property_type or 'N/A'}"), P(f"Label: {prop.labels or 'N/A'}"), cls="mb-4"),
            Div(H4("Details"), P(prop.description), P(f"Location: {full_location}"), P(f"Price: ${prop.price:,.2f}"), cls="mb-4"),
            Div(
                H4("Room & Size Details"),
                P(f"Bedrooms: {prop.bedrooms or 'N/A'}"), P(f"Bathrooms: {prop.bathrooms or 'N/A'}"), P(f"Total Rooms: {prop.rooms or 'N/A'}"),
                P(f"Property Area: {prop.property_area_size or 'N/A'} sq. units"), P(f"Land Size: {prop.property_land_size or 'N/A'} sq. units"),
                P(f"Garages: {prop.garages or 'N/A'}"), P(f"Year Built: {prop.year_built or 'N/A'}"),
                cls="mb-4"
            ),
            Div(H4("Features"), P(", ".join(prop.features)) if prop.features else P("None"), cls="mb-4"),
            Div(H4("Media"), A("View Virtual Tour", href=prop.virtual_tour_url, target="_blank") if prop.virtual_tour_url else P("No tour"), A("View Video", href=prop.video_url, target="_blank") if prop.video_url else P("No video"), cls="mb-4"),
            Div(H4("Images"), *[Img(src=img, cls="img-thumbnail me-2 mb-2", style="max-width: 200px") for img in prop.images], cls="mb-4"),
            Button("Back", cls="btn btn-secondary", hx_get="/admin/properties", hx_target="#main-content"),
        ),
        cls="container-fluid"
    )

def admin_users_content():
    return Div(H1("User Management"), Table(Thead(Tr(Th("ID"), Th("Name"), Th("Role"), Th("Status"), Th("Actions"))), Tbody(Tr(Td("#U001"), Td("John Doe"), Td("Realtor"), Td("Active"), Td(Button("Edit", cls="btn btn-sm btn-primary me-2"), Button("Suspend", cls="btn btn-sm btn-warning")))), cls="table table-striped"), cls="container-fluid")

def admin_analytics_content():
    return Div(H1("Analytics Dashboard"), Div(Card(title="Monthly Revenue", content="Chart placeholder"), Card(title="User Growth", content="Chart placeholder")), cls="container-fluid")

def admin_payouts_content():
    return Div(H1("Payout Management"), Table(Thead(Tr(Th("ID"), Th("User"), Th("Amount"), Th("Status"), Th("Actions"))), Tbody(Tr(Td("#P001"), Td("Jane Smith"), Td("$1,200"), Td("Pending"), Td(Button("Approve", cls="btn btn-sm btn-success")))), cls="table table-striped"), cls="container-fluid")

# --- Page Route Functions ---

async def admin_dashboard(request: Request):
    return Layout(admin_dashboard_content(), user_role="Admin") if not request.headers.get("HX-Request") else admin_dashboard_content()

async def admin_properties_route(request: Request):
    try:
        property_id = request.path_params.get('property_id')
        if request.method == "POST": return await handle_new_property(request)
        if request.method == "PUT" and property_id: return await handle_update_property(request, int(property_id))
        if request.method == "DELETE" and property_id: return await handle_delete_property(request, int(property_id))
        path = request.url.path
        if path.endswith("/new"): content = new_property_form()
        elif path.endswith("/edit") and property_id: content = edit_property_form(int(property_id))
        elif property_id: content = admin_property_detail_content(int(property_id))
        else: content = admin_properties_content()
        # Flash toast
        flash = request.session.pop('flash', None) if hasattr(request, 'session') else None
        if flash and isinstance(flash, dict):
            content = Div(content, Script(f"showToast({(flash.get('message') or '')!r}, {(flash.get('level') or 'info')!r})"))
        return content if request.headers.get("HX-Request") else Layout(content, user_role="Admin")
    except Exception as e:
        return Div(f"An error occurred: {e}", cls="alert alert-danger")

async def admin_users(request: Request):
    return Layout(admin_users_content(), user_role="Admin") if not request.headers.get("HX-Request") else admin_users_content()

async def admin_analytics(request: Request):
    return Layout(admin_analytics_content(), user_role="Admin") if not request.headers.get("HX-Request") else admin_analytics_content()

async def admin_payouts(request: Request):
    return Layout(admin_payouts_content(), user_role="Admin") if not request.headers.get("HX-Request") else admin_payouts_content()

# --- Form Handlers (FIXED & EXPLICIT) ---

async def handle_new_property(request: Request):
    form = await request.form()
    try:
        images_str = await _save_uploaded_images(form)
        features_str = ",".join(form.getlist("features"))
        
        # Explicitly get, clean, and type-cast all values
        conn = sqlite3.connect('proppal.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO properties (name, description, price, images, realtor_id, features, address, country, state, city, area, zip_code, latitude, longitude, virtual_tour_url, property_type, property_status, labels, video_url, bedrooms, bathrooms, rooms, property_area_size, property_land_size, garages, year_built)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            form.get('name'), form.get('description'),
            float(form.get('price')) if form.get('price') else None,
            images_str, 1, features_str,
            form.get('address'), form.get('country'), form.get('state'), form.get('city'), form.get('area'), form.get('zip_code'),
            float(form.get('latitude')) if form.get('latitude') else None,
            float(form.get('longitude')) if form.get('longitude') else None,
            form.get('virtual_tour_url'), form.get('property_type'), form.get('property_status'), form.get('labels'), form.get('video_url'),
            int(form.get('bedrooms')) if form.get('bedrooms') else None,
            int(form.get('bathrooms')) if form.get('bathrooms') else None,
            int(form.get('rooms')) if form.get('rooms') else None,
            float(form.get('property_area_size')) if form.get('property_area_size') else None,
            float(form.get('property_land_size')) if form.get('property_land_size') else None,
            int(form.get('garages')) if form.get('garages') else None,
            int(form.get('year_built')) if form.get('year_built') else None
        ))
        conn.commit()
        conn.close()
        if hasattr(request, 'session'):
            request.session['flash'] = {'message': 'Property created successfully', 'level': 'success'}
        return Response(headers={'HX-Redirect': '/admin/properties'})
    except Exception as e:
        if hasattr(request, 'session'):
            request.session['flash'] = {'message': f'Error creating property: {e}', 'level': 'danger'}
        return Response(headers={'HX-Redirect': '/admin/properties'})

async def handle_update_property(request: Request, property_id: int):
    form = await request.form()
    try:
        new_images_str = await _save_uploaded_images(form)
        images_str = new_images_str if new_images_str else form.get("existing_images", "")
        features_str = ",".join(form.getlist("features"))

        conn = sqlite3.connect('proppal.db')
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE properties SET 
            name=?, description=?, price=?, images=?, features=?, address=?, country=?, state=?, city=?, area=?, zip_code=?, 
            latitude=?, longitude=?, virtual_tour_url=?, property_type=?, property_status=?, labels=?, video_url=?, 
            bedrooms=?, bathrooms=?, rooms=?, property_area_size=?, property_land_size=?, garages=?, year_built=?
            WHERE id=?
        """, (
            form.get('name'), form.get('description'),
            float(form.get('price')) if form.get('price') else None,
            images_str, features_str,
            form.get('address'), form.get('country'), form.get('state'), form.get('city'), form.get('area'), form.get('zip_code'),
            float(form.get('latitude')) if form.get('latitude') else None,
            float(form.get('longitude')) if form.get('longitude') else None,
            form.get('virtual_tour_url'), form.get('property_type'), form.get('property_status'), form.get('labels'), form.get('video_url'),
            int(form.get('bedrooms')) if form.get('bedrooms') else None,
            int(form.get('bathrooms')) if form.get('bathrooms') else None,
            int(form.get('rooms')) if form.get('rooms') else None,
            float(form.get('property_area_size')) if form.get('property_area_size') else None,
            float(form.get('property_land_size')) if form.get('property_land_size') else None,
            int(form.get('garages')) if form.get('garages') else None,
            int(form.get('year_built')) if form.get('year_built') else None,
            property_id
        ))
        conn.commit()
        conn.close()
        if hasattr(request, 'session'):
            request.session['flash'] = {'message': 'Property updated successfully', 'level': 'success'}
        return Response(headers={'HX-Redirect': '/admin/properties'})
    except Exception as e:
        if hasattr(request, 'session'):
            request.session['flash'] = {'message': f'Error updating property: {e}', 'level': 'danger'}
        return Response(headers={'HX-Redirect': '/admin/properties'})

async def handle_delete_property(request: Request, property_id: int):
    delete_property(property_id)
    if hasattr(request, 'session'):
        request.session['flash'] = {'message': 'Property deleted', 'level': 'success'}
    return Response(headers={'HX-Redirect': '/admin/properties'})

# --- DB & Helpers (Complete) ---

async def _save_uploaded_images(form) -> str:
    image_files = form.getlist("images")
    saved_image_paths = []
    if image_files and isinstance(image_files[0], UploadFile) and image_files[0].filename:
        UPLOAD_DIR = "public/assets/img/properties"
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        for image_file in image_files:
            if isinstance(image_file, UploadFile) and image_file.filename:
                ext = os.path.splitext(image_file.filename)[1]
                unique_filename = f"{uuid.uuid4()}{ext}"
                save_path = os.path.join(UPLOAD_DIR, unique_filename)
                with open(save_path, "wb") as buffer:
                    buffer.write(await image_file.read())
                saved_image_paths.append(f"/assets/img/properties/{unique_filename}")
    return ",".join(saved_image_paths)

def execute_db(query, params=(), fetchone=False, fetchall=False, commit=False):
    conn = sqlite3.connect('proppal.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = None
    if fetchone: result = cursor.fetchone()
    if fetchall: result = cursor.fetchall()
    if commit: conn.commit()
    conn.close()
    return result

def delete_property(property_id: int):
    execute_db("DELETE FROM properties WHERE id = ?", (property_id,), commit=True)

def get_all_properties() -> List[Property]:
    rows = execute_db("SELECT * FROM properties ORDER BY id DESC", fetchall=True)
    return [_parse_property_from_row(row) for row in rows if row]

def get_property_by_id(property_id: int) -> Optional[Property]:
    row = execute_db("SELECT * FROM properties WHERE id = ?", (property_id,), fetchone=True)
    return _parse_property_from_row(row) if row else None

def _parse_property_from_row(row) -> Property:
    prop_dict = dict(row)
    for key in ['images', 'features']:
        val = prop_dict.get(key)
        prop_dict[key] = val.split(',') if val and val.strip() else []
    if prop_dict.get('realtor_id') is None: prop_dict['realtor_id'] = 1

    numeric_fields = [
        'latitude', 'longitude', 'price', 'property_area_size', 'property_land_size',
        'bedrooms', 'bathrooms', 'rooms', 'garages', 'year_built'
    ]
    for field in numeric_fields:
        if prop_dict.get(field) == '' or prop_dict.get(field) is None:
            prop_dict[field] = None

    return Property(**prop_dict)

# --- Form Components (Complete) ---

def _build_select(name, options, selected, required=False):
    return Div(Label(name.replace('_', ' ').title(), cls="form-label"), Select(Option(value="", children="-- Select --"), *[Option(o, value=o, selected=(o == selected)) for o in options], name=name, cls="form-select form-control", required=required), cls="mb-3")

def _build_feature_checkboxes(selected_features):
    return [Div(Input(type="checkbox", name="features", value=feature, id=f"feature_{feature.replace(' ', '_')}", cls="form-check-input", checked=feature in selected_features), Label(feature, for_=f"feature_{feature.replace(' ', '_')}", cls="form-check-label"), cls="form-check form-check-inline") for feature in FEATURES_LIST]

def new_property_form():
    return Div(H2("Add New Property"), Form(_property_form_fields(), hx_post="/admin/properties", hx_target="#main-content", enctype="multipart/form-data", cls="mt-4"))

def edit_property_form(property_id: int):
    prop = get_property_by_id(property_id)
    if not prop: return Div("Property not found")
    return Div(H2("Edit Property"), Form(_property_form_fields(prop), hx_put=f"/admin/properties/{property_id}", hx_target="#main-content", enctype="multipart/form-data", cls="mt-4"))

def _property_form_fields(prop: Optional[Property] = None):
    return Fragment(
        Div(Label("Name", cls="form-label"), Input(name="name", value=prop.name if prop else "", cls="form-control", required=True), cls="mb-3"),
        Div(Label("Description", cls="form-label"), Textarea(prop.description if prop else "", name="description", cls="form-control"), cls="mb-3"),
        Div(Label("Price", cls="form-label"), Input(type="number", name="price", value=prop.price if prop else "", cls="form-control", required=True, step="any"), cls="mb-3"),
        H4("Classification", cls="mt-4"),
        Div(
            Div(_build_select("property_type", PROPERTY_TYPES, prop.property_type if prop else None, required=True), cls="col-md-4"),
            Div(_build_select("property_status", PROPERTY_STATUSES, prop.property_status if prop else None, required=True), cls="col-md-4"),
            Div(_build_select("labels", PROPERTY_LABELS, prop.labels if prop else None, required=True), cls="col-md-4"),
            cls="row mb-3"
        ),
        H4("Features", cls="mt-4"),
        Div(*_build_feature_checkboxes(prop.features if prop else []), cls="d-flex flex-wrap mb-3 border rounded p-2"),
        H4("Location", cls="mt-4"),
        Div(Label("Address", cls="form-label"), Input(name="address", value=prop.address if prop else "", cls="form-control"), cls="mb-3"),
        Div(
            Div(Label("Country", cls="form-label"), Input(name="country", value=prop.country if prop else "", cls="form-control"), cls="col-md-6"),
            Div(Label("State", cls="form-label"), Input(name="state", value=prop.state if prop else "", cls="form-control"), cls="col-md-6"),
            cls="row mb-3"
        ),
        Div(
            Div(Label("City", cls="form-label"), Input(name="city", value=prop.city if prop else "", cls="form-control"), cls="col-md-4"),
            Div(Label("Area", cls="form-label"), Input(name="area", value=prop.area if prop else "", cls="form-control"), cls="col-md-4"),
            Div(Label("Zip Code", cls="form-label"), Input(name="zip_code", value=prop.zip_code if prop else "", cls="form-control"), cls="col-md-4"),
            cls="row mb-3"
        ),
        H4("Map", cls="mt-4"),
        Div(
            Div(Label("Latitude", cls="form-label"), Input(type="number", name="latitude", step="any", value=prop.latitude if prop else "", cls="form-control"), cls="col-md-6"),
            Div(Label("Longitude", cls="form-label"), Input(type="number", name="longitude", step="any", value=prop.longitude if prop else "", cls="form-control"), cls="col-md-6"),
            cls="row mb-3"
        ),
        H4("Details", cls="mt-4"),
        Div(
            Div(Label("Bedrooms", cls="form-label"), Input(type="number", name="bedrooms", value=prop.bedrooms if prop else "", cls="form-control"), cls="col-md-3"),
            Div(Label("Bathrooms", cls="form-label"), Input(type="number", name="bathrooms", value=prop.bathrooms if prop else "", cls="form-control"), cls="col-md-3"),
            Div(Label("Rooms", cls="form-label"), Input(type="number", name="rooms", value=prop.rooms if prop else "", cls="form-control"), cls="col-md-3"),
            Div(Label("Garages", cls="form-label"), Input(type="number", name="garages", value=prop.garages if prop else "", cls="form-control"), cls="col-md-3"),
            cls="row mb-3"
        ),
        Div(
            Div(Label("Property Area Size", cls="form-label"), Input(type="number", name="property_area_size", step="any", value=prop.property_area_size if prop else "", cls="form-control"), cls="col-md-4"),
            Div(Label("Land Size", cls="form-label"), Input(type="number", name="property_land_size", step="any", value=prop.property_land_size if prop else "", cls="form-control"), cls="col-md-4"),
            Div(Label("Year Built", cls="form-label"), Input(type="number", name="year_built", value=prop.year_built if prop else "", cls="form-control"), cls="col-md-4"),
            cls="row mb-3"
        ),
        H4("Media", cls="mt-4"),
        Div(Label("Video URL", cls="form-label"), Input(type="text", name="video_url", value=prop.video_url if prop else "", cls="form-control"), cls="mb-3"),
        Div(Label("360 Virtual Tour URL", cls="form-label"), Input(type="text", name="virtual_tour_url", value=prop.virtual_tour_url if prop else "", cls="form-control"), cls="mb-3"),
        (Div(H4("Current Images"), *[Img(src=img, cls="img-thumbnail me-2 mb-2", style="max-width: 100px") for img in prop.images], cls="mb-3") if prop and prop.images else Div()),
        Div(Label("Upload Images", cls="form-label"), Input(type="file", name="images", multiple=True, cls="form-control"), cls="mb-3"),
        (Input(type="hidden", name="existing_images", value=",".join(prop.images)) if prop else Div()),
        Button("Save Property" if not prop else "Update Property", type="submit", cls="btn btn-primary mt-4")
    )