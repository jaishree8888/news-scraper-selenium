# 📰 News Scraper with Selenium Automation

## 📌 Project Overview

This project is a **Flask-based web application** that fetches real-time news articles using the NewsAPI. Users can search for any topic and view relevant news articles in a clean and responsive UI.

The project also includes **Selenium-based automation testing**, making it suitable for QA testing and automation portfolio demonstration.

---

## 🚀 Features

- 🔍 Search news articles by topic
- 🌐 Real-time NewsAPI integration
- 📄 Pagination (Next / Prev results)
- ⚠️ Input validation (empty, invalid, long input)
- 🔁 Search history using localStorage
- 🌙 Dark mode toggle
- 🧪 Selenium automation testing
- 🔗 External article links

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask  
- **Frontend:** HTML, CSS (Jinja templates)  
- **API:** NewsAPI  
- **Testing:** Selenium WebDriver  
- **Environment:** python-dotenv, requests  

---

## 📂 Project Structure
news-scraper/
│
├── app.py # Flask application (routes + UI)
├── scraper.py # NewsAPI fetching logic
├── utils.py # Input validation logic
├── test_web.py # Selenium automation tests
├── test_cases.md # Manual + automation test cases
├── README.md # Project documentation
├── requirements.txt # Dependencies
├── .env.example # API key template


---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-link>
cd news-scraper
2. Install Dependencies
pip install -r requirements.txt
3. Configure Environment Variables

Create a .env file:
API_KEY=your_newsapi_key

4. Run the Application
python app.py

Open in browser:
http://127.0.0.1:5000

🧪 Run Selenium Tests
python test_web.py

🧪 Test Coverage
✔ Functional Testing
Valid topic search
Empty input validation
Invalid character handling
API failure handling

✔ UI Testing
Page load verification
Search bar functionality
News card rendering
Button interactions

✔ Automation Testing (Selenium)
Search execution flow
Error message validation
Pagination testing (Next / Prev)
Search history validation
UI element presence check

⚠️ Edge Cases Handled
Missing API key
API request failure
No results found
Special character input
Very long input handling

Key Highlights:
QA-focused automation project
Selenium test integration
Real-time API-based news fetching
Clean and responsive UI
Strong validation and error handling
Local storage-based search history



👩‍💻 Author
Jaishree Y