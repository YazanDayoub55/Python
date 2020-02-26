import requests
from decimal import getcontext, Decimal
import datetime
import pandas as pd
import matplotlib.pyplot as plt 
import tkinter
from tkinter import messagebox



#this is our data base
#default time
lastrequestdate = datetime.datetime(year=2020, month=2, day=25, hour=18)
#currency List
rate_name = []
#currency value
rate_value = []

#this fnction return currencies information
def checkdifferancetime():
    global lastrequestdate
    global rate_name
    global rate_value
    #check today date
    currentDT = datetime.datetime.now()
    #calculate the differance between load time from date base and curent date
    datedifferance = currentDT - lastrequestdate
    minute = datedifferance.total_seconds()/60
    #if differance is less than 10 minutes use data base 
    if(minute < 10):
        for x in range(1,len(rate_value)):
            i = rate_value[x]*100
            j = int(i)
            i = j/100
            print(rate_name[x],':',i)
    #if differance is bigger than 10 minutes
    if(minute >= 10):
    
        #save new date in database
        lastrequestdate = datetime.datetime.now()
        url = 'https://api.exchangerate-api.com/v4/latest/USD'

        # Making our request
        response = requests.get(url)
        data = response.json()

        # Extract rates and put in List
        key_list = list(data.keys()) 
        val_list = list(data.values()) 
        rate_data = data['rates']
        rate_name = list(rate_data.keys())
        rate_value = list(rate_data.values())


        for x in range(1,len(rate_value)):
            i = rate_value[x]*100
            j = int(i)
            i = j/100
            print(rate_name[x],':',i)
    return(rate_name,rate_value,lastrequestdate)
#this function convert to USD to currency, name is the name of the currency, money is the amount of money we want to convert
def convertto(money, name):
    #load data
    checkdifferancetime()
    #load data base 
    global rate_name
    global rate_value
    #find the index of the currency name
    index = rate_name.index(name)
    #use the convert
    result = money*rate_value[index]
    i = result*100
    j = int(i)
    i = j/100
    return i
#this function find exchange rate for currency, name is the currency name
def history(name):
        #take tody date
        tody = datetime.datetime.now().strftime('%Y-%m-%d')
        #find the date of the last week
        end_date = datetime.datetime.now() + datetime.timedelta(days=-7)
        #convert to String
        lasweek = end_date.strftime('%Y-%m-%d')
        #use the last week date and tody date and currency name in the query url
        url = 'https://api.exchangeratesapi.io/history?start_at=%s&end_at=%s&base=USD&symbols=%s'%(lasweek,tody,name)
        # Making our request
        response_ = requests.get(url)
        data_ = response_.json()
        # Extract rates and put in List
        rate_data_ = data_['rates']
        #if rates number is bigger than zero then there are exchange information we can show
        if(len(rate_data_) > 0):
            #extract data from the response
            rate_data_date = list(rate_data_.keys())
            rate_value_date = list(rate_data_.values())
            rate_val_drw = []
            #convert data to list to drw
            for y in range(0,len(rate_value_date)):
                rate_val_drw.append(list(rate_value_date[y].values())[0])   
            #sort dates
            rate_data_date.sort()
            plt.plot(rate_data_date,rate_val_drw) 
            plt.xlabel('Dates') 
            plt.ylabel('Exchange rate') 
            plt.title('Graph history rate for %s currency'%(name)) 
            plt.show()
        #here the case is rates number equal to zero so we have to show error message
        else:
            root = tkinter.Tk()
            root.withdraw()
            messagebox.showerror("Warning", "No exchange rate data is available for the selected currency")




#first part
checkdifferancetime()
#second part
amountmony = 10
name = 'CAD'
resultconvert = convertto(amountmony,name)
print(resultconvert)
#third & fourth part
name = 'CAD'
history(name)
