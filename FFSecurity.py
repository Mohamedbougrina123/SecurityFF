import requests
import os
import hashlib
import json
from colorama import Fore, Style
import datetime

def clear():
    os.system("clear")

def gettime(seconds):
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"Time remaining: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds"

def encrypt_number(number):
    number_str = str(number)
    hash_object = hashlib.sha256(number_str.encode())
    hex_dig = hash_object.hexdigest().upper()
    return hex_dig

def show_info(token):
    try:
        api = "https://100067.connect.garena.com/game/account_security/bind:get_bind_info?app_id=100067&access_token=" + token
        headers = {
            "User-Agent": "GarenaMSDK/4.0.19P9(J200F ;Android 7.1.2;ar;EG;)",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }
        response = requests.get(api, headers=headers).json()
        
        if "error" in response:
            print(f"{Fore.RED}Error: {response['error']}{Style.RESET_ALL}")
        else:
            email = response.get("email", "")
            email_to_be = response.get("email_to_be", "")
            mobile = response.get("mobile", "")
            mobile_to_be = response.get("mobile_to_be", "")
            request_exec_countdown = response.get("request_exec_countdown", 0)
            
            if email:
                print(f"{Fore.GREEN}Current Email: {email}{Style.RESET_ALL}")
            if email_to_be:
                print(f"{Fore.YELLOW}Pending Email: {email_to_be}{Style.RESET_ALL}")
            if mobile:
                print(f"{Fore.GREEN}Current Mobile: {mobile}{Style.RESET_ALL}")
            if mobile_to_be:
                print(f"{Fore.YELLOW}Pending Mobile: {mobile_to_be}{Style.RESET_ALL}")
            
            if request_exec_countdown > 0:
                time_remaining = gettime(request_exec_countdown)
                print(f"{Fore.CYAN}{time_remaining}{Style.RESET_ALL}")
                
    except Exception as error:
        print(f"{Fore.RED}Error in show_info: {error}{Style.RESET_ALL}")

