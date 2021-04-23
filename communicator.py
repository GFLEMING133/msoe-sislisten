import color_map_2d
import numpy
import requests
import datetime

def communicate_color_to_table(rgb, table_service):
    """
    Communicates a color to the table service using the /set_led_color endpoint
    """
    print(f'Recieved response @ {datetime.datetime.now()}')
    led_info = { "led_primary_color": rgb }
    wrapper = { 'data': { 'data' : led_info } }
    table_response = requests.post(table_service, json=wrapper)
    if table_response.status_code == requests.codes.ok:
        print(f'Successfully updated color to {rgb}')
    else:
        print(
            f'Error in table request - code: {table_response.status_code}'
        )
    return table_response.status_code