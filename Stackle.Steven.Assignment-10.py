"""
***********************************
Author: Steven Stackle
Assignment #10, ICT-4370, Winter 2020, Instructor: Dr. Steven Russell
Last Revision: March 13, 2020

Description: This program builds the record of an investor's stock holdings
by creating dictionaries to hold groups of objects. The objects,
representing company stocks owned and bonds owned, are built with data
pulled from external text files. Additionally, the program pulls
historical stock price data from a JSON file.
The program then writes data to four tables in a SQLite database 
in the local computer.
Next, the program retrieves data from the database into data classes.
The program prints a report using the data to 
calculate how much the investor has earned or lost in dollars and as a
percentage as well as the list of high and low prices for each stock
during the period for which the JSON file has price quotes.
************************************
"""

### breakpoint()

# Import the datetime function from the datetime module for date calculations.
from datetime import datetime
# Import the SQLite connector library.
import sqlite3
# Import the JSON connector library.
import json

# === Create Classes ===
class CompanyStockOwned():
    """ This class creates an object which is a model of an investor's
        ownership of stock in a single company and three methods for
        calculating gains. """
    
    def __init__(self, company_stock_symbol, number_of_shares,
                 share_purchase_price, current_share_value,
                 share_purchase_date, purchase_ID = ''):
        """ Initialize attributes of ownership in one company's stock. """
        # purchase price and current value are in dollars and cents, and
        # purchase dates are in the format of month/day/year -- mm/dd/yyyy.
        self.company_stock_symbol = company_stock_symbol
        try:
            self.number_of_shares = int(number_of_shares)
            self.share_purchase_price = float(share_purchase_price)
            self.current_share_value = float(current_share_value)
        except ValueError:
            print("Sorry. A number was expected.")
        self.share_purchase_date = share_purchase_date
        self.purchase_ID = purchase_ID
        
    def earnings(self):
        """ Calculate the total gains or losses for the shares owned in a
        given company and return that value. """
        # First find the gain or loss per share
        # by subtracting the purchase price from the current price.
        # Then multiply by the total number of shares owned.
        # Return the gain or loss.
        return ((self.current_share_value - self.share_purchase_price)
            * self.number_of_shares)

    def percent_earnings(self):
        """ Calculate the total percentage yield or loss of a stock holding
        and return that value. """
        # Formula: ((current value – purchase price)/purchase price))
        # First find the gain or loss per share
        # by subtracting the stock purchase price from the current price.
        # Then find the percentage yield by dividing by the purchase price.
        # Return the percentage.
        return ((self.current_share_value - self.share_purchase_price) 
            / self.share_purchase_price)
        
    def yearly_percent_earnings(self):
        """ Calculate the yearly earning or loss rate of a stock holding
        and return that value as a percentage. """
        # Formula: ((((current value – purchase price)/purchase price)/
        #                    (current date – purchase date)))*100        
        # Use the method 'percent_earnings' to find the total yield.
        # Divide the total yield by the number of years owned, and multiply 
        # by 100 to return a percentage.
        # To calculate the number of years the stock has been owned:
        # get today's date using datetime.now(), convert the
        # share_purchase_date string to a datetime object, subtract
        # the purchase date from today's date, and multiply by the number
        # of days in a year.
        return (self.percent_earnings() /
                (((datetime.now() - datetime.strptime(self.share_purchase_date,
                "%m/%d/%Y")).days) / 365.2425)) * 100

class Investor():
    """ This class creates an object which is a model of a securities owner. """
    
    def __init__(self, investor_name, investor_address,
                 investor_phone_number, investor_ID = ''):
        """Initialize attributes of the investor."""
        self.investor_name = investor_name
        self.investor_address = investor_address
        self.investor_phone_number = investor_phone_number
        self.investor_ID = investor_ID

