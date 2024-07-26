import pandas as pd

# Sample Data
products = pd.DataFrame({
    'product_id': [1, 2, 3],
    'name': ['Product A', 'Product B', 'Product C'],
    'category': ['Category 1', 'Category 2', 'Category 1'],
    'price': [10.0, 20.0, 30.0],
    'lead_time': [5, 7, 3]
})

warehouses = pd.DataFrame({
    'warehouse_id': [1, 2],
    'location': ['Location 1', 'Location 2']
})

stock_levels = pd.DataFrame({
    'product_id': [1, 1, 2, 3],
    'warehouse_id': [1, 2, 1, 2],
    'stock_level': [100, 50, 75, 30]
})

sales_data = pd.DataFrame({
    'product_id': [1, 1, 2, 3, 1],
    'sales_date': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-01', '2024-01-02', '2024-01-03']),
    'quantity_sold': [5, 10, 7, 3, 6]
})

# Function to Display Current Stock Levels
def display_stock(product_id):
    stock = stock_levels[stock_levels['product_id'] == product_id]
    return stock

# Function to Check Low Stock Levels
def check_stock_levels(threshold):
    low_stock = stock_levels[stock_levels['stock_level'] < threshold]
    return low_stock

# Function to Calculate Reorder Point
def calculate_reorder_point(product_id, lead_time, safety_stock):
    sales = sales_data[sales_data['product_id'] == product_id]
    avg_daily_sales = sales['quantity_sold'].mean()
    reorder_point = avg_daily_sales * lead_time + safety_stock
    return reorder_point

# Function to Calculate Order Quantity
def calculate_order_quantity(product_id, reorder_point, current_stock):
    if current_stock < reorder_point:
        order_quantity = reorder_point - current_stock
        return order_quantity
    return 0

# Function to Calculate Inventory Turnover Rate
def calculate_turnover_rate(product_id):
    total_sales = sales_data[sales_data['product_id'] == product_id]['quantity_sold'].sum()
    avg_stock = stock_levels[stock_levels['product_id'] == product_id]['stock_level'].mean()
    turnover_rate = total_sales / avg_stock if avg_stock > 0 else 0
    return turnover_rate

# Function to Calculate Stockout Occurrences
def stockout_occurrences(product_id, threshold):
    stock = stock_levels[(stock_levels['product_id'] == product_id) & (stock_levels['stock_level'] < threshold)]
    return len(stock)

# Function to Calculate Cost Implications of Overstock
def cost_implications(product_id):
    overstock = stock_levels[(stock_levels['product_id'] == product_id) & (stock_levels['stock_level'] > 100)]
    cost = overstock['stock_level'].sum() * products[products['product_id'] == product_id]['price'].values[0]
    return cost

# User Interface Function
def user_interface():
    while True:
        print("\n1. View Stock Levels")
        print("2. Check Reorder Recommendations")
        print("3. Generate Reports")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            product_id = int(input("Enter Product ID: "))
            print(display_stock(product_id))
        elif choice == '2':
            product_id = int(input("Enter Product ID: "))
            threshold = int(input("Enter Reorder Threshold: "))
            current_stock = stock_levels[stock_levels['product_id'] == product_id]['stock_level'].sum()
            reorder_point = calculate_reorder_point(product_id, products[products['product_id'] == product_id]['lead_time'].values[0], 10)
            print(f"Reorder Point: {reorder_point}")
            print(f"Order Quantity: {calculate_order_quantity(product_id, reorder_point, current_stock)}")
        elif choice == '3':
            print("1. Inventory Turnover Rate")
            print("2. Stockout Occurrences")
            print("3. Cost Implications")
            report_choice = input("Enter report choice: ")
            product_id = int(input("Enter Product ID: "))
            if report_choice == '1':
                print(calculate_turnover_rate(product_id))
            elif report_choice == '2':
                threshold = int(input("Enter Threshold: "))
                print(stockout_occurrences(product_id, threshold))
            elif report_choice == '3':
                print(cost_implications(product_id))
        elif choice == '4':
            break
        else:
            print("Invalid choice")

# Run the user interface
user_interface()
