from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

# Setup Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--headless")  # Uncomment to run without opening a browser

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    data = []
    total_projects = 6  # Number of projects to extract

    for idx in range(total_projects):
        driver.get("https://rera.odisha.gov.in/projects/project-list")

        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, "View Details"))
        )

        view_links = driver.find_elements(By.PARTIAL_LINK_TEXT, "View Details")

        if idx >= len(view_links):
            print(f"Only {len(view_links)} projects found.")
            break

        link = view_links[idx]
        driver.execute_script("arguments[0].scrollIntoView(true);", link)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", link)

        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "project-details"))
        )
        time.sleep(2)

        # Fixed get_value function to get <strong> after <label>
        def get_value(label):
            try:
                label_elem = driver.find_element(By.XPATH, f"//label[contains(text(), '{label}')]")
                parent_div = label_elem.find_element(By.XPATH, "./..")
                strong_elem = parent_div.find_element(By.TAG_NAME, "strong")
                value = strong_elem.text.strip()
                return value if value and value != "--" else "N/A"
            except Exception as e:
                print(f"❌ Could not extract '{label}':", e)
                return "N/A"

        print(f"\nFetching data for project: {idx+1}")

        # Project Overview tab
        rera_no = get_value("RERA Regd. No.")
        project_name = get_value("Project Name")

        # Switch to Promoter Details tab
        try:
            promoter_tab = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Promoter Details')]"))
            )
            promoter_tab.click()
            time.sleep(2)
        except Exception as e:
            print("❌ Could not open Promoter Details tab:", e)

        promoter_name = get_value("Company Name")
        promoter_address = get_value("Registered Office Address")
        gst_no = get_value("GST No.")

        print("RERA No:", rera_no)
        print("Project Name:", project_name)
        print("Promoter Name:", promoter_name)
        print("Promoter Address:", promoter_address)
        print("GST No:", gst_no)

        data.append({
            "RERA No": rera_no,
            "Project Name": project_name,
            "Promoter Name": promoter_name,
            "Promoter Address": promoter_address,
            "GST No": gst_no
        })

        # Close modal
        try:
            close_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'close') or contains(text(),'×')]"))
            )
            close_btn.click()
        except:
            body = driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.ESCAPE)
            time.sleep(1)

        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "project-details"))
        )

    # Save to CSV
    if data:
        with open("odisha_rera_projects.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        print("\n✅ Data saved to 'odisha_rera_projects.csv'")
    else:
        print("\n⚠️ No data extracted.")

finally:
    driver.quit()
