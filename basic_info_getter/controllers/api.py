from odoo import http
from odoo.http import request
import json
import uuid
import re

class CustomAPI(http.Controller):
    @http.route('/api/sales', auth='user', type='http', methods=['GET'])
    def get_sales(self, **kwargs):
        try:
            sales_orders = request.env['sale.order'].sudo().search([])

            sales_data = []
            order_lines_data = []

            for order in sales_orders:
                sales_data.append({
                    'order_id': order.name,
                    'partner_invoice': order.partner_invoice_id.name,
                    'partner_shipping': order.partner_shipping_id.name,
                    'date_order': str(order.date_order),
                    'state': order.state,
                    'amount_untaxed': order.amount_untaxed,
                    'amount_tax': order.amount_tax,
                    'amount_total': order.amount_total,
                    'country_code': order.partner_invoice_id.country_id.code if order.partner_invoice_id.country_id else '',
                })

                for line in order.order_line:
                    order_lines_data.append({
                        'id': str(uuid.uuid4()),
                        'order_id': order.name,
                        'product_name': line.product_id.name,
                        'quantity': line.product_uom_qty,
                        'unit_price': line.price_unit,
                        'subtotal': line.price_subtotal,
                    })

            response_data = {
                'sales_orders': sales_data,
                'order_lines': order_lines_data
            }

            return http.Response(json.dumps(response_data), content_type="application/json", status=200)

        except Exception as e:
            return http.Response(json.dumps({'error': str(e)}), content_type="application/json", status=500)
    
    @http.route('/api/crm', auth='user', type='http', methods=['GET'])
    def get_crm(self, **kwargs):
        try:
            crm_s = request.env['crm.lead'].sudo().search([])

            crm_data = []

            for crm in crm_s:
                user_image = ''
                if crm.contact_name:
                    cleaned_name = bytes(crm.contact_name, "utf-8").decode("unicode_escape")
                    user_image = f'<img src="file:///C:/Users/User/Downloads/imgs{cleaned_name}.jpg" />'

                crm_data.append({
                    'lead_id': crm.id,
                    'name': crm.name,
                    'email_from': crm.email_from,
                    'phone': crm.phone,
                    'stage': crm.stage_id.name if crm.stage_id else '',
                    'contact_name': crm.contact_name,
                    'image_html': user_image
                })

            return http.Response(json.dumps({'CRM': crm_data}, indent=4), content_type="application/json", status=200)

        except Exception as e:
            return http.Response(json.dumps({'error': str(e)}), content_type="application/json", status=500)
        

    @http.route('/api/country', auth='user', type='http', methods=['GET'])
    def get_country(self, **kwargs):
        try:
            countries = request.env['res.country'].sudo().search([])

            country_data = []

            for country in countries:
            
                country_data.append({
                    'code': country.id,
                    'name': country.name,
                })

            return http.Response(json.dumps({'Countries': country_data}, indent=4), content_type="application/json", status=200)

        except Exception as e:
            return http.Response(json.dumps({'error': str(e)}), content_type="application/json", status=500)
        

    @http.route('/api/products', auth='user', type='http', methods=['GET'])
    def get_products(self, **kwargs):
        try:
            products = request.env['product.product'].sudo().search([])

            product_data = []

            for product in products:
                
                product_image = ''
                if product.name:

                    cleaned_name = re.sub(r'[^\w\s-]', '', product.name).strip()
                    cleaned_name = cleaned_name.replace(' ', '_')  
                    
                    product_image = f'<img src="file:///C:/Users/User/Downloads/imgs/{cleaned_name}.jpg" />'

                product_data.append({
                    'id': product.id,
                    'name': product.name,
                    'image_html': product_image
                })

            return http.Response(json.dumps({'Products': product_data}, indent=4), content_type="application/json", status=200)

        except Exception as e:
            return http.Response(json.dumps({'error': str(e)}), content_type="application/json", status=500)
                           

    @http.route('/api/env', auth='user', type='http', methods=['GET'])
    def get_all_env(self, **kwargs):
        try:
            
            env_data = {
                model: str(request.env[model]) 
                for model in request.env
            }

            return http.Response(json.dumps(env_data, indent=4), content_type="application/json", status=200)

        except Exception as e:
            return http.Response(json.dumps({'error': str(e)}), content_type="application/json", status=500)
    
    @http.route('/api/model', auth='user', type='http', methods=['GET'])
    def get_model(self, **query):
        try:
            model_name = query.get('model', 'base')

            if model_name not in request.env:
                return http.Response(json.dumps({'error': f'Model {model_name} not found'}), content_type="application/json", status=400)

            data = request.env['product.product'].sudo().search([])

            model = data.read([])

            return http.Response(json.dumps(model, indent=4, default=str), content_type="application/json", status=200)


        except Exception as e:
            return http.Response(json.dumps({'error': str(e)}), content_type="application/json", status=500)


