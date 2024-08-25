import requests
from datetime import datetime
import tkinter
from PIL import Image, ImageTk



Appid = "4bdce1b3d18c80b4fcb95f7737a82083"
def get_coordinates(city_name , country_code , api_key = Appid):
    base_url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {"q": f"{city_name},{country_code}", "limit": 1, "appid": api_key}

    response = requests.get(base_url, params= params)
    if response.status_code == 200 :
        data = response.json()
        if data :
            latitude = data[0]['lat']
            longitude = data[0]['lon']
            return latitude, longitude
        else:
            print("Girdiginiz bilgiler icin bir sonuc bulunamadi")
            return None, None
    else:
        print("API istegi basrisiz oldu")
        return None, None

def openweather_request(latitude, longitude, api_key = Appid):
    base_url = "https://api.openweathermap.org/data/3.0/onecall"
    params = {'lat' : latitude, "lon" : longitude, 'exclude': 'minutely,hourly', 'units': 'metric', "appid" : Appid}

    response = requests.get(base_url, params=params)
    if response.status_code == 200 :
        data = response.json()
        print("API islemi basarili")

        daily_forecasts = data.get('daily', [])
        if daily_forecasts:
            first_day = daily_forecasts[0]  # İlk günün verilerini alın
            temp_day = first_day['temp']['day']
            weather_description = first_day['weather'][0]['description']
            timestamp = first_day['dt']
            date_time = datetime.fromtimestamp(timestamp)
            formatted_date = date_time.strftime('%Y-%m-%d %A')
            final_text = f"Date: {formatted_date}, \nMorning Temp: {temp_day}°C, \nSituation: {weather_description}"
            msg = tkinter.Message(window, text= final_text, font=FONT)
            msg.config(background="light gray", width= 100)
            canvas.create_window(165, 270, window=msg,)

            '''
            canvas = tkinter.Canvas(window, width=500, height=500)
            canvas.create_text(250, 250, text=final_text, fill="black", font=FONT)
            canvas.pack()
            '''
    else:
        final_text = "Lutfen sehir ve ulke kodunu dogru girin"

        msg = tkinter.Message(window, text=final_text, font=FONT)
        msg.config(background= "light gray", width= 300)
        canvas.create_window(165, 270, window=msg)

        '''
        canvas = tkinter.Canvas(window, width=1000, height=2000)
        canvas.create_text(0, 0, text=final_text, fill="black", font=FONT)
        canvas.pack()
        '''
def find_weather():
    city = city_entry.get()
    country = country_entry.get()
    latitude, longitude = get_coordinates(city_name=city, country_code=country)
    if latitude and longitude:
        openweather_request(latitude=latitude, longitude=longitude)



# UI
FONT = ("Verdana", "11", "normal")

window = tkinter.Tk()

window.title("Weather")

canvas = tkinter.Canvas(window, width=324, height=575)
canvas.pack(fill = "both", expand = True)

image = Image.open("bg.png")
background_image = ImageTk.PhotoImage(image)
canvas.create_image(0, 0, image=background_image, anchor="nw")

city_label = tkinter.Label(text="Enter your city", font=FONT, padx=5, pady=5)
city_label.config(background="light gray")
canvas.create_window(165, 75, window= city_label)

city_entry = tkinter.Entry()
city_entry.config(width= 40)
canvas.create_window(165, 105, window= city_entry)


country_label = tkinter.Label(text="Enter your country code", font=FONT, padx=5, pady=5)
country_label.config(background="light gray")
canvas.create_window(165, 150, window= country_label)

country_entry = tkinter.Entry()
country_entry.config(width= 40)
canvas.create_window(165, 180, window= country_entry)

find_button = tkinter.Button()
find_button.config()


find_button = tkinter.Button(text="Find Weather", command=find_weather)
find_button.config(padx=5, pady=5)
canvas.create_window(165, 250, window= find_button)






window.mainloop()
