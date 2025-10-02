import os
import uuid
from fasthtml.common import *
from starlette.requests import Request
from starlette.datastructures import UploadFile
from components.layout import Layout
from components.card import Card
from components.property_sales_form import PropertySalesFormNew, PropertySalesForm
from backend.src.api.property_sales import (
    get_property_sales_by_realtor,
    get_property_sale_by_id,
    create_property_sale,
    update_property_sale,
    delete_property_sale,
    get_available_properties_for_realtor
)


def realtor_sales_dashboard_content(sales_data: list = None):
    """Dashboard content for realtor sales management"""
    sales_data = sales_data or []

    def action_dropdown(sale):
        # Support Pydantic models and dict-like rows
        status = getattr(sale, 'status', None)
        if status is None and isinstance(sale, dict):
            status = sale.get('status')
        sid = getattr(sale, 'id', None)
        if sid is None and isinstance(sale, dict):
            sid = sale.get('id')

        items = []
        # Show Action for pending sales; always allow View
        items.append(Li(A('View', hx_get=f"/realtor/sales/{sid}", hx_target="#main-content", cls='dropdown-item')))
        if status == 'pending':
            items.append(Li(A('Edit', hx_get=f"/realtor/sales/{sid}/edit", hx_target="#main-content", cls='dropdown-item')))
            items.append(Li(A('Delete', hx_delete=f"/realtor/sales/{sid}", hx_confirm="Are you sure you want to delete this sale?", hx_target="#main-content", cls='dropdown-item text-danger')))
        return Div(
            Button(cls='btn btn-sm btn-outline-secondary dropdown-toggle', data_bs_toggle='dropdown'),
            Ul(*items, cls='dropdown-menu'),
            cls='dropdown'
        )
    
    return Div(
        H1("Sales Management", cls="mb-4"),
        
        # Quick Stats
        Div(
            Div(
                Card(
                    title="Total Sales", 
                    content=f"{len(sales_data)} Sales", 
                    card_cls="card shadow"
                ), cls="col-12 col-md-4 mb-4 h-100"
            ),
            Div(
                Card(
                    title="Pending Approval", 
                    content=f"{len([s for s in sales_data if s.status == 'pending'])} Pending", 
                    card_cls="card col-12 col-md-4 mb-4 h-100 shadow"
                ), cls="col-12 col-md-4 mb-4 h-100"
            ),
            Div(
                Card(
                    title="Approved Sales", 
                    content=f"{len([s for s in sales_data if s.status == 'approved'])} Approved", 
                    card_cls="card col-12 col-md-4 mb-4 h-100 shadow"
                ), cls="col-12 col-md-4 mb-4 h-100"
            ),
            Div(
                Button(
                    "Add New Sale", 
                    cls="btn btn-primary me-2",
                    hx_get="/realtor/sales/new",
                    hx_target="#main-content"
                ),
                A(
                    I(cls="fa-solid fa-rotate-right"), 
                    cls="badge badge-outline-secondary",
                    hx_get="/realtor/sales",
                    hx_target="#main-content"
                ),
                cls="mb-4 d-flex align-items-center"
            ),
            Div(
                H4("Recent Sales", cls="mb-3"),
                Table(
                    Thead(
                        Tr(
                            Th("S/N"),
                            Th("Property"),
                            Th("Client"),
                            Th("Amount"),
                            Th("Status"),
                            Th("Date"),
                            Th("Action")
                        )
                    ),
                    Tbody(
                        *[Tr(
                            Td(f"{i + 1}"),
                            Td(sale.property_name or f"Property {sale.property_id}"),
                            Td(f"{sale.client_first_name} {sale.client_last_name}"),
                            Td(f"₦{sale.amount:,.2f}"),
                            Td(
                                Span(
                                    sale.status.title(),
                                    cls=f"badge bg-{'success' if sale.status == 'approved' else 'warning' if sale.status == 'pending' else 'danger'}"
                                )
                            ),
                            Td(sale.created_at.strftime("%b %d, %Y")),
                            Td(action_dropdown(sale))
                        ) for i, sale in enumerate(sales_data)] if sales_data else [
                            Tr(
                                Td("No sales found", colspan="7", cls="text-center text-muted py-4")
                            )
                        ]
                    ),
                    cls="table table-responsive table-striped table-hover"
                ),
                cls="card p-4 my-4"
            ),
            cls="row"
        ),
        
        cls="container-fluid"
    )


