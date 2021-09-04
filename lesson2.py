
# задание 1
import csv
import re


def get_data():
    files = ['info_1.txt', 'info_2.txt', 'info_3.txt']
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []

    for file in files:
        with open(file, 'r', encoding='windows-1251') as f:
            data = f.read()
            os_prod_list.append(get_value('Изготовитель ОС:', data))
            os_name_list.append(get_value('Название ОС:', data))
            os_code_list.append(get_value('Код продукта:', data))
            os_type_list.append(get_value('Тип системы:', data))

    main_data = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы'], ]
    for prod, name, code, type in zip(os_prod_list, os_name_list, os_code_list, os_type_list):
        main_data.append([prod, name, code, type])

    return main_data


def write_to_csv(file='lesson2.csv'):
    data = get_data()
    print(file)
    with open(file, 'w') as f:
        csv_writer = csv.writer(f)
        for row in data:
            csv_writer.writerow(row)
    return


def get_value(pattern: str, data: str):
    raw = re.findall(pattern + r'.*', data)[0]
    return re.sub(pattern, '', raw).strip()


write_to_csv('lesson2.csv')


# задание 2
import json


def write_order_to_json(item, quantity, price, buyer, date):
    with open('orders.json', 'r') as f:
        orders = json.load(f)

    orders['orders'].append({'item': item,
                             'quantity': quantity,
                             'price': price,
                             'buyer': buyer,
                             'date': date,
                             })

    with open('orders.json', 'w') as f:
        json.dump(orders, f, indent=2)


write_order_to_json('monitor', 2, 200, 'user1', '4.09.2021')
write_order_to_json('keyboard', 1, 10, 'user1', '4.09.2021')
write_order_to_json('motherboard', 1, 150, 'user2', '3.09.2021')


# задание 3
import yaml

dict1 = {
    "first": ["1", "2", "qwer"],
    "second": 3,
    "third": {key: chr(key) for key in range(256, 65535)}
}

with open('data.yaml', 'w')as f:
    yaml.dump(dict1, f, default_flow_style=True, allow_unicode=True)

with open('data.yaml') as f:
    content = yaml.load(f, Loader=yaml.FullLoader)

print(f'{dict1 == content}')

