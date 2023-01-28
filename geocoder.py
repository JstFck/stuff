import math

import requests
import pygame
import sys
import os

API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'


def geocode(address):
    geocoder_req = f'http://geocode-maps.yandex.ru/1.x/'
    geocoder_params = {
        'apikey': API_KEY,
        'geocode': address,
        'format': 'json'
    }
    response = requests.get(geocoder_req, params=geocoder_params)
    if response:
        json_response = response.json()
    else:
        raise RuntimeError(
            f'''Ошибка выполнения запроса: {geocoder_req} \n
            http статус {response.status_code} ({response.reason})'''
        )

    features = json_response['response']['GeoObjectCollection']['featureMember']

    return features[0]['GeoObject'] if features else None


def get_coordinate(address):
    toponym = geocode(address)
    if not toponym:
        return None, None

    toponym_coordinates = toponym['Point']['pos']
    toponym_long, toponym_lat = toponym_coordinates.split()
    return float(toponym_long), float(toponym_lat)


def get_ll_span(address):
    toponym = geocode(address)
    if not toponym:
        return None, None

    toponym_coordinates = toponym['Point']['pos']
    toponym_long, toponym_lat = toponym_coordinates.split()
    ll = ','.join([toponym_long, toponym_lat])
    envelope = toponym['boundedBy']['Envelope']
    l, b = envelope['lowerCorner'].split()
    r, t = envelope['upperCorner'].split()
    dx = abs(float(l) - float(r)) / 2.0
    dy = abs(float(t) - float(b)) / 2.0
    span = f'{dx},{dy}'
    return ll, span


def show_map(ll_spn=None, map_type='map', add_params=None):
    if ll_spn:
        map_request = f'http://static-map.yandex.ru/1.x/?{ll_spn}&l={map_type}'
    else:
        map_request = f'http://static-map.yandex.ru/1.x/?l={map_type}'
    if add_params:
        map_request += '&' + add_params
    response = requests.get(map_request)
    if not response:
        print(f"""Ошибка выполнения запроса: {map_request} \nHttp статус: {response.status_code} ({response.reason})"""
              )
        sys.exit(1)
    map_file = 'map.png'
    try:
        with open(map_file, 'wb') as file:
            file.write(response.content)
    except IOError as ex:
        print('Ошибка записи временного файла:', ex)
        sys.exit(2)
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    while pygame.event.wait() != pygame.QUIT:
        pass
    pygame.quit()
    os.remove(map_file)


def search(ll, spn, request, locale='ru_RU'):
    search_api_server = 'https://search-maps.yandex.ru/v1/'
    api_key = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
    search_params = {
        'apikey': api_key,
        'text': request,
        'lang': locale,
        'll': ll,
        'spn': spn,
        'type': 'biz'
    }
    response = requests.get(search_api_server, params=search_params)
    if not response:
        raise RuntimeError(f'''Ошибка выполнения запроса {search_api_server} \nhttp статус {response.status_code} 
        ({response.reason})''')
    json_response = response.json()
    organizations = json_response['features']
    return organizations


def find_business(ll, spn, request, locale='ru_ru'):
    orgs = find_business(ll, spn, request, locale=locale)
    if len(orgs):
        return orgs[0]


def lonlat_distance(a, b):
    degree_to_meters = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b

    radians_lat = math.radians((a_lat + b_lat) / 2)
    lat_lon_factor = math.cos(radians_lat)

    dx = abs(a_lon - b_lon) * degree_to_meters * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters

    distance = math.sqrt(dx ** 2 + dy ** 2)
    return distance
