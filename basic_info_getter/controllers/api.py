from odoo import http
from odoo.http import request
#from dotenv import load_dotenv
import os
import json
import uuid
import re

#load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))


class CustomAPI(http.Controller):

    @http.route('/api/sales', auth='public', type='http', methods=['GET'])
    def get_sales(self, **kwargs):
        user = self.authenticate_api()
        if isinstance(user, http.Response):  
            return user
        
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
    
    @http.route('/api/crm', auth='public', type='http', methods=['GET'])
    def get_crm(self, **kwargs):
        user = self.authenticate_api()
        if isinstance(user, http.Response):  
            return user
        
        try:
            crm_s = request.env['crm.lead'].sudo().search([])

            crm_data = []

            for crm in crm_s:
                user_image = ''
                if crm.contact_name:
                    cleaned_name = bytes(crm.contact_name, "utf-8").decode("unicode_escape")
                    user_image = f'C:/Users/User/Downloads/imgs/{cleaned_name}.jpg'

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
        

    @http.route('/api/country', auth='public', type='http', methods=['GET'])
    def get_country(self, **kwargs):
        user = self.authenticate_api()
        if isinstance(user, http.Response):  
            return user
        
        try:
            countries = request.env['res.country'].sudo().search([])

            country_data = []

            for country in countries:
            
                country_data.append({
                    'id': country.id,
                    'code': country.code,
                    'name': country.name,
                })

            return http.Response(json.dumps({'Countries': country_data}, indent=4), content_type="application/json", status=200)

        except Exception as e:
            return http.Response(json.dumps({'error': str(e)}), content_type="application/json", status=500)
        

    @http.route('/api/products', auth='public', type='http', methods=['GET'])
    def get_products(self, **kwargs):
        user = self.authenticate_api()
        if isinstance(user, http.Response):  
            return user
        
        try:
            products = request.env['product.product'].sudo().search([])

            product_data = []

            for product in products:
                
                product_image = ''
                if product.name:

                    cleaned_name = re.sub(r'[^\w\s-]', '', product.name).strip()
                    cleaned_name = cleaned_name.replace(' ', '_')  
                    
                    product_image = f'C:/Users/User/Downloads/imgs/{cleaned_name}.jpg'

                product_data.append({
                    'id': product.id,
                    'name': product.name,
                    'category': product.categ_id.name if product.categ_id else None,
                    'image_route': product_image
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
        
    def authenticate_api(self):
        api_key = request.httprequest.headers.get('Authorization')

        if not api_key or not api_key.startswith("ApiKey "):
            return False 

        api_key = api_key[7:]

        return self.is_valid_api_key(api_key)

    def is_valid_api_key(self, api_key):
        #API_KEY_1 = os.getenv('ODOO_API_KEY')
        valid_api_keys = [
            "bd1d5c433d13df65e2d4f41e1cd28053667db67e",
        ]

        if api_key in valid_api_keys:
            return True
        return False
