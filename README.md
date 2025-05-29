# 🏗️ Odisha RERA Project Scraper

This Python script scrapes the first 6 registered real estate projects from the [Odisha RERA website](https://rera.odisha.gov.in/projects/project-list), collecting key information from each project’s detail page.

## 📌 Features

- Scrapes the following fields from each project:
  - **RERA Regd. No**
  - **Project Name**
  - **Promoter Name** (Company Name)
  - **Promoter Address** (Registered Office Address)
  - **GST No**
- Navigates through project detail modals
- Switches to the "Promoter Details" tab to collect relevant data
- Saves the extracted data in a `CSV` file

## 💻 Requirements

Create a `requirements.txt` with the following content:

```
selenium
webdriver-manager
```

Install the dependencies using:

```
pip install -r requirements.txt
```

## 🚀 How to Run

1. Clone this repository or copy the project files.
2. Ensure [Google Chrome](https://www.google.com/chrome/) is installed on your system.
3. Run the script using Python:

```
python odisha_rera_scraper.py
```

4. After execution, a file named `odisha_rera_projects.csv` will be created with the scraped data.

## 📂 Output

Example `CSV` structure:

| RERA No | Project Name | Promoter Name | Promoter Address | GST No |
|---------|--------------|----------------|-------------------|--------|
| ...     | ...          | ...            | ...               | ...    |

## 🛠 Notes

- For **headless scraping**, uncomment the `--headless` line in the script.
- If you are running this on a Linux server, you may need to install extra dependencies (e.g., `libnss3`, `libgconf-2-4`, etc.).
- Make sure you have stable internet access while scraping.