class BondOwned():
    """ This class creates an object which is a model of an investor's
    ownership of bonds in a single entity. """

    def __init__(self, bond_name, bond_quantity,
                 bond_purchase_price, current_bond_value,
                 bond_purchase_date, bond_coupon, bond_yield, bond_ID, purchase_ID = ''):
        """ Initialize attributes of ownership in one entity's bond. """
        # purchase price and current value are in dollars and cents, and
        # purchase dates are in the format of month/day/year -- mm/dd/yyyy.
        self.bond_name = bond_name
        try:
            self.bond_quantity = int(bond_quantity)
            self.bond_purchase_price = float(bond_purchase_price)
            self.current_bond_value = float(current_bond_value)
        except ValueError:
            print("Sorry. A number was expected.")
        self.bond_purchase_date = bond_purchase_date
        self.bond_coupon = bond_coupon
        self.bond_yield = bond_yield
        self.bond_ID = bond_ID
        self.purchase_ID = purchase_ID
        
    def earnings(self):
        """ Calculate the total gains or losses for the bonds owned in a
        given company and return that value. """
        # First find the gain or loss per bond
        # by subtracting the purchase price from the current price.
        # Then multiply by the total number of bonds owned.
        # Return the gain or loss.
        return ((self.current_bond_value - self.bond_purchase_price)
            * self.bond_quantity)

    def percent_earnings(self):
        """ Calculate the total percentage yield or loss of a bond holding
        and return that value. """
        # Formula: ((current value – purchase price)/purchase price))
        # First find the gain or loss per share
        # by subtracting the bond purchase price from the current price.
        # Then find the percentage yield by dividing by the purchase price.
        # Return the percentage.
        return ((self.current_bond_value - self.bond_purchase_price) 
            / self.bond_purchase_price)
        
    def yearly_percent_earnings(self):
        """ Calculate the yearly earning or loss rate of a bond holding
        and return that value as a percentage. """
        # Formula: ((((current value – purchase price)/purchase price)/
        #                    (current date – purchase date)))*100        
        # Use the method 'percent_earnings' to find the total yield.
        # Divide the total yield by the number of years owned, and multiply 
        # by 100 to return a percentage.
        # To calculate the number of years the bond has been owned:
        # get today's date using datetime.now(), convert the
        # bond_purchase_date string to a datetime object, subtract
        # the purchase date from today's date, and multiply by the number
        # of days in a year.
        return (self.percent_earnings() /
                (((datetime.now() - datetime.strptime(self.bond_purchase_date,
                "%m/%d/%Y")).days) / 365.2425)) * 100

class CompanyStock():
    """ This class creates an object which is a model of a
        single stock over time. """
    
    def __init__(self, company_stock_symbol):
        """Initialize the company stock."""
        self.company_stock_symbol = company_stock_symbol
        self.opening_price_list = []
        self.high_price_list = []
        self.low_price_list = []
        self.closing_price_list = []
        self.volume_list = []
        self.valuation_date_list = []

    def addQuote(self, opening_price, high_price, low_price, closing_price, \
                 volume, valuation_date):
        """Add price and volume data and date information to the class."""
        self.opening_price_list.append(opening_price)
        self.high_price_list.append(high_price)
        self.low_price_list.append(low_price)
        self.closing_price_list.append(closing_price)
        self.volume_list.append(volume)
        self.valuation_date_list.append(valuation_date)
        

# === Initialize Variables ===

# - Create variables for the text files to be imported. -
stocks_filename = 'Stocks_Data.txt'
bonds_filename = 'Bond_data.txt'

# - Read the stock data from a text file. -
# Intitalize counter variables and create an empty list into which
# the program will read the data from the text file.
loop_counter = 0
stock_counter = 0
stock_data_headings = []
companies_stock_data = []
# Try to open the stock file. Throw an exception if the file does not exist.
try:
    with open(stocks_filename) as file_object:
        stock_data_lines = file_object.readlines()
        
except IOError:
    print("Sorry. The file " + filename + " does not exist.")

# Loop through the imported stock data
for stock_data_line in stock_data_lines:
    # Treat the first 5 lines differently, because they are column headings.
    # The first 5 iterations, append the stock data lines to the headings list.
    if stock_counter == 0:
        stock_data_headings.append(stock_data_line.rstrip())

    # After the first five iterations, if the loop counter is 0,
    # create a new empty inner list and append the next stock data line to it.
    # Subtract 1 from stock_counter because list indexes start at 0.
    elif (stock_counter > 0 and loop_counter == 0):
        companies_stock_data.append([])
        companies_stock_data[stock_counter - 1].append(stock_data_line.rstrip())

    # All other times through the loop, append the stock data line
    # to the curremt inner list.
    else:
        companies_stock_data[stock_counter - 1].append(stock_data_line.rstrip())

    # Count the line added from the stock file.
    loop_counter += 1

    # After 5 lines have been read/added, 
    # reset the line/loop counter, and increment the stock counter.
    if loop_counter == 5:
        stock_counter += 1
        loop_counter = 0  

