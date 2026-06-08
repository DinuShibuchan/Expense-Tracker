# Rupee Tracker

Rupee Tracker is a simple personal expense tracker web application built to help users manage, audit, and visualize their daily financial transactions in Indian Rupees (₹). It runs entirely in the web browser, saving transaction data locally in the browser's `localStorage` for privacy and offline usability.

---

## 🚀 How to Run Locally

Since the application is built entirely as a static client-side web application, you do not need to install any servers or Python dependencies!

To run the app:
1. Open the repository folder.
2. Double-click the `index.html` file to open it directly in any modern web browser (or run a local development server like Live Server).

---

## 🛠️ Tech Stack

- **Frontend:** HTML5, CSS3, JavaScript (ES6)
- **Charts:** Chart.js (loaded via CDN)
- **Database / Persistence:** Web Storage API (`localStorage`)

---

## 💡 Key Features

- **Add Expense:** Form to input title, amount, category, date (defaults to today), and optional note.
- **View Expenses:** Comprehensive tabular log listing expenses in Indian Rupees (₹), sorted by date (latest first).
- **Delete Expense:** Quick-action delete button for individual entries, protected by a browser confirmation dialog.
- **Filter Log:** Dynamic filters allowing users to search expenses by Category, Date Range (From - To), and/or Month-wise (`YYYY-MM`).
- **Total Calculation:** Real-time summary card compiling overall expenses matching the active filter.
- **Category-wise Summary:** Visual indicators compiling total spend and percentages across the 6 core categories.
- **Pie Chart & Line Graph Visualizations:** Dynamic aggregate charts using Chart.js that update in real-time as you add, delete, or filter expenses.
- **Highest Expense Category Highlight:** A callout banner highlighting the category with the highest spending for the active view.

---

## ⚠️ Data Persistence

- All transaction history is bound strictly to your web browser's `localStorage`.
- Your financial data remains 100% private and offline.
- Clearing your browser cache or site data for this domain will reset the tracker.
