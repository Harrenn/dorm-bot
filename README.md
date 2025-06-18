# Dorm Bot

A simple Telegram chatbot that tracks dorm expenses for renters. It uses Google
Gemini's 2.5 Flash model with automatic function calling to manage renters,
payments and balance inquiries.

## Features
- Add renters and record when they join the dorm
- Record payments for water, electricity, internet and shared purchases (abono)
- Query balances per renter
- Automatic function calling through Gemini to interpret natural language

## Requirements
- Python 3.11+
- Telegram bot token
- Gemini API key

Install dependencies:
```bash
pip install -r requirements.txt
```

The bot loads environment variables from a `.env` file using `python-dotenv`.

## Environment
Create a `.env` file with:
```
TELEGRAM_BOT_TOKEN=your-telegram-token
GEMINI_API_KEY=your-gemini-key
```

## Usage
Run the bot locally:
```bash
python bot.py
```
The bot will start polling Telegram for new messages. Ask questions like "What is my balance?" or "Record 500 pesos payment for water." Gemini's function calling will map these to database operations.

Database is stored in `dorm.db` for easy backups.
