print("\n####### задание 1 ########")
strings = ["разработка", "сокет", "декоратор"]
for string in strings:
    print(f'{string} {type(string)}')

strings_unicode = [u'\u0440\u0430\u0437\u0440\u0430\u0431\u043E\u0442\u043A\u0430',
                   u'\u0441\u043E\u043A\u0435\u0442',
                   u'\u0434\u0435\u043A\u043E\u0440\u0430\u0442\u043E\u0440',
                   ]
for string in strings_unicode:
    print(f'{string} {type(string)}')


print("\n####### задание 2 ########")
strings = ["class", "function", "method"]
for string in strings:
    result = b''.join([bytes([ord(char)]) for char in string])
    print(f'type={type(result)}; {result=}; len={len(result)}')


print("\n####### задание 3 ########")
strings = ["attribute", "класс", "функция", "type"]
for string in strings:
    try:
        raw = string.encode()
        print(f'{string=} {raw=} {type(raw)} преобразование возможно')
    except Exception:
        print(f'{string=} преобразование не возможно ', Exception)


print("\n####### задание 4 ########")
strings = ["разработка", "администрирование", "protocol", "standard"]
for string in strings:
    raw = string.encode()
    decoded = raw.decode(encoding="utf-8")
    print(f'{string=} {decoded=} {raw=} ')


print("\n####### задание 5 ########")
import subprocess
sites = ['yandex.com', 'youtube.com']
for site in sites:
    proc = subprocess.Popen(['ping', '-c', '1', site], stdout=subprocess.PIPE)
    for line in proc.stdout:
        print(line.decode('cp1252'), end='')


print("\n####### задание 6 ########")
with open('test_file.txt', "w", encoding="utf8") as f:
    [f.write(string + '\n') for string in ["сетевое программирование", "сокет", "декоратор"]]

from chardet.universaldetector import UniversalDetector

detector = UniversalDetector()
with open('test_file.txt', "rb") as f:
    for line in f:
        detector.feed(line)
        if detector.done:
            break
    detector.close()
    print(f'кодировка: {detector.result}')

with open('test_file.txt', "r", encoding='utf-8') as f:
    text = f.read()
    new_text = text.encode('utf-8').decode("utf-16")
    print(f'текст в кодировке utf-16: {new_text}')
