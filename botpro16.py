#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IMPERIAL HYBRID VIEWER - OPTIMIZED EDITION
Fixed version with proper error handling and fallback mechanisms
"""

import os
import time
import random
import shutil
import tempfile
import sys
import socket

print("="*60)
print("👑 IMPERIAL HYBRID VIEWER - OPTIMIZED EDITION")
print("="*60)

# ==========================================
# ⚙️ IMPERIAL CONFIGURATION
# ==========================================
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

# ==========================================
# 🔧 SYSTEM SETUP
# ==========================================
def setup_environment():
    """Setup Chrome and dependencies"""
    print("🔧 Setting up environment...")
    
    # Kill existing processes
    os.system("pkill -f chrome 2>/dev/null || true")
    time.sleep(2)
    
    # Check Chrome
    chrome_path = None
    possible_paths = [
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/usr/bin/chromium-browser",
        "/usr/bin/chromium"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            chrome_path = path
            print(f"✅ Chrome found: {chrome_path}")
            break
    
    if not chrome_path:
        print("❌ Chrome not found. Installing...")
        try:
            os.system("apt-get update && apt-get install -y wget")
            os.system("wget -q -O /tmp/chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb")
            os.system("apt-get install -y /tmp/chrome.deb 2>/dev/null || dpkg -i /tmp/chrome.deb 2>/dev/null")
            chrome_path = "/usr/bin/google-chrome"
            print("✅ Chrome installed")
        except:
            print("⚠️ Chrome installation failed")
            return None
    
    return chrome_path

# ==========================================
# 🌍 TOR MANAGEMENT WITH FALLBACK
# ==========================================
def check_tor_connection():
    """Check if TOR is available"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex(("127.0.0.1", 9050))
        sock.close()
        
        if result == 0:
            print("🌍 TOR proxy available on port 9050")
            return True
        else:
            print("⚠️ TOR not available, using direct connection")
            return False
    except:
        print("⚠️ TOR check failed, using direct connection")
        return False

# ==========================================
# 🚀 BROWSER CREATION WITH FALLBACK
# ==========================================
def create_browser(device, use_tor):
    """Create browser with fallback options"""
    profile_dir = tempfile.mkdtemp(prefix="imperial_")
    
    try:
        # Try to import selenium
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
        except ImportError:
            print("📦 Installing selenium...")
            os.system("pip install selenium > /dev/null 2>&1")
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
        
        options = Options()
        
        # Basic options for stability
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--headless=new')
        options.add_argument('--mute-audio')
        options.add_argument(f'--user-data-dir={profile_dir}')
        
        # User agent
        options.add_argument(f'--user-agent={device["ua"]}')
        
        # Window size
        if not device['mobile']:
            options.add_argument(f'--window-size={device["w"]},{device["h"]}')
        
        # Proxy (only if TOR is available)
        if use_tor:
            options.add_argument('--proxy-server=socks5://127.0.0.1:9050')
        
        # Anti-detection
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Mobile emulation for mobile devices
        if device['mobile']:
            mobile_emulation = {
                "deviceMetrics": {"width": device['w'], "height": device['h'], "pixelRatio": 3.0},
                "userAgent": device['ua']
            }
            options.add_experimental_option("mobileEmulation", mobile_emulation)
        
        print(f"  🛠️ Creating browser for {device['name']}...")
        
        # Create driver
        driver = webdriver.Chrome(options=options)
        
        # Set timeouts
        driver.set_page_load_timeout(30)
        
        return driver, profile_dir
        
    except Exception as e:
        print(f"  ❌ Browser creation failed: {e}")
        return None, profile_dir

# ==========================================
# 📺 VIDEO PLAYBACK SYSTEM
# ==========================================
def play_and_watch_video(driver, video_id, session_num):
    """Play video and watch for duration"""
    try:
        # Navigate to video
        url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"  🌐 Loading video {video_id}...")
        
        driver.get(url)
        time.sleep(5)  # Wait for page load
        
        # Check if page loaded
        page_title = driver.title
        print(f"  📄 Page: {page_title[:50]}...")
        
        # Enhanced video playback script
        playback_script = """
        try {
            // Find and play video
            const videos = document.getElementsByTagName('video');
            if (videos.length > 0) {
                const video = videos[0];
                video.muted = true;
                video.playbackRate = 2.0;
                
                const playPromise = video.play();
                if (playPromise !== undefined) {
                    playPromise.then(() => {
                        console.log('Video playing at 2x');
                    }).catch(e => {
                        console.log('Play error:', e);
                    });
                }
                return true;
            }
            return false;
        } catch(e) {
            console.log('Player error:', e);
            return false;
        }
        """
        
        # Execute playback
        result = driver.execute_script(playback_script)
        
        if result:
            print(f"  ✅ Video playing at 2x speed")
        else:
            print(f"  ⚠️ Video auto-play may need manual intervention")
        
        # Watch time
        watch_time = random.randint(120, 300)  # 2-5 minutes
        print(f"  ⏱️ Watching for {watch_time} seconds...")
        
        # Watch loop with interactions
        start_time = time.time()
        last_progress = 0
        
        while time.time() - start_time < watch_time:
            elapsed = int(time.time() - start_time)
            
            # Show progress every 30 seconds
            if elapsed >= last_progress + 30:
                print(f"  📊 Progress: {elapsed}/{watch_time}s")
                last_progress = elapsed
                
                # Random interaction
                if random.random() < 0.3:  # 30% chance
                    scroll_amount = random.randint(-100, 200)
                    driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            
            # Auto-skip ads
            try:
                driver.execute_script("""
                    const skipBtn = document.querySelector('.ytp-ad-skip-button');
                    if (skipBtn) skipBtn.click();
                """)
            except:
                pass
            
            time.sleep(1)
        
        print(f"  ✅ Session {session_num} completed")
        return True
        
    except Exception as e:
        print(f"  ❌ Video playback error: {str(e)[:80]}")
        return False

