import tkinter as tk
import requests

# FastAPI backend URL
FASTAPI_URL = "http://127.0.0.1:8000/weather"

# Mapping weather conditions to emojis
WEATHER_ICONS = {
    "clear sky": "☀️",
    "few clouds": "🌤️",
    "scattered clouds": "⛅",
    "broken clouds": "☁️",
    "shower rain": "🌧️",
    "rain": "🌦️",
    "thunderstorm": "⛈️",
    "snow": "❄️",
    "mist": "🌫️",
}

# Function to determine temperature color & emojis
def get_temp_style(temp):
    if temp <= 5:
        return "blue", "❄️"  
    elif temp <= 20:
        return "yellow", ""  
    else:
        return "red", "🔥"  

# Function to convert Celsius to Fahrenheit
def convert_temperature(temp_c):
    return round((temp_c * 9/5) + 32, 1)

# Function to fetch weather
def get_weather():
    city = city_entry.get()
    if not city:
        result_label.config(text="Please enter a city name.", font=("Arial", 14))
        return

    try:
        response = requests.get(f"{FASTAPI_URL}?city={city}")
        data = response.json()

        if "error" in data:
            result_label.config(text="City not found or API error.", font=("Arial", 14))
            temp_label.config(text="")
            weather_icon_label.config(text="")
            condition_label.config(text="")
        else:
            temp_c = round(data['temperature'], 1)
            temp_f = convert_temperature(temp_c)
            weather = data['weather']

            # Check Fahrenheit toggle
            if fahrenheit_var.get():
                temperature = f"{temp_f}°F"
            else:
                temperature = f"{temp_c}°C"

            color, emoji = get_temp_style(temp_c)
            weather_icon = WEATHER_ICONS.get(weather, "☁️") 

            # Update labels
            temp_label.config(text=f"{emoji} {temperature} {emoji}", font=("Arial", 40, "bold"), fg=color)
            weather_icon_label.config(text=weather_icon, font=("Arial", 80))
            condition_label.config(text=weather, font=("Arial", 18))
    except requests.exceptions.RequestException:
        result_label.config(text="Error connecting to API.", font=("Arial", 14))

# Create Tkinter window
root = tk.Tk()
root.title("Weather App")
root.geometry("350x550")
root.resizable(False, False)
root.configure(bg="#87CEEB")  

# City Input
city_label = tk.Label(root, text="Enter city name:", font=("Arial", 16, "italic"), bg="#87CEEB")
city_label.pack(pady=(20, 5))

city_entry = tk.Entry(root, font=("Arial", 18), justify="center", width=20, bd=2, relief="solid", bg="lightgreen")
city_entry.pack(pady=10)

# Custom Yellow Button 
button_canvas = tk.Canvas(root, width=160, height=50, bg="#87CEEB", highlightthickness=0)
button_canvas.pack(pady=10)
button_rect = button_canvas.create_rectangle(5, 5, 155, 45, fill="yellow", outline="black", width=2)
button_text = button_canvas.create_text(80, 25, text="Get Weather", font=("Arial", 14, "bold"), fill="black")

def button_click(event):
    get_weather()

button_canvas.tag_bind(button_rect, "<Button-1>", button_click)
button_canvas.tag_bind(button_text, "<Button-1>", button_click)

# Fahrenheit Toggle
fahrenheit_var = tk.BooleanVar(value=False)
fahrenheit_toggle = tk.Checkbutton(root, text="Show temperature in Fahrenheit", font=("Arial", 12),
                                   variable=fahrenheit_var, bg="#87CEEB", activebackground="#87CEEB")
fahrenheit_toggle.pack(pady=5)

# Display Temperature & Weather
temp_label = tk.Label(root, text="", font=("Arial", 50, "bold"), bg="#87CEEB")
temp_label.pack(pady=10)

weather_icon_label = tk.Label(root, text="", font=("Arial", 80), bg="#87CEEB")
weather_icon_label.pack()

condition_label = tk.Label(root, text="", font=("Arial", 18), bg="#87CEEB")
condition_label.pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 14), bg="#87CEEB")
result_label.pack()

root.mainloop()
