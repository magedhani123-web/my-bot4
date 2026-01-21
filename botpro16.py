import time
import random
import os
import shutil
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# --- [ الإعدادات الأساسية ] ---
SEARCH_KEYWORDS = "وش الحلم اللي حققته" 
VIDEO_ID = "MrKhyV4Gcog"
DIRECT_URL = f"https://youtube.com/shorts/{VIDEO_ID}"
TOR_PROXY = "socks5://127.0.0.1:9050"

# --- [ مكتبة الأنظمة الشاملة ] ---
DEVICES = [
    # --- iOS Devices (iPhones & iPads) ---
    {"name": "iPhone 16 Pro Max", "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1", "plat": "iPhone", "w": 430, "h": 932, "gpu": "Apple GPU"},
    {"name": "iPhone 15 Pro", "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1", "plat": "iPhone", "w": 393, "h": 852, "gpu": "Apple GPU"},
    {"name": "iPhone 14", "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1", "plat": "iPhone", "w": 390, "h": 844, "gpu": "Apple GPU"},
    {"name": "iPhone 13 Mini", "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1", "plat": "iPhone", "w": 375, "h": 812, "gpu": "Apple GPU"},
    {"name": "iPad Pro 12.9 M2", "ua": "Mozilla/5.0 (iPad; CPU OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1", "plat": "MacIntel", "w": 1024, "h": 1366, "gpu": "Apple M2 GPU"},
    {"name": "iPad Air (Gen 5)", "ua": "Mozilla/5.0 (iPad; CPU OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1", "plat": "MacIntel", "w": 820, "h": 1180, "gpu": "Apple M1 GPU"},

    # --- Android High-End ---
    {"name": "Samsung Galaxy S24 Ultra", "ua": "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.64 Mobile Safari/537.36", "plat": "Linux armv8l", "w": 384, "h": 854, "gpu": "Adreno 750"},
    {"name": "Samsung Galaxy S23 Ultra", "ua": "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36", "plat": "Linux armv8l", "w": 360, "h": 800, "gpu": "Adreno 740"},
    {"name": "Google Pixel 9 Pro", "ua": "Mozilla/5.0 (Linux; Android 15; Pixel 9 Pro Build/AD1A.240530.019) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.103 Mobile Safari/537.36", "plat": "Linux aarch64", "w": 412, "h": 915, "gpu": "Mali-G715"},
    {"name": "Google Pixel 8 Pro", "ua": "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.164 Mobile Safari/537.36", "plat": "Linux aarch64", "w": 412, "h": 892, "gpu": "Mali-G715"},
    {"name": "Xiaomi 14 Ultra", "ua": "Mozilla/5.0 (Linux; Android 14; 24030PN60G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.119 Mobile Safari/537.36", "plat": "Linux armv8l", "w": 393, "h": 873, "gpu": "Adreno 750"},
    {"name": "OnePlus 12", "ua": "Mozilla/5.0 (Linux; Android 14; CPH2581) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36", "plat": "Linux armv8l", "w": 384, "h": 854, "gpu": "Adreno 750"},

    # --- Android Mid-Range & Others ---
    {"name": "Samsung Galaxy A54", "ua": "Mozilla/5.0 (Linux; Android 13; SM-A546B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36", "plat": "Linux armv8l", "w": 360, "h": 800, "gpu": "Mali-G68"},
    {"name": "Nothing Phone (2)", "ua": "Mozilla/5.0 (Linux; Android 13; A065) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36", "plat": "Linux armv8l", "w": 412, "h": 915, "gpu": "Adreno 730"},
    {"name": "Samsung Galaxy Tab S9", "ua": "Mozilla/5.0 (Linux; Android 13; SM-X710) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36", "plat": "Linux armv8l", "w": 800, "h": 1280, "gpu": "Adreno 740"},

    # --- Desktop Devices (Windows, Mac, Linux) ---
    {"name": "Windows 11 PC (Chrome)", "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36", "plat": "Win32", "w": 1920, "h": 1080, "gpu": "NVIDIA GeForce RTX 4090"},
    {"name": "Windows 11 PC (Edge)", "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/124.0.0.0 Edg/124.0.0.0", "plat": "Win32", "w": 2560, "h": 1440, "gpu": "NVIDIA GeForce RTX 3080"},
    {"name": "MacBook Pro M3", "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36", "plat": "MacIntel", "w": 1728, "h": 1117, "gpu": "Apple M3 Max GPU"},
    {"name": "MacBook Air M2", "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36", "plat": "MacIntel", "w": 1440, "h": 900, "gpu": "Apple M2 GPU"},
    {"name": "Linux Desktop (Ubuntu/Firefox)", "ua": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0", "plat": "Linux x86_64", "w": 1920, "h": 1080, "gpu": "AMD Radeon RX 7900 XT"}
]


def get_current_ip():
    proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
    try: return requests.get('https://api.ipify.org', proxies=proxies, timeout=10).text
    except: return "Unknown"

def inject_ultra_stealth(driver, dev):
    """تزييف الهوية والمنطقة الزمنية والحساسات"""
    tz = random.choice(['America/New_York', 'Europe/Paris', 'Asia/Dubai', 'Asia/Riyadh', 'Europe/London'])
    js = f"""
    Object.defineProperty(navigator, 'webdriver', {{get: () => undefined}});
    Object.defineProperty(navigator, 'platform', {{get: () => '{dev["plat"]}'}});
    Object.defineProperty(Intl.DateTimeFormat().resolvedOptions(), 'timeZone', {{value: '{tz}'}});
    
    // تزييف البطارية
    navigator.getBattery = () => Promise.resolve({{charging: true, level: {random.uniform(0.6, 0.9)}}});

    const getParam = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = function(p) {{
        if (p === 37446) return '{dev["gpu"]}';
        return getParam.apply(this, arguments);
    }};
    """
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})

