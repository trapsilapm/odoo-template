import xmlrpc.client
import os

# ==============================================================================
# Hermes Agent Odoo Connector (Standard Odoo 17.0 External XML-RPC API)
# Reference: https://www.odoo.com/documentation/17.0/developer/reference/external_api.html
# ==============================================================================

class HermesOdooBridge:
    def __init__(self, url=None, db=None, username=None, password=None):
        self.url = url or os.getenv("ODOO_URL", "http://127.0.0.1:8069")
        self.db = db or os.getenv("ODOO_DB", "postgres")
        self.username = username or os.getenv("ODOO_USER", "admin")
        self.password = password or os.getenv("ODOO_PASSWORD", "admin")
        
        self.uid = None
        self.common = None
        self.models = None

    def connect(self):
        """Otentikasi resmi ke Odoo via XML-RPC common endpoint"""
        try:
            self.common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
            self.uid = self.common.authenticate(self.db, self.username, self.password, {})
            if self.uid:
                self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')
                return True
            return False
        except Exception as e:
            print(f"Error connecting to Odoo XML-RPC API: {e}")
            return False

    def check_product_stock(self, product_name):
        """Query stok barang dari model resmi 'product.product'"""
        if not self.uid and not self.connect():
            return "Gagal terhubung ke Odoo."

        products = self.models.execute_kw(
            self.db, self.uid, self.password,
            'product.product', 'search_read',
            [[['name', 'ilike', product_name]]],
            {'fields': ['id', 'name', 'qty_available', 'list_price'], 'limit': 5}
        )
        return products

    def get_sales_summary(self):
        """Query total penjualan dari model resmi 'sale.order'"""
        if not self.uid and not self.connect():
            return "Gagal terhubung ke Odoo."

        orders = self.models.execute_kw(
            self.db, self.uid, self.password,
            'sale.order', 'search_read',
            [[['state', 'in', ['sale', 'done']]]],
            {'fields': ['name', 'amount_total', 'date_order', 'partner_id']}
        )
        total_omset = sum(order['amount_total'] for order in orders)
        return {
            "total_orders": len(orders),
            "total_omset": total_omset,
            "orders": orders
        }

    def create_crm_lead(self, lead_name, contact_name, phone, email=None):
        """Insert prospek baru ke model resmi 'crm.lead'"""
        if not self.uid and not self.connect():
            return None

        lead_id = self.models.execute_kw(
            self.db, self.uid, self.password,
            'crm.lead', 'create',
            [{
                'name': lead_name,
                'contact_name': contact_name,
                'phone': phone,
                'email_from': email or '',
            }]
        )
        return lead_id

if __name__ == "__main__":
    print("Hermes Odoo Bridge initialized. Ready for API calls.")
