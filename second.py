import sys
from geocoder import find_business, lonlat_distance, get_coordinate, show_map


def main():
    toponym_to_find = ' '.join(sys.argv[1:])

    lat, lon = get_coordinate(toponym_to_find)
    address_ll = f'{lat},{lon}'
    span = '0.005,0.005'

    organizations = find_business(address_ll, span, 'аптека')
    point = organizations['geometry']['coordinates']
    org_lan, org_lon = float(point[0]), float(point[1])
    point_param = f'pt={org_lan},{org_lon},pm2dgl'
    show_map(f'll={address_ll}&spn={span}', 'map', add_params=point_param)
    point_param = point_param + f'~{address_ll},pm2rdl'
    show_map(f'll={address_ll}&spn={span}', 'map', add_params=point_param)
    show_map(map_type='map', add_params=point_param)

    name = organizations['properties']['CompanyMetaData']['name']
    address = organizations['properties']['CompanyMetaData']['address']
    time = organizations['properties']['CompanyMetaData']['Hours']['text']
    distance = round(lonlat_distance((lon, lat), (org_lon, org_lan)))
    snippet = f'Название:\t{name}\nАдрес\t{address}\nВремя работы\t{time}\nРасстояние\t{distance}'
    print(snippet)


if __name__ == '__main__':
    main()