# - Read the bond data from a text file. -
# Intitalize counter variables and create an empty list into which
# the program will read the data from the text file.
loop_counter = 0
bond_counter = 0
bond_data_headings = []
bond_data = []
# Try to open the bond file. Throw an exception if the file does not exist.
try:
    with open(bonds_filename) as file_object:
            bond_data_lines = file_object.readlines()

except IOError:
    print("Sorry. The file " + filename + " does not exist.")

# Loop through the imported bond data
for bond_data_line in bond_data_lines:
    # Treat the first 7 lines differently, because they are column headings.
    # The first 7 iterations, append the bond data lines to the headings list.
    if bond_counter == 0:
        bond_data_headings.append(bond_data_line.rstrip())

    # After the first seven iterations, if the loop counter is 0,
    # create a new empty inner list and append the next stock data line to it.
    # Subtract 1 from bond_counter because lists start at 0.
    elif (bond_counter > 0 and loop_counter == 0):
        bond_data.append([])
        bond_data[bond_counter - 1].append(bond_data_line.rstrip())

    # All other times through the loop, append the bond data line
    # to the existing inner list.
    else:
        bond_data[bond_counter - 1].append(bond_data_line.rstrip())

    # Count the line added from the bond file.
    loop_counter += 1

    # After 7 lines have been read/added, 
    # reset the line/loop counter, and increment the bond counter.
    if loop_counter == 7:
        bond_counter += 1
        loop_counter = 0

# Create a single bond holding.
# Hard code the last attribute (bond_ID) for now.
bond_1_owned = BondOwned(bond_data[0][0],
        bond_data[0][1], bond_data[0][2],
        bond_data[0][3], bond_data[0][4],
        bond_data[0][5], bond_data[0][6], 1)

# Create an Investor object instance to represent the owner of the portfolio.
investor_1 = Investor('Bob Smith', '123 Sesame Street', '212-867-5309', 1)


# Load the stock data by opening a JSON file.
# Throw an exception if the file does not exist.
filepath =  "AllStocks.json"
try:
    with open(filepath) as file_object:
        stock_data = json.load(file_object)
except FileNotFoundError:
    print("Sorry. There was an error opening the JSON file.")

# Make an empty dictionary to store the stock data.
stock_dictionary = {}

# Make an empty list to store the stock names.
stock_names_list = []

# Loop through the stock data.
# Throw an exception if there is not stock data.
try:
    for stock in stock_data:
        # Check if a stock's data is in the dictionary.
        # If not, create a new CompanyStock object and add it to the dictionary
        # and add the stock symbol to a list of stock names.
        if stock['Symbol'] not in stock_dictionary:
            new_stock = CompanyStock(stock['Symbol'])
            stock_dictionary[stock['Symbol']] = {'stock_data' : new_stock}
            stock_names_list.append(stock['Symbol'])
        # Add valuation date, price, and volume data for
        # each quote in the JSON file.
        stock_dictionary[stock['Symbol']]['stock_data'].addQuote( \
                    stock['Open'], stock['High'], stock['Low'], \
                    stock['Close'], stock['Volume'], \
                    datetime.strptime(stock['Date'], '%d-%b-%y'))
except NameError:
    print("Sorry. The stock data did not load.")

    

# === Output ===

# Write the data to three tables in a SqLite database in the local computer
# for investors, stocks, and bonds. 
database_path = "Database_for_Financial_Data.sqlite"
conn = sqlite3.connect(database_path)

