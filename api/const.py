from re import compile, IGNORECASE
from string import ascii_letters, digits


MAX_INTERVAL = 86400 * 7 # максимальный интервал для отслеживания
MIN_INTERVAL = 5 # мин интервал для отслеживания 

max_len_username = 64 # максимальная длина username
min_len_username_len = 4 # минимальная длина username
verify_username_regex = compile(
    rf'^[\w\d]{{{min_len_username_len},{max_len_username}}}$', 
    IGNORECASE
) # regex для проверки username
 
prohibited_urls = "localhost", # запрещенные url для отслеживания // Tuple[...]
verify_url_regex = compile(
    r'^(https?)://(?:[A-Za-z0-9.-]+|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?::\d+)?(?:[/?#][\w&%=-]*)?$'
    ) # regex для проверки url
max_len_url = 2048 # максимальная длина для url 

verify_token_regex = compile(r'^(?!.*\..*\..*\..*)[A-Za-z0-9_.-]+$', IGNORECASE)

verify_password_regex = compile(r'^[A-Za-z0-9!@#$%^&*()_\-+=\[\]{}.,:;?]+$', IGNORECASE) # regex для проверки пароля
min_len_password = 8 # минимальная длина пароля
max_len_password = 256 # максимальная длина пароля

generator_wordlist = ascii_letters + digits # алфавит для генератора

private_key = "keys/private.pem" # путь к приватному ключу // для jwt
public_key = "keys/public.pem" # путь к публичному ключу // для jwt

access_token_exp_minutes = 30 # время действия токена // для jwt
refresh_token_exp_days = 7 # days

max_logs_size = "8MB" # максимальный размер файла {logs_path}
logs_path = "log" # путь к файлу для логов
logs_level = "INFO" # уровень log