# 🏦 Bank Queueing Simulation Web App

This is a Queueing Simulation web application built with Python (Flask) and JavaScript. It simulates **customer arrival and wait times** at a bank, using both **single-channel** (one teller) and **multi-channel** (multiple tellers) queueing models.


<img width="930" alt="bss" src="https://github.com/user-attachments/assets/e39c184b-2ce6-433e-a2db-54c6d376bbd5" />


## 📚 Project Description

This project uses a **5-day hourly data case study** to analyze and compare queue wait times in:

- A **single-channel** system (one bank teller).
- A **multi-channel** system (three bank tellers).

The app allows:
- **Automatic data generation** or **manual input** of hourly arrival rates.
- **Dynamic simulation** showing daily breakdown of arrival and wait times.
- **Exporting the results as a PDF report**, organized by each day.

---

## 🎯 Objective

To demonstrate how queueing systems impact customer service delivery in banks. It allows comparison of two common models:
- **Single-line single-server**
- **Single-line multi-server**

The goal is to visualize wait times and help optimize resource allocation.

---

## 🧮 Queueing Theory Concepts Used

- **Arrival Rate (λ)**: Number of customers arriving per hour.
- **Service Rate (μ)**: Fixed in this project as each teller serves 5 customers/hour.
- **Single Channel Queue**: One teller.
- **Multi-Channel Queue**: Three tellers working simultaneously.

---

## 💡 Features

- 📥 Simulate automatically or manually input 60 hourly values (12 hours/day × 5 days).
- 📊 Results displayed in a clean, organized **HTML table** by day.
- 📄 One-click **PDF download** with all 5-day results.
- 📱 Responsive and user-friendly interface.

---



