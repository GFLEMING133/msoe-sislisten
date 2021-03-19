import color_map_2d
import numpy
import requests


def communicate_color_to_table(rgba, table_service, settings=None):
    """
    Communicates a color to the table
    """

    led_info = {"led_primary_color": rgba}
    wrapper = {'data': {'data' : led_info }}
    table_response = requests.post(table_service, json=wrapper)
    if table_response.status_code == requests.codes.ok:
        print(f'Successfully updated color to {rgba}')
    else:
        print(f'Error in table request - code: {table_response.status_code}')