import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("love_sandwiches")


def get_sales_data():
    """
    Get sales figures input from user.
    Runs a while loop to repeatedly ask for a valid data input, which
    must be 6 valid integers separated by commas. The loop will
    ask for data repeatedly until it is valid.
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here:\n")
        print(f"The data provided is {data_str}")

        sales_data = data_str.split(",")
        if validate_data(sales_data):
            print("Data is valid!")
            break

    return sales_data

def validate_data(values):
    """
    Inside the try, converts string values to integers
    Returns a ValueError if strings cannot be converted to ints,
    or if there are more than 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Error! 6 values required, you provided {len(values)}"
            )
        
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True

def update_worksheet(worksheet, data):
    """
    Update the specified worksheet, adding a new row with the data provided.
    """
    print(f"Updating {worksheet} worksheet...\n")
    to_update = SHEET.worksheet(worksheet)
    to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully!\n")

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock to calculate surplus for each item type
    
    Surplus is equal to sales figure subtracted from the stock
    Positive surplus indicates waste
    Negative surplus indicates extra made when stock was sold out
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data

def get_last_5_entries_sales():
    """
    Collects the last 5 rows of sales data for each sandwich
    and returns them as a list of lists
    """
    sales = SHEET.worksheet("sales")
    columns = []
    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    
    return columns

def calculate_stock_data(data):
    """
    Calculate the average stock for each item, adding 10%
    """
    print("Calculating stock data...\n")
    new_stock_data = []
    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data


def main():
    """
    Run all program functions
    """

    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet("sales", sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet("surplus", new_surplus_data)
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    print(stock_data)

print("Welcome to Love Sandwiches Data Automation")
main()