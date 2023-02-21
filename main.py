# import pendulum
# import json
# import pandas as pd
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
# from sqlalchemy import create_engine

load_dotenv()

# conn = create_engine('postgresql://postgres:postgres@localhost:54321/etl')
API = os.getenv('WEATHER_API')

lat = '45.039268'
lon = '38.987221'

def k2c(temp) -> float:
    return round(temp - 272.15, 2)

# URL = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API}'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather?'
CITY = ['Krasnodar','Maykop']


code_to_smile = {
    'Clear':'ясно',
    'Clouds':'облачно',
    'Rain':'дождь',
    'Drizzle':'дождь',
    'Thunderstorm':'гроза',
    'Snow':'снег',
    'Mist':'туман'
}

def get_mkp():
    url = BASE_URL + 'appid=' + API + '&q=' + CITY[-1]

    response = requests.get(url).json()

    temp_kelvin = response['main']['temp']
    temp_celcius = k2c(temp_kelvin)

    feels_like_kelvin = response['main']['feels_like']
    feels_like_celcius = k2c(feels_like_kelvin)

    weather_description = response['weather'][0]['main']
    if weather_description in code_to_smile:
        wd = code_to_smile[weather_description]
    else:
        wd = 'Необходимо проверить погоду за окном самостоятельно'
    # sunrise = pendulum.from_timestamp(response['sys']['sunrise'], tz=3)
    sunset = datetime.fromtimestamp(response['sys']['sunset']).time()
    sunrise = datetime.fromtimestamp(response['sys']['sunrise']).time()
    diff = datetime.fromtimestamp(response['sys']['sunset']) - datetime.fromtimestamp(response['sys']['sunrise'])

    wind_speed = response['wind']['speed']
    humidity = response['main']['humidity']
    pressure = response['main']['pressure']

    return f'В Майкопе сейчас {temp_celcius}°C, {wd}\nОщущается как {feels_like_celcius}°С\n\nТекущая влажность - {humidity}%\nСкорость ветра - {wind_speed} м/с\nДавление - {pressure} мм.рт.ст.\n\nРассвет в этом прекрасном городе\nсегодня наступает в {sunrise},\nа время заката - {sunset}\n\nПродолжительность светового дня {diff}'

def get_krd():
    url = BASE_URL + 'appid=' + API + '&q=' + CITY[0]

    response = requests.get(url).json()

    temp_kelvin = response['main']['temp']
    temp_celcius = k2c(temp_kelvin)

    feels_like_kelvin = response['main']['feels_like']
    feels_like_celcius = k2c(feels_like_kelvin)

    weather_description = response['weather'][0]['main']
    if weather_description in code_to_smile:
        wd = code_to_smile[weather_description]
    else:
        wd = 'Необходимо проверить погоду за окном самостоятельно'

    # sunrise = pendulum.from_timestamp(response['sys']['sunrise'], tz=3)
    sunset = datetime.fromtimestamp(response['sys']['sunset']).time()
    sunrise = datetime.fromtimestamp(response['sys']['sunrise']).time()
    diff = datetime.fromtimestamp(response['sys']['sunset']) - datetime.fromtimestamp(response['sys']['sunrise'])

    wind_speed = response['wind']['speed']
    humidity = response['main']['humidity']
    pressure = response['main']['pressure']
    return f'В Краснодаре сейчас {temp_celcius}°C, {wd}\nОщущается как {feels_like_celcius}°С\n\nТекущая влажность - {humidity}%\nСкорость ветра - {wind_speed} м/с\nДавление - {pressure} мм.рт.ст.\n\nРассвет в этом прекрасном городе\nсегодня наступает в {sunrise},\nа время заката - {sunset}\n\nПродолжительность светового дня {diff}'



print(get_mkp())

# -------    
# def select(sql):
#     return pd.read_sql(sql, conn)


# current = [{"coord":{"lon":38.9872,"lat":45.0393},"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04n"}],"base":"stations","main":{"temp":279.85,"feels_like":277.1,"temp_min":279.82,"temp_max":281.18,"pressure":1010,"humidity":99},"visibility":8000,"wind":{"speed":4,"deg":240},"clouds":{"all":75},"dt":1676833772,"sys":{"type":2,"id":2012251,"country":"RU","sunrise":1676780394,"sunset":1676818577},"timezone":10800,"id":542420,"name":"Krasnodar","cod":200}]


# dt = pendulum.from_timestamp(current[0].get('dt'), tz='Europe/Moscow')

# sunrise = pendulum.from_timestamp(current[0].get('sys').get('sunrise'), tz='Europe/Moscow')
# sunset = pendulum.from_timestamp(current[0].get('sys').get('sunset'), tz='Europe/Moscow')

# with open('weather.json', 'r') as f:
#     weather = json.load(f)

# forecast = [_ for _ in weather.get('list')]

# fetching_date = [pendulum.now().date() for _ in range(40)]
# dt = [pendulum.from_timestamp(dt.get('dt'), tz=3) for dt in forecast]
# temp = [_.get('main')['temp'] for _ in forecast]
# wind = [_.get('wind')['speed'] for _ in forecast]
# gust = [_.get('wind')['gust'] for _ in forecast]
# description = [_.get('weather')[0].get('description') for _ in forecast]


# # for _ in forecast:
# #     print()

# lst = list()
# lst.append(fetching_date)
# lst.append(dt)
# lst.append(temp)
# lst.append(wind)
# lst.append(gust)
# lst.append(description)

# df = pd.DataFrame(lst).transpose()
# df.columns = ['fetching_date', 'dt', 'temp', 'wind', 'gust', 'description']
# df['temp'] = df['temp'].apply(k2c)
# df['forecast_date'] = df['dt'].dt.date
# df['forecast_hour'] = df['dt'].dt.hour
# df.drop(labels='dt', axis=1, inplace=True)
# cols = ['fetching_date', 'forecast_date', 'forecast_hour', 'temp', 'wind', 'gust', 'description']
# df = df[cols]

# # print(df['wind'].sort_values())
# # print(df.sample(40))

# # sql = '''
# # create table if not exists weather (
# #     id serial primary key,
# #     fetching_date date,
# #     forecast_date date,
# #     forecast_hour smallint,
# #     temp float,
# #     wind float,
# #     gust float,
# #     description varchar(100)
# # )
# # '''

# df.to_sql('weather', con=conn, if_exists='append', index=False)

# # print(select(sql))

