import tkinter as tk
from PIL import ImageTk, Image
import mysql.connector
from tkinter import messagebox

mydb = mysql.connector.connect(
    host="Ideaknight",
    user="epiloger",
    password="mysql",
    database="ananya"
)

root = tk.Tk()
root.title("Inventory Management System")
root.state("zoomed")
# Create a cursor to execute the SQL queries
mycursor = mydb.cursor()

def open_billing_window():
    # root.withdraw()
    # billing_window = tk.Toplevel()
    # billing_window.title("Billing")
    # billing_window.geometry("800x600")

    for widget in billing_window.winfo_children():
        widget.destroy()
    billing_window.pack_forget()

    for widget in main_container.winfo_children():
        widget.destroy()
    main_container.pack_forget()

    billing_window.pack(side="top", fill="both", expand=True)

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

    # def go_back():
    #     billing_window.destroy()
    #     root.deiconify()

    # Create a frame for adding new products
    cart_frame = tk.LabelFrame(billing_window, text="Cart", width=300)
    # cart_frame.pack(side="right", fill="both", padx=(5,10), pady=10, expand=True)
    cart_frame.pack(side="right", fill="both", ipadx=10, padx=20, pady=5, expand=True)

    # Create a frame for searching products
    shopping_frame = tk.LabelFrame(billing_window, text="Shopping Zone")
    # shopping_frame.pack(side="left", fill="both", padx=(10,5), pady=10)
    shopping_frame.pack(side="left", fill="both", ipadx=10, padx=20, pady=5, expand=True)

    # Create a frame for the search bar and search button
    search_frame = tk.Frame(shopping_frame)
    search_frame.pack(side="top", anchor="w", pady=10)

    # Create a search bar
    search_label = tk.Label(search_frame, text="lookup:", font=('Arial', 20))
    search_label.pack(side="left", padx=20)
    search_entry = tk.Entry(search_frame, width=15, font=('Arial', 20))
    search_entry.pack(side="left", fill="x", anchor="center", padx=10)

    # Create a search button
    search_button = tk.Button(search_frame, text="Search", command=search_product, width=15, font=('Arial', 15))
    search_button.pack(side="left", anchor="center", padx=20)

    # Search product section
    # search_label = tk.Label(billing_window, text="Search Product:")
    # search_label.grid(row=0, column=0, padx=10, pady=10)
    # search_entry = tk.Entry(billing_window)
    # search_entry.grid(row=0, column=1, padx=10, pady=10)
    # search_button = tk.Button(billing_window, text="Search", command=search_product)
    # search_button.grid(row=0, column=2, padx=10, pady=10)

    # Search results section
    search_results = tk.Listbox(shopping_frame, width=40, height=15, selectmode=tk.MULTIPLE, font=('Arial', 15))
    # search_results.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
    search_results.pack(side="left", anchor="ne", padx=(20,10), pady=50)
    add_to_cart_button = tk.Button(shopping_frame, text="Add to Cart\n>>", command=add_to_cart, font=('Arial', 15))
    add_to_cart_button.pack(side="top", fill="x", padx=10, ipadx=5, pady=50)
    # add_to_cart_button.grid(row=2, column=1, padx=10, pady=10)

    # Cart section
    cart_inner_frame=tk.Frame(cart_frame)
    cart_inner_frame.pack(side="top", anchor="center")

    cart_label = tk.Label(cart_inner_frame, text="CART", width=20, font=('Arial', 17))
    cart_label.grid(row=3, column=0, columnspan=3 , ipady=10, ipadx=20)
    cart_list = tk.Listbox(cart_inner_frame, width=60, height=10)
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

    update_quantity_button = tk.Button(cart_inner_frame, text="Update Quantity", command=update_quantity, font=('Arial', 15))
    update_quantity_button.grid(row=5, column=0, ipadx=10, pady=10)

    # Checkout and go back buttons
    checkout_button = tk.Button(cart_inner_frame, text="Checkout", command=checkout, font=('Arial', 15))
    checkout_button.grid(row=5, column=1, ipadx=10, pady=10)
    # back_button = tk.Button(cart_inner_frame, text="Back", command=go_back)
    # back_button.grid(row=5, column=2, padx=10, pady=10)

