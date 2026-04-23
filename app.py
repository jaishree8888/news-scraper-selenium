from flask import Flask, request, render_template_string
from scraper import fetch_articles
from utils import validate_topic
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Article Finder</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <style>
        body {
            margin:0;
            font-family:'Segoe UI';
            background:#f5f7fb;
            text-align:center;
        }

        .navbar {
           background:#1e293b;
           color:white;
           padding:15px 30px;

           display:flex;
           justify-content:space-between;  /* pushes items apart */
           align-items:center;
        }

        .navbar button {
            background:#334155;
            border-radius:6px;
        }

        .container {
            max-width:900px;
            margin:40px auto;
        }

        .search-box {
            display:flex;
            justify-content:center;
            gap:10px;
            margin-bottom:20px;
        }

        input {
            width:60%;
            padding:12px;
            border-radius:8px;
            border:1px solid #ccc;
            font-size:16px;
        }

        button {
            padding:12px 20px;
            background:#2563eb;
            color:white;
            border:none;
            border-radius:8px;
            cursor:pointer;
        }

        button:hover {
            background:#1d4ed8;
        }

        .history {
            margin-bottom:20px;
        }

        .history button {
            margin:5px;
            padding:6px 10px;
            background:#e2e8f0;
            color:black;
        }

        .error {
            background:#fee2e2;
            color:#b91c1c;
            padding:10px;
            border-radius:6px;
            margin-bottom:15px;
        }

        .status {
            background:#e0f2fe;
            padding:10px;
            border-radius:6px;
            margin-bottom:20px;
        }

        .grid {
            display:grid;
            grid-template-columns:1fr;
            gap:20px;
        }

        .card {
            background:white;
            padding:20px;
            border-radius:10px;
            box-shadow:0 5px 15px rgba(0,0,0,0.1);
            text-align:left;
        }

        .card a {
            color:#2563eb;
            font-weight:bold;
        }

        /* Pagination */
        .pagination {
            margin-top:30px;
            display:flex;
            justify-content:center;
            gap:20px;
        }

        /* Dark mode */
        .dark {
            background:#0f172a;
            color:white;
        }

        .dark .card {
            background:#1e293b;
        }

        .dark input {
            background:#1e293b;
            color:white;
            border:1px solid #475569;
        }

    </style>

<script>
function toggleDarkMode() {
    document.body.classList.toggle("dark");
}

function saveSearch() {
    let topic = document.querySelector('[name="topic"]').value;
    if(!topic) return;

    let history = JSON.parse(localStorage.getItem("history")) || [];

    if(!history.includes(topic)) history.unshift(topic);
    if(history.length>5) history.pop();

    localStorage.setItem("history", JSON.stringify(history));
}

function loadHistory() {
    let history = JSON.parse(localStorage.getItem("history")) || [];
    let div = document.getElementById("history");

    div.innerHTML = "";

    history.forEach(item=>{
        let btn=document.createElement("button");
        btn.innerText=item;
        btn.onclick=()=>document.querySelector('[name="topic"]').value=item;
        div.appendChild(btn);
    });
}

window.onload = loadHistory;
</script>

</head>

<body>

<div class="navbar">
    <h2>Article Finder🔎</h2>
    <div>
        <button onclick="toggleDarkMode()">🌙</button>
    </div>
</div>

<div class="container">

<form method="POST" onsubmit="saveSearch()">

<div class="search-box">
<input name="topic" placeholder="Search global news..." required>
<button>Search</button>
</div>

<div id="history" class="history"></div>

<input type="hidden" name="page" value="{{page}}">

</form>

{% if error %}
<div class="error">{{error}}</div>
{% endif %}

{% if articles %}
<div class="status">{{total}} results found</div>

<div class="grid">
{% for a in articles %}
<div class="card">
<h3>{{a.title}}</h3>
<p>{{a.description}}</p>
<a href="{{a.url}}" target="_blank">Read more →</a>
</div>
{% endfor %}
</div>

<div class="pagination">

<form method="POST">
<input type="hidden" name="topic" value="{{topic}}">
<input type="hidden" name="page" value="{{page-1}}">
<button {% if page<=1 %}disabled{% endif %}>⬅ Prev</button>
</form>

<form method="POST">
<input type="hidden" name="topic" value="{{topic}}">
<input type="hidden" name="page" value="{{page+1}}">
<button>Next ➡</button>
</form>

</div>

{% endif %}

</div>

</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def home():
    articles=[]
    error=None
    page=1
    total=0

    if request.method=="POST":
        topic=request.form.get("topic")
        date=request.form.get("date")
        page=int(request.form.get("page",1))

        valid,msg=validate_topic(topic)
        if not valid:
            error=msg
        elif not API_KEY:
            error="API key missing"
        else:
            try:
                all_articles=fetch_articles(topic,API_KEY,date)
                total=len(all_articles)
                start=(page-1)*5
                end=start+5
                articles=all_articles[start:end]

                if not articles:
                    error="No results"

            except Exception as e:
                error=str(e)

    return render_template_string(
        HTML_TEMPLATE,
        articles=articles,
        error=error,
        page=page,
        total=total,
        topic=request.form.get("topic","")
    )

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)