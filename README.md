# UTA Research Commons Data Migration Tool

## Description
This tool is designed to facilitate the process of downloading PDF/PPT files from the UTA Research Commons website. It utilizes a combination of Python libraries including Selenium, BeautifulSoup, and PySimpleGUI to automate the web browsing process, parse HTML content, and provide a user-friendly interface. The tool was created to bypass the issue of access control to emargoed items while migrating the data to BePress. Manually downloading each full_text file of every paper/item and palce them into their respective folder with the item number would take up atleast months approx 720hours of work time. So, in order to cut it down to a few hours this tool is developed and it uses a combination of data scraping techniques,excel and os based python automation techniques to automate the whole process. For easier operation a GUI is developed on the fronted all using python.

## Features
- **Automated Login:** Automates the login process to the UTA Research Commons website.
- **Spreadsheet Integration:** Reads URLs from an Excel spreadsheet and processes each link.
- **PDF/PPT Download:** Automatically downloads PDF/PPT files from the provided URLs.
- **User Interface:** Provides a simple and intuitive GUI for easy operation.

## Installation

To use this tool, you need to have Python installed on your system along with the necessary libraries. Follow these steps to set up the environment:

1. **Install Python:** Download and install Python from [python.org](https://www.python.org/).

2. **Install Required Libraries:** Open your command prompt or terminal and install the required libraries using pip:
   ```bash
   pip install PySimpleGUI pandas selenium bs4 requests webdriver_manager
   ```

## Usage

1. **Start the Application:** Run the script to open the GUI.

2. **Input Details:**
   - **Select Spreadsheet:** Choose the Excel file containing the list of URLs for the PDF/PPT files.
   - **Select Output Folder:** Choose a directory where the downloaded files will be saved.
   - **Enter Username and Password:** Provide your UTA Research Commons Admin login credentials.

3. **Begin Download:** Click on the 'Download' button to start the downloading process. 

## Working Principle

- **Login to Website:** The script logs into the UTA Research Commons using the provided credentials.
- **Read Spreadsheet:** URLs are read from the provided Excel spreadsheet.
- **Scrape and Download:** For each URL, the script navigates to the web page, scrapes the PDF/PPT link, and downloads the file to the specified output folder.

## Output

- The downloaded PDF/PPT files are saved in the specified output folder.
- An updated Excel file `output.xlsx` is created in the output folder with links to the downloaded files.

## Disclaimer

- This tool is intended for authorized users of the UTA Research Commons only.
- Ensure that you have the right to download and use the content from the website.

## Contribution

Feel free to fork this repository and contribute to its development. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)

---

For any issues or suggestions, please contact the repository owner.