def realtor_sales_detail_content(sale_data):
    """Detailed view of a property sale"""
    if not sale_data:
        return Div(
            H1("Sale Not Found"),
            P("The requested sale could not be found."),
            Button("Back to Sales", cls="btn btn-secondary", hx_get="/realtor/sales", hx_target="#main-content")
        )
    
    return Div(
        Div(
            Button("← Back to Sales", cls="btn btn-outline-secondary mb-4", hx_get="/realtor/sales", hx_target="#main-content"),
            cls="d-flex justify-content-between align-items-center mb-4"
        ),
        
        H1(f"Sale #{sale_data.id} - {sale_data.client_first_name} {sale_data.client_last_name}", cls="mb-4"),
        
        Div(
            # Property Information Card
            Div(
                Div(
                    H5("Property Information", cls="card-header"),
                    Div(
                        P(f"Property ID: {sale_data.property_id}", cls="mb-2"),
                        P(f"Location Size: {sale_data.location_size}", cls="mb-2"),
                        P(f"Property Type: {sale_data.property_type.title()}", cls="mb-2"),
                        P(f"Available: {sale_data.property_available}", cls="mb-2"),
                        P(f"Payment Plan: {sale_data.payment_plan}", cls="mb-2"),
                        P(f"Corner Piece: {'Yes' if sale_data.property_corner == 'yes' else 'No'}", cls="mb-2"),
                        P(f"Corner Total: {sale_data.property_corner_total}", cls="mb-2"),
                        P(f"First Sale in Estate: {'Yes' if sale_data.estate_first_sale == 'yes' else 'No'}", cls="mb-0"),
                        cls="card-body"
                    ),
                    cls="card h-100"
                ),
                cls="col-md-6"
            ),
            
            # Client Information Card
            Div(
                Div(
                    H5("Client Information", cls="card-header"),
                    Div(
                        P(f"Name: {sale_data.client_first_name} {sale_data.client_last_name}", cls="mb-2"),
                        P(f"ID Type: {sale_data.client_identification.replace('_', ' ').title()}", cls="mb-2"),
                        P("Photo: ", A("View", href=f"/assets/uploads/{sale_data.client_photo}") if sale_data.client_photo else "Not uploaded", cls="mb-2"),
                        P("Front ID: ", A("View", href=f"/assets/uploads/{sale_data.client_identification_upload_1}") if sale_data.client_identification_upload_1 else "Not uploaded", cls="mb-2"),
                        P("Back ID: ", A("View", href=f"/assets/uploads/{sale_data.client_identification_upload_2}") if sale_data.client_identification_upload_2 else "Not uploaded", cls="mb-0"),
                        cls="card-body"
                    ),
                    cls="card h-100"
                ),
                cls="col-md-6"
            ),
            cls="row mb-4"
        ),
        
        Div(
            # Payment Information Card
            Div(
                Div(
                    H5("Payment Information", cls="card-header"),
                    Div(
                        P(f"Reference: {sale_data.payment_reference.replace('_', ' ').title()}", cls="mb-2"),
                        P(f"Amount: ₦{sale_data.amount:,.2f}", cls="mb-2"),
                        P(f"Status: ", Span(sale_data.status.title(), cls=f"badge bg-{'success' if sale_data.status == 'approved' else 'warning' if sale_data.status == 'pending' else 'danger'}"), cls="mb-2"),
                        (P(f"Decision On: {(sale_data.approved_at or sale_data.rejected_at).strftime('%B %d, %Y at %I:%M %p')}", cls="mb-2") if (getattr(sale_data, 'approved_at', None) or getattr(sale_data, 'rejected_at', None)) and sale_data.status in ['approved','rejected'] else Div()),
                        (P(f"Rejection Reason: {sale_data.reject_reason}", cls="mb-2 text-danger") if getattr(sale_data, 'reject_reason', None) and sale_data.status == 'rejected' else Div()),
                        P(f"Payment Info: {sale_data.payment_information or 'None'}", cls="mb-0"),
                        cls="card-body"
                    ),
                    cls="card h-100"
                ),
                cls="col-md-6"
            ),
            
            # Additional Information Card
            Div(
                Div(
                    H5("Additional Information", cls="card-header"),
                    Div(
                        P(f"Created: {sale_data.created_at.strftime('%B %d, %Y at %I:%M %p')}", cls="mb-2"),
                        P(f"Updated: {sale_data.updated_at.strftime('%B %d, %Y at %I:%M %p')}", cls="mb-2"),
                        P(f"Additional Notes: {sale_data.additional_information or 'None'}", cls="mb-0"),
                        cls="card-body"
                    ),
                    cls="card h-100"
                ),
                cls="col-md-6"
            ),
            cls="row mb-4"
        ),
        
        # Action Buttons
        Div(
            Button(
                "Edit Sale",
                cls="btn btn-primary me-2",
                hx_get=f"/realtor/sales/{sale_data.id}/edit",
                hx_target="#main-content"
            ),
            Button(
                "Delete Sale",
                cls="btn btn-danger",
                hx_delete=f"/realtor/sales/{sale_data.id}",
                hx_confirm="Are you sure you want to delete this sale?",
                hx_target="#main-content"
            ),
            cls="text-center"
        ),
        
        cls="container-fluid"
    )


