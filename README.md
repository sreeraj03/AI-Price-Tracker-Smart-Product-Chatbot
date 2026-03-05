# # 🤖 AI Price Tracker – Smart Product Chatbot

AI Price Tracker is a **FastAPI-based chatbot application** that allows users to search, compare, and analyze product prices using natural language queries.
It also includes an **admin panel** to add and manage products stored in a CSV dataset.

The system supports filters like **price, category, location, platform, rating**, and also enables **product comparison**.

---

# 🚀 Features

### 💬 Smart Chatbot

Users can ask questions like:

* `cheapest mobile`
* `mobile under 50000`
* `most rated phone`
* `compare samsung iphone`
* `mobile in kochi amazon`

The chatbot processes the query and returns relevant product results.

---

### 📊 Product Filtering

The chatbot can filter products using:

* Category
* Price range
* Location
* Platform
* Rating

---

### ⭐ Ranking Queries

Supports intelligent ranking queries like:

* Most rated product
* Lowest rated product
* Cheapest product
* Second highest rated product

---

### 📄 Pagination

Large results are automatically divided into pages.

---

### 🔍 Product Comparison

Users can compare products visually with cards showing:

* Price
* Rating
* Platform
* Location

---

### 🛠 Admin Panel

Admins can:

* Add new products
* View all products
* Delete products

---

# 🧠 Tech Stack

Backend:

* **FastAPI**
* **Python**
* **Pandas**

Frontend:

* **HTML**
* **TailwindCSS**
* **JavaScript**

Database:

* **CSV file storage**

---

# 📂 Project Structure

```
AI-Price-Tracker
│
├── main.py               # FastAPI backend
├── products.csv         # Product dataset
│
├── templates
│   ├── chat.html        # Chat interface
│   └── admin.html       # Admin panel
│
├── static               # CSS / JS files
│
└── README.md
```

---

# ⚙ Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/ai-price-tracker.git
cd ai-price-tracker
```

---

### 2️⃣ Install Dependencies

```bash
pip install fastapi uvicorn pandas python-multipart
```

---

### 3️⃣ Run the Server

```bash
uvicorn main:app --reload
```

---

### 4️⃣ Open in Browser

```
http://127.0.0.1:8000
```

---

# 🧪 Example Queries

```
cheapest mobile
mobile under 50000
most rated phone
mobile in kochi amazon
compare samsung iphone
```

---

# 📸 Screenshots

### Chat Interface

Smart chatbot that returns product tables or comparison cards.

### Admin Panel

Add or remove products from the dataset.

---

# 📈 Future Improvements

* AI Natural Language Processing using **OpenAI / LLM**
* Real-time price tracking
* Database integration (PostgreSQL / MongoDB)
* Product recommendation system
* Price history graphs
* User authentication for admin panel

---




