# read.py

# Function to read products from the file and return them as a dictionary
def read_products():
    product = {}  # Initialize an empty dictionary to store products
    with open("product.txt", "r") as file:  # Open the product file in read mode
        data = file.readlines()  # Read all lines from the file

    pid = 1  # Starting product ID for assigning to products
    for line in data:
        line = line.replace("\n", "").split(",")  # Split each line by commas
        line[2] = int(line[2])  # Quantity (convert to integer)
        line[3] = int(line[3])  # Price (convert to integer)
        product[pid] = line  # Add the product to the dictionary with a unique ID
        pid = pid + 1  # Increment product ID for the next product

    return product  # Return the dictionary of products