async def _save_uploaded_files(form_data, field_name: str) -> list:
    """Helper function to save uploaded files"""
    files = form_data.getlist(field_name)
    saved_files = []
    
    upload_dir = "public/assets/uploads"
    os.makedirs(upload_dir, exist_ok=True)
    
    for file in files:
        if isinstance(file, UploadFile) and file.filename:
            # Generate unique filename
            ext = file.filename.split('.')[-1] if '.' in file.filename else ''
            filename = f"{uuid.uuid4()}.{ext}"
            filepath = os.path.join(upload_dir, filename)
            
            # Save file
            with open(filepath, "wb") as f:
                content = await file.read()
                f.write(content)
            
            saved_files.append(filename)
    
    return saved_files


async def _save_single_file(form_data, field_name: str) -> str:
    """Helper function to save a single uploaded file"""
    file = form_data.get(field_name)
    
    if not isinstance(file, UploadFile) or not file.filename:
        return None
    
    upload_dir = "public/assets/uploads"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    ext = file.filename.split('.')[-1] if '.' in file.filename else ''
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(upload_dir, filename)
    
    # Save file
    with open(filepath, "wb") as f:
        content = await file.read()
        f.write(content)
    
    return filename


# Route Handlers

async def realtor_sales_dashboard(request: Request):
    """Main sales dashboard"""
    user = request.scope.get('user')
    if not user:
        return RedirectResponse(url="/login")
    
    sales = await get_property_sales_by_realtor(user.id)
    content = realtor_sales_dashboard_content(sales)
    
    return content if request.headers.get("HX-Request") else Layout(content, user_role="Realtor")


async def realtor_sales_new(request: Request):
    """New sale form"""
    user = request.scope.get('user')
    if not user:
        return RedirectResponse(url="/login")
    
    properties = await get_available_properties_for_realtor(user.id)
    content = Div(
        H1("New Property Sale", cls="mb-4"),
        Button("← Back to Sales", cls="btn btn-outline-secondary mb-4", hx_get="/realtor/sales", hx_target="#main-content"),
        PropertySalesFormNew(properties=properties),
        cls="container-fluid"
    )
    
    # Flash toast (on page render)
    flash = request.session.pop('flash', None) if hasattr(request, 'session') else None
    if flash and isinstance(flash, dict):
        content = Div(content, Script(f"showToast({(flash.get('message') or '')!r}, {(flash.get('level') or 'info')!r})"))
    return content if request.headers.get("HX-Request") else Layout(content, user_role="Realtor")