def create_tables(database_path):
    """ Create the database and set up the three tables. """
    sql_create_stock_table = ''' CREATE TABLE IF NOT EXISTS   \
                   stock_table ( 
	                            stock_ID integer PRIMARY KEY,
	                            company_stock_symbol text NOT NULL,
	                            number_of_shares integer NOT NULL,
	                            share_purchase_price real NOT NULL,
	                            current_share_value real NOT NULL,
	                            share_purchase_date text NOT NULL,
	                            purchase_ID integer,
	                            investor_ID integer NOT NULL
	                            ); '''
                                    
    sql_create_bond_table = """ CREATE TABLE IF NOT EXISTS  \
                     bond_table (
	                            bond_ID integer PRIMARY KEY,
	                            bond_name text NOT NULL,
	                            bond_quantity integer NOT NULL,
	                            bond_purchase_price real NOT NULL,
	                            current_bond_value real NOT NULL,
	                            bond_purchase_date text NOT NULL,
	                            purchase_ID integer,
	                            investor_ID integer NOT NULL,
	                            bond_coupon real NOT NULL,
	                            bond_yield real NOT NULL
	                            ); """

    sql_create_investor_table = """ CREATE TABLE IF NOT EXISTS  \
                     investor_table (
	                            investor_ID integer PRIMARY KEY,
	                            investor_name text NOT NULL,
	                            investor_address text NOT NULL,
	                            investor_phone_number text NOT NULL
	                            ); """
	
    # Connect SQLite to the database
    # - located in the same directory as this Python code file.
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    # Use the table creation/layout above to set up the rows
    #  - then commit and close the database.
    cursor.execute(sql_create_stock_table)
    cursor.execute(sql_create_bond_table)
    cursor.execute(sql_create_investor_table)
    connection.commit()	
    connection.close()

def write_database_rows(database_path, investor_table, bond_table,
                        companies_stock_data):
    """ Write rows to the database from the class objects. """
    connection = sqlite3.connect(database_path)
    cursor	=	connection.cursor()
  
    # Build a string with an investor's data fields - for inserting a row
    #   (a string of the field values separated by commas).
    #   The SQLite command to Insert is first in the string,
    #   to pass to sqlite3, including the name of the table.
    sql_insert_investor = "INSERT INTO investor_table VALUES('" 
    sql_insert_investor = sql_insert_investor + str(investor_1.investor_ID) + "'"
    sql_insert_investor = sql_insert_investor + ", '" + investor_1.investor_name + "'"
    sql_insert_investor = sql_insert_investor + ", '" + investor_1.investor_address + "'"
    sql_insert_investor = sql_insert_investor + ", '" + investor_1.investor_phone_number
    sql_insert_investor = sql_insert_investor + "')"

    # Write the investor's data into the database.
    try:
        cursor.execute(sql_insert_investor)
    except sqlite3.IntegrityError:
        print("Sorry. That investor database field already exists.")

    # Build a string with the bond data fields - for inserting a row.
    sql_insert_bond = "INSERT INTO bond_table VALUES('" 
    sql_insert_bond = sql_insert_bond + str(bond_1_owned.bond_ID) + "'"
    sql_insert_bond = sql_insert_bond + ", '"
    sql_insert_bond = sql_insert_bond + \
                      bond_1_owned.bond_name
    sql_insert_bond = sql_insert_bond + "'"
    sql_insert_bond = sql_insert_bond + ", '"
    sql_insert_bond = sql_insert_bond + \
                      str(bond_1_owned.bond_quantity)
    sql_insert_bond = sql_insert_bond + "'"
    sql_insert_bond = sql_insert_bond + ", '"
    sql_insert_bond = sql_insert_bond + \
                      str(bond_1_owned.bond_purchase_price)
    sql_insert_bond = sql_insert_bond + "'"
    sql_insert_bond = sql_insert_bond + ", '"
    sql_insert_bond = sql_insert_bond + \
                      str(bond_1_owned.current_bond_value)
    sql_insert_bond = sql_insert_bond + "'"
    sql_insert_bond = sql_insert_bond + ", '"
    sql_insert_bond = sql_insert_bond + \
                      bond_1_owned.bond_purchase_date
    sql_insert_bond = sql_insert_bond + "'"
    sql_insert_bond = sql_insert_bond + ", '"
    sql_insert_bond = sql_insert_bond + \
                      str(bond_1_owned.purchase_ID)
    sql_insert_bond = sql_insert_bond + "'"
    sql_insert_bond = sql_insert_bond + ", '"
    sql_insert_bond = sql_insert_bond + str(investor_1.investor_ID)
    sql_insert_bond = sql_insert_bond + "'"
    sql_insert_bond = sql_insert_bond + ", '"
    sql_insert_bond = sql_insert_bond + str(bond_1_owned.bond_coupon)
    sql_insert_bond = sql_insert_bond + "'"
    sql_insert_bond = sql_insert_bond + ", '"
    sql_insert_bond = sql_insert_bond + str(bond_1_owned.bond_yield)
    sql_insert_bond = sql_insert_bond + "')"

    # Write the bond data into the database.
    try:
        cursor.execute(sql_insert_bond)
    except sqlite3.IntegrityError:
        print("Sorry. That bond database field already exists.")

    # Build strings with the stock data fields - for inserting a row.
    # Use a for loop to loop through the entire companies_stock_data list.
    # Initialize a counter variable to use for the 'stock_ID' field.
    stock_counter = 0
    for company_stock_data in companies_stock_data:
        stock_counter += 1
        sql_insert_stock = "INSERT INTO stock_table VALUES('"
        # Make stock_ID consecutive integers starting at 1.
        sql_insert_stock = sql_insert_stock + str(stock_counter) + "'"
        sql_insert_stock = sql_insert_stock + ", '"
        # company_stock_symbol
        sql_insert_stock = sql_insert_stock + company_stock_data[0] + "'"
        sql_insert_stock = sql_insert_stock + ", '"
        # number_of_shares
        sql_insert_stock = sql_insert_stock + company_stock_data[1] + "'"
        sql_insert_stock = sql_insert_stock + ", '"
        # share_purchase_price
        sql_insert_stock = sql_insert_stock + company_stock_data[2] + "'"
        sql_insert_stock = sql_insert_stock + ", '"
        # current_share_value
        sql_insert_stock = sql_insert_stock + company_stock_data[3] + "'"
        sql_insert_stock = sql_insert_stock + ", '"
        # share_purchase_date
        sql_insert_stock = sql_insert_stock + company_stock_data[4] + "'"
        sql_insert_stock = sql_insert_stock + ", '"
        # purchase_ID -- leave blank for now
        sql_insert_stock = sql_insert_stock + "'"
        sql_insert_stock = sql_insert_stock + ", '"
        # investor_ID
        sql_insert_stock = sql_insert_stock + str(investor_1.investor_ID)
        # Close quotes.
        sql_insert_stock = sql_insert_stock + "')"
        
        # Write one company's stock data into the database.
        try:
            cursor.execute(sql_insert_stock)
        except sqlite3.IntegrityError:
            print("Sorry. That stock database field already exists.")
        
    # Commit and close the database.
    connection.commit()	
    connection.close()

