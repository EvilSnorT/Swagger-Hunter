import argparse
import requests
import time
import os
from urllib.parse import urljoin

ASCII_ART = '''
  ______                                                                  
 /      \                                                                 
|  $$$$$$\ __   __   __   ______    ______    ______    ______    ______  
| $$___\$$|  \ |  \ |  \ |      \  /      \  /      \  /      \  /      \ 
 \$$    \ | $$ | $$ | $$  \$$$$$$\|  $$$$$$\|  $$$$$$\|  $$$$$$\|  $$$$$$
 _\$$$$$$\| $$ | $$ | $$ /      $$| $$  | $$| $$  | $$| $$    $$| $$
|  \__| $$| $$_/ $$_/ $$|  $$$$$$$| $$__| $$| $$__| $$| $$$$$$$$| $$      
 \$$    $$ \$$   $$   $$ \$$    $$ \$$    $$ \$$    $$ \$$     \| $$      
  \$$$$$$   \$$$$$\$$$$   \$$$$$$$ _\$$$$$$$ _\$$$$$$$  \$$$$$$$ \$$      
                                  |  \__| $$|  \__| $$                    
                                   \$$    $$ \$$    $$                    
                                    \$$$$$$   \$$$$$$                     
 __    __                       __                                        
|  \  |  \                     |  \                                       
| $$  | $$ __    __  _______  _| $$_     ______    ______                 
| $$__| $$|  \  |  \|       \|   $$ \   /      \  /      \                
| $$    $$| $$  | $$| $$$$$$$\\$$$$$$  |  $$$$$$\|  $$$$$$               
| $$$$$$$$| $$  | $$| $$  | $$ | $$ __ | $$    $$| $$                  
| $$  | $$| $$__/ $$| $$  | $$ | $$|  \| $$$$$$$$| $$                     
| $$  | $$ \$$    $$| $$  | $$  \$$  $$ \$$     \| $$                     
 \$$   \$$  \$$$$$$  \$$   \$$   \$$$$   \$$$$$$$ \$$                     
                                                                          
                                                                          
                                                                          
Name: Swagger-Hunter
Author: EvilSnorT
'''

print(ASCII_ART)

def main():
    parser = argparse.ArgumentParser(description='Swagger Path Scanner')
    parser.add_argument('-u', '--url', required=True, help='Set target URL (Example: http://example.com)')
    parser.add_argument('-f', '--file', default='swagger_path_list.txt', 
                        help='Set the path dictionaries (Default: swagger_path_list.txt)')
    parser.add_argument('-t', '--timeout', type=float, default=5.0,
                        help='Set timeout(second) (Default: 5)')
    parser.add_argument('-d', '--delay', type=float, default=0.1,
                        help='Set delay time(second) (Default: 0.1)')
    parser.add_argument('--no-check', action='store_true',
                        help='No check certificate')
    
    args = parser.parse_args()
    
    target_url = args.url.rstrip('/') + '/'
    
    if not os.path.isfile(args.file):
        print(f"[!] Error: '{args.file}' is not exist!")
        return
    
    try:
        
        with open(args.file, 'r', encoding='utf-8', errors='ignore') as f:
            directories = [line.strip() for line in f if line.strip()]
        
        if not directories:
            print("[!] Error: The path list is not exist!")
            return
            
        print(f"Task: {target_url}")
        print(f"Loaded {len(directories)} ammo")
        print("=" * 60)
        
        for idx, directory in enumerate(directories, 1):
            full_url = urljoin(target_url, directory)
            
            try:
                response = requests.get(
                    full_url,
                    timeout=args.timeout,
                    verify=not args.no_check,
                    allow_redirects=True
                )
                
                if response.status_code == 200:
                    print(f"[+] Swagger detected: {full_url} (StatusCode: 200)")
                
                # show progress
                if idx % 50 == 0:
                    print(f"Task {idx}/{len(directories)} complete...")
                
            except (requests.ConnectionError, requests.Timeout, requests.TooManyRedirects) as e:
                pass  # ignore error
            
            time.sleep(args.delay)  # delay
            
        print("=" * 60)
        print("Complete")
        
    except KeyboardInterrupt:
        print("\n Suspended")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
