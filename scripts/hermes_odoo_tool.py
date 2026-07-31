import json
from hermes_odoo_bridge import HermesOdooBridge

# Inisialisasi bridge singleton
odoo_bridge = HermesOdooBridge()

# Schema Definisi Tools untuk Hermes Agent (OpenAI & DeepSeek API Compatible Format)
HERMES_ODOO_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "check_product_stock",
            "description": "Mengecek jumlah sisa stok dan harga produk di Odoo ERP berdasarkan nama barang.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": "Nama produk atau kata kunci nama barang (contoh: 'Laptop', 'Kertas', 'Printer')"
                    }
                },
                "required": ["product_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_sales_summary",
            "description": "Mengambil rangkuman total omset dan jumlah transaksi penjualan (Sales Order) dari Odoo ERP.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_crm_lead",
            "description": "Membuat prospek/lead pelanggan baru di CRM Odoo ERP.",
            "parameters": {
                "type": "object",
                "properties": {
                    "lead_name": {
                        "type": "string",
                        "description": "Judul prospek/kebutuhan (contoh: 'Prospek Pengadaan Laptop PT ABC')"
                    },
                    "contact_name": {
                        "type": "string",
                        "description": "Nama lengkap kontak/orang yang dihubungi"
                    },
                    "phone": {
                        "type": "string",
                        "description": "Nomor telepon/WhatsApp kontak"
                    },
                    "email": {
                        "type": "string",
                        "description": "Alamat email kontak (opsional)"
                    }
                },
                "required": ["lead_name", "contact_name", "phone"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_pos_summary",
            "description": "Mengambil rangkuman total omset dan jumlah transaksi penjualan kasir (Point of Sale / POS).",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_top_selling_products",
            "description": "Mendapatkan daftar produk terlaris (fast-moving items) dari transaksi kasir dan penjualan.",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Jumlah produk terlaris yang ingin ditampilkan (default: 5)"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_low_stock_products",
            "description": "Mengecek daftar barang yang stoknya di bawah batas minimal (stok menipis).",
            "parameters": {
                "type": "object",
                "properties": {
                    "threshold": {
                        "type": "integer",
                        "description": "Batas minimal stok (default: 5)"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_unpaid_invoices",
            "description": "Mengecek daftar invoice tagihan pelanggan yang belum lunas dan total piutang usaha.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_purchase_order",
            "description": "Membuat draft Purchase Order (PO) pengadaan barang baru ke supplier/vendor di Odoo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "vendor_name": {
                        "type": "string",
                        "description": "Nama vendor/supplier tempat membeli barang"
                    },
                    "product_name": {
                        "type": "string",
                        "description": "Nama barang yang akan dibeli"
                    },
                    "quantity": {
                        "type": "number",
                        "description": "Jumlah/kuantitas barang yang dibeli"
                    }
                },
                "required": ["vendor_name", "product_name", "quantity"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_customer_history",
            "description": "Mencari profil dan total riwayat transaksi belanja pelanggan dari Odoo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_name": {
                        "type": "string",
                        "description": "Nama pelanggan/perusahaan yang dicari"
                    }
                },
                "required": ["customer_name"]
            }
        }
    }
]

def execute_odoo_tool(tool_name: str, arguments: dict):
    """Eksekutor tool function call Odoo untuk Hermes Agent"""
    if tool_name == "check_product_stock":
        product_name = arguments.get("product_name", "")
        res = odoo_bridge.check_product_stock(product_name)
        return json.dumps(res, default=str)
        
    elif tool_name == "get_sales_summary":
        res = odoo_bridge.get_sales_summary()
        return json.dumps(res, default=str)

    elif tool_name == "get_pos_summary":
        res = odoo_bridge.get_pos_summary()
        return json.dumps(res, default=str)

    elif tool_name == "get_top_selling_products":
        limit = arguments.get("limit", 5)
        res = odoo_bridge.get_top_selling_products(limit)
        return json.dumps(res, default=str)

    elif tool_name == "get_low_stock_products":
        threshold = arguments.get("threshold", 5)
        res = odoo_bridge.get_low_stock_products(threshold)
        return json.dumps(res, default=str)

    elif tool_name == "get_unpaid_invoices":
        res = odoo_bridge.get_unpaid_invoices()
        return json.dumps(res, default=str)

    elif tool_name == "create_purchase_order":
        vendor_name = arguments.get("vendor_name")
        product_name = arguments.get("product_name")
        quantity = arguments.get("quantity")
        res = odoo_bridge.create_purchase_order(vendor_name, product_name, quantity)
        return json.dumps({"status": "info", "message": res})

    elif tool_name == "get_customer_history":
        customer_name = arguments.get("customer_name")
        res = odoo_bridge.get_customer_history(customer_name)
        return json.dumps(res, default=str)
        
    elif tool_name == "create_crm_lead":
        lead_name = arguments.get("lead_name")
        contact_name = arguments.get("contact_name")
        phone = arguments.get("phone")
        email = arguments.get("email", "")
        lead_id = odoo_bridge.create_crm_lead(lead_name, contact_name, phone, email)
        if lead_id:
            return json.dumps({"status": "success", "lead_id": lead_id, "message": f"Lead '{lead_name}' berhasil dibuat di Odoo CRM (ID: {lead_id})."})
        else:
            return json.dumps({"status": "error", "message": "Gagal membuat lead di Odoo CRM."})
            
    else:
        return json.dumps({"error": f"Tool '{tool_name}' tidak ditemukan."})