# Write the historical stock data to a table in a SqLite database
# in the local computer.
database_path = "Database_for_Financial_Data.sqlite"
conn = sqlite3.connect(database_path)

def create_history_table(database_path):
    """ Create the historical stock data table. """
    sql_create_history_table = ''' CREATE TABLE IF NOT EXISTS   \
                stock_history_table ( 
    	                            stock_ID integer NOT NULL,
	                            company_stock_symbol text NOT NULL,
	                            opening_price real NOT NULL,
	                            high_price real NOT NULL,
	                            low_price real NOT NULL,
	                            closing_price real NOT NULL,
	                            volume integer NOT NULL,
	                            valuation_date text NOT NULL,
	                            row_ID integer PRIMARY KEY
	                            ); '''

    # Connect SQLite to the database
    # located in the same directory as this Python code file.
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    # Use the table creation/layout above to set up the rows
    # then commit and close the database.
    cursor.execute(sql_create_history_table)
    connection.commit()	
    connection.close()

def write_history_db_rows(database_path, stock_dictionary):
    """ Write rows to the database from the class objects. """
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    # Build strings with the stock data fields - for inserting a row.
    # Use nested loops to loop through each stock object and
    # each list of quote data within each stock object.
    # Initialize a counter variable to use for the 'stock_ID' field.
    # Initialize a row counter variable to count the number of rows created
    # and use as the database table key.
    stock_counter = 0
    row_counter = 1
    for stock_name in stock_names_list:
        stock_counter += 1
        list_counter = 0
        for opening_price in stock_dictionary[stock_name]['stock_data'].opening_price_list:
            sql_insert_stock = "INSERT INTO stock_history_table VALUES('"
            stock_dictionary[stock_name]['stock_data'].company_stock_symbol
            # Make stock_ID consecutive integers starting at 1.
            sql_insert_stock = sql_insert_stock + str(stock_counter) + "'"
            sql_insert_stock = sql_insert_stock + ", '"
            # company_stock_symbol
            sql_insert_stock = sql_insert_stock + stock_dictionary[stock_name]['stock_data'].company_stock_symbol + "'"
            sql_insert_stock = sql_insert_stock + ", '"
            # opening_price
            sql_insert_stock = sql_insert_stock + str(stock_dictionary[stock_name]['stock_data'].opening_price_list[list_counter]) + "'"
            sql_insert_stock = sql_insert_stock + ", '"
            # high_price
            sql_insert_stock = sql_insert_stock + str(stock_dictionary[stock_name]['stock_data'].high_price_list[list_counter]) + "'"
            sql_insert_stock = sql_insert_stock + ", '"
            # low_price
            sql_insert_stock = sql_insert_stock + str(stock_dictionary[stock_name]['stock_data'].low_price_list[list_counter]) + "'"
            sql_insert_stock = sql_insert_stock + ", '"
            # closing_price
            sql_insert_stock = sql_insert_stock + str(stock_dictionary[stock_name]['stock_data'].low_price_list[list_counter]) + "'"
            sql_insert_stock = sql_insert_stock + ", '"
            # volume
            sql_insert_stock = sql_insert_stock + str(stock_dictionary[stock_name]['stock_data'].volume_list[list_counter]) + "'"
            sql_insert_stock = sql_insert_stock + ", '"
            # valuation_date
            sql_insert_stock = sql_insert_stock + str(stock_dictionary[stock_name]['stock_data'].valuation_date_list[list_counter]) + "'"
            sql_insert_stock = sql_insert_stock + ", '"
            # row_counter
            sql_insert_stock = sql_insert_stock + str(row_counter) + "'"
            # Close parenthesis.
            sql_insert_stock = sql_insert_stock + ")"
        
            # Write one company's stock data into the database.
            ###cursor.execute(sql_insert_stock)
            try:
                cursor.execute(sql_insert_stock)
            except sqlite3.IntegrityError:
                print("Sorry. That stock database field already exists.")
            list_counter += 1
            row_counter += 1

     
    # Commit and close the database.
    connection.commit()	
    connection.close()
   
