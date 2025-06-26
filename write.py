import datetime  # Importing datetime module for timestamping invoices

# Function to save updated product data to the file
def save_products(product):
    with open("product.txt", "w") as file:  # Open product file in write mode
        for pid in product:  # Iterate over the product dictionary
            line = product[pid][0] + "," + product[pid][1] + "," + str(product[pid][2]) + "," + str(product[pid][3]) + "," + product[pid][4] + "\n"
            # Prepare each product's data in comma-separated format
            file.write(line)  # Write each product's data to the file
    print("Stock updated and saved!")  # Notify the user that data was saved

# Function to generate a sales invoice after a transaction
def generate_invoice(customer_name, timestamp, sold_items, total_price, vat_percentage, shipping_fee, total_with_vat):
    invoice_name = "Sales_Invoices/sale_invoice_" + customer_name + "_" + str(timestamp) + ".txt"
    
    # Create a list to store invoice lines for both file and terminal output
    invoice_lines = []
    
    # Header section
    header1 = "+" + "-" * 60 + "+"
    header2 = "|" + " " * 22 + "SALES INVOICE" + " " * 22 + "|"
    header3 = "+" + "-" * 60 + "+"
    header4 = "| Customer Name: " + customer_name
    header5 = "| Date: " + str(timestamp)
    
    invoice_lines.append(header1)
    invoice_lines.append(header2)
    invoice_lines.append(header3)
    invoice_lines.append(header4)
    invoice_lines.append(header5)
    invoice_lines.append(header3)
    
    # Column headings - fixed width formatting
    table_header1 = "+-----------------+---------------+-----+------+------------+------------+"
    table_header2 = "| Product         | Brand         | Qty | Free | Unit Price | Amount     |"
    
    invoice_lines.append(table_header1)
    invoice_lines.append(table_header2)
    invoice_lines.append(table_header1)
    
    # Process each sold item's detail
    for item in sold_items:
        product = item[0]
        brand = item[1]
        qty = str(item[3])
        free = str(item[4])
        unit_price = str(int(item[6] / item[3]))  # derived from total amount / quantity
        amount = str(item[6])

        # Format each column with proper spacing manually
        product_col = (product + " " * 15)[:15]
        brand_col = (brand + " " * 13)[:13]
        qty_col = " " * (3 - len(qty)) + qty
        free_col = " " * (4 - len(free)) + free
        price_col = " " * (10 - len(unit_price)) + unit_price
        amount_col = " " * (10 - len(amount)) + amount
        
        # Build the line with proper spacing
        line = "| " + product_col + " | " + brand_col + " | " + qty_col + " | " + free_col + " | " + price_col + " | " + amount_col + " |"
        invoice_lines.append(line)
    
    # Footer line
    invoice_lines.append(table_header1)
    
    # Totals section
    vat_amount = (total_price * vat_percentage) / 100
    grand_total = total_with_vat + shipping_fee
    
    subtotal_str = str(total_price)
    vat_str = str(vat_amount)
    shipping_str = str(shipping_fee)
    grand_total_str = str(grand_total)

    subtotal_line = "| Subtotal      : Rs. " + " " * (10 - len(subtotal_str)) + subtotal_str + " |"
    vat_line = "| VAT (" + str(vat_percentage) + "%)     : Rs. " + " " * (10 - len(vat_str)) + vat_str + " |"
    shipping_line = "| Shipping      : Rs. " + " " * (10 - len(shipping_str)) + shipping_str + " |"
    total_line = "| GRAND TOTAL   : Rs. " + " " * (10 - len(grand_total_str)) + grand_total_str + " |"
    
    invoice_lines.append(subtotal_line)
    invoice_lines.append(vat_line)
    invoice_lines.append(shipping_line)
    invoice_lines.append(header3)
    invoice_lines.append(total_line)
    invoice_lines.append(header3)
    
    # Print invoice to terminal
    print("\n=== INVOICE PREVIEW ===")
    for line in invoice_lines:
        print(line)
        
    # Write invoice to file
    with open(invoice_name, "w") as invoice_file:
        for line in invoice_lines:
            invoice_file.write(line + "\n")
    
    print("\nSale invoice created successfully!")
    print("Invoice saved as: " + invoice_name)
    print("Total amount: Rs. " + str(grand_total))