async def realtor_sales_create(request: Request):
    """Create new sale"""
    user = request.scope.get('user')
    if not user:
        return RedirectResponse(url="/login")
    
    try:
        form = await request.form()
        
        # Handle file uploads
        client_photo = await _save_single_file(form, 'client_photo')
        client_id_1 = await _save_single_file(form, 'client_identification_upload_1')
        client_id_2 = await _save_single_file(form, 'client_identification_upload_2')
        subscription_files = await _save_uploaded_files(form, 'client_subscription_uploads')
        payment_files = await _save_uploaded_files(form, 'payment_uploads')
        
        # Prepare sale data with safe defaults for required fields
        def _coerce_int(val, default=0):
            try:
                return int(val)
            except (TypeError, ValueError):
                return default
        def _coerce_float(val, default=0.0):
            try:
                return float(val)
            except (TypeError, ValueError):
                return default

        sale_data = {
            'property_id': _coerce_int(form.get('property')),
            'location_size': (form.get('location') or 'standard'),
            'property_type': (form.get('property_type') or 'residential'),
            'property_available': _coerce_int(form.get('property_available'), 1),
            'payment_plan': (form.get('payment_plan') or 'outright'),
            'property_corner': (form.get('property_corner') or 'no'),
            'property_corner_total': _coerce_int(form.get('property_corner_total'), 0),
            'estate_first_sale': (form.get('estate_first_sale') or 'no'),
            'client_first_name': form.get('client_first_name'),
            'client_last_name': form.get('client_last_name'),
            'client_photo': client_photo,
            'client_identification': form.get('client_identification') or 'international_passport',
            'client_identification_upload_1': client_id_1,
            'client_identification_upload_2': client_id_2,
            'client_subscription_uploads': subscription_files,
            'payment_reference': (form.get('payment_reference') or 'existing'),
            'amount': _coerce_float(form.get('amount'), 0.01),
            'payment_uploads': payment_files,
            'payment_information': form.get('payment_information'),
            'additional_information': form.get('additional_information'),
            'realtor_id': user.id
        }
        
        # Create sale
        created_sale = await create_property_sale(sale_data)
        if hasattr(request, 'session'):
            request.session['flash'] = {'message': 'Property sale created successfully!', 'level': 'success'}
        return Response(headers={'HX-Redirect': '/realtor/sales'})
        
    except Exception as e:
        if hasattr(request, 'session'):
            request.session['flash'] = {'message': f'Error creating sale: {str(e)}', 'level': 'danger'}
        return Response(headers={'HX-Redirect': '/realtor/sales'})


async def realtor_sales_detail(request: Request):
    """View sale details"""
    user = request.scope.get('user')
    if not user:
        return RedirectResponse(url="/login")
    
    sale_id = int(request.path_params.get('sale_id'))
    sale = await get_property_sale_by_id(sale_id)
    
    # Check if sale belongs to current realtor
    if sale and sale.realtor_id != user.id:
        sale = None
    
    content = realtor_sales_detail_content(sale)
    # Flash toast
    flash = request.session.pop('flash', None) if hasattr(request, 'session') else None
    if flash and isinstance(flash, dict):
        content = Div(content, Script(f"showToast({(flash.get('message') or '')!r}, {(flash.get('level') or 'info')!r})"))
    return content if request.headers.get("HX-Request") else Layout(content, user_role="Realtor")


