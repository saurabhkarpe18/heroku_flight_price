import pickle

from flask import Flask, render_template, request
import numpy as np
import json
import datetime
import math

app = Flask(__name__)
model = pickle.load(open("./model/flightPrice1.pkl", "rb"))

@app.route('/')
def dropDown():
    with open('./model/flightADAS.json', 'r') as f:
        arrival = json.load(f)['arrival']
    with open('./model/flightADAS.json', 'r') as f:
        departure = json.load(f)['departure']
    with open('./model/flightADAS.json', 'r') as f:
        airline = json.load(f)['airline']
    with open('./model/flightADAS.json', 'r') as f:
        stops = json.load(f)['stops']
    return render_template('flight1.html', arrival=arrival, departure=departure, airline=airline,
                           stops=stops)

@app.route("/predict", methods = ["GET", "POST"])
def predict():
    airline_air_India = 0
    airline_Goair = 0
    airline_IndiGo = 0
    airline_Jet_airways = 0
    airline_Jet_airways_Business = 0
    airline_Multiple_carriers = 0
    airline_Multiple_carriers_Premium_economy = 0
    airline_spiceJet = 0
    airline_Trujet = 0
    airline_Vistara = 0
    airline_Vistara_Premium_economy = 0

    # delhi ,Kolkata ,Banglore ,Mumbai ,Chennai

    departure_station_Chennai = 0
    departure_station_delhi = 0
    departure_station_Kolkata = 0
    departure_station_Mumbai = 0

    # Cochin ,Banglore ,delhi ,Hyderabad,Kolkata

    arrival_station_Cochin = 0
    arrival_station_delhi = 0
    arrival_station_Hyderabad = 0
    arrival_station_Kolkata = 0

    stop1=0

    #################################################

    if request.method == "POST":

        deptime = request.form["deptime"]
        deptime = deptime.replace('T', ' ')
        day = int(datetime.datetime.strptime(deptime, "%Y-%m-%d %H:%M").day)
        month = int(datetime.datetime.strptime(deptime, "%Y-%m-%d %H:%M").month)
        # print("Journey Date : ",Journey_day, Journey_month)

        # Departure
        departure_hr = int(datetime.datetime.strptime(deptime, "%Y-%m-%d %H:%M").hour)
        departure_mins = int(datetime.datetime.strptime(deptime, "%Y-%m-%d %H:%M").minute)
        # print("Departure : ",Dep_hour, Dep_min)

        # Arrival
        arrtime = request.form["arrtime"]
        arrtime = arrtime.replace('T', ' ')
        arrival_hr = int(datetime.datetime.strptime(arrtime, "%Y-%m-%d %H:%M").hour)
        arrival_mins = int(datetime.datetime.strptime(arrtime, "%Y-%m-%d %H:%M").minute)
        # print("Arrival : ", Arrival_hour, Arrival_min)

        stops = request.form["stops"]

        if stops =='non-stop':
            stop1 = 0
        elif stops =='1 stop':
            stop1 = 1
        elif stops =='2 stops':
            stop1 = 2
        else:
            stop1=3



        ######################################################################################

        airline = request.form['airline']

        if airline == 'air India':
            airline_air_India = 1

        elif airline == 'Goair':
            airline_Goair = 1

        elif airline == 'IndiGo':
            airline_IndiGo = 1

        elif airline == 'Jet airways':
            airline_Jet_airways = 1

        elif airline == 'Jet airways Business':
            airline_Jet_airways_Business = 1

        elif airline == 'Multiple carriers':
            airline_Multiple_carriers = 1

        elif airline == 'Multiple carriers Premium economy':
            airline_Multiple_carriers_Premium_economy = 1

        elif airline == 'spiceJet':
            airline_spiceJet = 1

        elif airline == 'Trujet':
            airline_Trujet = 1

        elif airline == 'Vistara':
            airline_Vistara = 1

        elif airline == 'Vistara Premium economy':
            airline_Vistara_Premium_economy = 1

        else:
            airline_air_India = 0
            airline_Goair = 0
            airline_IndiGo = 0
            airline_Jet_airways = 0
            airline_Jet_airways_Business = 0
            airline_Multiple_carriers = 0
            airline_Multiple_carriers_Premium_economy = 0
            airline_spiceJet = 0
            airline_Trujet = 0
            airline_Vistara = 0
            airline_Vistara_Premium_economy = 0

        #######################################################################

        departure = request.form["departure"]

        if departure == 'Chennai':
            departure_station_Chennai = 1
        elif departure == 'Delhi':
            departure_station_delhi = 1
        elif departure == 'Kolkata':
            departure_station_Kolkata = 1
        elif departure == 'Mumbai':
            departure_station_Mumbai = 1
        else:
            departure_station_Chennai = 0
            departure_station_delhi = 0
            departure_station_Kolkata = 0
            departure_station_Mumbai = 0

        ####################################################################

        arrival = request.form["arrival"]

        if arrival == 'Cochin':
            arrival_station_Cochin = 1
        elif arrival == 'Delhi':
            arrival_station_delhi = 1
        elif arrival == 'Hyderabad':
            arrival_station_Hyderabad = 1
        elif arrival == 'Kolkata':
            arrival_station_Kolkata = 1
        else:
            arrival_station_Cochin = 0
            arrival_station_delhi = 0
            arrival_station_Hyderabad = 0
            arrival_station_Kolkata = 0

        ####################################################################################################
        print(stop1,departure_hr,departure_mins,arrival_hr,arrival_mins,day, month,
              airline_air_India ,airline_Goair ,airline_IndiGo ,airline_Jet_airways ,
               airline_Jet_airways_Business ,airline_Multiple_carriers ,airline_Multiple_carriers_Premium_economy ,
               airline_spiceJet ,airline_Trujet ,airline_Vistara ,airline_Vistara_Premium_economy,
              departure_station_Chennai ,departure_station_delhi ,departure_station_Kolkata ,
               departure_station_Mumbai ,arrival_station_Cochin ,arrival_station_delhi ,
               arrival_station_Hyderabad ,arrival_station_Kolkata)

        prediction = model.predict(np.array([[stop1, departure_hr, departure_mins, arrival_hr, arrival_mins, day, month,
                                              airline_air_India, airline_Goair, airline_IndiGo, airline_Jet_airways,
                                              airline_Jet_airways_Business, airline_Multiple_carriers,
                                              airline_Multiple_carriers_Premium_economy,
                                              airline_spiceJet, airline_Trujet, airline_Vistara,
                                              airline_Vistara_Premium_economy,
                                              departure_station_Chennai, departure_station_delhi,
                                              departure_station_Kolkata,
                                              departure_station_Mumbai, arrival_station_Cochin, arrival_station_delhi,
                                              arrival_station_Hyderabad, arrival_station_Kolkata]])[0:1])
        output = round(math.e**(float(round(prediction[0], 2))),2)

        return render_template('flight1.html', prediction_text="Your Flight price is Rs. {}".format(output))
    return render_template("flight1.html")


if __name__ == "__main__":
    app.run(debug=True)

