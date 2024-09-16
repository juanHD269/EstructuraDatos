from flask import Flask, render_template, request, redirect, url_for
from collections import deque

app = Flask(__name__)

# Arrays to store products
products = []

# Stack for undo actions
undo_stack = []

# Queue for orders (FIFO)
order_queue = deque()

# List for order history
order_history = []

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Inventory Management
@app.route('/inventory')
def inventory():
    return render_template('inventory.html', products=products)

@app.route('/add_product', methods=['POST'])
def add_product():
    product_name = request.form['product_name']
    product_quantity = int(request.form['product_quantity'])
    
    # Adding product to the inventory (array)
    products.append({'name': product_name, 'quantity': product_quantity})
    
    # Adding the action to the undo stack
    undo_stack.append(('add', {'name': product_name, 'quantity': product_quantity}))
    
    return redirect(url_for('inventory'))

@app.route('/remove_product/<int:index>')
def remove_product(index):
    # Removing product and adding the action to the undo stack
    removed_product = products.pop(index)
    undo_stack.append(('remove', removed_product))
    
    return redirect(url_for('inventory'))

@app.route('/undo')
def undo():
    if undo_stack:
        action, product = undo_stack.pop()
        
        if action == 'add':
            # Undo adding a product
            products.remove(product)
        elif action == 'remove':
            # Undo removing a product
            products.append(product)
    
    return redirect(url_for('inventory'))

# Order Management
@app.route('/orders')
def orders():
    return render_template('orders.html', orders=order_queue)

@app.route('/place_order', methods=['POST'])
def place_order():
    product_name = request.form['product_name']
    quantity = int(request.form['quantity'])
    
    # Creating a new order and adding it to the order queue (FIFO)
    order = {'product_name': product_name, 'quantity': quantity}
    order_queue.append(order)
    
    return redirect(url_for('orders'))

@app.route('/process_order')
def process_order():
    if order_queue:
        # Process order from the front of the queue
        processed_order = order_queue.popleft()
        order_history.append(processed_order)  # Add to order history
        
    return redirect(url_for('orders'))

# Order History
@app.route('/history')
def history():
    return render_template('history.html', history=order_history)

if __name__ == '__main__':
    app.run(debug=True)
