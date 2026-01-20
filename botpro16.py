#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
👑 ULTIMATE IMPERIAL VIEWER - MILLION SESSIONS EDITION (UPDATED)
الميزات المضافة: التحكم في الصوت، بطارية مخصصة، تخطي شاشة الموافقة، ومشاهدة مقترحة 20 ثانية.
"""

import os
import time
import random
import shutil
import tempfile
import sys
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# ==========================================
# ⚙️ الإعدادات الكبرى
# ==========================================
MAX_SESSIONS = 1000000 
TOR_PROXY = "socks5://127.0.0.1:9050"

DEVICES = [
    {"name": "iPhone 16 Pro Max", "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1", "plat": "iPhone", "w": 430, "h": 932, "mobile": True},
    {"name": "iPhone 15 Pro", "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1", "plat": "iPhone", "w": 393, "h": 852, "mobile": True},
    {"name": "Samsung Galaxy S24 Ultra", "ua": "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.64 Mobile Safari/537.36", "plat": "Linux armv8l", "w": 384, "h": 854, "mobile": True},
    {"name": "Samsung Galaxy S23 Ultra", "ua": "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36", "plat": "Linux armv8l", "w": 360, "h": 800, "mobile": True},
    {"name": "Google Pixel 9 Pro", "ua": "Mozilla/5.0 (Linux; Android 15; Pixel 9 Pro Build/AD1A.240530.019) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.103 Mobile Safari/537.36", "plat": "Linux aarch64", "w": 412, "h": 915, "mobile": True},
    {"name": "Huawei Mate 60 Pro", "ua": "Mozilla/5.0 (Linux; Android 12; ALN-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36", "plat": "Linux aarch64", "w": 412, "h": 915, "mobile": True},
    {"name": "Xiaomi 14 Ultra", "ua": "Mozilla/5.0 (Linux; Android 14; 24030PN60G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.119 Mobile Safari/537.36", "plat": "Linux armv8l", "w": 393, "h": 873, "mobile": True},
    {"name": "Windows 11 PC", "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36", "plat": "Win32", "w": 1920, "h": 1080, "mobile": False},
    {"name": "MacBook Pro (macOS)", "ua": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36", "plat": "MacIntel", "w": 1440, "h": 900, "mobile": False}
]

VIDEOS_POOL = [
    {"id": "MrKhyV4Gcog", "keywords": "وش الحلم اللي حققته"},
    {"id": "bmgpC4lGSuQ", "keywords": "أجمل جزيرة في العالم سقطرى"},
    {"id": "6hYLIDz-RRM", "keywords": "هنا اختلفنا وفارقنا علي شان"},
    {"id": "AvH9Ig3A0Qo", "keywords": "Socotra treasure island"}
]

def show_current_ip():
    try:
        proxies = {'http': TOR_PROXY, 'https': TOR_PROXY}
        ip = requests.get('https://api.ipify.org', proxies=proxies, timeout=15).text
        print(f"🌍 IP النشط حالياً: {ip}")
        return ip
    except:
        return None

def apply_advanced_stealth(driver, device):
    # تحسين البطارية حسب القيم المطلوبة بالضبط
    batt_level = random.choice([1.0, 0.45, 0.78, 0.34, 0.62, 0.80, 0.25])
    net_speed = random.choice([15, 30, 50, 100])
    lat, lon = random.uniform(24.0, 48.0), random.uniform(35.0, 58.0)
    
    js = f"""
    Object.defineProperty(navigator, 'webdriver', {{get: () => undefined}});
    if (navigator.getBattery) {{
        navigator.getBattery = () => Promise.resolve({{
            charging: true, level: {batt_level}, chargingTime: 0, dischargingTime: Infinity
        }});
    }}
    Object.defineProperty(navigator, 'connection', {{
        get: () => ({{ effectiveType: '4g', downlink: {net_speed}, rtt: 50 }})
    }});
    navigator.geolocation.getCurrentPosition = (s) => s({{ coords: {{ latitude: {lat}, longitude: {lon}, accuracy: 10 }} }});
    """
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})

def run_session(session_num):
    os.system("pkill -f chrome 2>/dev/null || true")
    device = random.choice(DEVICES)
    video = random.choice(VIDEOS_POOL)
    
    print(f"\n🚀 الجلسة الإمبراطورية #{session_num}")
    show_current_ip()
    
    profile_dir = tempfile.mkdtemp(prefix="imperial_")
    options = uc.ChromeOptions()
    options.add_argument(f'--user-data-dir={profile_dir}')
    options.add_argument(f'--user-agent={device["ua"]}')
    options.add_argument(f'--proxy-server={TOR_PROXY}')
    options.add_argument(f"--window-size={device['w']},{device['h']}")
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    try:
        driver = uc.Chrome(options=options, use_subprocess=True)
        apply_advanced_stealth(driver, device)
        wait = WebDriverWait(driver, 30)

        # 1. تخطي شاشة الموافقة (Consent Screen Bypass)
        driver.get("https://www.youtube.com")
        time.sleep(5)
        try:
            # البحث عن أزرار الموافقة في نافذة الكوكيز (كما في صورك)
            consent_btns = driver.find_elements(By.XPATH, "//button[contains(.,'Accept all') or contains(.,'موافق') or contains(.,'I agree')]")
            if consent_btns:
                consent_btns[0].click()
                print("🛡️ تم تخطي شاشة الموافقة بنجاح.")
        except: pass

        # 2. البحث والتشغيل
        try:
            search_box = wait.until(EC.presence_of_element_located((By.NAME, "search_query")))
            for char in video['keywords']:
                search_box.send_keys(char)
                time.sleep(0.1)
            search_box.send_keys(Keys.ENTER)
            video_el = wait.until(EC.element_to_be_clickable((By.XPATH, f"//a[contains(@href, '{video['id']}')]")))
            video_el.click()
        except:
            driver.get(f"https://www.youtube.com/watch?v={video['id']}")

        # 3. فتح الصوت وتشغيل الفيديو
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "video")))
        # تفعيل الصوت عند البدء
        driver.execute_script("document.querySelector('video').muted = false; document.querySelector('video').volume = 0.5;")
        print("🔊 تم فتح الصوت للجلسة الحالية.")
        
        speed = random.choice([1.25, 1.5, 2.0])
        driver.execute_script(f"document.querySelector('video').playbackRate = {speed};")
        driver.execute_script("document.querySelector('video').play();")

        # 4. المشاهدة
        watch_time = random.randint(110, 180)
        time.sleep(watch_time)
        
        # كتم الصوت عند الانتهاء من الفيديو الأساسي
        driver.execute_script("document.querySelector('video').muted = true;")
        print("🔇 تم كتم الصوت بعد انتهاء المشاهدة الأساسية.")

        # 5. مشاهدة فيديو مقترح لمدة 20 ثانية بالضبط
        print("🔗 الانتقال لمشاهدة فيديو مقترح لـ 20 ثانية...")
        try:
            suggestions = driver.find_elements(By.CSS_SELECTOR, "a.ytd-thumbnail, a.yt-simple-endpoint.inline-block.ytd-thumbnail")
            if suggestions:
                suggestions[0].click()
                time.sleep(20) # مدة المشاهدة المطلوبة للفيديو المقترح
                print("✅ اكتملت مشاهدة الفيديو المقترح.")
        except: pass

        print(f"✅ اكتملت الجلسة {session_num} بنجاح.")
        driver.quit()

    except Exception as e:
        print(f"❌ تعثرت الجلسة: {str(e)[:50]}")
    finally:
        if os.path.exists(profile_dir):
            shutil.rmtree(profile_dir, ignore_errors=True)

if __name__ == "__main__":
    for i in range(1, MAX_SESSIONS + 1):
        run_session(i)
        time.sleep(random.randint(5, 10))
        if os.path.exists("stop.txt"): break