async def realtor_sales_edit(request: Request):
    """Edit sale form"""
    user = request.scope.get('user')
    if not user:
        return RedirectResponse(url="/login")
    
    sale_id = int(request.path_params.get('sale_id'))
    sale = await get_property_sale_by_id(sale_id)
    
    if not sale or sale.realtor_id != user.id:
        return Div("Sale not found", cls="alert alert-danger")
    
    properties = await get_available_properties_for_realtor(user.id)
    
    content = Div(
        H1(f"Edit Sale #{sale_id}", cls="mb-4"),
        Button("← Back to Sale", cls="btn btn-outline-secondary mb-4", hx_get=f"/realtor/sales/{sale_id}", hx_target="#main-content"),
        PropertySalesForm(properties=properties, sale_data=sale.__dict__),
        cls="container-fluid"
    )
    
    return content if request.headers.get("HX-Request") else Layout(content, user_role="Realtor")


async def realtor_sales_update(request: Request):
    """Update sale"""
    user = request.scope.get('user')
    if not user:
        return RedirectResponse(url="/login")
    
    sale_id = int(request.path_params.get('sale_id'))
    sale = await get_property_sale_by_id(sale_id)
    
    if not sale or sale.realtor_id != user.id:
        return Div("Sale not found", cls="alert alert-danger")
    
    try:
        form = await request.form()
        
        # Handle file uploads (only update if new files provided)
        update_data = {}
        
        for field in ['client_first_name', 'client_last_name', 'property_type', 
                     'property_available', 'payment_plan', 'property_corner',
                     'property_corner_total', 'estate_first_sale', 'client_identification',
                     'payment_reference', 'amount', 'payment_information', 'additional_information']:
            value = form.get(field)
            if value is not None:
                if field in ['property_available', 'property_corner_total']:
                    update_data[field] = int(value)
                elif field == 'amount':
                    update_data[field] = float(value)
                else:
                    update_data[field] = value
        
        # Update sale
        updated_sale = await update_property_sale(sale_id, update_data)
        if hasattr(request, 'session'):
            request.session['flash'] = {'message': 'Property sale updated successfully!', 'level': 'success'}
        return Response(headers={'HX-Redirect': '/realtor/sales'})
        
    except Exception as e:
        if hasattr(request, 'session'):
            request.session['flash'] = {'message': f'Error updating sale: {str(e)}', 'level': 'danger'}
        return Response(headers={'HX-Redirect': '/realtor/sales'})


async def realtor_sales_delete(request: Request):
    """Delete sale"""
    user = request.scope.get('user')
    if not user:
        return RedirectResponse(url="/login")
    
    sale_id = int(request.path_params.get('sale_id'))
    sale = await get_property_sale_by_id(sale_id)
    
    if not sale or sale.realtor_id != user.id:
        return Div("Sale not found", cls="alert alert-danger")
    
    try:
        await delete_property_sale(sale_id)
        if hasattr(request, 'session'):
            request.session['flash'] = {'message': 'Property sale deleted successfully!', 'level': 'success'}
        return Response(headers={'HX-Redirect': '/realtor/sales'})
        
    except Exception as e:
        if hasattr(request, 'session'):
            request.session['flash'] = {'message': f'Error deleting sale: {str(e)}', 'level': 'danger'}
        return Response(headers={'HX-Redirect': '/realtor/sales'})


# Main route dispatcher
async def realtor_sales_route_handler(request: Request):
    """Main route handler for realtor sales"""
    method = request.method
    path = request.url.path
    
    if method == "GET":
        if path.endswith("/new"):
            return await realtor_sales_new(request)
        elif path.endswith("/edit"):
            return await realtor_sales_edit(request)
        elif "/sales/" in path and not path.endswith("/edit") and not path.endswith("/new"):
            return await realtor_sales_detail(request)
        else:
            return await realtor_sales_dashboard(request)
    
    elif method == "POST":
        return await realtor_sales_create(request)
    
    elif method == "PUT":
        return await realtor_sales_update(request)
    
    elif method == "DELETE":
        return await realtor_sales_delete(request)
    
    else:
        return Div("Method not allowed", cls="alert alert-danger")