def run_store():

    for widget in main_container.winfo_children():
        widget.destroy()
    main_container.pack_forget()
    
    for widget in billing_window.winfo_children():
        widget.destroy()
    billing_window.pack_forget()
    
    # Create a search function that queries the database for matching products
    def search_products():
        # Clear the previous search results
        for widget in products_frame.winfo_children():
            widget.destroy()

        tk.Label(products_frame, text="Product Name", borderwidth=1, relief="solid", font=('Arial', 15)).grid(row=0, column=0, sticky="nsew", ipady=10, ipadx=5, padx=1, pady=1)
        tk.Label(products_frame, text="Product Quantity", borderwidth=1, relief="solid", font=('Arial', 15)).grid(row=0, column=1, sticky="nsew", ipady=10, ipadx=5, padx=1, pady=1)
        tk.Label(products_frame, text="Product Price", borderwidth=1, relief="solid", font=('Arial', 15)).grid(row=0, column=2, sticky="nsew", ipady=10, ipadx=5, padx=1, pady=1)

        # Get the search query from the search bar
        search_query = search_entry.get()

        # Execute the SQL query to get matching products
        mycursor.execute("SELECT product_name, product_quantity, product_price FROM products WHERE product_name LIKE %s", ("%"+search_query+"%",))

        # Display the matching products in the products frame
        for i, row in enumerate(mycursor):
            for j, value in enumerate(row):
                # tk.Label(products_frame, text="Product Name", borderwidth=1, relief="solid", font=('Arial', 15)).grid(row=0, column=0, sticky="nsew", ipadx=5, padx=1, pady=1)
                product_label = tk.Label(products_frame, text=value, borderwidth=1, relief="solid", font=('Arial', 15), wraplength=250)
                product_label.grid(row=i+1, column=j, sticky="nsew", ipadx=5, padx=1, pady=1) # Start at row 1 to preserve the header row
                # .grid(row=0, column=0, sticky="nsew", ipadx=5, padx=1, pady=1)

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
    # main_container = tk.Frame(root)
    main_container.pack(fill="x")

    # Create a frame for adding new products
    add_product_frame = tk.LabelFrame(main_container, text="Add Products", width=300, pady=10)
    add_product_frame.pack(side="right", fill="both", ipadx=10, padx=20, expand=True)

    # Create a frame for searching products
    search_product_frame = tk.LabelFrame(main_container, text="Search Products", width=300, pady=10)
    search_product_frame.pack(side="left", fill="both", ipadx=10, padx=20, expand=True)

    # Add labels and entry fields for the product details
    name_frame=tk.Frame(add_product_frame)
    name_label = tk.Label(name_frame, text="Product Name:", width=20, font=('Arial', 20), justify="left")
    name_label.pack(side="left", fill="x", pady=20, anchor="w")
    name_entry = tk.Entry(name_frame, width=20, font=('Arial', 20))
    name_entry.pack(side="right", fill="x", pady=20)
    name_frame.pack()
    
    quantity_frame=tk.Frame(add_product_frame)
    quantity_label = tk.Label(quantity_frame, text="Product Quantity:", width=20, font=('Arial', 20), justify="left")
    quantity_label.pack(side="left", fill="x", pady=20, anchor="w")
    quantity_entry = tk.Entry(quantity_frame, width=20, font=('Arial', 20))
    quantity_entry.pack(side="right", fill="x", pady=20)
    quantity_frame.pack()

    price_frame=tk.Frame(add_product_frame)
    price_label = tk.Label(price_frame, text="Product Price:", width=20, font=('Arial', 20), justify="left")
    price_label.pack(side="left", fill="x", pady=20, anchor="w")
    price_entry = tk.Entry(price_frame, width=20, font=('Arial', 20))
    price_entry.pack(side="right", fill="x", pady=20)
    price_frame.pack()

    # Add a button to add the new product to the database
    add_button = tk.Button(add_product_frame, text="Add Product", command=add_product, font=('Arial', 20))
    add_button.pack()
    # add_button.grid(row=3, column=1, padx=10, pady=10)

    # Add a label to display messages
    message_label = tk.Label(add_product_frame, text="")
    message_label.pack()
    # message_label.grid(row=4, column=1, padx=10, pady=10)

    # Create a frame for the search bar and search button
    search_frame = tk.Frame(search_product_frame)
    search_frame.pack(side="top", fill="x")

    # Create a search bar
    search_label = tk.Label(search_frame, text="Search:", width=10, font=('Arial', 15))
    search_label.pack(side="left", fill="x", anchor="center", padx=20)
    search_entry = tk.Entry(search_frame, width=20, font=('Arial', 15))
    search_entry.pack(side="left", fill="x", anchor="center", padx=20)

    # Create a search button
    search_button = tk.Button(search_frame, text="Search", command=search_products, width=15, font=('Arial', 15))
    search_button.pack(side="left", fill="x", anchor="center", padx=20)

    # Create a frame for the matching products
    products_frame = tk.Frame(search_product_frame)
    products_frame.pack(side="top", fill="both", expand=True, pady=(20,30), padx=30)

    # Add column headings for the products frame
    tk.Label(products_frame, text="Product Name", borderwidth=1, relief="solid", font=('Arial', 15)).grid(row=0, column=0, sticky="nsew", ipady=10, ipadx=5, padx=1, pady=1)
    tk.Label(products_frame, text="Product Quantity", borderwidth=1, relief="solid", font=('Arial', 15)).grid(row=0, column=1, sticky="nsew", ipady=10, ipadx=5, padx=1, pady=1)
    tk.Label(products_frame, text="Product Price", borderwidth=1, relief="solid", font=('Arial', 15)).grid(row=0, column=2, sticky="nsew", ipady=10, ipadx=5, padx=1, pady=1)

    # product_label = tk.Label(products_frame, text="\n\n\n\n", borderwidth=1, relief="solid", font=('Arial', 15), wraplength=250)
    # product_label.grid(row=i+1, column=j, sticky="nsew", ipadx=5, padx=1, pady=1)
    for j in range(3):
        product_label = tk.Label(products_frame, text="\n\n--xx--\n\n", borderwidth=1, relief="solid", font=('Arial', 15), wraplength=250)
        product_label.grid(row=1, column=j, sticky="nsew", ipadx=5, padx=1, pady=1)
    # for i in range(10):
    #     for j in range(3):
    #         product_label = tk.Label(products_frame, text="    ", borderwidth=1, relief="solid", font=('Arial', 15), wraplength=250)
    #         product_label.grid(row=i+1, column=j, sticky="nsew", ipadx=5, padx=1, pady=1)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":

    # Create the side bar
    Side_bar = tk.Frame(root, width=200, height=350, bg='white', highlightthickness=2)#border=1, borderwidth=10)
    Side_bar.pack(side="left", fill="y")

    #Sidebar Image
    img = Image.open('profile.png')
    img = img.resize((80, 80), Image.LANCZOS)
    my_img = ImageTk.PhotoImage(img)
    my_label = tk.Label(Side_bar, image=my_img, background="white", text="Labl")
    my_label.pack(side="top", fill="x", pady=(5,10))#.pack(side=LEFT, padx=15, pady=15, fill=X)

    # Add a button to open the products window
    product_button = tk.Button(Side_bar, width=10, text="Products", command=run_store, borderwidth=1, relief="solid", font=('Arial', 12))
    product_button.pack(side="top", fill="x", pady=2, ipady=2)

    # Add a button to open the billing window
    billing_button = tk.Button(Side_bar, width=10, text="Billing", command=open_billing_window, borderwidth=1, relief="solid", font=('Arial', 12))
    billing_button.pack(side="top", fill="x", pady=5, ipady=2)

    # Logout button
    # leaveimage = Image.open('leave.png')
    # leaveimage = leaveimage.resize((30, 30), Image.LANCZOS)
    # my_img = ImageTk.PhotoImage(img)
    # leaveimage = ImageTk.PhotoImage(file='leave.png', size=(30,30))
    # main_button = Button(root, image=img, command=open_level_menu, fg="white", bg="black",)
    logout_button = tk.Button(Side_bar, text="Logout", width=10, command=lambda: root.destroy())
    logout_button.pack(side="bottom", fill="y", pady=5, ipadx=2)

    # Heading Label
    HeadLabel=tk.Label(root, text="Fashion Inventory Management Store")
    HeadLabel.configure(font=('Arial', 40), bg="white")
    HeadLabel.pack(side="top", fill="x", ipady=20)

    main_container = tk.Frame(root)
    billing_window = tk.Frame(root)

    run_store()
