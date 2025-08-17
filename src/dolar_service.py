from config import settings
import requests
import os

def get_current_dolar_value():
    """
    Fetches the current value of the dollar from an external API.
    
    Returns:
        float: The current value of the dollar.
    """
    print(os.getenv('BASE_API_DOLAR'))
    api_url = settings.BASE_API_DOLAR + "/latest"
    response = _execute_dolar_api(api_url)
    if response:
        return response
    raise Exception("No se pudo obtener el valor del dólar actual.")

def get_dolar_value_by_date(date: str):
    """
    Fetches the value of the dollar for a specific date from an external API.
    
    Args:
        date (str): The date in 'YYYY/MM/DD' format.
    Returns:
        float: The dollar value for the specified date.
    """
    date_formatted = date.replace('/', '-')
    api_url = settings.BASE_API_DOLAR + f"/historical?day={date_formatted}"
    response = _execute_dolar_api(api_url)
    if response:
        return response
    raise Exception(f"No se pudo obtener el valor del dólar para la fecha {date}.")


def _execute_dolar_api(url: str) -> dict:
    from models import Dolar
    try:
        response = requests.get(url)
        data = response.json()
        print(f"Estado de la solicitud: {response.status_code}")
        print(f"Respuesta de la API: {data}")

        dolar = Dolar()
        dolar.setValores(data)
        return dolar
    except Exception as e:
        print(f"Error al ejecutar la solicitud: {e}")
        return None
    