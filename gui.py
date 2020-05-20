import tkinter as tk
from tkinter import *
import pandas as pd
import numpy as np

url_cases = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"

url_deaths = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"

data_cases = pd.read_csv(url_cases)
data_deaths = pd.read_csv(url_deaths)

# cases_dates = data_cases.loc[:,"1/22/20":].columns
dates = data_deaths.loc[:,"1/22/20":].columns
dates = dates[::-1]
states = np.unique(data_deaths["Province_State"])


root = tk.Tk()

root.title("COVID Time Series")

root.geometry("500x500")

def reset():
    for widget in root.winfo_children():
        widget.destroy()
    get_states()


def first_draw():
    welcome = tk.Label(text = "Hello! This application is designed to only provide you with the data for covid cases and deaths in the United States.\n" 
    "This data is maintained by Johns Hopkins and can be found on their reposity found here: \nhttps://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data", wraplength = 400)
    welcome.place(relx = .5, rely = .2, anchor = 'center')
    next_button = tk.Button(text = "Next", command = reset)
    next_button.place(relx = .5, rely = .5, anchor = 'center')


def get_states():
    state_var = StringVar(root)
    state_var.set(states[0])
    state_menu = OptionMenu(root, state_var, *states)
    state_menu.place(relx = .5, rely = .25, anchor = 'center')

    next_county = tk.Button(text = "Next", command = lambda: get_county(state_var.get()))
    next_county.place(relx =.5, rely = .3, anchor = 'center')

    reset_button = tk.Button(text = "clear", command = reset)
    reset_button.place(relx = .5, rely = .9, anchor = 'center')


def get_county(state_var):
    for widget in root.winfo_children():
        widget.destroy()

    counties = data_deaths.loc[(data_deaths["Province_State"] == state_var)]["Admin2"].values

    state_label = tk.Label(text = state_var)
    state_label.place(relx = .5, rely = .25, anchor = 'center')

    county_var = StringVar(root)
    county_var.set(counties[0])
    county_menu = OptionMenu(root, county_var, *counties)
    county_menu.place(relx = .5, rely = .3, anchor = 'center')

    next_county = tk.Button(text = "Next", command = lambda: get_date(state_var, county_var.get()))
    next_county.place(relx =.5, rely = .35, anchor = 'center')

    reset_button = tk.Button(text = "clear", command = reset)
    reset_button.place(relx = .5, rely = .9, anchor = 'center')


def get_date(state_var, county_var):
    for widget in root.winfo_children():
        widget.destroy()

    from_date = StringVar(root)
    from_date.set(dates[0])
    from_date_menu = OptionMenu(root, from_date, *dates)
    from_date_menu.place(relx = .4, rely = .35, anchor = 'center')

    to_label = tk.Label(text = "to")
    to_label.place(relx = .5, rely = .35, anchor = 'center')

    to_date = StringVar(root)
    to_date.set(dates[0])
    to_date_menu = OptionMenu(root, to_date, *dates)
    to_date_menu.place(relx = .6, rely = .35, anchor = 'center')

    state_label = tk.Label(text = state_var)
    state_label.place(relx = .5, rely = .25, anchor = 'center')

    county_label = tk.Label(text = county_var)
    county_label.place(relx = .5, rely = .3, anchor = 'center')

    next_deaths_cases = tk.Button(text = "Next", command = lambda: deaths_cases(state_var, county_var, from_date.get(), to_date.get()))
    next_deaths_cases.place(relx =.5, rely = .4, anchor = 'center')

    reset_button = tk.Button(text = "clear", command = reset)
    reset_button.place(relx = .5, rely = .9, anchor = 'center')


def deaths_cases(state_var, county_var, from_date, to_date):
    for widget in root.winfo_children():
        widget.destroy()

    outcomes = ["Cases", "Deaths"]

    which_data = StringVar(root)
    which_data.set(outcomes[0])
    which_data_menu = OptionMenu(root, which_data, *outcomes)
    which_data_menu.place(relx = .5, rely = .4, anchor = 'center')

    state_label = tk.Label(text = state_var)
    state_label.place(relx = .5, rely = .25, anchor = 'center')

    county_label = tk.Label(text = county_var)
    county_label.place(relx = .5, rely = .3, anchor = 'center')

    from_date_label = tk.Label(text = from_date)
    from_date_label.place(relx = .4, rely = .35, anchor = 'center')

    to_label = tk.Label(text = "to")
    to_label.place(relx = .5, rely = .35, anchor = 'center')

    to_date_label = tk.Label(text = to_date)
    to_date_label.place(relx = .6, rely = .35, anchor = 'center')

    next_results = tk.Button(text = "Next", command = lambda: results(state_var, county_var, from_date, to_date, which_data.get()))
    next_results.place(relx =.5, rely = .45, anchor = 'center')

    reset_button = tk.Button(text = "clear", command = reset)
    reset_button.place(relx = .5, rely = .9, anchor = 'center')


def results(state_var, county_var, from_date, to_date, which_data):
    for widget in root.winfo_children():
        widget.destroy()
    
    if from_date == to_date:
        if which_data == "Deaths":
            ans = data_deaths.loc[(data_deaths["Province_State"] == state_var) & (data_deaths["Admin2"] == county_var)][from_date].values
            results_label = tk.Label(text = "Deaths on " + from_date + " in " + county_var + " county, " + state_var + ": \n" + str(int(ans)))
            results_label.place(relx = .5, rely = .5, anchor = 'center')
        else:
            ans = data_cases.loc[(data_cases["Province_State"] == state_var) & (data_cases["Admin2"] == county_var)][from_date].values
            results_label = tk.Label(text = "Total cases on " + from_date + " in " + county_var + " county, " + state_var + ": \n" + str(int(ans)))
            results_label.place(relx = .5, rely = .5, anchor = 'center')
    else:
        if which_data == "Deaths":
            ans = data_deaths.loc[(data_deaths["Province_State"] == state_var) & (data_deaths["Admin2"] == county_var), from_date:to_date].values
            results_label = tk.Label(text = "Deaths from " + from_date +"to "+to_date+ " in " + county_var + " county, " + state_var + ": \n" + str(ans))#, wraplength = 400)
            results_label.place(relx = .5, rely = .5, anchor = 'center')
        else:
            ans = data_cases.loc[(data_cases["Province_State"] == state_var) & (data_cases["Admin2"] == county_var), from_date:to_date].values
            results_label = tk.Label(text = "Total cases from " + from_date + " " + "to " + to_date + " in " + county_var + " county, " + state_var + ": \n" + str(ans))#, wraplength = 400)
            results_label.place(relx = .5, rely = .5, anchor = 'center')
            # for i in ans:
            #     for val in i:
            #         results_label = tk.Label(text = val)#"Total cases on " + from_date + ": \n" + str(np.matrix(ans)))
            #         results_label.pack()#.place(relx = .5, rely = .5, anchor = 'center')
    
    reset_button = tk.Button(text = "clear", command = reset)
    reset_button.place(relx = .5, rely = .9, anchor = 'center')

first_draw()

root.mainloop()