# Use the above function to create the database tables.
create_tables(database_path)

# Write the stock, bond, and investor data,
# using the above list and dictionary data.
write_database_rows(database_path, investor_1, bond_1_owned, \
                    companies_stock_data)

# Use the above function to create the stock history database table.
create_history_table(database_path)

# Write the stock history table using the dictionary data.
write_history_db_rows(database_path, stock_dictionary)

# Connect the program to the database (its location),
# and facilitate subsequent processing with the cursor.
db_connection = sqlite3.connect("Database_for_Financial_Data.sqlite")
cursor = db_connection.cursor()

# Set up new empty lists, for adding the stock, bond and investor
# info from the database.
investors_list_db = []
bonds_list_db = []
stocks_list_db = []

# - Read the one investor's data from the investor table. -
for investor_record in cursor.execute("SELECT * FROM investor_table;"):
    # Put an investor into a class as an instance of the Investor class.
    investor_as_class_db = Investor(str(investor_record[1]), 
                              str(investor_record[2]), 
                              str(investor_record[3]),      
                              str(investor_record[0]))
    # Add this investor instance into the list of investors. 
    investors_list_db.append(investor_as_class_db)
  
# - Read the one bond's data from the bond table. -
for bond_record in cursor.execute("SELECT * FROM bond_table;"):
    # Put a bond into a class as an instance of the BondOwned class.
    bond_as_class_db = BondOwned(bond_record[1], bond_record[2],
            bond_record[3], bond_record[4], bond_record[5], bond_record[8],
            bond_record[9], bond_record[0])
    
    # Add this bond instance into the list of bonds. 
    bonds_list_db.append(bond_as_class_db)

# - Read data from the stock table one record at a time. -
for stock_record in cursor.execute("SELECT * FROM stock_table;"):
    # Put a stock into a class as an instance of the CompanyStockOwned class.
    stock_as_class_db = CompanyStockOwned(stock_record[1], stock_record[2],
                stock_record[3], stock_record[4], stock_record[5])

    # Add this stock instance into the list of stocks. 
    stocks_list_db.append(stock_as_class_db)


    
# -- Print the report. --
# Use the newly-copied data read from the database
# from the classes and list just created.

# -- Print the document header. --
print("\nStock ownership for " + investors_list_db[0].investor_name)
print("----------------------------------------------------\n")

