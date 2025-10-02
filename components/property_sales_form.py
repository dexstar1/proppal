from fasthtml.common import *
from typing import List, Optional


def PropertySalesForm(properties: List[dict] = None, sale_data: dict = None):
    """
    Multi-step property sales form following the existing component patterns
    """
    properties = properties or []
    sale_data = sale_data or {}
    
    # Property options for select dropdown
    property_options = [Option("Select Property", value="")]
    for prop in properties:
        property_type_attr = f'data-type="{prop.get("property_type", "")}"'
        property_options.append(
            Option(prop["name"], value=str(prop["id"]), **{"data-type": prop.get("property_type", "")})
        )
    
    return Form(
        Div(
            # Section 01: Property Information
            Div(
                Div(
                    Div("01", cls="badge bg-primary fs-6 me-3"),
                    Div(
                        H5("Property Information", cls="mb-1"),
                        P("Provide the details of the property", cls="text-muted small mb-0")
                    ),
                    cls="d-flex align-items-start mb-4"
                ),
                
                # Info note
                Div(
                    I(cls="fe fe-info me-2 text-primary"),
                    P("Please type carefully and fill out the form, you can't edit these details once you submitted the form. Also please be informed you'll have to select the property before you could select the property size field.", 
                      cls="mb-0 text-muted small"),
                    cls="alert alert-light d-flex align-items-start mb-4"
                ),
                
                Div(
                    # Property Selection
                    Div(
                        Div(
                            Label("Select Property", Span(" *", cls="text-danger"), cls="form-label"),
                            cls="form-label-group"
                        ),
                        Select(
                            *property_options,
                            name="property",
                            required=True,
                            cls="form-select form-control",
                            id="property-select"
                        ),
                        cls="col-md-6"
                    ),
                    
                    # Available Type/Size
                    Div(
                        Div(
                            Label("Available Type", Span(" *", cls="text-danger"), cls="form-label"),
                            cls="form-label-group"
                        ),
                        Select(
                            Option("Select Size", value=""),
                            name="location",
                            required=True,
                            disabled=True,
                            cls="form-select form-control",
                            id="location-select"
                        ),
                        cls="col-md-6"
                    ),
                    
                    # Property Type and Quantity
                    Div(
                        Div(
                            Div(
                                Label("Property Type", Span(" *", cls="text-danger"), cls="form-label"),
                                Select(
                                    Option("Select Type", value=""),
                                    Option("Commercial", value="commercial"),
                                    Option("Residential", value="residential"),
                                    name="property_type",
                                    required=True,
                                    cls="form-select form-control",
                                    id="property-type-select"
                                ),
                                cls="col"
                            ),
                            Div(
                                Label("How Many", Span(" *", cls="text-danger"), cls="form-label"),
                                Input(
                                    type="number",
                                    name="property_available",
                                    value="1",
                                    min="1",
                                    required=True,
                                    cls="form-control form-control"
                                ),
                                cls="col"
                            ),
                            cls="row g-2"
                        ),
                        cls="col-md-6"
                    ),
                    
                    # Payment Plan
                    Div(
                        Label("Property Payment Plan", Span(" *", cls="text-danger"), cls="form-label"),
                        Select(
                            Option("Select Plan", value=""),
                            # Will be populated dynamically based on property selection
                            name="payment_plan",
                            required=True,
                            cls="form-select form-control",
                            id="payment-plan-select"
                        ),
                        cls="col-md-6"
                    ),
                    
                    # Corner Piece Options
                    Div(
                        Div(
                            Div(
                                Label("Is Corner Piece Needed?", Span(" *", cls="text-danger"), cls="form-label"),
                                Select(
                                    Option("Select", value=""),
                                    Option("Yes, Add Corner Piece", value="yes"),
                                    Option("No Thanks", value="no"),
                                    name="property_corner",
                                    required=True,
                                    cls="form-select form-control",
                                    id="corner-select"
                                ),
                                cls="col"
                            ),
                            Div(
                                Label("How Many Corner Piece?", Span(" *", cls="text-danger"), cls="form-label"),
                                Input(
                                    type="number",
                                    name="property_corner_total",
                                    value="0",
                                    min="0",
                                    disabled=True,
                                    cls="form-control form-control",
                                    id="corner-total"
                                ),
                                cls="col"
                            ),
                            cls="row g-2"
                        ),
                        cls="col-md-6"
                    ),
                    
                    # First Time Sale
                    Div(
                        Label("First Time Sale Within The Selected Estate", Span(" *", cls="text-danger"), cls="form-label"),
                        Select(
                            Option("Select", value=""),
                            Option("YES, THIS IS MY FIRST TIME SALE WITHIN THE ESTATE", value="yes"),
                            Option("NO, THIS IS NOT MY FIRST TIME SALE WITHIN THE ESTATE", value="no"),
                            name="estate_first_sale",
                            required=True,
                            cls="form-select form-control"
                        ),
                        cls="col-md-6"
                    ),
                    
                    cls="row g-4"
                ),
                cls="mb-5"
            ),
            
            # Section 02: Client Information
            Div(
                Div(
                    Div("02", cls="badge bg-primary fs-6 me-3"),
                    Div(
                        H5("Client Information", cls="mb-1"),
                        P("Provide the required details and upload proof of payments", cls="text-muted small mb-0")
                    ),
                    cls="d-flex align-items-start mb-4"
                ),
                
                Div(
                    # Client Names
                    Div(
                        Label("Client First Name", Span(" *", cls="text-danger"), cls="form-label"),
                        Input(
                            type="text",
                            name="client_first_name",
                            placeholder="Enter first name eg. Kelvin",
                            required=True,
                            cls="form-control form-control"
                        ),
                        cls="col-md-6"
                    ),
                    
                    Div(
                        Label("Client Last Name", Span(" *", cls="text-danger"), cls="form-label"),
                        Input(
                            type="text",
                            name="client_last_name",
                            placeholder="Enter last name eg. Johnson",
                            required=True,
                            cls="form-control form-control"
                        ),
                        cls="col-md-6"
                    ),
                    
                    # Client Photo
                    Div(
                        Label("Upload Client Passport/Image", Span(" *", cls="text-danger"), cls="form-label"),
                        Input(
                            type="file",
                            name="client_photo",
                            accept=".jpg,.png,.jpeg,.webp",
                            required=True,
                            cls="form-control form-control"
                        ),
                        cls="col-md-12"
                    ),
                    
                    cls="row g-4 mb-4"
                ),
                
                # ID Selection
                H6("Means Of Identification For Client", Span(" *", cls="text-danger"), cls="mb-3"),
                
                Div(
                    Label(
                        Input(
                            type="radio",
                            name="client_identification",
                            value="international_passport",
                            checked=True,
                            cls="me-2"
                        ),
                        "International Passport",
                        cls="form-check-label d-flex align-items-center p-3 border rounded mb-2"
                    ),
                    Label(
                        Input(
                            type="radio",
                            name="client_identification",
                            value="nin_national_id",
                            cls="me-2"
                        ),
                        "NIN / National ID",
                        cls="form-check-label d-flex align-items-center p-3 border rounded mb-2"
                    ),
                    Label(
                        Input(
                            type="radio",
                            name="client_identification",
                            value="driver_licence",
                            cls="me-2"
                        ),
                        "Driving License",
                        cls="form-check-label d-flex align-items-center p-3 border rounded mb-2"
                    ),
                    cls="mb-4"
                ),
                
                # Guidelines
                H6("To avoid delays when verifying client credentials, Please make sure below:", cls="mb-2"),
                Ul(
                    Li("Chosen credential must not be expired."),
                    Li("Document should be good condition and clearly visible."),
                    Li("Make sure that there is no light glare on the card."),
                    cls="list-unstyled mb-4"
                ),
                
                # ID Uploads
                Div(
                    Div(
                        H6("Upload Client Front ID (Required)", cls="mb-3"),
                        Input(
                            type="file",
                            name="client_identification_upload_1",
                            accept=".jpg,.png,.jpeg,.webp,.pdf,.doc,.docx",
                            required=True,
                            cls="form-control form-control"
                        ),
                        cls="col-md-6"
                    ),
                    
                    Div(
                        H6("Upload Client Back ID (Optional)", cls="mb-3"),
                        Input(
                            type="file",
                            name="client_identification_upload_2",
                            accept=".jpg,.png,.jpeg,.webp,.pdf,.doc,.docx",
                            cls="form-control form-control"
                        ),
                        cls="col-md-6"
                    ),
                    
                    # Subscription Forms
                    Div(
                        Label("Copy(ies) Of Client Subscription Form", Span(" *", cls="text-danger"), cls="form-label"),
                        Input(
                            type="file",
                            name="client_subscription_uploads",
                            multiple=True,
                            required=True,
                            cls="form-control form-control"
                        ),
                        cls="col-md-12"
                    ),
                    
                    cls="row g-4"
                ),
                cls="mb-5"
            ),
            
            # Section 03: Payment Uploads
            Div(
                Div(
                    Div("03", cls="badge bg-primary fs-6 me-3"),
                    Div(
                        H5("Payment Uploads", cls="mb-1"),
                        P("Provide and upload proof of payments", cls="text-muted small mb-0")
                    ),
                    cls="d-flex align-items-start mb-4"
                ),
                
                # Info note
                Div(
                    I(cls="fe fe-info me-2 text-primary"),
                    P("Please upload good condition and clearly visible photos of payments and client subscriptions. Your sales post can be declined due to bad images.", 
                      cls="mb-0 text-muted small"),
                    cls="alert alert-light d-flex align-items-start mb-4"
                ),
                
                Div(
                    # Payment Details
                    Div(
                        Label("Payment Preference", Span(" *", cls="text-danger"), cls="form-label"),
                        Select(
                            Option("Select Preference", value=""),
                            Option("FOR AN EXISTING CLIENT", value="existing"),
                            Option("FOR A NEW SUBSCRIPTION", value="new"),
                            name="payment_reference",
                            required=True,
                            cls="form-select form-control"
                        ),
                        cls="col-md-6"
                    ),
                    
                    Div(
                        Label("Amount Paid", Span(" *", cls="text-danger"), cls="form-label"),
                        Input(
                            type="number",
                            name="amount",
                            step="0.01",
                            min="0",
                            required=True,
                            cls="form-control form-control",
                            placeholder="0.00"
                        ),
                        cls="col-md-6"
                    ),
                    
                    # Payment Uploads
                    Div(
                        H6("Proof Of Payment(s)", cls="mb-3"),
                        Input(
                            type="file",
                            name="payment_uploads",
                            multiple=True,
                            required=True,
                            cls="form-control form-control mb-3"
                        ),
                        cls="col-md-12"
                    ),
                    
                    # Additional Payment Info
                    Div(
                        Label("Additional Payment Information? (Optional)", cls="form-label"),
                        Textarea(
                            name="payment_information",
                            rows="3",
                            placeholder="Please provide additional payment information you may have about this payment",
                            cls="form-control form-control"
                        ),
                        cls="col-md-12"
                    ),
                    
                    cls="row g-4"
                ),
                cls="mb-5"
            ),
            
            # Section 04: Miscellaneous
            Div(
                Div(
                    Div("04", cls="badge bg-primary fs-6 me-3"),
                    Div(
                        H5("Miscellaneous", cls="mb-1"),
                        P("This section is not really required.", cls="text-muted small mb-0")
                    ),
                    cls="d-flex align-items-start mb-4"
                ),
                
                Div(
                    Label("Any Additional Information? (Optional)", cls="form-label"),
                    Textarea(
                        name="additional_information",
                        rows="5",
                        cls="form-control form-control"
                    ),
                    cls="col-12"
                ),
                cls="mb-5"
            ),
            
            # Submit Section
            Div(
                Div(
                    Input(
                        type="checkbox",
                        name="accept",
                        id="info-assure",
                        required=True,
                        cls="form-check-input me-2"
                    ),
                    Label("All payment and property Information I have entered is correct.", 
                          cls="form-check-label", **{"for": "info-assure"}),
                    cls="form-check mb-3"
                ),
                Button("Submit Property Sale", type="submit", cls="btn btn-lg btn-primary"),
                cls="text-center"
            ),
            
            cls="container-fluid"
        ),
        
        # JavaScript for form interactions
        Script(r"""
            // Corner piece toggle
            document.getElementById('corner-select').addEventListener('change', function() {
                const cornerTotal = document.getElementById('corner-total');
                if (this.value === 'yes') {
                    cornerTotal.disabled = false;
                    cornerTotal.required = true;
                    cornerTotal.min = 1;
                } else {
                    cornerTotal.disabled = true;
                    cornerTotal.required = false;
                    cornerTotal.value = 0;
                }
            });

            // Populate size and payment plan based on selected property type
            const propSelect = document.getElementById('property-select');
            const locSelect = document.getElementById('location-select');
            const planSelect = document.getElementById('payment-plan-select');
            const propTypeSelect = document.getElementById('property-type-select');

            function resetSelect(selectEl, placeholder) {
                while (selectEl.firstChild) selectEl.removeChild(selectEl.firstChild);
                const opt = document.createElement('option');
                opt.value = '';
                opt.textContent = placeholder;
                selectEl.appendChild(opt);
            }

            function populateForType(type) {
                const isLand = type === 'land';
                const isApt = type === 'apartment' || type === 'house';

                // Sizes
                const sizes = isLand ? ['300 sqm','450 sqm','600 sqm'] : isApt ? ['Studio','1 Bedroom','2 Bedroom','3 Bedroom'] : ['Standard'];
                resetSelect(locSelect, 'Select Size');
                sizes.forEach(s => {
                    const o = document.createElement('option');
                    o.value = s.toLowerCase().replace(/\s/g,'_');
                    o.textContent = s;
                    locSelect.appendChild(o);
                });
                locSelect.disabled = false;

                // Payment plans
                const plans = ['Outright','3 Months','6 Months','12 Months'];
                resetSelect(planSelect, 'Select Plan');
                plans.forEach(p => {
                    const o = document.createElement('option');
                    o.value = p.toLowerCase().replace(/\s/g,'_');
                    o.textContent = p;
                    planSelect.appendChild(o);
                });
            }

            propSelect.addEventListener('change', function() {
                const selected = this.options[this.selectedIndex];
                const type = selected ? selected.getAttribute('data-type') : '';
                if (type) populateForType(type);
            });

            // React to property type changes as well
            if (propTypeSelect) {
                propTypeSelect.addEventListener('change', function() {
                    const type = this.value || '';
                    if (type) populateForType(type);
                });
            }

            // Initialize on load if a property or property type is already selected (e.g., editing)
            (function initOnLoad(){
                let type = '';
                const selected = propSelect ? propSelect.options[propSelect.selectedIndex] : null;
                if (selected) type = selected.getAttribute('data-type') || '';
                if (!type && propTypeSelect) type = propTypeSelect.value || '';
                if (type) populateForType(type);
            })();
        """),
        
        method="post",
        enctype="multipart/form-data",
        hx_post="/realtor/sales",
        hx_target="#main-content"
    )


def PropertySalesFormNew(properties: List[dict] = None):
    """Wrapper for new property sales form"""
    return PropertySalesForm(properties=properties)