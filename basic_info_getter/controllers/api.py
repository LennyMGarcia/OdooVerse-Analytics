from odoo import http
from odoo.http import request
import json

class CustomAPI(http.Controller):
    @http.route('/api/sales', auth='user', type='http', methods=['GET'])
    def get_sales(self, **kwargs):
        try:
            sales_orders = request.env['sale.order'].sudo().search([])

            sales_data = [
                {
                    'order_id': order.id,
                    'customer': order.partner_id.name,
                    'date_order': str(order.date_order),
                    'amount_total': order.amount_total,
                    'state': order.state,
                } for order in sales_orders
            ]

            return http.Response(json.dumps(sales_data), content_type="application/json", status=200)

        except Exception as e:
            return http.Response(json.dumps({'error': str(e)}), content_type="application/json", status=500)


