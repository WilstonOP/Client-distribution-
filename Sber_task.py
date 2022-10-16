import pandas as pd
import random

# Создаем случайные значения для входных данных
cur_capacity = [random.randint(1, 300) for _ in range(1, 101)]
max_capacity = [x + random.randint(0, 20) for x in cur_capacity]
company_random = [i for i in range(1, 101)]

clients_random = [i for i in range(1, 301)]
div1_random = [random.randint(1, 101) for _ in range(1, 301)]
div2_random = [random.randint(1, 101) for _ in range(1, 301)]
div3_random = [random.randint(1, 101) for _ in range(1, 301)]
# Создаем дата-фреймы
company = {"div_id": company_random, "cur_capacity": cur_capacity, "max_capacity": max_capacity}
clients = {"client_id": clients_random, "div1_id": div1_random,
           "div2_id": div2_random, "div3_id": div3_random}

d_d = pd.DataFrame(company)
d_c = pd.DataFrame(clients)

recommendation = list()  # recommendation - список с клиентом и рекомендованным отделом
assigned_list = list()  # assigned_list - список с клиентами, которым уже порекомендовали отдел
print(d_c, end='\n\n')
d_d = d_d.assign(vacant_place=lambda x: x['max_capacity'] - x['cur_capacity'])  # добавление поля vacant_place,
                                                                                # которое хранит свободные места отдела
print(d_d)

for prior in ['div1_id', 'div2_id', 'div3_id']:  # Цикл по полям рекомендаций
    for index, row in d_c.iterrows():  # Цикл по дата-фрейму клиентов
        if row['client_id'] in assigned_list:  # Проверка на то, что клиенту уже назначена рекомендация
            continue  # Если да, то пропускаем клиента
        else:
            div_client = row[prior]  # Получаем приоритет клиента в зависимости от цикла
            if (d_d[(d_d['div_id'] == div_client) & (d_d['vacant_place'] > 0)])['div_id'].size > 0:  # Свободный отдел
                assigned_list.append(row['client_id'])  # Добавляем в список, чтобы пропускать клиента в будущем
                div = d_d['div_id'][(d_d['div_id'] == div_client) & (d_d['vacant_place'] > 0)].tolist()[0]  # Получаем id отдела
                d_d.loc[(d_d.div_id == div), "vacant_place"] -= 1  # Уменьшаем кол-во вакантных мест в отделе
                recommendation.append([row['client_id'], div])  # Заносим в финальную таблицу клиента и отдел

remaining_clients = set(d_c['client_id'].values) - set(assigned_list)  # Находим клиентов, которые не попали в приоритетные отделы
assigned_clients = set()  # Список клиентов, которые назначены в отдел не по рекомендации
if remaining_clients:  # Существуют ли вообще клиенты, которые не попали в приоритетные отделы
    print('\n\nКлиенты без учета приоритета:')
    for client in remaining_clients:
        if d_d[d_d['vacant_place'] > 0].size > 0:  # Есть ли любой свободный отдел
            d = d_d[d_d['vacant_place'] > 0].iloc[0]['div_id']  # Находим любой свободный отдел
            d_d.loc[(d_d.div_id == d), "vacant_place"] -= 1  # Уменьшаем счетчик вакантных мест
            recommendation.append([client, d])  # Добавляем в финальный список
            assigned_clients.add(client)  # Добавляем в список клиентов, которые назначены в отдел не по рекомендации
            print(f'  Добавлен клиент {client} в отдел {d}')
        else:
            unassigned_clients = list(remaining_clients - assigned_clients)
            print(f'Завершение: эти клиенты не получили места {unassigned_clients}')
else:
    print('Все клиенты получили свои рекомендации согласно приоритетам')

d_d['cur_capacity'] = (d_d['max_capacity'] - d_d['vacant_place']).apply(lambda x: x)  # Обновляем данные входной таблицы
print(f'Информация по отделам:\n{d_d}', end='\n\n')
unassigned_clients = list(remaining_clients - assigned_clients)  # Создаем список клиентов, которые никуда не попали
unassigned_clients = [[x, -1] for x in unassigned_clients]  # И для таких клиентов назначаем отдел -1

all_recommendation = recommendation.extend(unassigned_clients)  # Добавляем эти клиентов к общим
output = pd.DataFrame(recommendation, columns=['CLIENT_ID', 'DIV_ID'])  # Создаем финальную таблицу
print(f'Список рекомендаций\n: {output}')
