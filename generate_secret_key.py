#!/usr/bin/env python
"""
Генерирует надежный секретный ключ для Django и обновляет файл .env.prod.
"""
import os
import sys
import string
import random

def generate_secret_key(length=50):
    """Генерирует криптографически надежный случайный ключ заданной длины"""
    chars = string.ascii_letters + string.digits + string.punctuation
    # Используем systemrandom для криптографически надежных случайных чисел
    return ''.join(random.SystemRandom().choice(chars) for _ in range(length))

def update_env_file(env_file=".env.prod.example"):
    """Обновляет или создает переменную SECRET_KEY в файле окружения"""
    secret_key = generate_secret_key()
    
    # Проверяем существование файла
    if os.path.exists(env_file):
        with open(env_file, 'r') as file:
            lines = file.readlines()
        
        # Ищем строку с SECRET_KEY
        secret_key_found = False
        for i, line in enumerate(lines):
            if line.startswith('SECRET_KEY='):
                lines[i] = f'SECRET_KEY={secret_key}\n'
                secret_key_found = True
                break
        
        # Добавляем SECRET_KEY, если он не найден
        if not secret_key_found:
            lines.append(f'SECRET_KEY={secret_key}\n')
        
        # Записываем обновленный файл
        with open(env_file, 'w') as file:
            file.writelines(lines)
    else:
        # Создаем новый файл
        with open(env_file, 'w') as file:
            file.write(f'SECRET_KEY={secret_key}\n')
    
    print(f"✅ Секретный ключ успешно сгенерирован и добавлен в {env_file}")
    return secret_key

if __name__ == "__main__":
    # Принимаем имя файла как необязательный аргумент
    env_file = ".env.prod.example"
    if len(sys.argv) > 1:
        env_file = sys.argv[1]
    
    update_env_file(env_file)
