from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import os
import time
from PIL import Image
import io

currencies = {
    "vnd_1000": "tờ 1000 đồng",
}

base_dir = "vnd_currency"
os.makedirs(base_dir, exist_ok=True)

target_images = 20
min_width = 180
min_height = 180

# Thiết lập Selenium
options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def check_image_size(image_data):
    try:
        with Image.open(io.BytesIO(image_data)) as img:
            width, height = img.size
            return width >= min_width and height >= min_height
    except Exception as e:
        print(f"Lỗi khi kiểm tra kích thước: {e}")
        return False

try:
    for folder_name, keyword in currencies.items():
        save_dir = os.path.join(base_dir, folder_name)
        os.makedirs(save_dir, exist_ok=True)

        downloaded_images = 0
        print(f"\n🔍 Bắt đầu crawl hình ảnh cho: {keyword}")
        url = f"https://www.google.com/search?tbm=isch&q={keyword.replace(' ', '+')}"
        driver.get(url)

        # Cuộn để load thêm ảnh
        for _ in range(25):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        img_tags = soup.find_all("img")
        print(f"📸 Tìm thấy {len(img_tags)} ảnh trên trang")

        for i, img in enumerate(img_tags):
            if downloaded_images >= target_images:
                break

            img_url = img.get("src") or img.get("data-src")
            if img_url and img_url.startswith("http"):
                try:
                    headers = {"User-Agent": "Mozilla/5.0"}
                    response = requests.get(img_url, headers=headers, timeout=10)
                    response.raise_for_status()
                    img_data = response.content

                    if check_image_size(img_data):
                        img_name = f"{folder_name}_{downloaded_images}.jpg"
                        img_path = os.path.join(save_dir, img_name)
                        with open(img_path, "wb") as f:
                            f.write(img_data)
                        print(f"✅ Đã lưu: {img_name}")
                        downloaded_images += 1
                    else:
                        print(f"⚠️ Bỏ qua ảnh vì kích thước nhỏ: {img_url}")

                except Exception as e:
                    print(f"❌ Lỗi tải ảnh {img_url}: {e}")
                    continue

        print(f"🎯 Đã tải {downloaded_images} ảnh cho {keyword}")

finally:
    driver.quit()

print("\n✅ Hoàn tất crawl toàn bộ!")