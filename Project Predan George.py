import tkinter
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Global data frame
data_PG = pd.DataFrame()

def fetch_data_PG():
    global data_PG
    servicePG = Service(ChromeDriverManager().install())
    driverPG = webdriver.Chrome(service=servicePG)
    urlPG = 'https://www.nintendo.com/us/store/merchandise/toys/'
    driverPG.get(urlPG)
    
    driverPG.implicitly_wait(10)

    product_namesPG = []
    product_pricesPG = []
    
    products_box = driverPG.find_element("class name", "cJbBZh")
    product_items = products_box.find_elements("class name", "eGpKAT")
    
    for product_property in product_items:
        title = product_property.find_element("class name", "iiGOlC").get_attribute("innerText")
        product_namesPG.append(title)
        price = product_property.find_element("class name", "gGJMHZ").get_attribute("innerText")
        price = price.replace("$", "")
        price = price.replace("Regular Price:\n", "")
        product_pricesPG.append(float(price))
    
    data_PG = pd.DataFrame({
        'Name': pd.Series(product_namesPG),
        'Price': pd.Series(product_pricesPG)
    })
    
    driverPG.quit()

def create_graph_PG():
    global data_PG
    data_PG.plot.bar(x='Name', y='Price')

def display_matrix_PG():
    global data_PG
    if not data_PG.empty:
        print(data_PG)
    else:
        print('No data to display.')

def save_to_excel_PG(name):
    global data_PG
    data_PG.to_excel('/Users/georgepredan/Desktop/{0}.xlsx'.format(name), sheet_name=name, engine='xlsxwriter')

# UI Elements
def create_ui_PG():
    form_PG = tkinter.Tk()
    excel_name_PG = tkinter.Entry(form_PG)
    excel_name_PG.pack()
    
    #name_PG = excel_name_PG.get()

    tkinter.Button(form_PG, text="Retrieve data", command=fetch_data_PG, fg="green").pack()
    tkinter.Button(form_PG, text="Create the graph", command=create_graph_PG, fg="red").pack()
    tkinter.Button(form_PG, text="Display the matrix", command=display_matrix_PG, fg="blue").pack()
    tkinter.Button(form_PG, text="Save to Excel file", command= lambda: save_to_excel_PG(excel_name_PG.get()), fg="purple").pack()

    form_PG.mainloop()

create_ui_PG()