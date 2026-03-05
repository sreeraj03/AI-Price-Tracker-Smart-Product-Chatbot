from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import pandas as pd
import os
import re
import math
from typing import Optional

app = FastAPI()

DATA_FILE = "products.csv"
COLUMNS = [
    "Product_ID", "Product_Name", "Category",
    "Price", "Discount", "Final_Price",
    "Rating", "Location", "Platform"
]

# -----------------------------
# CREATE DATASET IF NOT EXISTS
# -----------------------------
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame([
        [1, "iPhone 15", "Mobile", 80000, 10, 72000, 4.8, "Kochi", "Amazon"],
        [2, "Samsung S23", "Mobile", 75000, 5, 71250, 4.6, "Kochi", "Flipkart"],
        [3, "OnePlus 12", "Mobile", 60000, 8, 55200, 4.5, "Bangalore", "Amazon"]
    ], columns=COLUMNS)
    df.to_csv(DATA_FILE, index=False)
else:
    df = pd.read_csv(DATA_FILE)
    # Fix missing columns if needed
    for col in COLUMNS:
        if col not in df.columns:
            if col == "Product_ID":
                df[col] = range(1, len(df) + 1)
            elif col == "Final_Price":
                df[col] = df["Price"] - (df["Price"] * df.get("Discount", 0)/100)
            else:
                df[col] = ""
    df = df[COLUMNS]
    df.to_csv(DATA_FILE, index=False)

def load_data():
    return pd.read_csv(DATA_FILE)

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# -----------------------------
# LANDING PAGE
# -----------------------------
@app.get("/", response_class=HTMLResponse)
def landing():
    return """
    <html>
    <head>
        <title>Smart Product Chatbot</title>
        <style>
            body { font-family: Arial; background:#e5ddd5; text-align:center; padding-top:100px;}
            .button { padding:20px 40px; font-size:20px; margin:20px; border:none; border-radius:10px; cursor:pointer;}
            .chat-btn { background:#4caf50; color:white; }
            .add-btn { background:#2196f3; color:white; }
        </style>
    </head>
    <body>
        <h1>🤖 Smart Product Chatbot</h1>
        <button class="button chat-btn" onclick="window.location.href='/chat_page'">💬 Chat</button>
        <button class="button add-btn" onclick="window.location.href='/add_product_page'">➕ Add Product</button>
    </body>
    </html>
    """

# -----------------------------
# CHAT PAGE
# -----------------------------
@app.get("/chat_page", response_class=HTMLResponse)
def chat_page():
    return render_page("", "", 1)

@app.post("/chat", response_class=HTMLResponse)
def chat(message: Optional[str] = Form(None), page: int = Form(1)):
    message = message or ""
    df = load_data()
    result = df.copy()
    single_mode = False
    query = message.lower().strip()

    # ---------------- SINGLE RESULT LOGIC ----------------
    if "most rated" in query:
        result = df.sort_values(by="Rating", ascending=False).head(1)
        single_mode = True
    elif "lowest rated" in query or "low rated" in query:
        result = df.sort_values(by="Rating", ascending=True).head(1)
        single_mode = True
    elif "second highest" in query:
        result = df.sort_values(by="Rating", ascending=False).iloc[1:2]
        single_mode = True
    elif "cheapest" in query:
        result = df.sort_values(by="Final_Price", ascending=True).head(1)
        single_mode = True

    # ---------------- LOCATION FILTER ----------------
    for loc in df["Location"].str.lower().unique():
        if loc in query:
            result = result[result["Location"].str.lower() == loc]

    # ---------------- CATEGORY FILTER ----------------
    for cat in df["Category"].str.lower().unique():
        if cat in query:
            result = result[result["Category"].str.lower() == cat]

    # ---------------- PLATFORM FILTER ----------------
    for plat in df["Platform"].str.lower().unique():
        if plat in query:
            result = result[result["Platform"].str.lower() == plat]

    # ---------------- PRICE FILTER ----------------
    under = re.search(r'under\s*(\d+)', query)
    if under:
        price = int(under.group(1))
        result = result[result["Final_Price"] < price]

    # ---------------- PAGINATION ----------------
    if not single_mode:
        page_size = 3
        total = len(result)
        total_pages = max(1, math.ceil(total / page_size))
        start = (int(page) - 1) * page_size
        end = start + page_size
        result = result.iloc[start:end]
    else:
        total_pages = 1

    # ---------------- OUTPUT ----------------
    if result.empty:
        output = "❌ No matching products found."
    else:
        output = result.to_html(index=False)

    return render_page(message, output, total_pages)

