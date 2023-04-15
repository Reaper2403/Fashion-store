import tkinter as tk
import mysql.connector
from tkinter import messagebox

# Connect to the database
mydb = mysql.connector.connect(
    host="localhost",
    user="sqluser",
    password="password",
    database="ananya"
)

# # Connect to the database #Ananya's version
# mydb = mysql.connector.connect(
#     host="localhost",
#     user="sqluser",
#     password="password",
#     database="ananya"
# )

# Connect to the database #Punyam's version
# mydb = mysql.connector.connect(
#     host="Ideaknight",
#     user="epiloger",
#     password="mysql",
#     database="ananya"
# )

root = tk.Tk()
root.title("Inventory Management System")
root.geometry("800x600")
    # Create a cursor to execute the SQL queries
mycursor = mydb.cursor()

def open_billing_window():
    root.withdraw()
    billing_window = tk.Toplevel()
    billing_window.title("Billing")
    billing_window.geometry("800x600")

    cart = []

    def search_product():
        search_query = search_entry.get()
        mycursor.execute("SELECT id, product_name, product_quantity, product_price FROM products WHERE product_name LIKE %s", ("%"+search_query+"%",))
        search_results.delete(0, tk.END)
        for product in mycursor:
            search_results.insert(tk.END, f"{product[1]} (Qty: {product[2]}) - ${product[3]}")

    def add_to_cart():
        selected_indices = search_results.curselection()

        if not selected_indices:
            messagebox.showwarning("Warning", "Please select a product to add to the cart.")
            return

        for index in selected_indices:
            search_results.selection_clear(index)
            product_data = search_results.get(index).split(' ')
            product_name = ' '.join(product_data[:-4])
            product_quantity = int(product_data[-3][:-1])
            product_price = float(product_data[-1][1:])

            if product_quantity > 0:
                cart.append((product_name, 1, product_quantity, product_price))
                update_cart_list()
            else:
                messagebox.showerror("Error", "Insufficient product quantity in the inventory.")

    def update_cart_list():
        cart_list.delete(0, tk.END)
        for product in cart:
            cart_list.insert(tk.END, f"{product[0]} - Quantity: {product[1]} - ${product[3]}")

    def update_product_quantity(product_name, quantity_to_remove):
        mycursor.execute("UPDATE products SET product_quantity = product_quantity - %s WHERE product_name = %s", (quantity_to_remove, product_name))
        mydb.commit()

    def get_total_cost():
        return sum(product[1] * product[3] for product in cart)

    def checkout():
        total_cost = get_total_cost()
        messagebox.showinfo("Total Cost", f"The total cost is ${total_cost:.2f}")

        for product_name, quantity, _, price in cart:
            update_product_quantity(product_name, quantity)

        cart.clear()
        update_cart_list()

    def go_back():
        billing_window.destroy()
        root.deiconify()


    # Search product section
    search_label = tk.Label(billing_window, text="Search Product:")
    search_label.grid(row=0, column=0, padx=10, pady=10)
    search_entry = tk.Entry(billing_window)
    search_entry.grid(row=0, column=1, padx=10, pady=10)
    search_button = tk.Button(billing_window, text="Search", command=search_product)
    search_button.grid(row=0, column=2, padx=10, pady=10)

    # Search results section
    search_results = tk.Listbox(billing_window, width=60, height=10, selectmode=tk.MULTIPLE)
    search_results.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
    add_to_cart_button = tk.Button(billing_window, text="Add to Cart", command=add_to_cart)
    add_to_cart_button.grid(row=2, column=1, padx=10, pady=10)

    # Cart section
    cart_label = tk.Label(billing_window, text="Cart:")
    cart_label.grid(row=3, column=0, padx=10, pady=10)
    cart_list = tk.Listbox(billing_window, width=60, height=10)
    cart_list.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

    # Update quantity section
    def update_quantity():
        selected_index = cart_list.curselection()

        if not selected_index:
            messagebox.showwarning("Warning", "Please select a product to update the quantity.")
            return

        cart_list.selection_clear(selected_index)
        product_name, current_quantity, max_quantity, product_price = cart[selected_index[0]]

        quantity_dialog = tk.Toplevel(billing_window)
        quantity_dialog.geometry("200x100")

        quantity_label = tk.Label(quantity_dialog, text="Enter New Quantity:")
        quantity_label.pack(padx=10, pady=10)
        quantity_entry = tk.Entry(quantity_dialog)
        quantity_entry.pack()

        def update_cart_item():
            new_quantity = int(quantity_entry.get())
            if 0 < new_quantity <= max_quantity:
                cart[selected_index[0]] = (product_name, new_quantity, max_quantity, product_price)
                update_cart_list()
                quantity_dialog.destroy()
            else:
                messagebox.showerror("Error", f"Quantity should be between 1 and {max_quantity}.")

        update_button = tk.Button(quantity_dialog, text="Update Quantity", command=update_cart_item)
        update_button.pack(pady=10)

    update_quantity_button = tk.Button(billing_window, text="Update Quantity", command=update_quantity)
    update_quantity_button.grid(row=5, column=0, padx=10, pady=10)

    # Checkout and go back buttons
    checkout_button = tk.Button(billing_window, text="Checkout", command=checkout)
    checkout_button.grid(row=5, column=1, padx=10, pady=10)
    back_button = tk.Button(billing_window, text="Back", command=go_back)
    back_button.grid(row=5, column=2, padx=10, pady=10)

