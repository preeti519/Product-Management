
# main.py
from read import read_products  # Import function to read product data
from write import save_products  # Import function to save updated product data
from write import generate_invoice  # Import the generate_invoice function from write.py

from operation import display_products, handle_sale, handle_restock  # Import operation functions
import datetime  # Import datetime for timestamping invoices

# Load product data from the file
product = read_products()

main_loop = True  # Main loop for program operation

# Program loop to continuously ask for user input
while main_loop:
    print("\n" + "-" * 33)
    print("# CHOOSE THE OPTION YOU WOULD LIKE TO PERFORM -->")
    print("-" * 33)
    print("| Option | Action               |")
    print("|--------|----------------------|")
    print("|   0    | Display product      |")
    print("|   1    | Sale (Customer Buy)  |")
    print("|   2    | Purchase (Restock)   |")
    print("|   3    | Exit                 |")
    print("-" * 33)

    try:
        choice = int(input(">> Enter your choice: "))  # Get user input for the action

        if choice == 0:
            print("\n# THESE ARE THE AVAILABLE PRODUCTS IN THE STOCK -->")
            display_products(product)  # Display the available products
        elif choice == 1:
            flag = handle_sale(product) 
            if flag == "error":
                continue
            else:
                save_products(product)  # Save updated stock
        elif choice == 2:
            handle_restock(product)  # Handle product restocking
            save_products(product)  # Save updated stock
        
            
        elif choice == 3:
            print("Thank you for using our system!")  # Exit message
            main_loop = False  # End the main loop
        else:
            print("Invalid input. Please select from 0 to 3.")  # Handle invalid input
    except ValueError:
        print("Invalid input! Please enter a number.")  # Handle invalid input

# Save product data back to the file after any operation
save_products(product)
