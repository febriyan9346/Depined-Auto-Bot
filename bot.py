import os
import time
import random
from datetime import datetime
import pytz
from colorama import Fore, Style, init
import requests
import json
from typing import Optional, Dict, List

os.system('clear' if os.name == 'posix' else 'cls')

import warnings
warnings.filterwarnings('ignore')

import sys
if not sys.warnoptions:
    import os
    os.environ["PYTHONWARNINGS"] = "ignore"

init(autoreset=True)

class TwoCaptchaSolver:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.2captcha.com"
    
    def solve_turnstile(self, website_url: str, website_key: str, log_func) -> Optional[str]:
        log_func("Solving Cloudflare Turnstile captcha...", "INFO")
        
        create_task = {
            "clientKey": self.api_key,
            "task": {
                "type": "TurnstileTaskProxyless",
                "websiteURL": website_url,
                "websiteKey": website_key
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/createTask",
                json=create_task,
                timeout=30
            )
            result = response.json()
            
            if result.get("errorId") != 0:
                log_func(f"Error creating task: {result.get('errorDescription')}", "ERROR")
                return None
            
            task_id = result.get("taskId")
            
            for _ in range(60):
                time.sleep(3)
                
                get_result = {
                    "clientKey": self.api_key,
                    "taskId": task_id
                }
                
                response = requests.post(
                    f"{self.base_url}/getTaskResult",
                    json=get_result,
                    timeout=30
                )
                result = response.json()
                
                if result.get("status") == "ready":
                    token = result.get("solution", {}).get("token")
                    log_func("Captcha solved successfully!", "SUCCESS")
                    return token
                elif result.get("errorId") != 0:
                    log_func(f"Error: {result.get('errorDescription')}", "ERROR")
                    return None
            
            log_func("Timeout waiting for captcha", "ERROR")
            return None
            
        except Exception as e:
            log_func(f"Error solving captcha: {str(e)}", "ERROR")
            return None


class DepinedBot:
    def __init__(self):
        self.captcha_solver = None
        self.api_key = None
        self.use_proxy = False
        self.accounts = []
        self.proxies = []
        
    def get_wib_time(self):
        wib = pytz.timezone('Asia/Jakarta')
        return datetime.now(wib).strftime('%H:%M:%S')
    
    def print_banner(self):
        banner = f"""
{Fore.CYAN}DEPINED AUTO BOT{Style.RESET_ALL}
{Fore.WHITE}By: FEBRIYAN{Style.RESET_ALL}
{Fore.CYAN}============================================================{Style.RESET_ALL}
"""
        print(banner)
    
    def log(self, message, level="INFO"):
        time_str = self.get_wib_time()
        
        if level == "INFO":
            color = Fore.CYAN
            symbol = "[INFO]"
        elif level == "SUCCESS":
            color = Fore.GREEN
            symbol = "[SUCCESS]"
        elif level == "ERROR":
            color = Fore.RED
            symbol = "[ERROR]"
        elif level == "WARNING":
            color = Fore.YELLOW
            symbol = "[WARNING]"
        elif level == "CYCLE":
            color = Fore.MAGENTA
            symbol = "[CYCLE]"
        else:
            color = Fore.WHITE
            symbol = "[LOG]"
        
        print(f"[{time_str}] {color}{symbol} {message}{Style.RESET_ALL}")
    
    def random_delay(self, min_sec=1, max_sec=5):
        delay = random.randint(min_sec, max_sec)
        time.sleep(delay)
    
    def show_menu(self):
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Select Mode:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1. Run with proxy")
        print(f"2. Run without proxy{Style.RESET_ALL}")
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        
        while True:
            try:
                choice = input(f"{Fore.GREEN}Enter your choice (1/2): {Style.RESET_ALL}").strip()
                if choice in ['1', '2']:
                    return choice
                else:
                    print(f"{Fore.RED}Invalid choice! Please enter 1 or 2.{Style.RESET_ALL}")
            except KeyboardInterrupt:
                print(f"\n{Fore.RED}Program terminated by user.{Style.RESET_ALL}")
                exit(0)
    
    def countdown(self, seconds):
        for i in range(seconds, 0, -1):
            hours = i // 3600
            minutes = (i % 3600) // 60
            secs = i % 60
            print(f"\r[COUNTDOWN] Next cycle in: {hours:02d}:{minutes:02d}:{secs:02d} ", end="", flush=True)
            time.sleep(1)
        print("\r" + " " * 60 + "\r", end="", flush=True)
    
    def load_file(self, filename: str) -> List[str]:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            return []
    
    def load_config(self):
        api_keys = self.load_file('2captcha.txt')
        if not api_keys:
            self.log("2captcha.txt is empty or not found!", "ERROR")
            return False
        
        self.api_key = api_keys[0]
        self.captcha_solver = TwoCaptchaSolver(self.api_key)
        self.log(f"API Key loaded", "SUCCESS")
        
        self.accounts = self.load_file('accounts.txt')
        if not self.accounts:
            self.log("accounts.txt is empty or not found!", "ERROR")
            return False
        
        self.log(f"Loaded {len(self.accounts)} accounts successfully", "SUCCESS")
        
        self.proxies = self.load_file('proxy.txt')
        if self.proxies:
            self.log(f"Loaded {len(self.proxies)} proxies", "SUCCESS")
        
        return True
    
    def login(self, email: str, password: str, proxy: Optional[str] = None) -> Optional[str]:
        session = requests.Session()
        session.headers.update({
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://app.depined.org',
            'referer': 'https://app.depined.org/',
            'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'
        })
        
        if proxy and self.use_proxy:
            session.proxies = {
                'http': proxy,
                'https': proxy
            }
        
        website_url = "https://app.depined.org/"
        website_key = "0x4AAAAAAA_n_DLiban-lfA5"
        
        captcha_token = self.captcha_solver.solve_turnstile(website_url, website_key, self.log)
        
        if not captcha_token:
            return None
        
        login_data = {
            "email": email,
            "password": password,
            "cf-turnstile-response": captcha_token
        }
        
        try:
            response = session.post(
                "https://api.depined.org/api/user/login",
                json=login_data,
                timeout=30
            )
            
            if response.status_code != 200:
                self.log(f"Login failed with status code: {response.status_code}", "ERROR")
                return None
            
            result = response.json()
            
            if result.get("status") and result.get("code") == 200:
                token = result.get("data", {}).get("token")
                self.log("Login successful!", "SUCCESS")
                return token
            else:
                self.log(f"Login failed: {result.get('message')}", "ERROR")
                return None
                
        except requests.exceptions.RequestException as e:
            self.log(f"Network error: {str(e)}", "ERROR")
            return None
        except Exception as e:
            self.log(f"Error login: {str(e)}", "ERROR")
            return None
    
    def get_profile(self, token: str, proxy: Optional[str] = None) -> Optional[Dict]:
        session = requests.Session()
        
        if proxy and self.use_proxy:
            session.proxies = {
                'http': proxy,
                'https': proxy
            }
        
        headers = {
            'accept': 'application/json, text/plain, */*',
            'authorization': f'Bearer {token}',
            'origin': 'https://app.depined.org',
            'referer': 'https://app.depined.org/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        try:
            response = session.get(
                "https://api.depined.org/api/user/overview/profile",
                headers=headers,
                timeout=30
            )
            
            result = response.json()
            
            if result.get("status"):
                return result.get("data")
            
            return None
            
        except Exception as e:
            self.log(f"Error get profile: {str(e)}", "ERROR")
            return None
    
    def widget_connect(self, token: str, proxy: Optional[str] = None) -> bool:
        session = requests.Session()
        
        if proxy and self.use_proxy:
            session.proxies = {
                'http': proxy,
                'https': proxy
            }
        
        headers = {
            'accept': '*/*',
            'authorization': f'Bearer {token}',
            'content-type': 'application/json',
            'origin': 'chrome-extension://pjlappmodaidbdjhmhifbnnmmkkicjoc',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        try:
            response = session.post(
                "https://api.depined.org/api/user/widget-connect",
                json={"connected": True},
                headers=headers,
                timeout=30
            )
            
            result = response.json()
            
            if result.get("status") and result.get("code") == 200:
                return True
            
            return False
            
        except Exception as e:
            self.log(f"Error widget connect: {str(e)}", "ERROR")
            return False
    
    def get_epoch_earnings(self, token: str, proxy: Optional[str] = None) -> Optional[Dict]:
        session = requests.Session()
        
        if proxy and self.use_proxy:
            session.proxies = {
                'http': proxy,
                'https': proxy
            }
        
        headers = {
            'accept': '*/*',
            'authorization': f'Bearer {token}',
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        try:
            response = session.get(
                "https://api.depined.org/api/stats/epoch-earnings",
                headers=headers,
                timeout=30
            )
            
            result = response.json()
            
            if result.get("status"):
                return result.get("data")
            
            return None
            
        except Exception as e:
            return None
    
    def process_account(self, account_line: str, account_num: int, total_accounts: int, proxy: Optional[str] = None):
        self.log(f"Account #{account_num}/{total_accounts}", "INFO")
        
        if proxy and self.use_proxy:
            self.log(f"Proxy: {proxy}", "INFO")
        else:
            self.log(f"Proxy: No Proxy", "INFO")
        
        if ':' not in account_line:
            self.log(f"Invalid format: {account_line}", "ERROR")
            return False
        
        email, password = account_line.split(':', 1)
        masked_email = email[:3] + "***" + email[-10:]
        self.log(f"{masked_email}", "INFO")
        
        self.random_delay(2, 5)
        
        token = self.login(email, password, proxy)
        
        if not token:
            return False
        
        self.random_delay(1, 3)
        
        self.log(f"Processing Task:", "INFO")
        
        if self.widget_connect(token, proxy):
            self.log("Widget connected successfully!", "SUCCESS")
        else:
            self.log("Widget connect failed, continue...", "WARNING")
        
        self.random_delay(2, 4)
        
        profile = self.get_profile(token, proxy)
        if profile:
            user_details = profile.get('user_details', {})
            total_points = user_details.get('points_balance', 0)
            points_today = user_details.get('points_today', 0)
            username = profile.get('profile', {}).get('username', 'Unknown')
            
            self.log(f"User: {username}", "SUCCESS")
            self.log(f"Total Points: {total_points:,.2f} | Today: +{points_today}", "SUCCESS")
        
        earnings = self.get_epoch_earnings(token, proxy)
        if earnings:
            epoch = earnings.get('epoch', 0)
            earned = earnings.get('earnings', 0)
            self.log(f"Epoch {epoch}: +{earned} points earned", "SUCCESS")
        
        return True
    
    def run(self):
        self.print_banner()
        
        if not self.load_config():
            return
        
        choice = self.show_menu()
        
        if choice == '1':
            self.use_proxy = True
            self.log("Running with proxy", "INFO")
        else:
            self.use_proxy = False
            self.log("Running without proxy", "INFO")
        
        print(f"\n{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
        
        cycle = 1
        while True:
            self.log(f"Cycle #{cycle} Started", "CYCLE")
            print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
            
            success_count = 0
            total_accounts = len(self.accounts)
            
            for idx, account_line in enumerate(self.accounts, 1):
                proxy = None
                if self.use_proxy and self.proxies:
                    proxy = self.proxies[idx % len(self.proxies)]
                
                if self.process_account(account_line, idx, total_accounts, proxy):
                    success_count += 1
                
                if idx < total_accounts:
                    print(f"{Fore.WHITE}............................................................{Style.RESET_ALL}")
                    self.random_delay(2, 5)
            
            print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
            self.log(f"Cycle #{cycle} Complete | Success: {success_count}/{total_accounts}", "CYCLE")
            print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
            
            cycle += 1
            
            wait_time = 300
            self.countdown(wait_time)

if __name__ == "__main__":
    bot = DepinedBot()
    bot.run()
