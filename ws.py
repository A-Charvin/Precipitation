#####################################################################
# UI Based Precipitation Shape File Generator                       #
# Created for Kawartha Regional Conservation Authority              #
# By Anand Charvin G  - 2024                                        #
# This tool generates a shapefile based on the provided data        #
#                                                                   #
# Usage:                                                            #
#   python WS.py                                                    #
#####################################################################

import tkinter as tk
from tkinter import ttk, messagebox
import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
from PIL import Image, ImageTk
from datetime import datetime


# Hardcoded weather station data
weather_stations = {
    "Indian Point Provincial Park": (671762.467765, 4942091.670869),
    "Trent Lakes": (698755.170782, 4939899.274223),
    "Ken Reid CA": (677995.773456, 4919108.288842),
    "Emily Provincial Park": (696573.633603, 4912811.396583),
    "Mariposa Brook": (672204.305075, 4906307.845103),
    "Port Perry Weather Station": (663228.542903, 4886175.508981),
    "Blackstock Creek": (673675.877741, 4888815.840527),
    "Pigeon River": (684408.215127, 4888258.639894)
}

class WeatherStationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Station Data Entry")
        
        # GUI Components
        self.create_widgets()
        
        # Data Storage
        self.data = []

    def create_widgets(self):
        # Station Selection
        self.station_label = tk.Label(self.root, text="Station:")
        self.station_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.station_combo = ttk.Combobox(self.root, values=list(weather_stations.keys()), state="readonly")
        self.station_combo.grid(row=0, column=1, padx=10, pady=10)
        self.station_combo.bind("<<ComboboxSelected>>", self.populate_coordinates)

        # Add New Station Section
        self.new_station_label = tk.Label(self.root, text="New Station (optional):")
        self.new_station_label.grid(row=1, column=0, padx=10, pady=10)
        
        self.new_station_entry = tk.Entry(self.root)
        self.new_station_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Date Entry
        self.date_label = tk.Label(self.root, text="Date (DD-MM-YY):")
        self.date_label.grid(row=2, column=0, padx=10, pady=10)
        
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=2, column=1, padx=10, pady=10)
        
        # Precipitation Entry
        self.precipitation_label = tk.Label(self.root, text="Precipitation (mm):")
        self.precipitation_label.grid(row=3, column=0, padx=10, pady=10)
        
        self.precipitation_entry = tk.Entry(self.root)
        self.precipitation_entry.grid(row=3, column=1, padx=10, pady=10)
        
        # Coordinates Entry
        self.coord_label = tk.Label(self.root, text="Coordinates (X, Y):")
        self.coord_label.grid(row=4, column=0, padx=10, pady=10)
        
        self.coord_entry = tk.Entry(self.root)
        self.coord_entry.grid(row=4, column=1, padx=10, pady=10)
        
        # Buttons
        self.add_button = tk.Button(self.root, text="Add Entry", command=self.add_entry)
        self.add_button.grid(row=5, column=0, padx=10, pady=10)
        
        self.save_button = tk.Button(self.root, text="Save to Shapefile", command=self.save_to_shapefile)
        self.save_button.grid(row=5, column=1, padx=10, pady=10)
        
        # Preview List
        self.preview_label = tk.Label(self.root, text="Preview:")
        self.preview_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        
        self.preview_listbox = tk.Listbox(self.root, width=50, height=10)
        self.preview_listbox.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    def populate_coordinates(self, event):
        station = self.station_combo.get()
        if station in weather_stations:
            coords = weather_stations[station]
            self.coord_entry.delete(0, tk.END)
            self.coord_entry.insert(0, f"{coords[0]}, {coords[1]}")
    
    def add_entry(self):
        station = self.station_combo.get()
        new_station = self.new_station_entry.get()
        date = self.date_entry.get()
        precipitation = self.precipitation_entry.get()
        coords = self.coord_entry.get()
        
        if new_station:
            if new_station in weather_stations:
                messagebox.showerror("Input Error", "Station already exists.")
                return
            else:
                station = new_station
                weather_stations[new_station] = None
                messagebox.showinfo('Success', "New station added successfully.")
        
        if not (station and date and precipitation and coords):
            messagebox.showerror("Input Error", "Please fill in all fields.")
            return
        
        # Validate date
        try:
            datetime.strptime(date, '%d-%m-%y')
        except ValueError:
            messagebox.showerror("Input Error", "Date must be in DD-MM-YY format.")
            return
        
        try:
            x, y = map(float, coords.split(","))
        except ValueError:
            messagebox.showerror("Input Error", "Coordinates must be two numbers separated by a comma.")
            return
        
        entry = (station, date, float(precipitation), x, y)
        self.data.append(entry)
        self.preview_listbox.insert(tk.END, f"{entry}")

        if new_station:
            self.station_combo['values'] = list(weather_stations.keys())
            self.new_station_entry.delete(0, tk.END)
    
    def save_to_shapefile(self):
        if not self.data:
            messagebox.showerror("Data Error", "No data to save.")
            return
        
        # Rename columns to be 10 characters or less
        df = pd.DataFrame(self.data, columns=["Station", "Date", "Prec", "X", "Y"])
        gdf = gpd.GeoDataFrame(df, geometry=[Point(xy) for xy in zip(df.X, df.Y)], crs="EPSG:4326")
        
        filepath = "weather_stations.shp"
        gdf.to_file(filepath)
        messagebox.showinfo("Success", f"Data successfully saved to {filepath}")

# Main
if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherStationApp(root)
    ico = Image.open(r'ws.png')
    photo = ImageTk.PhotoImage(ico)
    root.wm_iconphoto(False, photo)
    root.mainloop()

# GUI Code Samples and Source : https://realpython.com/python-gui-tkinter/
# Icon Section Sourced from : https://stackoverflow.com/questions/33137829/how-to-replace-the-icon-in-a-tkinter-app
# Icon source : https://www.flaticon.com/free-icons/rainy 
# Rainy icons created by berkahicon - Flaticon
