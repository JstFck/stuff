import sys
from geocoder import get_coordinate, get_ll_span, show_map


def main():
    toponym_to_find = ' '.join(sys.argv[1:])
    if toponym_to_find:
        lat, lon = get_coordinate(toponym_to_find)
        ll_spn = f'll={lat},{lon}&spn=0.005,0.005'
        show_map(ll_spn, 'map')

        ll, spn = get_ll_span(toponym_to_find)
        ll_spn = f'll={ll}&spn={spn}'
        show_map(ll_spn, 'map')

        point_params = f'pt={ll}'
        show_map(ll, 'map', add_params=point_params)
    else:
        print('no data')


if __name__ == '__main__':
    main()
