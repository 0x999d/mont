from string import digits, ascii_letters

API_URL = "http://api:8080"

logs_path = "log"
logs_level = "INFO"
max_logs_size = "4MB"
 
MIN_INTERVAL = 5 
MAX_INTERVAL = 86400*3

password_wordlist=ascii_letters+digits
password_len=15