import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.lang import Builder

# funktion for at tjekke om bynavnet er "valid"
def is_valid_city(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=efdbb015c8f18f890b8803a3007366f2'
    response = requests.get(url).json()
    if response['cod'] == 200:
        return True
    else:
        return False

# funktion for at få "weather data" for en valid by
def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=efdbb015c8f18f890b8803a3007366f2'
    response = requests.get(url).json()
    return response

# funktion for at få et "valid" bynavn for en by
def get_country(city, api_key):
    url = f'https://api.opencagedata.com/geocode/v1/json?q={city}&key={api_key}'
    response = requests.get(url).json()

    if response['total_results'] > 0:
        result = response['results'][0]
        return result['components']['country']
    else:
        return f"No results found for {city}"


# skab et root widget for appen
Builder.load_string('''
<RootWidget>:
    orientation: 'horizontal'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Enter a city name:'
        TextInput:
            id: city_input
        Button:
            text: 'Get Weather'
            on_release: root.get_weather_data()
        Label:
            text: root.weather_data
        AsyncImage:
            id: weather_icon
            source: ''
    Image:
        id: image
        source: ''
''')

# skaber et widget for appen
class RootWidget(BoxLayout):
    weather_data = StringProperty()

    def get_weather_data(self):

        # få bynavnet fra input feltet
        city = self.ids.city_input.text

        # spørg for et bynavn indtil et "valid city name" er indtastet
        if is_valid_city(city):
            api_key = "db38cfac983849f391974a679585dd2f"

            # få "weather data" og "country" for en valid by
            weather_data = get_weather_data(city)
            country = get_country(city, api_key)

            # updater "weather icon"
            icon_id = weather_data['weather'][0]['icon']
            self.ids.weather_icon.source = f'http://openweathermap.org/img/w/{icon_id}.png'

            # vis "weather data" og "country name" for brugeren
            self.weather_data = f"Country: {country}\nTemperature: {weather_data['main']['temp']}°C\nHumidity: {weather_data['main']['humidity']}%\nWind Speed: {weather_data['wind']['speed']} m/s\nDescription: {weather_data['weather'][0]['description']}"
        else:
            self.weather_data = f"Invalid city, please try again"


# byg appen
class WeatherApp(App):
    def build(self):
        return RootWidget()

# kør appen
if __name__ == '__main__':
    WeatherApp().run()
