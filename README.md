# Rupee Tracker

Rupee Tracker is a simple personal expense tracker web application built to help users manage, audit, and visualize their daily financial transactions in Indian Rupees (₹). It features a local-first architecture combining a backend server and lightweight storage, complete with multi-criteria logs filtering and dynamic real-time data visualizations.

---

## 🚀 How to Run

Follow these simple steps to set up and run the project locally:

1. **Install Flask:**
   ```bash
   pip install flask
   ```

2. **Run the Application:**
   Navigate to the project root directory and execute the following:
   ```bash
   python app.py
   ```

3. **Open in Browser:**
   Once running, open your web browser and navigate to:
   [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript
- **Charts:** Chart.js (CDN-loaded)

---

## 💡 Design Choices & Tradeoffs

- **Why Flask?**
  Flask was selected for its extreme simplicity, minimal footprint, and rapid development speed. It eliminates boilerplate and configuration overhead, making it ideal for self-contained local web applications.
  *Tradeoff:* Lacks built-in support for enterprise-grade features (e.g. built-in administrative portals or advanced ORMs), which would require additional third-party dependencies if scaled up.

- **Why SQLite?**
  SQLite provides a lightweight, serverless relational database that stores data locally in a single file (`expenses.db`). It requires zero installation or runtime setups.
  *Tradeoff:* It is single-file based and is not suited for highly concurrent multi-user write scenarios; however, it is perfect for single-user local applications.

- **Why Minimal UI?**
  A sleek, framework-free vanilla approach focused purely on functional layouts (forms, logs tables, and card grids) ensures rapid page load times and robust performance without loading heavy CSS or UI packages.
  *Tradeoff:* Developing complex components (like side-by-side grids or custom select elements) must be written from scratch using pure CSS and JS rather than dragging in large component libraries.

---

## ✅ What is Completed

- **Add Expense:** Form to input title, amount, category, date (defaults to today), and optional note, featuring validation check blocks.
- **View Expenses:** Comprehensive tabular log listing expenses in Indian Rupees (₹), sorted by date (latest first).
- **Delete Expense:** Quick-action delete button for individual entries, protected by a browser confirmation dialog.
- **Filter Log:** Dynamic filters allowing users to search expenses by Category, Date Range (From - To), and/or Month-wise (`YYYY-MM`).
- **Total Calculation:** Real-time summary card compiling overall expenses matching the active filter.
- **Category-wise Summary:** Visual indicators compiling total spend and percentages across the 6 core categories.
- **Pie Chart Visualization:** A visual category-wise spending distribution chart using Chart.js, designed with smooth entry rotation animations.
- **Line Graph Visualization:** A visual expense trend chart plotting daily aggregate spending over time using tension-smoothed curves.
- **Highest Expense Category Highlight:** A dedicated callout banner highlighting the category with the highest spending for the active view.

---

## ❌ What is Skipped / Not Implemented

- **Edit/Update Expense:** Modifying an existing expense record directly in place has been skipped for project simplicity.
- **Authentication & Multi-User Support:** Built as a local-first tool for single users; username logs, password encryptions, and sessions are not implemented.
- **Advanced UI Design:** Avoided bloated external component libraries or intricate third-party dashboard packages in order to prioritize rapid utility.
- **Deployment:** Focused strictly on a clean, robust offline-local developer execution server (`localhost`).

---

## ⚠️ Known Limitations

- **Basic UI Styling:** Relies exclusively on core styled Vanilla CSS without dynamic dark/light mode toggles.
- **No Remote Data Persistence:** Transaction history is bound strictly to the local `expenses.db` SQLite database file. Deleting this file will reset the app.
- **Limited Validation:** Basic validation is enforced (amounts `> 0` and non-empty titles); advanced character sanitization or transaction limits are not implemented.
- **Charts Depend on Available Data:** If no data exists or active filters produce empty sets, the analytics block is hidden, displaying a basic fallback placeholder message.
