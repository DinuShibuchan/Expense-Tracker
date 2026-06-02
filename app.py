import sqlite3
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
# Secure but simple key for flask flash messages session encryption
app.secret_key = 'expense_tracker_secret_session_key_2026'
DATABASE = 'expenses.db'

# Predefined categories for input validation and classification
CATEGORIES = ['Food', 'Transport', 'Shopping', 'Bills', 'Entertainment', 'Other']

def get_db_connection():
    """Establishes a connection to the SQLite database with Row factory enabled."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database schema if it doesn't already exist."""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            note TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Auto-initialize database on startup
init_db()

@app.route('/')
def index():
    """Main route. Retrieves and summarizes all expenses sorted by date descending."""
    conn = get_db_connection()
    try:
        # Retrieve all expenses sorted by date (latest first) and id descending
        expenses = conn.execute('SELECT * FROM expenses ORDER BY date DESC, id DESC').fetchall()
        
        # Calculate overall total spent
        total_spent = conn.execute('SELECT SUM(amount) FROM expenses').fetchone()[0] or 0.0
        
        # Calculate category-wise total spent (group by category)
        category_totals_raw = conn.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category').fetchall()
        category_totals = {cat: 0.0 for cat in CATEGORIES}
        for row in category_totals_raw:
            if row[0] in category_totals:
                category_totals[row[0]] = row[1]
                
        # Calculate highest spending category
        highest_category = None
        if total_spent > 0:
            max_cat = max(category_totals, key=category_totals.get)
            max_val = category_totals[max_cat]
            if max_val > 0:
                highest_category = {'category': max_cat, 'total': max_val}
                
        # Retrieve date-wise totals ordered by date ascending
        date_totals_raw = conn.execute('SELECT date, SUM(amount) FROM expenses GROUP BY date ORDER BY date').fetchall()
        date_totals = [{'date': row[0], 'total': row[1]} for row in date_totals_raw]
                
    finally:
        conn.close()
        
    return render_template(
        'index.html',
        expenses=expenses,
        total_spent=total_spent,
        category_totals=category_totals,
        categories=CATEGORIES,
        highest_category=highest_category,
        date_totals=date_totals,
        filters=None
    )

@app.route('/add', methods=['POST'])
def add_expense():
    """Handles adding a new expense with thorough server-side validations."""
    title = request.form.get('title', '').strip()
    amount_str = request.form.get('amount', '').strip()
    category = request.form.get('category', '').strip()
    date_str = request.form.get('date', '').strip()
    note = request.form.get('note', '').strip()
    
    errors = []
    
    # 1. Title Validation
    if not title:
        errors.append("Expense title cannot be empty.")
        
    # 2. Amount Validation (> 0 and valid float)
    try:
        amount = float(amount_str)
        if amount <= 0:
            errors.append("Amount must be greater than zero.")
    except ValueError:
        errors.append("Amount must be a valid number.")
        
    # 3. Category Validation
    if category not in CATEGORIES:
        errors.append("Invalid category selected.")
        
    # 4. Date Validation & Graceful Fallback
    # Requirement: Date defaults to today if empty. Gracefully recover from invalid formats.
    if not date_str:
        date_str = datetime.today().strftime('%Y-%m-%d')
    else:
        try:
            # Parse to ensure valid date format
            parsed_date = datetime.strptime(date_str, '%Y-%m-%d')
            date_str = parsed_date.strftime('%Y-%m-%d')
        except ValueError:
            # Graceful recovery: set to today's date if invalid
            date_str = datetime.today().strftime('%Y-%m-%d')
            
    # If any error exists, flash them and redirect back
    if errors:
        for error in errors:
            flash(error, 'error')
        return redirect(url_for('index'))
        
    # Insert new record into database
    conn = get_db_connection()
    try:
        conn.execute(
            'INSERT INTO expenses (title, amount, category, date, note) VALUES (?, ?, ?, ?, ?)',
            (title, amount, category, date_str, note)
        )
        conn.commit()
        flash("Expense added successfully!", "success")
    except Exception as e:
        flash(f"Database error: {str(e)}", "error")
    finally:
        conn.close()
        
    return redirect(url_for('index'))

@app.route('/delete/<int:expense_id>', methods=['GET', 'POST'])
def delete_expense(expense_id):
    """Deletes an expense record based on its ID. Supports GET and POST for convenience."""
    conn = get_db_connection()
    try:
        # Check if record exists
        expense = conn.execute('SELECT id FROM expenses WHERE id = ?', (expense_id,)).fetchone()
        if not expense:
            flash("Expense not found or already deleted.", "error")
        else:
            conn.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
            conn.commit()
            flash("Expense deleted successfully!", "success")
    except Exception as e:
        flash(f"Database error: {str(e)}", "error")
    finally:
        conn.close()
        
    # Smart redirect back to search filters if they were active
    referrer = request.referrer
    if referrer and ('/filter' in referrer or '?' in referrer):
        return redirect(referrer)
    return redirect(url_for('index'))

@app.route('/filter')
def filter_expenses():
    """Filters expenses by category, date range, and/or month. Re-calculates filtered summaries."""
    category = request.args.get('category', '').strip()
    from_date = request.args.get('from_date', '').strip()
    to_date = request.args.get('to_date', '').strip()
    month = request.args.get('month', '').strip()
    
    # Simple base query
    query = "SELECT * FROM expenses WHERE 1=1"
    params = []
    
    # Dynamically build filter clauses
    if category and category != 'All':
        query += " AND category = ?"
        params.append(category)
        
    if from_date:
        query += " AND date >= ?"
        params.append(from_date)
        
    if to_date:
        query += " AND date <= ?"
        params.append(to_date)

    if month:
        parts = month.split('-')
        if len(parts) == 2:
            query += " AND strftime('%Y', date) = ? AND strftime('%m', date) = ?"
            params.extend([parts[0], parts[1]])
        
    # Sort order
    query += " ORDER BY date DESC, id DESC"
    
    conn = get_db_connection()
    try:
        expenses = conn.execute(query, params).fetchall()
        
        # Calculate summary metrics specifically for the FILTERED results
        filtered_total = sum(e['amount'] for e in expenses)
        
        # Calculate category totals based ONLY on filtered items
        category_totals = {cat: 0.0 for cat in CATEGORIES}
        for e in expenses:
            if e['category'] in category_totals:
                category_totals[e['category']] += e['amount']
                
        # Calculate highest spending category on filtered set
        highest_category = None
        if filtered_total > 0:
            max_cat = max(category_totals, key=category_totals.get)
            max_val = category_totals[max_cat]
            if max_val > 0:
                highest_category = {'category': max_cat, 'total': max_val}
                
        # Calculate date-wise totals from filtered items
        date_totals_dict = {}
        for e in expenses:
            d = e['date']
            date_totals_dict[d] = date_totals_dict.get(d, 0.0) + e['amount']
        date_totals = [{'date': d, 'total': amt} for d, amt in sorted(date_totals_dict.items())]
                
    finally:
        conn.close()
        
    # Setup filter status metadata to return to UI
    filters = {
        'category': category,
        'from_date': from_date,
        'to_date': to_date,
        'month': month,
        'is_active': bool((category and category != 'All') or from_date or to_date or month)
    }
    
    return render_template(
        'index.html',
        expenses=expenses,
        total_spent=filtered_total,
        category_totals=category_totals,
        categories=CATEGORIES,
        highest_category=highest_category,
        date_totals=date_totals,
        filters=filters
    )

if __name__ == '__main__':
    # Run the application locally
    app.run(debug=True, port=5000)
