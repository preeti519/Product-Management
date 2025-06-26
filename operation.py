# operation.py
import datetime  # Importing datetime for timestamping
from write import generate_invoice

# Function to display all products with details
def display_products(product):
    print("-" * 80)
    print("ID" + " " * 5 + "|" + "Name" + " " * 15 + "|" + "Brand" + " " * 11 + "|" + "Qty" + " " * 8 + "|" + "Price" + " " * 7 + "|" + "Country")
    for i in product.items(): 
        print("-" * 80)
        pid = str(i[0])  # Product ID
        name = i[1][0]  # Product Name
        brand = i[1][1]  # Product Brand
        qty = str(i[1][2])  # Product Quantity
        price = str(i[1][3])  # Product Price
        country = i[1][4]  # Product Country

        # Print each product's details in a table format
        print("|" + pid + " " * (5 - len(pid)),
              "|" + name + " " * (18 - len(name)),
              "|" + brand + " " * (15 - len(brand)),
              "|" + qty + " " * (10 - len(qty)),
              "|" + price + " " * (11 - len(price)),
              "|" + country)
    print("-" * 80)

# Function to handle sale operations (customer buying products)
def handle_sale(product):
    try:
        customer_name = input("Enter customer name: ") 
        if not isinstance(customer_name, str) or customer_name.strip().isdigit():
            print("Invalid customer name. A name cannot be a number. Please enter a valid name.")
            return "error"
        timestamp = datetime.datetime.now()
        total_price = 0  # Initialize total price of sale
        sold_items = []  # List to store sold items for the invoice
        vat_percentage = 13  # Example VAT percentage

        while True:
            product_id = int(input("Enter product ID to buy (0 to finish): "))  # Get product ID
            if product_id == 0:  # If user enters 0, end the sale
                break

            if product_id not in product:  # If product ID is invalid
                print("Invalid Product ID!")
                continue

            name, brand, stock, cost_price, country = product[product_id]  # Get product details
            quantity = int(input("Enter quantity to buy for " + name + ": "))  # Get quantity to buy


            
            free_items = quantity // 3  # Calculate free items based on the "Buy 3 Get 1 Free" rule
            total_items = quantity + free_items  # Total items being purchased (including free items)

            if stock < total_items:  # Check if enough stock is available
                print("Not enough stock!")
                continue

            selling_price = cost_price * 2  # Selling price is double the cost price
            price_for_product = quantity * selling_price  # Calculate price for the sold quantity
            total_price += price_for_product  # Add to total sale price
            product[product_id][2] -= total_items  # Update stock after sale

            # Add sold item to sold items list for invoice generation
            sold_items.append([name, brand, country, quantity, free_items, total_items, price_for_product])

        if len(sold_items) == 0:  # If no items were sold, notify the user
            print("No valid items were purchased.")
            return

        print("\nTransaction Successful!")
        print("Total Price: Rs. " + str(total_price))

        # Calculate VAT and total with VAT
        vat_amount = (total_price * vat_percentage) / 100
        total_with_vat = total_price + vat_amount

        # Ask if the user wants to add shipping charge
        shipping_charge = input("Do you want to add shipping charge? (yes/no): ").lower()
        if shipping_charge == "yes":
            shipping_fee = float(input("Enter shipping charge: "))
        else:
            shipping_fee = 0.0

        final_total = total_with_vat + shipping_fee  # Calculate the final total

        # Generate the invoice timestamp and filename
        time = datetime.datetime.now()
        

        # Call function to generate the invoice
        generate_invoice(customer_name, timestamp, sold_items, total_price, vat_percentage, shipping_fee, final_total)

    except ValueError:
        print("Invalid input! Please enter valid numbers.")  # Handle invalid inputs

