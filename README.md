# 📈 Stock Trading Simulator

An interactive stock trading simulator that empowers users to learn market dynamics and trading strategies using **virtual currency**—all in a risk-free environment. Users can buy/sell mock stocks based on **real or delayed stock market data**, track portfolio performance, view transaction history, and compete on a **global leaderboard**.

## 🚀 Features

* 🏦 **Virtual Trading**: Trade with mock money based on real or delayed stock market data.
* 📊 **Portfolio Tracker**: Visual breakdown of assets, net worth, and holdings.
* 📈 **Real-Time/Delayed Market Data**: Integrated via external stock APIs (e.g., Twelve Data, Finnhub).
* 📜 **Transaction History**: Logs of buys, sells, prices, and time of trade.
* 💹 **Profit/Loss Calculation**: Instant feedback on individual trades and overall portfolio.
* 🏆 **Leaderboard**: Compete with others and climb the rankings.
* 📉 **Data Visualizations**: Graphs and charts for trends, holdings, and performance.

---

## 🧠 Why This Matters

This project simulates a real-world trading platform with educational value, combining **financial literacy**, **data engineering**, and **web development**. It’s ideal for those looking to understand the **stock market**, build **fintech apps**, or practice **API integration and data visualization**.

---

## 🔧 Tech Stack

| Layer              | Tools Used                                                                                |
| ------------------ | ----------------------------------------------------------------------------------------- |
| **Frontend**       | HTML + CSS + Bootstrap, Jinjja2 for templating                                                |
| **Backend**        | Flask                                                                  |
| **APIs**           | [Trading View](https://www.tradingview.com/), [Finnhub](https://finnhub.io/) |
| **Database**       | SQLite / SQLAlchemy                                                             |
| **Deployment**     | Netlify
---

## 🛠️ Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/VaishnaviBhosalee/StockTradeSimulator.git
   cd StockTradeSimulator
   ```

2. **Set up environment**

   * Create a `.env` file and add your API keys:

     ```
     FINNHUB_KEY=your_api_key
     ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt  # for Flask backend)
   ```

4. **Run the project**

   ```bash
   flask run        # Backend
   ```

---

## 📌 Usage

* **Sign Up / Log In** to your account
* Get free virtual currency (e.g., \$100,000)
* Use the **Search** bar to find stocks
* Click **Buy** or **Sell** and confirm transaction
* View your **portfolio dashboard**, **trade history**, and **leaderboard position**

---

## 🔐 Security Considerations

* Prevent over-buying or invalid trades
* Sanitize all user inputs
* Secure API keys using environment variables

---
