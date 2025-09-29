from fasthtml.common import *
from fasthtml.components import *
from tinydb import TinyDB, Query
import uvicorn

# --- Database Setup ---
db = TinyDB('sales_db.json')
sales_table = db.table('sales')

# --- Data Model (simplified from the form) ---
# In a real app, you'd use a more robust validation library like Pydantic
@dataclass
class PropertySale:
    id: int = -1
    property: str = ""
    location: str = ""
    property_type: str = ""
    payment_plan: str = ""
    client_first_name: str = ""
    client_last_name: str = ""
    amount: float = 0.0
    # File fields would need special handling for storage
    # client_photo: str = ""
    # client_identification_upload_1: str = ""

    def __post_init__(self):
        if self.id == -1:
            # Get the max id and increment
            all_sales = sales_table.all()
            if all_sales:
                self.id = max(s['id'] for s in all_sales) + 1
            else:
                self.id = 1

# --- FastHTML App ---
app = FastHTML()
rt = app.route

# --- Page Layout ---
def page_layout(title: str, *content):
    return Title(title), Main(
        H1(title),
        *content,
        cls='container'
    )

# --- CRUD Operations ---

# CREATE: Display form for a new sale
@rt('/sales/new')
def get_new_sale_form():
    # A simplified version of your form using fasthtml components
    # In a real app, you would convert your entire form structure.
    sale_form = Form(
        Div(
            Label("Property Name:", for_="property"),
            Input(id="property", name="property", required=True),
            cls="form-group"
        ),
        Div(
            Label("Location:", for_="location"),
            Input(id="location", name="location", required=True),
            cls="form-group"
        ),
        Div(
            Label("Property Type:", for_="property_type"),
            Select(
                Option("Select Type", value=""),
                Option("Commercial", value="commercial"),
                Option("Residential", value="residential"),
                id="property_type", name="property_type", required=True
            ),
            cls="form-group"
        ),
        Div(
            Label("Client First Name:", for_="client_first_name"),
            Input(id="client_first_name", name="client_first_name", required=True),
            cls="form-group"
        ),
        Div(
            Label("Client Last Name:", for_="client_last_name"),
            Input(id="client_last_name", name="client_last_name", required=True),
            cls="form-group"
        ),
        Div(
            Label("Amount:", for_="amount"),
            Input(id="amount", name="amount", type="number", step="0.01", required=True),
            cls="form-group"
        ),
        Button("Create Sale", type="submit"),
        action="/sales", method="post"
    )
    return page_layout("Add New Property Sale", sale_form)

# CREATE: Handle form submission
@rt('/sales', methods=['POST'])
def create_sale(
    property:str, location:str, property_type:str,
    client_first_name:str, client_last_name:str, amount:float
):
    new_sale = PropertySale(
        property=property, location=location, property_type=property_type,
        client_first_name=client_first_name, client_last_name=client_last_name,
        amount=amount
    )
    sales_table.insert(new_sale.__dict__)
    return RedirectResponse('/sales', status_code=303)

# READ: List all sales
@rt('/sales')
def get_sales_list():
    sales = sales_table.all()
    
    def sale_row(sale_data):
        sale = PropertySale(**sale_data)
        return Tr(
            Td(sale.id),
            Td(sale.property),
            Td(sale.client_first_name, " ", sale.client_last_name),
            Td(f"${sale.amount:,.2f}"),
            Td(
                A("View", href=f"/sales/{sale.id}"), " | ",
                A("Edit", href=f"/sales/{sale.id}/edit"), " | ",
                A("Delete", href=f"/sales/{sale.id}/delete")
            )
        )

    sales_table_component = Table(
        Thead(Tr(Th("ID"), Th("Property"), Th("Client"), Th("Amount"), Th("Actions"))),
        Tbody(*[sale_row(s) for s in sales])
    )

    return page_layout(
        "All Property Sales",
        A("Add New Sale", href="/sales/new", cls="button"),
        sales_table_component
    )

# READ: Show a single sale
@rt('/sales/{id}')
def get_sale_details(id:int):
    Sale = Query()
    sale_data = sales_table.get(Sale.id == id)
    if not sale_data:
        return "Sale not found", 404
    
    sale = PropertySale(**sale_data)
    details = Ul(
        Li(B("Property: "), sale.property),
        Li(B("Location: "), sale.location),
        Li(B("Type: "), sale.property_type),
        Li(B("Client: "), f"{sale.client_first_name} {sale.client_last_name}"),
        Li(B("Amount: "), f"${sale.amount:,.2f}"),
    )
    return page_layout(f"Sale #{sale.id}", details, A("Back to list", href="/sales"))

# UPDATE: Display edit form
@rt('/sales/{id}/edit')
def get_edit_sale_form(id:int):
    Sale = Query()
    sale_data = sales_table.get(Sale.id == id)
    if not sale_data:
        return "Sale not found", 404
    
    sale = PropertySale(**sale_data)
    edit_form = Form(
        Input(type="hidden", name="id", value=sale.id),
        Div(
            Label("Property Name:", for_="property"),
            Input(id="property", name="property", value=sale.property, required=True),
            cls="form-group"
        ),
        Div(
            Label("Amount:", for_="amount"),
            Input(id="amount", name="amount", type="number", step="0.01", value=sale.amount, required=True),
            cls="form-group"
        ),
        # Add other fields as needed for editing
        Button("Update Sale", type="submit"),
        action=f"/sales/{id}/edit", method="post"
    )
    return page_layout(f"Edit Sale #{sale.id}", edit_form)

# UPDATE: Handle edit form submission
@rt('/sales/{id}/edit', methods=['POST'])
def update_sale(id:int, property:str, amount:float):
    Sale = Query()
    sales_table.update({'property': property, 'amount': amount}, Sale.id == id)
    return RedirectResponse(f'/sales/{id}', status_code=303)

# DELETE: Show confirmation and handle deletion
@rt('/sales/{id}/delete')
def delete_sale_confirmation(id:int):
    Sale = Query()
    sale_data = sales_table.get(Sale.id == id)
    if not sale_data:
        return "Sale not found", 404
    
    return page_layout(
        f"Delete Sale #{id}?",
        P(f"Are you sure you want to delete the sale for property: {sale_data['property']}?"),
        Form(
            Button("Yes, Delete", type="submit"),
            action=f"/sales/{id}/delete", method="post"
        ),
        A("Cancel", href=f"/sales/{id}")
    )

@rt('/sales/{id}/delete', methods=['POST'])
def handle_delete_sale(id:int):
    Sale = Query()
    sales_table.remove(Sale.id == id)
    return RedirectResponse('/sales', status_code=303)

# --- Run the app ---
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
