# не использовать в коммерчиских целях
import requests
import json
import time
import pandas as pd
"""
Скрипт при бесплатном использовании обрабатывает 500 запросов в сутки
"""
# персональный апи ключ пользователя Яндекс Апи поиск по организациям

api_key = "Вставьте Ваш ключ сюда"
"""
ТУТ НАЗВАНИЕ ФАЙЛА, 
файл должен содержать стоблец Адрес(500 строк адресов) и столбец Название(пустой)
"""
file = 'Тест.xlsx'

"""
ФУНКЦИЯ SUGGEST
на вход строку адреса, на выход готовый ответ на запрос к яндекс апи в формате JSON
"""


def suggest(s):
    # ссылка на сайт яндекса

    site = 'https://search-maps.yandex.ru/v1/?'

    # входные параметры запроса(в параметрах при желании можно настроить радиус поиска через координатные величины)
    # подробнее смотреть на https://tech.yandex.ru/maps/doc/geosearch/concepts/request-docpage/

    inputs = 'text=%s&type=biz&rspn=1' % (s)

    # персональный апи ключ
    key = '&apikey=%s&lang=ru_RU' % (api_key)

    # Создать ссылку для http запроса
    url = site + inputs + key

    r = requests.get(url)
    return r.json()


if __name__ == '__main__':

    # создание датафрейма с адресами
    data = pd.read_excel(file, index_col=None, encoding='utf-8')
    values = {'Адрес': [], 'Название': []}
    values['Адрес'] = data['Адрес'].values.tolist()
    num = len(values['Адрес'])
    values['Название'] = ['' for element in range(num)]

    for i in range(num):
        print('(' + str(i + 1) + '/' + str(num) + '): ' + values['Адрес'][i])
        org_data = suggest(values['Адрес'][i])
        if len(org_data['features']) != 0:
            org_data = org_data['features']
            for j in range(len(org_data)):
                values['Название'][i] += org_data[j]['properties']['name'] + '; '
            print('Название' + values['Название'][i])
        else:
            print('Не удалось найти информацию')
        time.sleep(0.1)

    writer = pd.ExcelWriter(file)
    pd.DataFrame.from_dict(values).to_excel(writer, startcol=0, startrow=0, index=False)
    writer.save()
    print('Всё готово')

