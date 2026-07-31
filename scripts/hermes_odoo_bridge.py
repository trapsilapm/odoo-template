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

    def get_pos_summary(self):
        """Query total penjualan kasir dari model resmi 'pos.order'"""
        if not self.uid and not self.connect():
            return "Gagal terhubung ke Odoo."

        orders = self.models.execute_kw(
            self.db, self.uid, self.password,
            'pos.order', 'search_read',
            [[['state', 'in', ['paid', 'done', 'invoiced']]]],
            {'fields': ['name', 'amount_total', 'date_order', 'session_id', 'partner_id']}
        )
        total_omset = sum(order['amount_total'] for order in orders)
        return {
            "total_pos_transactions": len(orders),
            "total_pos_omset": total_omset,
            "orders": orders[:10]
        }

    def get_top_selling_products(self, limit=5):
        """Query produk paling laris berdasarkan transaksi POS & Sales"""
        if not self.uid and not self.connect():
            return "Gagal terhubung ke Odoo."

        pos_lines = self.models.execute_kw(
            self.db, self.uid, self.password,
            'pos.order.line', 'search_read',
            [],
            {'fields': ['product_id', 'qty', 'price_subtotal_incl'], 'limit': 100}
        )
        
        product_summary = {}
        for line in pos_lines:
            p_name = line['product_id'][1] if line['product_id'] else "Unknown"
            qty = line['qty']
            total = line['price_subtotal_incl']
            if p_name not in product_summary:
                product_summary[p_name] = {'total_qty': 0, 'total_revenue': 0}
            product_summary[p_name]['total_qty'] += qty
            product_summary[p_name]['total_revenue'] += total

        sorted_products = sorted(product_summary.items(), key=lambda x: x[1]['total_qty'], reverse=True)
        return dict(sorted_products[:limit])

    def get_low_stock_products(self, threshold=5):
        """Query barang yang stoknya di bawah threshold"""
        if not self.uid and not self.connect():
            return "Gagal terhubung ke Odoo."

        products = self.models.execute_kw(
            self.db, self.uid, self.password,
            'product.product', 'search_read',
            [[['qty_available', '<=', threshold], ['type', '=', 'product']]],
            {'fields': ['id', 'name', 'qty_available', 'list_price']}
        )
        return products

    def get_unpaid_invoices(self):
        """Query invoice pelanggan yang belum lunas (Accounts Receivable)"""
        if not self.uid and not self.connect():
            return "Gagal terhubung ke Odoo."

        invoices = self.models.execute_kw(
            self.db, self.uid, self.password,
            'account.move', 'search_read',
            [[['move_type', '=', 'out_invoice'], ['payment_state', 'in', ['not_paid', 'partial']]]],
            {'fields': ['name', 'partner_id', 'amount_residual', 'invoice_date', 'invoice_date_due']}
        )
        total_piutang = sum(inv['amount_residual'] for inv in invoices)
        return {
            "total_unpaid_invoices": len(invoices),
            "total_piutang": total_piutang,
            "invoices": invoices
        }

    def create_purchase_order(self, vendor_name, product_name, quantity):
        """Draf Purchase Order (PO) baru untuk vendor"""
        if not self.uid and not self.connect():
            return "Gagal terhubung ke Odoo."

        # Search Vendor
        vendors = self.models.execute_kw(
            self.db, self.uid, self.password,
            'res.partner', 'search_read',
            [[['name', 'ilike', vendor_name]]],
            {'fields': ['id', 'name'], 'limit': 1}
        )
        if not vendors:
            return f"Vendor '{vendor_name}' tidak ditemukan di Odoo."
        vendor_id = vendors[0]['id']

        # Search Product
        products = self.models.execute_kw(
            self.db, self.uid, self.password,
            'product.product', 'search_read',
            [[['name', 'ilike', product_name]]],
            {'fields': ['id', 'name', 'standard_price'], 'limit': 1}
        )
        if not products:
            return f"Produk '{product_name}' tidak ditemukan di Odoo."
        product_id = products[0]['id']
        price_unit = products[0]['standard_price'] or 10000

        # Create PO
        po_id = self.models.execute_kw(
            self.db, self.uid, self.password,
            'purchase.order', 'create',
            [{
                'partner_id': vendor_id,
                'order_line': [(0, 0, {
                    'product_id': product_id,
                    'name': products[0]['name'],
                    'product_qty': float(quantity),
                    'price_unit': price_unit,
                })]
            }]
        )
        return f"Draft PO berhasil dibuat dengan ID PO #{po_id} untuk Vendor {vendors[0]['name']}"

    def get_customer_history(self, customer_name):
        """Query riwayat belanja dan profil customer"""
        if not self.uid and not self.connect():
            return "Gagal terhubung ke Odoo."

        customers = self.models.execute_kw(
            self.db, self.uid, self.password,
            'res.partner', 'search_read',
            [[['name', 'ilike', customer_name]]],
            {'fields': ['id', 'name', 'phone', 'email', 'total_invoiced'], 'limit': 1}
        )
        if not customers:
            return f"Pelanggan '{customer_name}' tidak ditemukan."
        return customers[0]

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

