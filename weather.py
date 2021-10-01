import requests

def weather_by_city(city_name):
    weather_url = "http://api.worldweatheronline.com/premium/v1/weather.ashx"
    params = {"key": "846bc400028b44cbb82133616212309",
        "q": city_name,
        "format": "json",
        "num_of_days": 1,
        "lang": "ru"}
    try:
        text = requests.get(weather_url,params=params)
        text.raise_for_status()
        weather = text.json()
        if 'data' in weather: 
            if 'current_condition' in weather['data']:
                try:
                    return weather['data']['current_condition'][0]
                except (IndexError, TypeError):
                    return False
    except (requests.RequestException,ValueError):
        print("сетевая ошибка")                
        return False 
    return False         
    
if __name__ == "__main__":
    print(weather_by_city('Khabarovsk,Russia'))