import openpyxl
import herepy
import datetime
import os
import tkinter as tk

from dotenv import load_dotenv
from tkinter import filedialog
from herepy import GeocoderApi

# Load .env file
load_dotenv('../.env')
apikey = os.getenv('apikey')

# Set Here Maps API key
here = GeocoderApi(apikey)

# Set the maximum limit of daily requests
DAILY_LIMIT = 15000

# Count the number of requests made today
today = datetime.date.today()
count_today = 0

# Create a dialog box to select Excel file
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

# Open Excel file and get active worksheet
workbook = openpyxl.load_workbook(file_path)
sheet = workbook.active

# Get the list of column headers
headers = [cell.value for cell in sheet[1]]

# Displays a numbered list of column headers
print("List of column headings:")
for i, header in enumerate(headers):
    print(f"{i+1}. {header}")

# Ask the user to select the column containing the addresses
address_col_num = int(input("Select the column number containing the addresses: "))
# Ask the user to select the column for latitude
latitude_col_num = int(input("Select the column number for latitude: "))
# Ask the user to select the column for longitude
longitude_col_num = int(input("Select the column number for longitude: "))

# Geocode addresses and enter coordinates in selected columns
for row in sheet.iter_rows(min_row=2):
    # Check if we have reached the maximum limit of daily requests
    if count_today >= DAILY_LIMIT:
        print("Maximum limit of daily requests reached. Program interruption...")
        break
    address = row[address_col_num - 1].value
    latitude = row[latitude_col_num - 1].value
    longitude = row[longitude_col_num - 1].value
    # If address already has some value in its latitude and longitude values
    if address and (latitude and longitude):
        print(f"{address} already has geo coordinates: {latitude}, {longitude}")
    # If address does not have complete latitude and longitude values
    elif address and not (latitude and longitude):
        # Geocode the address using Here Maps
        try:
            geocoding_result = here.free_form(address).as_dict()
            # Update the counter of requests made today
            count_today += 1
            # Extract coordinates from geocoding result
            latitude = geocoding_result['items'][0]['position']['lat']
            longitude = geocoding_result['items'][0]['position']['lng']
            # Enter coordinates in selected columns
            row[latitude_col_num - 1].value = latitude
            row[longitude_col_num - 1].value = longitude
            # Print out the geocoding result
            print("Successfully retrieved geocoding data:")
            print(f"{address}: {latitude}, {longitude}")
        except herepy.HEREError as e:
            print(f"Error geocoding {address}: {e}")
        except IndexError:
            print(f"No results found for {address}")
        except ValueError:
            print(f"Error geocoding {address}: Invalid address")
    else:
        print("Input address value is not valid.")

# Save the updated workbook
workbook.save(file_path)