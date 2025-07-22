from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect('bill.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS bills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer TEXT NOT NULL,
                items TEXT NOT NULL,
                total REAL NOT NULL
            )
        ''')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_bill():
    customer = request.form['customer']
    items = request.form.getlist('item[]')
    prices = list(map(float, request.form.getlist('price[]')))

    total = sum(prices)
    item_details = ", ".join([f"{items[i]} - ₹{prices[i]}" for i in range(len(items))])

    with sqlite3.connect('bill.db') as conn:
        conn.execute("INSERT INTO bills (customer, items, total) VALUES (?, ?, ?)",
                     (customer, item_details, total))

    return render_template('bill.html', customer=customer, items=item_details, total=total)

@app.route('/bills')
def view_bills():
    with sqlite3.connect('bill.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bills ORDER BY id DESC")
        bills = cursor.fetchall()
    return render_template('view_bills.html', bills=bills)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
