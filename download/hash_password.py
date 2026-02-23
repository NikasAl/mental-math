#!/usr/bin/env python3
"""
Скрипт для генерации хэша пароля bcrypt.
Запуск: python hash_password.py <пароль>
"""

import bcrypt
import sys

def generate_hash(password: str) -> str:
    """Генерирует bcrypt хэш для пароля"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode()

def main():
    if len(sys.argv) > 1:
        password = sys.argv[1]
    else:
        password = input("Введите пароль: ")
    
    hashed = generate_hash(password)
    
    print(f"\nПароль: {password}")
    print(f"Хэш: {hashed}")
    print(f"\nSQL для обновления:")
    print(f"UPDATE users SET hashed_password = '{hashed}' WHERE username = 'имя_пользователя';")

if __name__ == "__main__":
    main()
