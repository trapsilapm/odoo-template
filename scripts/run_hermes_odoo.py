import os
import sys
import logging
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from openai import OpenAI
from hermes_odoo_tool import HERMES_ODOO_TOOLS, execute_odoo_tool

# Setup Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger("HermesOdooAgent")

# Load Configurations
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "deepseek").lower()

# DeepSeek / OpenAI Configurations
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY") or os.getenv("LLM_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

SYSTEM_PROMPT = """Anda adalah Hermes AI Assistant khusus untuk Odoo ERP Perusahaan.
Tugas Anda adalah membantu pengguna/tim bisnis untuk:
1. Mengecek sisa stok dan harga barang di Odoo gudang.
2. Memberikan ringkasan omset penjualan dan transaksi dari Odoo.
3. Mencatat prospek/lead calon pelanggan baru ke Odoo CRM.

Gunakan tool function yang tersedia ketika user menanyakan stok, omset, atau meminta pembuatan lead CRM.
Anda terisolasi penuh hanya untuk data Odoo ERP. Jawablah dengan ringkas, ramah, dan profesional dalam Bahasa Indonesia."""

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler /start command"""
    welcome_msg = (
        "👋 **Selamat datang di Hermes Agent for Odoo ERP! (Powered by DeepSeek AI)**\n\n"
        "Saya adalah asisten AI terisolasi khusus untuk sistem Odoo Anda.\n"
        "Anda dapat bertanya kepada saya tentang:\n"
        "• 📦 Cek stok barang (Contoh: *Cek stok laptop*)\n"
        "• 📊 Omset penjualan (Contoh: *Berapa omset penjualan hari ini?*)\n"
        "• 👤 Input CRM Lead (Contoh: *Buatkan lead baru Pak Eko HP 08123456789*)\n"
    )
    await update.message.reply_text(welcome_msg, parse_mode='Markdown')

def process_llm_with_deepseek(user_message: str):
    """Proses query LLM menggunakan DeepSeek API (OpenAI Compatible) + Tool Calling"""
    if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY == "your_deepseek_api_key_here":
        return "⚠️ `DEEPSEEK_API_KEY` belum dikonfigurasi di file `.env` VPS. Silakan masukkan API Key DeepSeek Anda."

    try:
        client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL
        )

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ]

        # Call DeepSeek API with function tools
        response = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=messages,
            tools=HERMES_ODOO_TOOLS,
            tool_choice="auto"
        )

        response_message = response.choices[0].message

        # Cek jika DeepSeek memanggil Tool Function
        if response_message.tool_calls:
            messages.append(response_message)
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                logger.info(f"DeepSeek Triggered Tool: {function_name} with args: {function_args}")
                tool_output = execute_odoo_tool(function_name, function_args)
                
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": tool_output,
                })

            # Re-call DeepSeek untuk merangkum hasil function call
            second_response = client.chat.completions.create(
                model=DEEPSEEK_MODEL,
                messages=messages
            )
            return second_response.choices[0].message.content

        return response_message.content

    except Exception as e:
        logger.error(f"Error DeepSeek LLM processing: {e}")
        return f"Mohon maaf, terjadi kendala saat memproses permintaan via DeepSeek API: {str(e)}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler pesan teks pengguna"""
    user_text = update.message.text
    logger.info(f"Received Telegram message: {user_text}")

    # Kirim status mengetik di Telegram
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # Dapatkan jawaban dari DeepSeek LLM
    response_text = process_llm_with_deepseek(user_text)
    await update.message.reply_text(response_text)

def main():
    if not TELEGRAM_TOKEN or TELEGRAM_TOKEN == "your_telegram_bot_token_here":
        logger.warning("TELEGRAM_BOT_TOKEN belum diset di .env. Hermes Agent akan beroperasi dalam mode IDLE.")
        print("💡 Masukkan TELEGRAM_BOT_TOKEN di .env VPS lalu restart container.")
        sys.exit(0)

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    logger.info("🤖 Hermes Agent for Odoo (DeepSeek API + Telegram Bot) is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