def email_binding():
    try:
        # Step 1: Get token and code first
        token = input(f"{Fore.CYAN}Enter token: {Style.RESET_ALL}")
        code = input(f"{Fore.CYAN}Enter security code: {Style.RESET_ALL}")
        
        headers = {
            'User-Agent': "GarenaMSDK/4.0.19P9(J200F ;Android 7.1.2;ar;EG;)",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip"
        }
        
        # Step 2: Verify Identity
        print(f"\n{Fore.MAGENTA}--- Verifying Identity ---{Style.RESET_ALL}")
        url = "https://100067.connect.garena.com/game/account_security/bind:verify_identity"
        payload = {
            'app_id': "100067",
            'access_token': token,
            'secondary_password': encrypt_number(code)
        }
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
        identity_token = response.json()["identity_token"]
        print(f"{Fore.GREEN}Identity verified successfully{Style.RESET_ALL}")
        
        # Step 3: Get email and send OTP
        email = input(f"\n{Fore.CYAN}Enter email: {Style.RESET_ALL}")
        
        print(f"\n{Fore.MAGENTA}--- Sending OTP ---{Style.RESET_ALL}")
        url = "https://100067.connect.garena.com/game/account_security/bind:send_otp"
        payload = {
            'app_id': "100067",
            'access_token': token,
            'email': email,
            'locale': "ar_EG"
        }
        headers_copy = headers.copy()
        headers_copy['Accept'] = "application/json"
        headers_copy['Cookie'] = "datadome=L5aWQatkvEKgi0kcs9RfqX3IJ6EI2JPR7uuWg8LmfZcX8Uc297Z1jzndyNgMh~zookrgYaD3hEHfMo9WNEZL1yyGy20TuVkkdiFFB9NNuHn7LuHs_WXyFF7XvfbntaJL"
        response = requests.post(url, data=payload, headers=headers_copy)
        response.raise_for_status()
        print(f"{Fore.GREEN}OTP sent successfully{Style.RESET_ALL}")
        
        # Step 4: Get OTP and verify
        otp = input(f"\n{Fore.CYAN}Enter OTP: {Style.RESET_ALL}")
        
        print(f"\n{Fore.MAGENTA}--- Verifying OTP ---{Style.RESET_ALL}")
        url = "https://100067.connect.garena.com/game/account_security/bind:verify_otp"
        payload = {
            'app_id': "100067",
            'access_token': token,
            'otp': otp,
            'email': email
        }
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
        verifier_token = response.json()["verifier_token"]
        print(f"{Fore.GREEN}OTP verified successfully{Style.RESET_ALL}")
        
        # Step 5: Create rebind request
        print(f"\n{Fore.MAGENTA}--- Creating Rebind Request ---{Style.RESET_ALL}")
        url = "https://100067.connect.garena.com/game/account_security/bind:create_rebind_request"
        payload = {
            'app_id': "100067",
            'access_token': token,
            'identity_token': identity_token,
            'verifier_token': verifier_token,
            'email': email
        }
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
        print(f"{Fore.GREEN}Success: {response.text}{Style.RESET_ALL}")
        
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Request Error: {e}{Style.RESET_ALL}")
    except KeyError as e:
        print(f"{Fore.RED}Key Error: {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

BASE_URL = "https://100067.connect.garena.com/game/account_security/bind"
APP_ID = "100067"
COMMON_HEADERS = {
    'User-Agent': "GarenaMSDK/4.0.19P9(J200F ;Android 7.1.2;ar;EG;)",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip"
}

def simple_bind_flow():
    try:
        # Step 1: Get token first
        token = input(f"{Fore.CYAN}Enter token: {Style.RESET_ALL}")
        
        # Step 2: Get security code
        code = input(f"{Fore.CYAN}Enter security code: {Style.RESET_ALL}")
        
        # Step 3: Get email
        email = input(f"{Fore.CYAN}Enter email: {Style.RESET_ALL}")
        
        print(f"\n{Fore.MAGENTA}--- Sending OTP ---{Style.RESET_ALL}")
        send_otp_request(token, email)
        
        print(f"\n{Fore.MAGENTA}--- Verifying OTP ---{Style.RESET_ALL}")
        verify_response = verify_otp_request(token, email)
        
        if verify_response.status_code == 200:
            try:
                response_data = verify_response.json()
                verifier_token = response_data.get("verifier_token")      
                if verifier_token:
                    print(f"\n{Fore.MAGENTA}--- Creating Bind Request ---{Style.RESET_ALL}")
                    create_bind_request(token, email, verifier_token, code)
                else:
                    print(f"{Fore.RED}Error: verifier_token not found in response{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Error: Invalid JSON response from OTP verification{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Error: OTP verification failed with status code {verify_response.status_code}{Style.RESET_ALL}")
            
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")

def send_otp_request(token, email):
    url = f"{BASE_URL}:send_otp"
    payload = {
        'app_id': APP_ID,
        'access_token': token,
        'email': email,
        'locale': "ar_EG"
    }
    
    headers = COMMON_HEADERS.copy()
    headers['Accept'] = "application/json"
    
    response = requests.post(url, data=payload, headers=headers)
    print(f"{Fore.YELLOW}OTP Response: {response.text}{Style.RESET_ALL}")
    return response

def verify_otp_request(token, email):
    otp_code = input(f"{Fore.CYAN}Enter OTP: {Style.RESET_ALL}")
    
    url = f"{BASE_URL}:verify_otp"
    payload = {
        'app_id': APP_ID,
        'access_token': token,
        'otp': otp_code,
        'email': email
    }
    
    response = requests.post(url, data=payload, headers=COMMON_HEADERS)
    print(f"{Fore.YELLOW}Verify OTP Response: {response.text}{Style.RESET_ALL}")
    return response

def create_bind_request(token, email, verifier_token, code):
    url = f"{BASE_URL}:create_bind_request"
    payload = {
        'app_id': APP_ID,
        'access_token': token,
        'verifier_token': verifier_token,
        'secondary_password': encrypt_number(code),
        'email': email
    }
    
    response = requests.post(url, data=payload, headers=COMMON_HEADERS)
    print(f"{Fore.YELLOW}Create Bind Response: {response.text}{Style.RESET_ALL}")
    return response

def show_menu():
    print(f"\n{Fore.GREEN}╔══════════════════════════════╗")
    print(f"║       GARENA TOOL MENU       ║")
    print(f"╠══════════════════════════════╣")
    print(f"║ {Fore.CYAN}1{Fore.GREEN}. Show Account Info           ║")
    print(f"║ {Fore.CYAN}2{Fore.GREEN}. Simple Email Binding        ║")
    print(f"║ {Fore.CYAN}3{Fore.GREEN}. Advanced Email Binding      ║")
    print(f"║ {Fore.CYAN}4{Fore.GREEN}. Exit                        ║")
    print(f"╚══════════════════════════════╝{Style.RESET_ALL}")

def main():
    clear()
    
    while True:
        show_menu()
        choice = input(f"\n{Fore.YELLOW}Select an option (1-4): {Style.RESET_ALL}")
        
        if choice == '1':
            token = input(f"{Fore.CYAN}Enter token: {Style.RESET_ALL}")
            print(f"\n{Fore.MAGENTA}--- Account Information ---{Style.RESET_ALL}")
            show_info(token)
            
        elif choice == '2':
            print(f"\n{Fore.MAGENTA}--- Simple Email Binding ---{Style.RESET_ALL}")
            simple_bind_flow()
            
        elif choice == '3':
            print(f"\n{Fore.MAGENTA}--- Advanced Email Binding ---{Style.RESET_ALL}")
            email_binding()
            
        elif choice == '4':
            print(f"{Fore.GREEN}Goodbye!{Style.RESET_ALL}")
            break
            
        else:
            print(f"{Fore.RED}Invalid choice! Please select 1-4.{Style.RESET_ALL}")
        
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        clear()

if __name__ == "__main__":
    main()
