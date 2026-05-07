from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import requests
from datetime import datetime

app = FastAPI()

# --- API endpoint to fetch BTC data ---
@app.get("/api/btc")
def get_btc_data():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {
        "vs_currency": "usd",
        "days": "30"
    }

    res = requests.get(url, params=params)
    data = res.json()

    prices = data["prices"]

    dates = [
        datetime.fromtimestamp(p[0] / 1000).strftime("%Y-%m-%d")
        for p in prices
    ]
    values = [p[1] for p in prices]

    return JSONResponse({
        "dates": dates,
        "prices": values
    })


# --- Frontend ---
@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Bitcoin Price Tracker</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #0f172a, #1e293b);
            color: #f8fafc;
            text-align: center;
            padding: 30px;
        }
        h1 {
            margin-bottom: 20px;
        }
        .card {
            background: #1e293b;
            border-radius: 16px;
            padding: 20px;
            max-width: 900px;
            margin: auto;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        canvas {
            margin-top: 20px;
        }
        .footer {
            margin-top: 20px;
            opacity: 0.7;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <h1>📈 Bitcoin Price (Last 30 Days)</h1>
    <div class="card">
        <canvas id="chart"></canvas>
    </div>
    <div class="footer">Data from CoinGecko</div>

    <script>
        async function loadChart() {
            const res = await fetch('/api/btc');
            const data = await res.json();

            const ctx = document.getElementById('chart').getContext('2d');

            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.dates,
                    datasets: [{
                        label: 'BTC Price (USD)',
                        data: data.prices,
                        borderColor: '#38bdf8',
                        backgroundColor: 'rgba(56,189,248,0.2)',
                        tension: 0.3,
                        fill: true,
                        pointRadius: 0
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            labels: {
                                color: '#f8fafc'
                            }
                        }
                    },
                    scales: {
                        x: {
                            ticks: { color: '#cbd5f5' }
                        },
                        y: {
                            ticks: { color: '#cbd5f5' }
                        }
                    }
                }
            });
        }

        loadChart();
    </script>
</body>
</html>
"""