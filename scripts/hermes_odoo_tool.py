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