# ==========================================
# 📊 STATISTICS TRACKING
# ==========================================
class SessionStats:
    def __init__(self):
        self.total_sessions = 0
        self.successful_sessions = 0
        self.failed_sessions = 0
        self.start_time = time.time()
    
    def add_session(self, success):
        self.total_sessions += 1
        if success:
            self.successful_sessions += 1
        else:
            self.failed_sessions += 1
    
    def print_stats(self):
        elapsed = time.time() - self.start_time
        if self.total_sessions > 0:
            success_rate = (self.successful_sessions / self.total_sessions) * 100
        else:
            success_rate = 0
        
        print(f"\n📊 Statistics: {self.successful_sessions}/{self.total_sessions} successful ({success_rate:.1f}%)")
        print(f"⏱️ Elapsed: {elapsed//60:.0f}m {elapsed%60:.0f}s")

# ==========================================
# 🚀 MAIN EXECUTION
# ==========================================
def main():
    """Main execution function"""
    
    # Setup Chrome
    chrome_path = setup_environment()
    if not chrome_path:
        print("❌ Cannot continue without Chrome")
        return
    
    # Check TOR
    use_tor = check_tor_connection()
    
    # Statistics
    stats = SessionStats()
    
    print(f"\n🎯 Starting Imperial viewing sessions")
    print(f"🌍 TOR enabled: {use_tor}")
    print(f"📱 Devices available: {len(DEVICES)}")
    print(f"📺 Videos in pool: {len(VIDEOS_POOL)}")
    print("\nPress Ctrl+C to stop\n")
    
    session_num = 1
    
    try:
        while True:
            print(f"\n{'='*50}")
            print(f"🚀 IMPERIAL SESSION #{session_num}")
            print(f"{'='*50}")
            
            # Select device and video
            device = random.choice(DEVICES)
            video = random.choice(VIDEOS_POOL)
            
            print(f"📱 Device: {device['name']}")
            print(f"📺 Video: {video['keywords']}")
            
            # Create browser
            driver, profile_dir = create_browser(device, use_tor)
            
            success = False
            if driver:
                try:
                    # Play and watch video
                    success = play_and_watch_video(driver, video['id'], session_num)
                finally:
                    # Cleanup
                    try:
                        driver.quit()
                    except:
                        pass
                    
                    if os.path.exists(profile_dir):
                        shutil.rmtree(profile_dir, ignore_errors=True)
            else:
                print("  ❌ Skipping session due to browser failure")
            
            # Update statistics
            stats.add_session(success)
            stats.print_stats()
            
            session_num += 1
            
            # Cooldown before next session
            if success:
                cooldown = random.randint(10, 20)
            else:
                cooldown = random.randint(5, 10)
            
            print(f"\n⏳ Next session in {cooldown} seconds...")
            time.sleep(cooldown)
    
    except KeyboardInterrupt:
        print("\n\n🛑 Stopped by user")
    
    # Final statistics
    print("\n" + "="*60)
    print("📊 FINAL STATISTICS")
    print("="*60)
    print(f"Total sessions: {stats.total_sessions}")
    print(f"Successful: {stats.successful_sessions}")
    print(f"Failed: {stats.failed_sessions}")
    
    if stats.total_sessions > 0:
        success_rate = (stats.successful_sessions / stats.total_sessions) * 100
        print(f"Success rate: {success_rate:.1f}%")
    
    elapsed = time.time() - stats.start_time
    print(f"Total time: {elapsed//60:.0f}m {elapsed%60:.0f}s")
    print("="*60)
    print("\n👑 Imperial mission complete!")

# ==========================================
# ENTRY POINT
# ==========================================
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Critical error: {e}")
        print("Please check your Chrome installation and try again.")