# Function to handle product restocking operations
def handle_restock(product):
    try:
        supplier_name = input("Enter supplier name: ")  # Get supplier name
        total_cost = 0  # Initialize total cost of restocking
        restock_items = []  # List to store restocked items
        
        # Get VAT percentage
        vat_percentage = float(input("Enter VAT percentage: "))

        while True:
            product_id = int(input("Enter product ID to restock (0 to finish): "))  # Get product ID
            if product_id == 0:  # If user enters 0, end the restocking
                break

            if product_id not in product:  # If product ID is invalid
                print("Invalid Product ID!")
                continue

            name, brand, stock, cost_price, country = product[product_id]  # Get product details
            restock_quantity = int(input("Enter restock quantity for " + name + ": "))  # Get restock quantity
            new_cost_price = int(input("Enter new cost price for " + name + ": "))  # Get new cost price

            product[product_id][2] += restock_quantity  # Update the stock quantity
            product[product_id][3] = new_cost_price  # Update the cost price

            item_cost = restock_quantity * new_cost_price  # Calculate total cost for the restocked items
            total_cost += item_cost  # Add to the total restock cost
            restock_items.append([name, brand, country, restock_quantity, new_cost_price, item_cost])

        if len(restock_items) == 0:  # If no items were restocked, notify the user
            print("No products restocked.")
            return
            
        # Calculate VAT and total with VAT
        vat_amount = (total_cost * vat_percentage) / 100
        total_with_vat = total_cost + vat_amount

        print("\nRestock Successful!")
        print("Total Restock Cost: Rs. " + str(total_cost))
        print("VAT Amount (" + str(vat_percentage) + "%): Rs. " + str(vat_amount))
        print("Total Cost with VAT: Rs. " + str(total_with_vat))

        # Generate restock invoice timestamp and filename
        time = datetime.datetime.now()
        

        # Create restock invoice and write it to a file
        restock_invoice = "Restock_Invoices/restock_invoice_" + supplier_name + "_" + str(time).replace(":", "-").replace(" ", "_") + ".txt"
        with open(restock_invoice, "w") as restock_file:
            # Write invoice header to file
            restock_file.write("Supplier Name: " + supplier_name + "\n")
            restock_file.write("Date: " + str(time) + "\n")
            restock_file.write("-" * 40 + "\n")
            
            # Print invoice header to terminal
            print("\n" + "=" * 50)
            print("RESTOCK INVOICE")
            print("=" * 50)
            print("Supplier Name: " + supplier_name)
            print("Date: " + str(time))
            print("-" * 50)

            for item in restock_items:
                # Write item details to file
                restock_file.write("Product: " + item[0] + "\n")
                restock_file.write("Brand: " + item[1] + "\n")
                restock_file.write("Country: " + item[2] + "\n")
                restock_file.write("Quantity Restocked: " + str(item[3]) + "\n")
                restock_file.write("New Cost Price: Rs. " + str(item[4]) + "\n")
                restock_file.write("Item Total Cost: Rs. " + str(item[5]) + "\n")
                restock_file.write("-" * 40 + "\n")
                
                # Print item details to terminal
                print("Product: " + item[0])
                print("Brand: " + item[1])
                print("Country: " + item[2])
                print("Quantity Restocked: " + str(item[3]))
                print("New Cost Price: Rs. " + str(item[4]))
                print("Item Total Cost: Rs. " + str(item[5]))
                print("-" * 50)

            # Write summary to file
            restock_file.write("Total Cost: Rs. " + str(total_cost) + "\n")
            restock_file.write("VAT Amount (" + str(vat_percentage) + "%): Rs. " + str(vat_amount) + "\n")
            restock_file.write("Total Cost with VAT: Rs. " + str(total_with_vat) + "\n")
            
            # Print summary to terminal
            print("Total Cost: Rs. " + str(total_cost))
            print("VAT Amount (" + str(vat_percentage) + "%): Rs. " + str(vat_amount))
            print("Total Cost with VAT: Rs. " + str(total_with_vat))
            print("=" * 50)
        
        print("Restock invoice saved as: " + restock_invoice)  # Notify user of the restock invoice creation

    except ValueError:
        print("Invalid input! Please enter valid numbers.")  # Handle invalid inputs