# -----------------------------
# ADD PRODUCT PAGE
# -----------------------------
@app.get("/add_product_page", response_class=HTMLResponse)
def add_product_page():
    return render_add_page("")

@app.post("/add_product", response_class=HTMLResponse)
def add_product(
    add_name: str = Form(...),
    add_category: str = Form(...),
    add_price: float = Form(...),
    add_discount: float = Form(...),
    add_rating: float = Form(...),
    add_location: str = Form(...),
    add_platform: str = Form(...)
):
    df = load_data()
    new_id = int(df["Product_ID"].max()) + 1
    final_price = add_price - (add_price * add_discount / 100)
    new_row = {
        "Product_ID": new_id,
        "Product_Name": add_name,
        "Category": add_category,
        "Price": add_price,
        "Discount": add_discount,
        "Final_Price": final_price,
        "Rating": add_rating,
        "Location": add_location,
        "Platform": add_platform
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_data(df)
    output = f"✅ Product '{add_name}' added successfully."
    return render_add_page(output)

# -----------------------------
# RENDER FUNCTIONS
# -----------------------------
def render_page(message, output, total_pages):
    pagination = ""
    if total_pages > 1:
        pagination += "<div style='margin-top:15px;'>Pages: "
        for p in range(1, total_pages + 1):
            pagination += f"""
            <form method="post" action="/chat" style="display:inline;">
                <input type="hidden" name="message" value="{message}">
                <input type="hidden" name="page" value="{p}">
                <button>{p}</button>
            </form>
            """
        pagination += "</div>"

    return f"""
    <html>
    <head>
        <title>Chat</title>
        <style>
            body {{ font-family: Arial; background: #e5ddd5; }}
            .chat-container {{ width: 60%; margin: 30px auto; background: white; padding: 20px; border-radius: 10px; }}
            .user {{ text-align: right; margin: 10px; }}
            .bot {{ text-align: left; margin: 10px; }}
            .bubble-user {{ background: #dcf8c6; padding: 10px; border-radius: 10px; display: inline-block; }}
            .bubble-bot {{ background: #f1f0f0; padding: 10px; border-radius: 10px; display: inline-block; width: 100%; }}
            table {{ width:100%; border-collapse: collapse; margin-top:10px; }}
            th, td {{ border:1px solid #ddd; padding:8px; text-align:center; }}
            th {{ background:#333; color:white; }}
            input {{ width:75%; padding:10px; margin:3px 0; }}
            button {{ padding:8px 12px; margin:3px; }}
            hr {{ margin:20px 0; border:1px solid #ccc; }}
        </style>
    </head>
    <body>
        <div class="chat-container">
            <h2>💬 Chat</h2>
            {f'<div class="user"><div class="bubble-user">{message}</div></div>' if message else ''}
            {f'<div class="bot"><div class="bubble-bot">{output}{pagination}</div></div>' if output else ''}
            <form method="post" action="/chat">
                <input type="text" name="message" placeholder="Ask something...">
                <input type="hidden" name="page" value="1">
                <button type="submit">Send</button>
            </form>
        </div>
    </body>
    </html>
    """

def render_add_page(output):
    return f"""
    <html>
    <head>
        <title>Add Product</title>
        <style>
            body {{ font-family: Arial; background: #e5ddd5; }}
            .chat-container {{ width: 60%; margin: 30px auto; background: white; padding: 20px; border-radius: 10px; }}
            input {{ width:75%; padding:10px; margin:3px 0; }}
            button {{ padding:8px 12px; margin:3px; }}
            hr {{ margin:20px 0; border:1px solid #ccc; }}
        </style>
    </head>
    <body>
        <div class="chat-container">
            <h2>➕ Add Product</h2>
            {f'<p>{output}</p>' if output else ''}
            <form method="post" action="/add_product">
                <input type="text" name="add_name" placeholder="Product Name" required>
                <input type="text" name="add_category" placeholder="Category" required>
                <input type="number" name="add_price" placeholder="Price" step="0.01" required>
                <input type="number" name="add_discount" placeholder="Discount %" step="0.01" required>
                <input type="number" name="add_rating" placeholder="Rating" step="0.1" required>
                <input type="text" name="add_location" placeholder="Location" required>
                <input type="text" name="add_platform" placeholder="Platform" required>
                <button type="submit">Add Product</button>
            </form>
        </div>
    </body>
    </html>
    """