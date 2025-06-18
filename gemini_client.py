import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from database import add_renter, record_transaction, get_balance

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY not set. Create a .env file with GEMINI_API_KEY=<your-key>"
    )

client = genai.Client(api_key=api_key)

# Declare functions for function calling

def add_renter_fn(name: str, group_name: str | None = None, start_date: str | None = None) -> str:
    add_renter(name, group_name=group_name, start_date=start_date)
    return f"Added renter {name}."


def record_payment_fn(renter: str, typ: str, amount: float, description: str, date: str) -> str:
    record_transaction(renter, typ, amount, description, date)
    return f"Recorded {amount} for {renter} ({typ})."


def get_balance_fn(renter: str) -> str:
    bal = get_balance(renter)
    return f"Balance for {renter} is {bal:.2f}"

FUNCTION_DECLS = [
    types.FunctionDeclaration.from_callable(client=client._api_client, callable=add_renter_fn),
    types.FunctionDeclaration.from_callable(client=client._api_client, callable=record_payment_fn),
    types.FunctionDeclaration.from_callable(client=client._api_client, callable=get_balance_fn),
]


def generate_response(message: str) -> str:
    contents = [
        types.Content(role="user", parts=[types.Part.from_text(text=message)])
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=-1),
        tools=FUNCTION_DECLS,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(),
        response_mime_type="text/plain",
    )
    stream = client.models.generate_content_stream(
        model="gemini-2.5-flash",
        contents=contents,
        config=generate_content_config,
    )
    return "".join(chunk.text for chunk in stream)

