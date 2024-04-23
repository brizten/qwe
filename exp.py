from cryptography.fernet import Fernet

# Генерируем ключ
key = b'DHJDAOFPOqTX6ERGTpgaFxersf713KytTICSwQVGAqQ='

# Создаем объект Fernet с сгенерированным ключом
cipher_suite = Fernet(key)

# Сообщение, которое нужно зашифровать
message = "kuanysh"

# Шифруем сообщение
encrypted_message = cipher_suite.encrypt(message.encode())

# Выводим зашифрованное сообщение
print("Зашифрованное сообщение:", encrypted_message)

# Для дальнейшего декодирования зашифрованного сообщения необходимо сохранить ключ
# Можно сохранить ключ в файл или базу данных, чтобы иметь к нему доступ в будущем
print("Ключ:", key)
