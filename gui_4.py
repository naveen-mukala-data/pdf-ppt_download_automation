import PySimpleGUI as sg
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import os
import time
import threading
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to login to the website
def login_to_website(username, password, driver):
    driver.get("https://rc.library.uta.edu/uta-ir/")
    login_link = driver.find_element(By.XPATH, "//a[@href='/uta-ir/login']")
    login_link.click()

    # Locate the username field using its ID
    username_field = WebDriverWait(driver, 80).until(EC.presence_of_element_located((By.ID, "i0116")))
    username_field.send_keys(username)

    # Locate and click the "Next" button to navigate to the password page
    time.sleep(5)  # Adjust the sleep time as needed
    next_button = WebDriverWait(driver, 80).until(EC.presence_of_element_located((By.ID, "idSIButton9")))
    next_button.click()

    # Locate the password field on the next page
    password_field = WebDriverWait(driver, 80).until(EC.presence_of_element_located((By.ID, "i0118")))
    password_field.send_keys(password)

    # Find and click the login button
    time.sleep(5)  # Adjust the sleep time as needed
    login_button = WebDriverWait(driver, 80).until(EC.element_to_be_clickable((By.ID, "idSIButton9")))
    login_button.click()

# Function to download PDFs
def download_pdfs(spreadsheet_path, output_folder, driver, window):
    df = pd.read_excel(spreadsheet_path)
    df['pdf_link'] = ''

    for index, row in df.iterrows():
        url = row.get('dc.identifier.uri[]')
        if url:
            driver.get(url)

            # Introduce a sleep interval before scraping the page
            time.sleep(5)  # Adjust the sleep time as needed

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            pdf_link_tag = soup.find('a', href=lambda href: href and "Allowed=y" in href)

            if pdf_link_tag:
                final_pdf_link = 'https://rc.library.uta.edu' + pdf_link_tag['href']
                df.at[index, 'pdf_link'] = final_pdf_link

                folder_name = url.split('/')[-1]
                file_name = final_pdf_link.split('/')[-1].split('?')[0]
                folder_path = os.path.join(output_folder, folder_name)

                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

                response = requests.get(final_pdf_link)
                with open(os.path.join(folder_path, file_name), "wb") as f:
                    f.write(response.content)

    df.to_excel(os.path.join(output_folder, 'output.xlsx'), index=False)
    window.write_event_value('-THREAD-', 'Download complete.')

# Function to handle the download process
def start_download_thread(window, spreadsheet_path, output_folder, username, password):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    login_to_website(username, password, driver)
    download_pdfs(spreadsheet_path, output_folder, driver, window)
    driver.quit()

# Define the layout of the UI
layout = [
    [sg.Text("Select Spreadsheet:"), sg.Input(key="spreadsheet"), sg.FileBrowse(file_types=(("Excel files", "*.xlsx"),))],
    [sg.Text("Select Output Folder:"), sg.Input(key="output"), sg.FolderBrowse()],
    [sg.Text("Enter Username:"), sg.Input(key="username")],
    [sg.Text("Enter Password:"), sg.Input(key="password", password_char="*")],
    [sg.Button("Download"), sg.Button("Cancel")],
    [sg.Text("", key="status", size=(40, 1))]
]

# Create the window object
window = sg.Window("PDF/PPT Downloader for UTA Research Commons Data Migration", layout)

# Define the main event loop
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == "Cancel":
        break
    elif event == "Download":
        spreadsheet_path = values["spreadsheet"]
        output_folder = values["output"]
        username = values["username"]
        password = values["password"]

        if spreadsheet_path and output_folder and username and password:
            threading.Thread(target=start_download_thread, args=(window, spreadsheet_path, output_folder, username, password), daemon=True).start()
        else:
            sg.popup("Please enter all the required information.")
    elif event == '-THREAD-':
        window["status"].update(values[event])

window.close()
