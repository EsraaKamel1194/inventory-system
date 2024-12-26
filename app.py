from flask import Flask, render_template, request, redirect, url_for
import mysql.connector


app = Flask(__name__)

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="salma",
        database="inventory_system"  
    )
    return connection

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_name = request.form['product-name']
        product_description = request.form['product-description']
        quantity_in_stock = request.form['quantity']
        price = request.form['price']

        connection = get_db_connection()
        cursor = connection.cursor()

    
        query = """
            INSERT INTO products (product_name, product_description, quantity_in_stock, price)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (product_name, product_description, quantity_in_stock, price))
        connection.commit()

        cursor.close()
        connection.close()
        return redirect(url_for('home'))

    return render_template('add.html')


@app.route('/search_order', methods=['POST'])
def search_order():
    order_id = request.form['order_id']
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        SELECT order_id, supplier_id, order_date, total_amount
        FROM purchase_orders
        WHERE order_id = %s
    """
    cursor.execute(query, (order_id,))
    result = cursor.fetchone()

    order = None
    if result:
        order = {
            "order_id": result[0],
            "supplier_id": result[1],
            "order_date": result[2],
            "total_amount": result[3],
        }

    cursor.close()
    connection.close()
    return render_template('indexS.html', order=order)

if __name__ == '__main__':
    app.run(debug=True)