def run_imperial_session(count):
    dev = random.choice(DEVICES)
    print(f"\n--- 👑 الجلسة {count} | الجهاز: {dev['name']} ---")
    print(f"🌍 IP: {get_current_ip()}")

    options = uc.ChromeOptions()
    p_dir = os.path.abspath(f"imperial_session_{random.randint(1000, 9999)}")
    options.add_argument(f'--user-data-dir={p_dir}')
    options.add_argument(f'--user-agent={dev["ua"]}')
    options.add_argument(f'--proxy-server={TOR_PROXY}')
    options.add_argument(f"--window-size={dev['w']},{dev['h']}")
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    try:
        driver = uc.Chrome(options=options, use_subprocess=True)
        inject_ultra_stealth(driver, dev)
        wait = WebDriverWait(driver, 25)

        # 1. الدخول عبر البحث
        driver.get("https://www.youtube.com")
        time.sleep(5)
        try:
            agree = driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Agree') or contains(@aria-label, 'موافق')]")
            if agree: agree[0].click()
            
            search_box = wait.until(EC.element_to_be_clickable((By.NAME, "search_query")))
            for char in SEARCH_KEYWORDS:
                search_box.send_keys(char)
                time.sleep(random.uniform(0.1, 0.2))
            search_box.send_keys(Keys.ENTER)
            time.sleep(5)
            wait.until(EC.element_to_be_clickable((By.XPATH, f"//a[contains(@href, '{VIDEO_ID}')]"))).click()
        except: driver.get(DIRECT_URL)

        # 2. المشاهدة مع تغيير السرعة العشوائي
        video = wait.until(EC.presence_of_element_located((By.TAG_NAME, "video")))
        driver.execute_script("arguments[0].play();", video)
        
        # ميزة تغيير السرعة
        random_speed = random.choice([0.75, 1.0, 1.25, 1.5])
        driver.execute_script(f"arguments[0].playbackRate = {random_speed};", video)
        print(f"⚡ السرعة الحالية: {random_speed}x")

        watch_time = random.randint(65, 95)
        print(f"📺 مشاهدة جارية لـ {watch_time} ثانية...")
        
        # حركات بشرية (Scroll)
        time.sleep(watch_time // 2)
        driver.execute_script(f"window.scrollBy(0, {random.randint(200, 600)});")
        
        # إعادة السرعة للطبيعية في منتصف المشاهدة
        time.sleep(5)
        driver.execute_script("arguments[0].playbackRate = 1.0;", video)

        # 3. التفاعل (لايك ومشاركة)
        if random.random() < 0.55:
            try:
                driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//button[contains(@aria-label, 'like') or contains(@aria-label, 'إعجاب')]"))
                print("👍 لايك")
                time.sleep(2)
                driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Share') or contains(@aria-label, 'مشاركة')]"))
                ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                print("🔗 مشاركة")
            except: pass

        print(f"✅ اكتملت المهمة.")

    except Exception as e:
        print(f"❌ خطأ: {str(e)[:50]}")
    finally:
        driver.quit()
        if p_dir: shutil.rmtree(p_dir, ignore_errors=True)

if __name__ == "__main__":
    os.system("pkill -f chrome")
    for i in range(500): # عدد الجلسات
        run_imperial_session(i + 1)
        time.sleep(random.randint(20, 45))