# Add a button to open the billing window
billing_button = tk.Button(root, text="Billing", command=open_billing_window)
billing_button.pack(side="top", padx=10, pady=10)



def run_store():
    # Create the menu bar
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    # Add the Billing option to the menu bar
    billing_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Billing", menu=billing_menu)
    billing_menu.add_command(label="Open Billing", command=open_billing_window)

    # Create a search function that queries the database for matching products
    def search_products():
        # Clear the previous search results
        for widget in products_frame.winfo_children():
            widget.destroy()

        # Get the search query from the search bar
        search_query = search_entry.get()

        # Execute the SQL query to get matching products
        mycursor.execute("SELECT product_name, product_quantity, product_price FROM products WHERE product_name LIKE %s", ("%"+search_query+"%",))

        # Display the matching products in the products frame
        for i, row in enumerate(mycursor):
            for j, value in enumerate(row):
                product_label = tk.Label(products_frame, text=value, borderwidth=1, relief="solid")
                product_label.grid(row=i+1, column=j) # Start at row 1 to preserve the header row

    # Create a function to add new products to the database
    def add_product():
        # Get the product details from the user
        product_name = name_entry.get()
        product_quantity = int(quantity_entry.get())
        product_price = float(price_entry.get())

        # Execute the SQL query to add the new product to the database
        sql = "INSERT INTO products (product_name, product_quantity, product_price) VALUES (%s, %s, %s)"
        val = (product_name, product_quantity, product_price)
        mycursor.execute(sql, val)
        mydb.commit()

        # Display a message to indicate that the product has been added to the database
        message_label.config(text="Product added to database")

    # Create the main container frame
    main_container = tk.Frame(root)
    main_container.pack(side="top", fill="both", expand=True)

    # Create a frame for adding new products
    add_product_frame = tk.Frame(main_container, width=300, padx=10, pady=10)
    add_product_frame.pack(side="left", fill="both", expand=False)

    # Create a frame for searching products
    search_product_frame = tk.Frame(main_container, width=300, padx=10, pady=10)
    search_product_frame.pack(side="right", fill="both", expand=False)

    # Add labels and entry fields for the product details
    name_label = tk.Label(add_product_frame, text="Product Name:")
    name_label.grid(row=0, column=0, padx=10, pady=10)
    name_entry = tk.Entry(add_product_frame)
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    quantity_label = tk.Label(add_product_frame, text="Product Quantity:")
    quantity_label.grid(row=1, column=0, padx=10, pady=10)
    quantity_entry = tk.Entry(add_product_frame)
    quantity_entry.grid(row=1, column=1, padx=10, pady=10)

    price_label = tk.Label(add_product_frame, text="Product Price:")
    price_label.grid(row=2, column=0, padx=10, pady=10)
    price_entry = tk.Entry(add_product_frame)
    price_entry.grid(row=2, column=1, padx=10, pady=10)
        # Add a button to add the new product to the database
    add_button = tk.Button(add_product_frame, text="Add Product", command=add_product)
    add_button.grid(row=3, column=1, padx=10, pady=10)

    # Add a label to display messages
    message_label = tk.Label(add_product_frame, text="")
    message_label.grid(row=4, column=1, padx=10, pady=10)

    # Create a frame for the search bar and search button
    search_frame = tk.Frame(search_product_frame)
    search_frame.pack(side="top", fill="x")

    # Create a search bar
    search_label = tk.Label(search_frame, text="Search:")
    search_label.pack(side="left")
    search_entry = tk.Entry(search_frame)
    search_entry.pack(side="left")

    # Create a search button
    search_button = tk.Button(search_frame, text="Search", command=search_products)
    search_button.pack(side="left")

    # Create a frame for the matching products
    products_frame = tk.Frame(search_product_frame)
    products_frame.pack(side="top", fill="both", expand=True)

    # Add column headings for the products frame
    tk.Label(products_frame, text="Product Name", borderwidth=1, relief="solid").grid(row=0, column=0, sticky="nsew")
    tk.Label(products_frame, text="Product Quantity", borderwidth=1, relief="solid").grid(row=0, column=1, sticky="nsew")
    tk.Label(products_frame, text="Product Price", borderwidth=1, relief="solid").grid(row=0, column=2, sticky="nsew")


# Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    run_store()
