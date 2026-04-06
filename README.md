# 🚀 VRP Dashboard — Vehicle Routing Optimization

<p align="center">
  <b>From theory to application — bringing optimization models to life.</b>
</p>

<p align="center">
  🚚 Logistics Optimization | 📊 Operations Research | ⚡ Interactive Dashboard
</p>

---

## 🌐 Live Demo
🔗 https://vrp-dashboard-q3h5vhhm6ltvyewnp4tqmq.streamlit.app/

---

## 📌 Project Overview
The **VRP Dashboard** is an interactive web application that solves the  
**Capacitated Vehicle Routing Problem (CVRP)** using:

- Clarke-Wright Savings Method  
- Google OR-Tools  
- Streamlit  

It transforms complex optimization models into a **visual and user-friendly tool** for real-world logistics decision-making.

---

## 🎯 Key Capabilities
✔ Optimize delivery routes under capacity constraints  
✔ Reduce total travel distance and cost  
✔ Automatically assign customers to vehicles  
✔ Compare initial vs optimized routing  
✔ Visualize step-by-step solution process  

---

## ⚙️ How It Works

### Step 1 — Initial Routes
Each customer is assigned a separate route:  
`0 → i → 0`

### Step 2 — Savings Calculation
Savings are calculated using:  
`S(i,j) = d(0,i) + d(0,j) - d(i,j)`

### Step 3 — Route Merging
Routes are merged while respecting:
- Vehicle capacity  
- Feasibility constraints  

### Step 4 — Final Optimization
Optimized routes are generated with reduced total cost.

---

## 📊 Example Output
- Initial Cost: 216  
- Final Cost: 101  
- Total Savings: 115  
- Vehicles Used: 2  

---

## 🖥️ Features
- 📂 CSV Upload (Latitude, Longitude, Demand)  
- 🚚 Vehicle Capacity Input  
- 🔢 Number of Vehicles Selection  
- 📊 Real-time Optimization Results  
- 🧠 Step-by-Step Academic Explanation  
- 🎨 Clean and Interactive UI  

---

## 🛠 Tech Stack

| Technology | Purpose |
|----------|--------|
| Python | Core logic |
| Streamlit | Web UI |
| Google OR-Tools | Optimization engine |

---

## 🚀 Run Locally

```bash
git clone https://github.com/YOUR-USERNAME/vrp-dashboard.git
cd vrp-dashboard
pip install -r requirements.txt
streamlit run app.py