# -- Print the stock chart. --
# - Print the stock chart headings with spaces. -
print("STOCK       SHARE#       EARNINGS/LOSS       " +
                  "YEARLY % EARNING/LOSS")    
print("--------------------------------------------------" +
                  "---------------------")

        
# - Print the body of the stock chart. -
# Loop through the new stock data list: 'stocks_list_db'.
# Each iteration of the loop is data for stock in a single company.
# 'company_stock_owned' is an object containing each holding.
for company_stock_owned in stocks_list_db:
    # - Print the chart. -
    # 1 - Print the stock symbol.
    # 2 - Print the share total.
    # 3 - Call the method to calculate the total gains
    #  for the shares owned in a given company. Print the earnings/loss.
    #  The total gain or loss is in dollars and cents.
    # 4 - Call the method to calculate the yearly earnings/loss 
    #  for the shares owned in a given company. Print as a percent.
    # Use blank spaces to roughly align the columns with the headings.
    # Use try-except to throw exceptions for value and attribute errors.
    try:
        print(company_stock_owned.company_stock_symbol + 
            "        " + str(company_stock_owned.number_of_shares) + 
            "        " + "$" +
            str(company_stock_owned.earnings()) + "      " +
            str(company_stock_owned.yearly_percent_earnings()) + "%" )
    except ValueError:
        print("Sorry. A number was expected.")
    except AttributeError:
        print("Sorry. An attribute is incorrect.")


# -- Print the bond section header. --
print("\n\n")
print("Bond ownership for " + investors_list_db[0].investor_name)

#-- Print the bond chart. --
# - Print the bond chart headings with spaces. -
print("--------------------------------------------------" +
                  "---------------------\n")
print("BOND       QUANTITY      EARNINGS/LOSS       " +
            "YEARLY % EARNING/LOSS")    
print("--------------------------------------------------" +
                  "----------------------------")

# - Print the body of the bond chart. -
# Loop through the new bond data list: 'bonds_list_db'.
# Each iteration of the loop is data for a bond in a single entity.
# 'company_bond_owned' is an object containing each holding.
for bond_owned in bonds_list_db:
    # - Print the chart. -
    # 1 - Print the stock symbol.
    # 2 - Print the share total.
    # 3 - Call the method to calculate the total gains or losses
    #  for the bonds owned in a given entity. Print the earnings/loss.
    #  The total gain or loss is in dollars and cents.
    # 4 - Call the method to calculate the yearly earnings/loss 
    #  for the bonds owned in a given entity. Print as a percent.
    # Use blank spaces to roughly align the columns with the headings.
    # Use try-except to throw exceptions for value and attribute errors.
    try:
        print(bond_owned.bond_name + 
            "      " + str(bond_owned.bond_quantity) + 
            "        " + "$" +
            str(bond_owned.earnings()) + "      " +
            str(bond_owned.yearly_percent_earnings()) + "%" )
    except ValueError:
        print("Sorry. A number was expected.")
    except AttributeError:
        print("Sorry. An attribute is incorrect.")


# -- Read data from the historical stock prices in
#    the database and report and the high and low
#    prices for the ownership period.

# -- Print the section header. --
print("\nHistorical Stock Prices for Ownership Period")
print("----------------------------------------------------\n")

# -- Print the stock price history chart. --
# - Print the stock history chart headings with spaces. -
print("STOCK       LOWEST PRICE       HIGHEST PRICE       ")    
print("--------------------------------------------------" +
                  "---------------------")
# Make empty lists to store the low and high prices
# for each stock in the database.
max_list = []
min_list = []
loop_counter = 0
for stock_name in stock_names_list:
    # Use SQLite queries to find maximum and minimum prices in the
    # historical price data table for each stock owned.
    # Using '+ 0' in the MAX() function ensures a number is used,
    # because there are missing high_price entries in the JSON file.
    for row in cursor.execute("""SELECT MAX(high_price + 0) FROM stock_history_table \
            WHERE "company_stock_symbol" = """ + "'" + stock_name + "'"):
        max_list.append(row[0])
    for row in cursor.execute("""SELECT MIN(low_price) FROM stock_history_table \
            WHERE "company_stock_symbol" = """ + "'" + stock_name + "'"):
        min_list.append(row[0])
    print(stock_name + "           " + str(min_list[loop_counter]) + \
          "               " + str(max_list[loop_counter]))
    loop_counter += 1



#
# End of program
#





