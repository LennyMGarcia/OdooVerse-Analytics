from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF
from responses import responses

g = Graph()

EX = URIRef("http://odoollm.org/")

products = responses.get("http://localhost:8069/api/products", {}).get("Products", [])
countries = responses.get("http://localhost:8069/api/country", {}).get("Countries", [])
sales_orders = responses.get("http://localhost:8069/api/sales", {}).get("sales_orders", [])
order_lines = responses.get("http://localhost:8069/api/sales", {}).get("order_lines", [])
CRM_s = responses.get("http://localhost:8069/api/crm", {}).get("CRM", [])

for sales_order in sales_orders:
    sales_order_uri = URIRef(f"{EX}Sales_order_{sales_order['order_id']}")
    g.add(( sales_order_uri, RDF.type, URIRef(f"{EX}Sales_order")))
    g.add(( sales_order_uri, URIRef(f"{EX}hasContactName"), Literal(sales_order["partner_invoice"])))
    g.add(( sales_order_uri, URIRef(f"{EX}hasPartnerShipping"), Literal(sales_order["partner_shipping"])))
    g.add(( sales_order_uri, URIRef(f"{EX}hasDate"), Literal(sales_order["date_order"])))
    g.add(( sales_order_uri, URIRef(f"{EX}hasState"), Literal(sales_order["state"])))
    g.add(( sales_order_uri, URIRef(f"{EX}hasAmountUntaxed"), Literal(sales_order["amount_untaxed"])))
    g.add(( sales_order_uri, URIRef(f"{EX}hasAmountTax"), Literal(sales_order["amount_tax"])))
    g.add(( sales_order_uri, URIRef(f"{EX}hasAmountTotal"), Literal(sales_order["amount_total"])))
    g.add(( sales_order_uri, URIRef(f"{EX}hasCountryCode"), Literal(sales_order["country_code"])))

for order_line in order_lines:
    order_line_uri = URIRef(f"{EX}Order_line_{order_line['id']}")
    g.add(( order_line_uri, RDF.type, URIRef(f"{EX}Order_line")))
    order_id = order_line["order_id"]
    sales_order_uri = URIRef(f"{EX}Sales_order_{order_id}")
    g.add(( order_line_uri, URIRef(f"{EX}hasSalesOrder"), sales_order_uri))
    g.add(( order_line_uri, URIRef(f"{EX}hasProductName"), Literal(order_line["product_name"])))
    g.add(( order_line_uri, URIRef(f"{EX}hasQuantity"), Literal(order_line["quantity"])))
    g.add(( order_line_uri, URIRef(f"{EX}hasPrice"), Literal(order_line["unit_price"])))
    g.add(( order_line_uri, URIRef(f"{EX}hasSubtotal"), Literal(order_line["subtotal"])))


for product in products:
    product_uri = URIRef(f"{EX}Product_{product['id']}")
    g.add((product_uri, RDF.type, URIRef(f"{EX}Product")))
    g.add((product_uri, URIRef(f"{EX}hasProductName"), Literal(product["name"])))
    g.add((product_uri, URIRef(f"{EX}hasImage"), Literal(product["image_route"])))

for country in countries:
    country_uri = URIRef(f"{EX}Country_{country['id']}")
    g.add((country_uri, RDF.type, URIRef(f"{EX}Country")))
    g.add((country_uri, URIRef(f"{EX}hasCountryCode"), Literal(country["code"])))
    g.add((country_uri, URIRef(f"{EX}hasCountryName"), Literal(country["name"])))

for CRM in CRM_s:
    CRM_uri = URIRef(f"{EX}CRM_{CRM['lead_id']}")
    g.add(( CRM_uri, RDF.type, URIRef(f"{EX}CRM")))
    g.add(( CRM_uri, URIRef(f"{EX}hasContactName"), Literal(CRM["name"])))
    g.add(( CRM_uri, URIRef(f"{EX}hasEmail"), Literal(CRM["email_from"])))
    g.add(( CRM_uri, URIRef(f"{EX}hasPhone"), Literal(CRM["phone"])))
    g.add(( CRM_uri, URIRef(f"{EX}hasStage"), Literal(CRM["stage"])))
    g.add(( CRM_uri, URIRef(f"{EX}hasContact"), Literal(CRM["contact_name"])))
    g.add(( CRM_uri, URIRef(f"{EX}hasImage"), Literal(CRM["image_html"])))
    
g.serialize(destination="data.ttl", format="turtle")

print("Archivo TTL guardado como data.ttl")