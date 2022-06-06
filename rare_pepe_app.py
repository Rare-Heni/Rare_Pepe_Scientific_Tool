from ast import If
from cmath import nan
from errno import EILSEQ
from pickle import TRUE
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import requests, json
import pandas as pd
from requests.auth import HTTPBasicAuth
from decimal import Decimal
from datetime import datetime
from datetime import date
import time
from pathlib import Path

# Title and Sidebar UI
from PIL import Image
st.set_page_config(layout="wide")

#ulm = Image.open("99_ulm.png")
pepe = Image.open("99_pepe.png")
st.sidebar.image(pepe)
c1, c2 = st.columns((2, 2))


endpoint_choices = ['Counterparty','Opensea']
endpoint = "Counterparty"

def header(content):
     c1.markdown(f'<p style="background-color:#ffffff;color:#011839;font-size:40px;border-radius:2%;">{content}</p>', unsafe_allow_html=True)
     c2.markdown(f'<p style="background-color:#ffffff;color:#ffffff;font-size:40px;border-radius:2%;">{content}</p>', unsafe_allow_html=True)

header("Rare Pepe Scientific Analysis Tool")

#############################################################
# Current prices Cryptocurrencies
#############################################################

if endpoint == "Counterparty":
    url = "https://xchain.io/api/network"
    headers = {'content-type': 'application/json'}
    auth = HTTPBasicAuth('rpc', '1234')
                
    # Speichern des Outputs als JSON Output um damit zu arbeiten
    response= requests.post(url, headers=headers, auth=auth)
    response = response.json()

    bitcoin_price = float(response["currency_info"][0]["price_usd"])
    xcp_price = float(response["currency_info"][1]["price_usd"])

    url = "https://xchain.io/api/asset/PEPECASH"
    headers = {'content-type': 'application/json'}
    auth = HTTPBasicAuth('rpc', '1234')
                
    # Speichern des Outputs als JSON Output um damit zu arbeiten
    response= requests.post(url, headers=headers, auth=auth)
    response = response.json()

    pepecash_price = float(response["estimated_value"]["usd"])

#############################################################
# Counterparty API
#############################################################

if endpoint == "Counterparty":
    import json
    import requests
    from requests.auth import HTTPBasicAuth
    from decimal import Decimal
    from datetime import datetime
    import time

    with st.sidebar.form(key = "columns in form"):
        st.subheader("Analysis Method")
        unweighted = st.checkbox("Unweighted Price Index")
        marketcap_weighted = st.checkbox("Market Cap Weighted Price Index")
        gini_coef = st.checkbox("Gini-Coefficient")
        volume_sold = st.checkbox("Volume Sold")
        #regression = st.checkbox("Regression Analysis")
        regression = False
        dataset_analysis = st.checkbox("Dataset")
        
        st.subheader("Filters")
        observation_time = st.selectbox(label = "Period of Time", options = ["All",2016,2017,2018,2019,2020,2021,2022])

        all_series = ["All"]
        series_test = list(range(1,38))
        all_series.extend(series_test)

        card_series = st.selectbox(label = "Card Series", options = all_series)

        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

        card_supply = st.radio(label = "Max Supply Card", options = [100, 500,1000])
        number_transactions = st.radio(label = "Min Number Transactions", options = [5,10])

        st.subheader("Benchmark Index")
        bitcoin_index = st.checkbox("Bitcoin")
        xcp_index = st.checkbox("XCP")
        pepecash_index = st.checkbox("PepeCash")
        nasdaq_index = st.checkbox("NASDAQ")  
        submitted = st.form_submit_button("Submit")
    st.sidebar.subheader("Impressum")
    st.sidebar.caption("This dashboard is a result of the master thesis of Henrik Pitz. If you like the analysis, you can support me with a donation at the following address. I am working on adding more analysis.")

    # Testen ob die Daten bereits aktuell sind
    f = open( "99_Load_Month.txt", 'r' )
    file_contents = f.read()
    load_month = file_contents

    begin_time = datetime.now()
    current_month = begin_time.strftime("%Y-%m")

    # Hier wird die Excel mit allen aktuellen Rare Pepe Karten eingelesen (Update falls neue Karten dazukommen)
    # !!! Dieses Befehl musss für jeden User angepasst werden und die Excel lokal gespeichert werden !!! )
    #df_all_pepes = pd.read_excel ('/Users/henrikpitz/Desktop/Masterthesis NFT/All_Rare_Pepes.xlsx')
    #df_all_pepes.to_csv('03_all_information_pepes.csv')

    df_all_pepes = pd.read_csv ("03_all_information_pepes.csv")

    if card_supply != "All":
        
        if card_supply == 100:
            #df_pepes = pd.read_csv("07_all_pepes_supply_max_100_test.csv")
            df_pepes = pd.read_csv("07_all_pepes_supply_max_100.csv")

        if card_supply == 500:
            df_pepes = pd.read_csv("08_all_pepes_supply_max_500.csv")

        if card_supply == 1000:
            df_pepes = pd.read_csv("09_all_pepes_supply_max_1000.csv")

        if card_supply == 10000:
            df_pepes = pd.read_csv("10_all_pepes_supply_max_10000.csv")

    if card_supply == "All":
        df_pepes = pd.read_csv ("04_official_rare_pepes.csv")


    df_pepes = df_pepes.iloc[: , 1:]
    pepes_list = df_pepes["Name"].tolist()
    official_rare_pepes = pepes_list

    #Nur zum testen !!!!!!!
    #official_rare_pepes = ["RAREQUEEM"]

    # Falls nichts ausgewählt wird kommt die Startseite zu Rare Pepes, wird später noch angepasst
    # Aktuell hier meine Themen die noch offen sind
    if unweighted == False and marketcap_weighted == False and volume_sold == False and dataset_analysis == False and gini_coef == False and regression == False:
        
        st.subheader("Fragen:")
        st.write("- Bereinigung innerhalb der Variable, max Preis ist ein Outlier! ~600k")
        st.write("- Regressionslinie hinzufügen bei den Plots")
        st.write("- Zwischenergebnisse anzeigen lassen bei der Bereinigung")

        st.subheader("To-Do's:")
        st.write("1. Code anpassen hinsichtlich Filter: Period of Time und Card Series")
        st.write("2. Korrelation zwischen Rare Pepes Index und Vergleichsindizes berechnen (Im Paper suchen) ")
        st.write("4. Anschauen wie ich damit mein Dashboard aufwerten kann: https://www.youtube.com/watch?v=Km2KDo6tFpQ ")
        st.write("5. Website live schalten auf GitHub mit https://share.streamlit.io")

        st.subheader("Anpassungen hinsichtlich Performance und Genauigkeit:")
        st.write("- Woher bekomme ich historische Daten per API von Bitcoin, XCP; PepeCash und NASDAQ? (Meine Daten sind bis jetzt von Yahoo Finance, die API kostet hier aber)")  

        # Informationen von Wikipedia zu Rare Pepes
        if False:
            st.subheader("What is Rare Pepe?")
            st.write("""Pepe the Frog is a cartoon green anthropomorphic frog with a humanoid body. The character originated in the 2005 Matt Furie comic Boy's Club,[2] and became an Internet meme in 2008, popularised through Myspace, Gaia Online and 4chan. In the 2010s, the character's image was appropriated as a symbol of the alt-right movement, and by white supremacists.[3] The Anti-Defamation League included Pepe in its hate symbol database in 2016, but said most instances of Pepe were not used in a hate-related context.[4]

    In 2015, a subset of Pepe memes began to be referred to as 'rare Pepes', with watermarks such as "RARE PEPE DO NOT SAVE", generally meaning that the artist had not previously posted the meme publicly.[5] In April 2015, a collection of rare Pepes were listed on eBay where it reached a price of $99,166 before being removed from the site.[6]

    In September 2016, the very first rare Pepes were mined in block 428919 on Bitcoin, pre-dating popular Ethereum based NFTs. A Telegram chat group dedicated to discussing the Counterparty NFT was created shortly after.[7][8] By 2017, a community had grown around the digital collectables,[9] spurring developers to build platforms for the purpose of cataloging and exchanging these unique images, thereby creating the first crypto art market in 2016.[10] Two components of this market, created simultaneously, both support each other to enable interaction and asset exchange among both contributors and market participants. Crypto artists used these resources to publish their work as digital tokens with a fixed circulation[9] and then issued the art to collectors who then sold, traded, or stored their collections.

    "Rare Pepe Wallet" is a web-based, encrypted wallet developed to allow users to buy, sell, and store rare Pepes using a medium of exchange called PepeCash.[11] The backbone of the Rare Pepe Wallet is the Counterparty platform, which is built upon the bitcoin network.

    "Rare Pepe Directory" was a directory built to catalog all known rare Pepes, with specific guidelines for submitting the images for inclusion. (Source: Wikipedia)""")

# Wenn in der Searchbar ein Rare Pepe eingegeben wird
    elif current_month != load_month: 
        
        # Datensatz für Gini erstellen mit erster Transaktion als Issuance
        page_counter = 100
        page = 1

        column_names = ["Name","Type","Date","Date_Index","Series","Supply","Price in USD","Quantity", "Source", "Destination"]
        df_gini_ts = pd.DataFrame(columns = column_names)

        for names in official_rare_pepes:

            # API Call nach Dispenser und 100 Assets pro Seite
            url = "https://xchain.io/api/issuances/" + names + "/" + str(page) + "/100"
            headers = {'content-type': 'application/json'}
            auth = HTTPBasicAuth('rpc', '1234')
                            
            # Speichern des Outputs als JSON Output um damit zu arbeiten
            response_xchain = requests.post(url, headers=headers, auth=auth)
            response_xchain_json = response_xchain.json()

            for data in response_xchain_json["data"]:
                names = data["asset"]
                supply = float(data["quantity"])
                source = "NON"
                destination = data["issuer"]
                ts = time.gmtime(data['timestamp'])
                date = time.strftime("%Y-%m-%d %H:%M:%S", ts)
                date_index = time.strftime("%Y-%m", ts)

                if supply > 0:
                    df_gini_ts.loc[df_gini_ts.shape[0]] = [names,"sends",date,date_index,0, supply,0,supply, source, destination]

        column_names = ["Name", "Date", "Price", "Currency", "Price in USD", "Quantity" , "TX_Hash_Dispenser", "TX_Hash_Dispenses"]
        df_dispensers = pd.DataFrame(columns = column_names)

        column_total = ["Name","Series", "Date", "Price in USD", "Quantity", "Type", "Date_Index"]
        df_total = pd.DataFrame(columns = column_total)

        # Hier wird nach den Verkäufen durch Dispenser gesucht
        for names in official_rare_pepes:
            card = df_all_pepes.loc[df_all_pepes['Name'] == names]
            series = card["Series"].iloc[0]

            page_counter = 100
            page = 1
            Assets = 0
            Used_Dispensers = 0

            # Page Counter, dieser läuft so lange bis auf einer Seite keine Assets mehr angezeigt werden
            while page_counter > 0:

                # API Call nach Dispenser und 100 Assets pro Seite
                url = "https://xchain.io/api/dispensers/" + names + "/" + str(page) + "/100"
                headers = {'content-type': 'application/json'}
                auth = HTTPBasicAuth('rpc', '1234')
                
                # Speichern des Outputs als JSON Output um damit zu arbeiten
                response_xchain = requests.post(url, headers=headers, auth=auth)
                response_xchain_json = response_xchain.json()

                page = page + 1
                page_counter = 0
                
                # Auslesen der Dispenser um den Transaktions-Hash zu bekommen
                # Da Dispenser öfter als einmal benutzt werden können, reicht es nicht aus nur den Dispenser anzuschauen
                # Man braucht alle durchgeführten Dispenses pro Dispenser
                for data in response_xchain_json["data"]:

                    page_counter = page_counter + 1

                    tx_hash = data["tx_hash"]
                    Assets = Assets + 1

                    # API Call für die passenden Dispenses
                    url = "https://xchain.io/api/dispenses/" + tx_hash
                    headers = {'content-type': 'application/json'}
                    auth = HTTPBasicAuth('rpc', '1234')
                
                    # Speichern des Outputs als JSON Output um damit zu arbeiten
                    dispenses_xchain = requests.post(url, headers=headers, auth=auth)
                    response_dispenses_xchain = dispenses_xchain.json()

                    # Falls es bei den jeweiligen Transkationen einen Eintrag gibt, bedeutet das, dass der Dispenser benutzt wurde
                    if response_dispenses_xchain["total"] > 0:
                        Used_Dispensers = Used_Dispensers + 1

                        # Loop durch die Transaktionen um alle durchgeführten Dispenses zu bekommen
                        for transactions in response_dispenses_xchain["data"]:
                            value_give = float(data['satoshirate'])
                            quantity = float((data['give_quantity']))
                            ts = time.gmtime(transactions['timestamp'])
                            date = time.strftime("%Y-%m-%d %H:%M:%S", ts)    
                            date_index = time.strftime("%Y-%m", ts) 

                            TX_Hash_Dispenser = data["tx_hash"]
                            TX_Hash_Dispenses = transactions["tx_hash"]
                            quantity_dispenses = float((transactions['quantity']))
                            value = (value_give / quantity)

                            #NEU                           
                            url = "https://xchain.io/api/tx/" + TX_Hash_Dispenses
                            headers = {'content-type': 'application/json'}
                            auth = HTTPBasicAuth('rpc', '1234')

                            # Speichern des Outputs als JSON Output um damit zu arbeiten
                            info_dispenses = requests.post(url, headers=headers, auth=auth)
                            response_info_dispenses = info_dispenses.json()
                            
                            source = response_info_dispenses["source"]
                            destination = response_info_dispenses["destination"]

                            #info für gini
                            df_gini_ts.loc[df_gini_ts.shape[0]] = [names,"dispenser",date,date_index,series,0,value*bitcoin_price,quantity, source, destination] 
                            #NEU

                            #df_dispender
                            df_dispensers.loc[df_dispensers.shape[0]] = [names, date, value, "BTC", value*bitcoin_price, quantity_dispenses, TX_Hash_Dispenser, TX_Hash_Dispenses]

                            #in die große Tabelle einlesen
                            df_total.loc[df_total.shape[0]] = [names,series, date, value*bitcoin_price,quantity_dispenses, "dispenser", date_index]

        # Dispensers in CSV speichern
        df_dispensers.to_csv('all_transactions_dispensers.csv')

        column_names = ["Name", "Date", "Price", "Currency", "Price in USD"]
        df_get = pd.DataFrame(columns = column_names)
        df_give = pd.DataFrame(columns = column_names)

        for names in official_rare_pepes:

            # Hier wird nach den Verkäufen durch Orders gesucht
            card = df_all_pepes.loc[df_all_pepes['Name'] == names]
            series = str(card["Series"].iloc[0])

            Assets = 0
            page_counter = 100
            page = 1
            pages = 0

            # Page Counter, dieser läuft so lange bis auf einer Seite keine Assets mehr angezeigt werden
            while page_counter > 0:

                # API Call nach Orders und 100 Assets pro Seite
                url = "https://xchain.io/api/order_matches/" + names + "/" + str(page) + "/100"
                headers = {'content-type': 'application/json'}
                auth = HTTPBasicAuth('rpc', '1234')
                    
                page = page + 1
                pages = pages + 1

                # Speichern des Outputs als JSON Output um damit zu arbeiten
                response_xchain = requests.post(url, headers=headers, auth=auth)
                response_xchain_json = response_xchain.json()

                page_counter = 0

                # Loop über alle Assets
                for data in response_xchain_json["data"]:
                    page_counter = page_counter + 1

                    Assets = Assets + 1
                    
                    # Auslesen aller Get_Assets
                    if data["forward_asset"] == names:

                            value_order = float(data['backward_quantity'])
                            quantity = float(data['forward_quantity'])
                            currency = data["backward_asset"]
                            value = (value_order / quantity)
                            
                            value_usd = 0
                            if currency == "BTC":
                                value_usd = value * bitcoin_price
        
                            if currency == "XCP":
                                value_usd = value * xcp_price

                            if currency == "PEPECASH":
                                value_usd = value * pepecash_price

                            ts = time.gmtime(data['timestamp'])
                            date = time.strftime("%Y-%m-%d %H:%M:%S", ts)  
                            date_index = time.strftime("%Y-%m", ts)

                            destination = data["tx1_address"]
                            source = data["tx0_address"]

                            #info für gini
                            df_gini_ts.loc[df_gini_ts.shape[0]] = [names,"get",date,date_index,series,0,value_usd, quantity, source, destination] 
                            
                            # in die get Tabelle einlesen
                            df_get.loc[df_get.shape[0]] = [names,date, value, currency, value_usd]

                            # in die große Tabelle einlesen
                            df_total.loc[df_total.shape[0]] = [names, series, date, value_usd,quantity, "order_get", date_index]

                    # Auslesen aller Give_Assets
                    if data["backward_asset"] == names:

                            value_order = float((data['forward_quantity']))
                            quantity = float((data['backward_quantity']))
                            currency = data["forward_asset"]
                            value = (value_order / quantity)

                            value_usd = 0
                            if currency == "BTC":
                                value_usd = value * bitcoin_price
        
                            if currency == "XCP":
                                value_usd = value * xcp_price

                            if currency == "PEPECASH":
                                value_usd = value * pepecash_price
                            ts = time.gmtime(data['timestamp'])
                            date = time.strftime("%Y-%m-%d %H:%M:%S", ts)
                            date_index = time.strftime("%Y-%m", ts) 

                            source = data["tx1_address"]
                            destination = data["tx0_address"]

                            #info für gini
                            df_gini_ts.loc[df_gini_ts.shape[0]] = [names,"give",date,date_index,series,0,value_usd, quantity, source, destination]

                            # in die get Tabelle einlesen
                            df_give.loc[df_get.shape[0]] = [names, date, value, currency, value_usd]

                            #in die große Tabelle einlesen
                            df_total.loc[df_total.shape[0]] = [names, series, date, value_usd,quantity, "order_give", date_index]

        # Orders in csv speichern
        df_get.to_csv('all_transactions_get_orders.csv')
        df_give.to_csv('all_transactions_give_orders.csv')

        # Sends für den Gini
        for names in official_rare_pepes:

            Assets = 0
            page_counter = 100
            page = 1
            pages = 0

            # Page Counter, dieser läuft so lange bis auf einer Seite keine Assets mehr angezeigt werden
            while page_counter > 0:

                # API Call nach Orders und 100 Assets pro Seite
                url = "https://xchain.io/api/sends/" + names + "/" + str(page) + "/100"
                headers = {'content-type': 'application/json'}
                auth = HTTPBasicAuth('rpc', '1234')
                    
                page = page + 1
                pages = pages + 1

                # Speichern des Outputs als JSON Output um damit zu arbeiten
                response_xchain = requests.post(url, headers=headers, auth=auth)
                response_xchain_json = response_xchain.json()

                page_counter = 0

                # Loop über alle Assets
                for data in response_xchain_json["data"]:
                    page_counter = page_counter + 1

                    Assets = Assets + 1

                    # Auslesen aller Get_Assets
                    if data["status"] == "valid":

                            quantity = float(data['quantity'])

                            ts = time.gmtime(data['timestamp'])
                            date = time.strftime("%Y-%m-%d %H:%M:%S", ts)  
                            date_index = time.strftime("%Y-%m", ts)

                            source = data["source"]
                            destination = data["destination"]

                            #info für gini
                            df_gini_ts.loc[df_gini_ts.shape[0]] = [names,"sends",date,date_index,0,0,0, quantity, source, destination]              

        # Hier werden die Burns abgefragt und die reale Menge der Assets ausgerechnet
        column_names = ["Name", "Date", "Quantity"]
        df_burns = pd.DataFrame(columns = column_names)

        column_names = ["Name","Series", "Supply", "Burns" , "Remaining_Supply", "Remaining_Percentage"]
        df_burns_total = pd.DataFrame(columns = column_names)
        
        for names in official_rare_pepes:

            card = df_all_pepes.loc[df_all_pepes['Name'] == names]
            series = card["Series"].iloc[0]

            page_counter = 100
            page = 1
            Assets = 0
            Used_Dispensers = 0
            total_quantity_burns = 0

            # Abfragen der Holders der Assets
            while page_counter > 0:

                url = "https://xchain.io/api/holders/" + names + "/" + str(page) + "/100"
                headers = {'content-type': 'application/json'}
                auth = HTTPBasicAuth('rpc', '1234')
                
                response_xchain = requests.post(url, headers=headers, auth=auth)
                response_xchain_json = response_xchain.json()

                page = page + 1
                page_counter = 0

                # Loop durch die Holders und Abfrage ob die Adresse "Burn" enthält
                for data in response_xchain_json["data"]:
                    page_counter = page_counter + 1
                    address = "nopepe"

                    # Falls ja wir die Holder-Adresse gespeichert
                    if "Burn" in data["address"]:
                        address = data["address"]

                    if "BURN" in data["address"]:
                        address = data["address"]
                        
                    if address != "nopepe":

                        page_counter_1 = 100
                        page_1 = 1

                        while page_counter_1 > 0:

                            # API Call um die Sends der Burn Adresse zu analysieren
                            # Alle Assets die hierher gesendet wurden sind geburned
                            url = "https://xchain.io/api/sends/"+  address + "/" + str(page_1) + "/100"
                            headers = {'content-type': 'application/json'}
                            auth = HTTPBasicAuth('rpc', '1234')
                
                            response_xchain = requests.post(url, headers=headers, auth=auth)
                            response_xchain_json = response_xchain.json()

                            page_1 = page_1 + 1
                            page_counter_1 = 0
                            
                            for data in response_xchain_json["data"]:
                                page_counter_1 = page_counter_1 + 1

                                # Nur die Assets nehmen, deren Name dem gesuchten Rare Pepe entspricht
                                if data["asset"] == names:
                                    Assets = Assets + 1
                                    quantity = float((data['quantity']))

                                    ts = time.gmtime(data['timestamp'])
                                    date = time.strftime("%Y-%m-%d %H:%M:%S", ts)  
                                    TX_Hash= data["tx_hash"]
                                    source = data["source"]

                                    df_burns.loc[df_burns.shape[0]] = [names, date, quantity]  
                                    total_quantity_burns = total_quantity_burns + quantity          

            # Wird so aktuell nicht mehr verwendet!
            name_supply = df_all_pepes["Name"] == names
            supply = df_all_pepes[name_supply]["Quantity"].iloc[0]

            if type(supply) == str:
                supply = supply.replace(",", "")
            
            supply = float(supply)
            supply_rem = supply - total_quantity_burns
            df_burns_total.loc[df_burns.shape[0]] = [names, series, supply, total_quantity_burns, supply_rem, ((supply_rem / supply)*100)]

        df_burns.to_csv('all_burns.csv')
        # Hier werden die Burns den Karten zugeordnet und die Anzahl der Karten nach Datum runtergezählt um dies in der Regression zu verwenden

        df_total["Supply"] = 0
        df_total = df_total.sort_values(by=["Date"], ascending = True)

        for names in official_rare_pepes:

            df_total_names = df_total.loc[df_total['Name'] == names]
            df_burns_names = df_burns.loc[df_burns['Name'] == names]
            df_burns_names = df_burns_names.sort_values(by=["Date"], ascending = True)

            name_supply = df_all_pepes["Name"] == names
            supply = df_all_pepes[name_supply]["Quantity"].iloc[0]

            if type(supply) == str:
                supply = supply.replace(",", "")

            amount = 0
            burns_row = 0
            burns_quantity = 0
            amount_burns = len(df_burns_names) -1
            length = len(df_burns_names)
            
            # Hier werden die Burns mit dem Daten verglichen und diese von der ursprünglichen Menge abgezogen
            for ind in df_total_names.index:
                if amount == 0 and burns_quantity == 0:
                    amount = float(supply)
                
                if burns_row < length:
                    if df_burns_names.iloc[burns_row]["Date"] < df_total_names["Date"][ind]:
                        burns_quantity = df_burns_names.iloc[burns_row]["Quantity"]
                        
                        amount = amount - burns_quantity

                        if burns_row <= amount_burns:
                            burns_row = burns_row + 1
                        

                df_total_names["Supply"][ind] = amount
                df_total["Supply"][ind] = amount

                # Burns werden in der großen Tabelle hinzugefügt
                df_total_names = df_total.loc[df_total['Name'] == names]

        # Hinzufügen der Supply in den Datensatz all_holders_gini übernommen.
        df_gini_ts["Supply"] = 0
        for names in official_rare_pepes:

            df_gini_ts_names = df_gini_ts.loc[df_gini_ts['Name'] == names]
            df_gini_ts_names = df_gini_ts_names.sort_values(by=["Date"], ascending = True)
            df_burns_names = df_burns.loc[df_burns['Name'] == names]
            df_burns_names = df_burns_names.sort_values(by=["Date"], ascending = True)

            name_supply = df_all_pepes["Name"] == names
            supply = df_all_pepes[name_supply]["Quantity"].iloc[0]

            if type(supply) == str:
                supply = supply.replace(",", "")

            amount = 0
            burns_row = 0
            burns_quantity = 0
            amount_burns = len(df_burns_names) -1
            length = len(df_burns_names)
            
            # Hier werden die Burns mit dem Daten verglichen und diese von der ursprünglichen Menge abgezogen
            for ind in df_gini_ts_names.index:
                if amount == 0 and burns_quantity == 0:
                    amount = float(supply)
                
                if burns_row < length:
                    if df_burns_names.iloc[burns_row]["Date"] < df_gini_ts_names["Date"][ind]:
                        burns_quantity = df_burns_names.iloc[burns_row]["Quantity"]
                        
                        amount = amount - burns_quantity

                        if burns_row <= amount_burns:
                            burns_row = burns_row + 1
                        

                df_gini_ts_names["Supply"][ind] = amount
                df_gini_ts["Supply"][ind] = amount

                # Burns werden in der großen Tabelle hinzugefügt
                df_gini_ts_names = df_gini_ts.loc[df_gini_ts['Name'] == names]


        df_gini_ts = df_gini_ts.sort_values(by=["Date"], ascending = True)
        df_gini_ts.to_csv('all_holders_gini.csv',index=False)

        
        if False:
            # Hier hinzufügen von Sweeps
            column_names = ["Name","Type","Date","Date_Index","Series","Supply","Price in USD","Quantity", "Source", "Destination", "TX_Hash"]
            df_sweep = pd.DataFrame(columns = column_names)

            for names in official_rare_pepes: 
                
                df_gini_ts_names = df_gini_ts.loc[df_gini_ts['Name'] == names]
                df_gini_ts_names = df_gini_ts_names.sort_values(by=["Date"], ascending = True)

                unique_source = df_gini_ts_names["Source"].unique()
                unique_destination = df_gini_ts_names["Destination"].unique()

                unique_adress = df_gini_ts_names["Source"].append(df_gini_ts_names["Destination"]).reset_index(drop=True)
                unique_adress = unique_adress.unique().tolist()

                unique_adress.remove('NON')

                for address in unique_adress:

                    page = 1
                    page_counter = 100
                    page = 1
                    pages = 0
                    # Page Counter, dieser läuft so lange bis auf einer Seite keine Assets mehr angezeigt werden
                    while page_counter > 0:

                        # API Call nach Dispenser und 100 Assets pro Seite
                        url = "https://xchain.io/api/debits/" + address + "/" + str(page) + "/100"
                        headers = {'content-type': 'application/json'}
                        auth = HTTPBasicAuth('rpc', '1234')

                        page = page + 1
                        pages = pages + 1                            
                                
                        # Speichern des Outputs als JSON Output um damit zu arbeiten
                        response_xchain = requests.post(url, headers=headers, auth=auth)
                        response_xchain_json = response_xchain.json()

                        page_counter = 0
                        
                        for data in response_xchain_json["data"]:
                            if data["action"] == "sweep":
                                if data["asset"] == "RAREQUEEM":
                                    
                                    names = data["asset"]
                                    quantity = float((data['quantity']))

                                    ts = time.gmtime(data['timestamp'])
                                    date = time.strftime("%Y-%m-%d %H:%M:%S", ts)  
                                    date_index = time.strftime("%Y-%m", ts)
                                    tx_hash = data["event"]

                                    if quantity > 0:
                                        df_sweep.loc[df_sweep.shape[0]] = [names,"sweep",date,date_index,0,0,0, quantity, 0, 0, tx_hash]
                        
                            page_counter = page_counter + 1
                    
                    if len(df_sweep) > 0:
                        sweep_list = df_sweep["TX_Hash"].tolist()

                        page = 1
                        page_counter = 100
                        page = 1
                        pages = 0

                        # Page Counter, dieser läuft so lange bis auf einer Seite keine Assets mehr angezeigt werden
                        while page_counter > 0:

                            # API Call nach Dispenser und 100 Assets pro Seite
                            url = "https://xchain.io/api/sweeps/" + address + "/" + str(page) + "/100"
                            headers = {'content-type': 'application/json'}
                            auth = HTTPBasicAuth('rpc', '1234')

                            page = page + 1
                            pages = pages + 1                            
                                    
                            # Speichern des Outputs als JSON Output um damit zu arbeiten
                            response_xchain = requests.post(url, headers=headers, auth=auth)
                            response_xchain_json = response_xchain.json()

                            page_counter = 0
                            
                            for data in response_xchain_json["data"]:
                                if data["tx_hash"] in sweep_list:
                                    df_sweep.loc[df_sweep.TX_Hash == data["tx_hash"], 'Source'] = data["source"]
                                    df_sweep.loc[df_sweep.TX_Hash == data["tx_hash"], 'Destination'] = data["destination"]

                                page_counter = page_counter + 1

                    column_names = list(df_sweep.columns.values)
                    if "TX_Hash" in column_names:
                        df_sweep.drop("TX_Hash", axis=1, inplace=True)
                    df_gini_ts = pd.concat([df_gini_ts, df_sweep], ignore_index=True, sort=False)
                    df_gini_ts = df_gini_ts.sort_values(by=["Date"], ascending = True)

        # Hier hinzufügen von Sweeps in die große Tabelle

        column_names = ["Name","Type","Date","Date_Index","Series","Supply","Price in USD","Quantity", "Gini", "Top_3", "Top_5", "Top_10"]
        df_gini_final = pd.DataFrame(columns = column_names)

        column_names = ["Name"]
        errors = pd.DataFrame(columns = column_names)
    
        for names in official_rare_pepes:
            non_test = 0
            supply_1 = 0
            holders = {}
            df_gini_ts_names = df_gini_ts.loc[df_gini_ts['Name'] == names]
            df_gini_ts_names = df_gini_ts_names.sort_values(by=["Date"], ascending = True)
            
            for ind in df_gini_ts_names.index:

                supply = df_gini_ts_names["Supply"][ind]
                date = df_gini_ts_names["Date"][ind]   
                source = df_gini_ts_names["Source"][ind]
                destination = df_gini_ts_names["Destination"][ind]
                quantity = df_gini_ts_names["Quantity"][ind]
                Type = df_gini_ts_names["Type"][ind]
                price_usd = df_gini_ts_names["Price in USD"][ind]
                date_index = df_gini_ts_names["Date_Index"][ind]
                series = df_gini_ts_names["Series"][ind]

                if source == "NON":
                    if destination in holders.keys():
                        holders[destination] += quantity

                    else:
                        holders[destination] = quantity
                    
                    if non_test ==0:
                        supply = quantity
                        non_test = non_test + 1
                        supply_1 = supply
                    else:
                        supply = supply_1 + quantity
                        supply_1 = supply
                
                # Hier noch Spezialfall Burns hinzufügen. Dann nämlich nur abziehen und nicht die Burn Adresse hinzufügen
                else:
                    send_burn = 0

                    if "Burn" in destination:
                        send_burn = 1

                    if "BURN" in destination:
                        send_burn = 1

                    if send_burn == 1:
                        holders[source] -= quantity
                    
                    if send_burn == 0:
                        if destination in holders.keys():
                            holders[destination] += quantity
                        else:
                            holders[destination] = quantity

                        if source in holders.keys():
                            holders[source]  -= quantity
                        else:
                            holders[source]  = quantity

                        if (source  , 0) in holders.items():
                            holders.pop(source)
                
                    send_burn = 0
                
                holders_list = pd.DataFrame(list(holders.items()),columns = ['Holder','Quantity'])
                holders_list= holders_list["Quantity"]
                holders_list_sorted = holders_list.sort_values(ascending = False)

                top_3 = holders_list_sorted.iloc[0:3].sum() / supply
                top_5 = holders_list_sorted.iloc[0:5].sum() / supply
                top_10 = holders_list_sorted.iloc[0:10].sum() / supply

                holders_list_sorted = holders_list.sort_values()
                
                def gini(list_of_values):
                    sorted_list = sorted(list_of_values)
                    height, area = 0, 0
                    for value in sorted_list:
                        height += value
                        area += height - value / 2.
                    fair_area = height * len(list_of_values) / 2.

                    try: 
                        return (fair_area - area) / fair_area
                    except ZeroDivisionError:
                        errors.loc[errors.shape[0]] = [names]
                        return nan
                             
                gini_holders = round(gini(holders_list_sorted),3)

                df_gini_final.loc[df_gini_final.shape[0]] = [names,Type,date,date_index,series, supply,price_usd,quantity, gini_holders, top_3, top_5, top_10]

        df_gini_final.to_csv('all_holders_gini_final.csv',index=False)
        df_total = pd.read_csv('all_holders_gini_final.csv')

        errors.to_csv('all_errors.csv',index=False)

        # Die Daten meiner neuen Tabelle mit time series gini, top holders und supply in große Tabelle einspielen
        # Exportieren der Daten um nur einmal am Tag/Monat die Daten durchzugehen
        name_dataframe = "all_transactions_max_" + str(card_supply) + ".csv"
        df_total.to_csv(name_dataframe,index=False)

        divisible_transactions = True
        filter_outliers = True

        # Hier wird gefiltert, ob Transaktionen durchgeführt wurden mit divisible Asssets, wenn ja werden diese gelöscht
        if divisible_transactions == True:
            df_total_non_divisible = df_total.loc[df_total['Quantity'] >= 1]
            df_total_non_divisible = df_total_non_divisible.loc[df_total_non_divisible['Price in USD'] > 0]

            # Speichern der Transaktionen als csv
            name_dataframe = "all_transactions_nd_max_" + str(card_supply) + ".csv"
            df_total_non_divisible.to_csv(name_dataframe)
        
        column_total = ["Name","Type","Date","Date_Index","Supply","Price in USD","Quantity", "Gini", "Top_3", "Top_5", "Top_10"]
        df_total_nd_no = pd.DataFrame(columns = column_total)

        # Hier wird der Datensatz von Outliern bereinigt
        if filter_outliers == True:
            for names in official_rare_pepes:

                # Droppen der Outliers Non Divisible
                name_transactions_1 = df_total_non_divisible.loc[df_total_non_divisible["Name"] == names]
                df_total_non_disible_non_outliers = name_transactions_1[name_transactions_1["Price in USD"] > name_transactions_1["Price in USD"].quantile(0.05)]
                df_total_non_disible_non_outliers = name_transactions_1[name_transactions_1["Price in USD"] < name_transactions_1["Price in USD"].quantile(0.95)]

                # Speichern der Transaktionen als csv non dvisible (nd) und non outliers (no)
                df_total_nd_no = df_total_nd_no.append(df_total_non_disible_non_outliers, ignore_index=True)
                name_dataframe = "all_transactions_nd_no_max_" + str(card_supply) + ".csv"
                df_total_nd_no.to_csv(name_dataframe,index=False)

        # Preisniveau der einzelnen Karten ausrechnen
        # Findet aktuell doppelt statt, da Max Supply Cards und Min Number Transactions jedes mal neu durchlaufen müssen

        df_total = df_total_nd_no

        column_names = [ "Price_Level", "Date_Index"]
        df_price_level = pd.DataFrame(columns = column_names)

        month = ["01", "02", "03", "04", "05","06","07","08","09","10","11","12"]
        year = ["2016", "2017", "2018", "2019", "2020", "2021", "2022"]

        today = datetime.now()
        current_month = today.strftime("%Y-%m")

        for names in official_rare_pepes:
            preisniveau = 0
            test = df_total.loc[df_total['Name'] == names]
            for y in year:

                for m in month:
                    date = y + "-" + m
                    if date == current_month:
                        break
                    else:
                        preisniveau_davor = preisniveau
                        test_names = test.loc[test['Date_Index'] == date]
                        anzahl = len(test_names)

                        if anzahl == 0 and preisniveau_davor == 0:
                            preisniveau = 0
                        if anzahl == 0 and preisniveau_davor !=0:
                            preisniveau = preisniveau_davor
                        if anzahl != 0:
                            preisniveau = test_names["Price in USD"].mean()

                        df_price_level.loc[df_price_level.shape[0]] = [preisniveau, date]
        
        name_dataframe = "df_price_level_nd_no_max_" + str(card_supply) + ".csv"
        df_price_level.to_csv(name_dataframe)
        df_price_level_series = df_price_level.groupby(["Date_Index"]).sum()

        # Volume sold wird ausgerechnet
        # Volume sold erstmal gelöscht.
        if False:
            dict_total = {}
            for ind in df_total.index:
                price = df_total["Price in USD"][ind]
                date = df_total["Date_Index"][ind]

                if date in dict_total.keys():
                    dict_total[date] += price
                else:
                    dict_total[date] = price

            data_items = dict_total.items()
            data_list = list(data_items)

            df_new_total = pd.DataFrame(data_list)
            df_new_total = df_new_total.rename(columns={0: 'Date', 1: 'Volume sold'})
            df_new_total = df_new_total.sort_values(by=["Date"], ascending = False)
            df_new_total = df_new_total.set_index('Date')

        # Last Load Day
        end_time = datetime.now()
        load_month = end_time.strftime("%Y-%m")

        f = open( "99_Load_Month.txt", 'w' )
        f.write(load_month)
        f.close()
       
    # ist das überhaupt noch nötig? Ist das nicht doppelt??   
    elif False:
        df_total = pd.read_csv ("all_transactions.csv")
        st.subheader("All Transactions")
        st.write("Quantity Transactions: " + str(len(df_total)))

        df_total = df_total.iloc[: , 1:]
        df_total = df_total.sort_values(by=["Date"], ascending = False)
        st.dataframe(df_total)
        
       # Preisniveau der einzelnen Karten ausrechnen
        column_names = [ "Price_Level", "Date_Index"]
        df_price_level = pd.DataFrame(columns = column_names)

        month = ["01", "02", "03", "04", "05","06","07","08","09","10","11","12"]
        year = ["2016", "2017", "2018", "2019", "2020", "2021", "2022"]

        today = datetime.now()
        current_month = today.strftime("%Y-%m")

        for names in official_rare_pepes:
            preisniveau = 0
            test = df_total.loc[df_total['Name'] == names]
            for y in year:

                for m in month:
                    date = y + "-" + m
                    if date == current_month:
                        break
                    else:
                        preisniveau_davor = preisniveau
                        test_names = test.loc[test['Date_Index'] == date]
                        anzahl = len(test_names)

                        if anzahl == 0 and preisniveau_davor == 0:
                            preisniveau = 0
                        if anzahl == 0 and preisniveau_davor !=0:
                            preisniveau = preisniveau_davor
                        if anzahl != 0:
                            preisniveau = test_names["Price in USD"].mean()

                        df_price_level.loc[df_price_level.shape[0]] = [preisniveau, date]

        df_price_level.to_csv('df_price_level.csv')

    else:
        # Einlesen Rare Pepes je nach Filter
        if card_supply != "All":
            
            if card_supply == 100:
                df_pepes = pd.read_csv("07_all_pepes_supply_max_100.csv")

            if card_supply == 500:
                df_pepes = pd.read_csv("08_all_pepes_supply_max_500.csv")

            if card_supply == 1000:
                df_pepes = pd.read_csv("09_all_pepes_supply_max_1000.csv")

            if card_supply == 10000:
                df_pepes = pd.read_csv("10_all_pepes_supply_max_10000.csv")

        if card_supply == "All":
            df_pepes = pd.read_csv ("04_official_rare_pepes.csv")

        df_pepes = df_pepes.iloc[: , 1:]
        pepes_list = df_pepes["Name"].tolist()
        official_rare_pepes = pepes_list
  
        name_dataframe = "all_transactions_nd_no_max_" + str(card_supply) + ".csv"
        df_total = pd.read_csv(name_dataframe)

        # Sortieren des Datensatzes
        df_total = df_total.iloc[: , 1:]
        df_total = df_total.sort_values(by=["Date"], ascending = False)

        # Filtern nach der Anzahl der Transaktionen einer Karte
        if number_transactions != "All":
            for names in official_rare_pepes:
                name_transaction = df_total.loc[df_total["Name"] == names]

                if len(name_transaction) < number_transactions:
                    df_total = df_total.loc[df_total["Name"] != names]
        
        # Schleife beschränken auf vorhandene Rare Pepes in dem verwendeten Datensatz
        column_values = df_total["Name"].values
        unique_values = np.unique(column_values)
        pepes_list = unique_values.tolist()
        official_rare_pepes = pepes_list

        # Filtern nach der Series
        if card_series != "All":
            for names in official_rare_pepes:
                name_transaction = df_total.loc[df_total["Name"] == names]

                if name_transaction["Series"].iloc[0] != card_series:
                    df_total = df_total.loc[df_total["Name"] != names]

        name_dataframe = "all_transactions_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".csv"
        df_total.to_csv(name_dataframe)

        # Schleife beschränken auf vorhandene Rare Pepes in dem verwendeten Datensatz
        column_values = df_total["Name"].values
        unique_values = np.unique(column_values)
        pepes_list = unique_values.tolist()
        official_rare_pepes = pepes_list

        d1, d2 = st.columns((2, 2))
        d1.write("Used Rare Pepes: " + str(len(unique_values)))
        st.markdown("<hr/>", unsafe_allow_html=True)
        #st.write(unique_values)

        name_dataframe = "df_price_level_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".csv"
        path_to_file = name_dataframe
        path = Path(path_to_file)

        if path.is_file() == True:
            df_price_level = pd.read_csv (name_dataframe)

        else:
            # Preisniveau der einzelnen Karten ausrechnen
            if number_transactions != "All" or card_series != "All" or observation_time !="All":
                column_names = [ "Price_Level", "Date_Index"]
                df_price_level = pd.DataFrame(columns = column_names)

                month = ["01", "02", "03", "04", "05","06","07","08","09","10","11","12"]
                year = ["2016", "2017", "2018", "2019", "2020", "2021", "2022"]

                today = datetime.now()
                current_month = today.strftime("%Y-%m")

                for names in official_rare_pepes:
                    preisniveau = 0
                    test = df_total.loc[df_total['Name'] == names]
                    for y in year:

                        for m in month:
                            date = y + "-" + m
                            if date == current_month:
                                break
                            else:
                                preisniveau_davor = preisniveau
                                test_names = test.loc[test['Date_Index'] == date]
                                anzahl = len(test_names)

                                if anzahl == 0 and preisniveau_davor == 0:
                                    preisniveau = 0
                                if anzahl == 0 and preisniveau_davor !=0:
                                    preisniveau = preisniveau_davor
                                if anzahl != 0:
                                    preisniveau = test_names["Price in USD"].mean()

                                df_price_level.loc[df_price_level.shape[0]] = [preisniveau, date]

                name_dataframe = "df_price_level_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".csv"
                df_price_level.to_csv(name_dataframe)
                df_price_level = df_price_level.sort_values(by=["Date_Index"], ascending = False)


        #df_price_level = df_price_level.iloc[: , 1:]
        df_price_level = df_price_level.sort_values(by=["Date_Index"], ascending = False)

        month = ["01", "02", "03", "04", "05","06","07","08","09","10","11","12"]
        year = ["2016", "2017", "2018", "2019", "2020", "2021", "2022"]

        if observation_time !="All":
            year = [str(observation_time)]

        today = datetime.now()
        current_month = today.strftime("%Y-%m")
    
    # UNGEWICHTETER INDEX
    # Ungewichteter Preisindex der nicht beachtet wie viele Werte enthalten sind oder wie groß die Marktkapitalisierung ist
    if unweighted==True:
    
        name_dataframe = "df_unweighted_price_level_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".csv"
        path_to_file = name_dataframe
        path = Path(path_to_file)

        un1, un2 = st.columns((2, 3)) 
        un1.subheader("Unweighted Price Index")
        e1, e2 = st.columns((2, 3))
        
        if path.is_file() == True:
            df = pd.read_csv(name_dataframe)
            e1.markdown("Data:")
            e1.dataframe(df)

            name_dataframe = "png_df_unweighted_price_level_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".png"
            price = Image.open(name_dataframe)
            e2.markdown("Graph:")
            e2.image(price)

        else:
            if observation_time !="All":
                test = df_price_level
                test["Year"] = df_price_level["Date_Index"].str.split("-").str[0]
                test = test.loc[test['Year'] == str(observation_time)]
                df_price_level = test
            
            df_unweighted_price_level = df_price_level.groupby(["Date_Index"]).sum()

            name_dataframe = "df_unweighted_price_level_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".csv"
            df_unweighted_price_level.to_csv(name_dataframe)
            
            df = pd.read_csv(name_dataframe)
            df_test = df[['Date_Index','Price_Level']]
            e1.markdown("Data:")
            e1.dataframe(df_test)
        
            e2.markdown("Graph:")
            df_test["time"] = pd.to_datetime(df_test["Date_Index"])
            df_test.plot(x ='time', y='Price_Level', kind = 'line')

            name_dataframe = "png_df_unweighted_price_level_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".png"
            plt.savefig(name_dataframe)
            plt.close()
            price = Image.open(name_dataframe)
            e2.image(price)
        st.markdown("<hr/>", unsafe_allow_html=True)     

    # GEWICHTETER INDEX NACH MARKTKAPITALISIERUNG
    # Hier gewichtete Marktkapitalisierung mit einbeziehen. Bedeutet dass man den Preis mit der Anzahl der Karten multipliziert.
    if marketcap_weighted == True:
        
        
        mcap1, mcap2 = st.columns((2, 3)) 
        mcap1.subheader("Market-Cap Weighted Price Index")
        f1, f2 = st.columns((2, 3))
        
        name_dataframe = "df_market_cap_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".csv"
        path_to_file = name_dataframe
        path = Path(path_to_file)

        if path.is_file() == True:
            df = pd.read_csv(name_dataframe)
            f1.markdown("Data:")
            f1.dataframe(df)

            name_dataframe = "png_market_cap_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".png"
            price = Image.open(name_dataframe)
            f2.markdown("Graph:")
            f2.image(price)
        else:

            # Preisniveau der einzelnen Karten ausrechnen mit Market Cap
            column_names = [ "Price_Level", "Date_Index"]
            df_price_level_market_cap = pd.DataFrame(columns = column_names)

            month = ["01", "02", "03", "04", "05","06","07","08","09","10","11","12"]
            year = ["2016", "2017", "2018", "2019", "2020", "2021", "2022"]

            today = datetime.now()
            current_month = today.strftime("%Y-%m")

            for names in official_rare_pepes:
                preisniveau_market_cap = 0
                test = df_total.loc[df_total['Name'] == names]
                for y in year:

                    for m in month:
                        date = y + "-" + m
                        if date == current_month:
                            break
                        else:
                            preisniveau_davor = preisniveau_market_cap
                            test_names = test.loc[test['Date_Index'] == date]
                            anzahl = len(test_names)

                            if anzahl == 0 and preisniveau_davor == 0:
                                preisniveau_market_cap = 0
                            if anzahl == 0 and preisniveau_davor !=0:
                                preisniveau_market_cap = preisniveau_davor
                            if anzahl != 0:
                                preisniveau = test_names["Price in USD"].mean()
                                supply = test_names["Supply"].mean()

                                # Hier wird die Marktkapitalisierung ausgerechnet
                                preisniveau_market_cap = preisniveau * supply

                            df_price_level_market_cap.loc[df_price_level_market_cap.shape[0]] = [preisniveau_market_cap, date]
            
            # Speichern des Preis Levels nach der Marktkapitalisierung als csv
            #name_dataframe = "df_market_cap_price_levels_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".csv"
            #df_price_level_market_cap.to_csv(name_dataframe)    

            if observation_time !="All":
                test = df_price_level_market_cap
                test["Year"] = df_price_level_market_cap["Date_Index"].str.split("-").str[0]
                test = test.loc[test['Year'] == str(observation_time)]
                df_price_level_market_cap = test
            
            df_market_cap = df_price_level_market_cap.groupby(["Date_Index"]).sum()
            name_dataframe = "df_market_cap_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".csv"
            df_market_cap.to_csv(name_dataframe)

            df = pd.read_csv(name_dataframe)
            df_test = df[['Date_Index','Price_Level']]
            f1.markdown("Data:")
            f1.dataframe(df_test)
        
            f2.markdown("Graph:")
            df_test["time"] = pd.to_datetime(df_test["Date_Index"])
            df_test.plot(x ='time', y='Price_Level', kind = 'line')

            name_dataframe = "png_market_cap_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".png"
            plt.savefig(name_dataframe)
            price = Image.open(name_dataframe)
            f2.image(price)
        st.markdown("<hr/>", unsafe_allow_html=True)

    if gini_coef == True:
        
        name_dataframe = "df_gini_list_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".csv"
        path_to_file = name_dataframe
        path = Path(path_to_file)

        gini1, gini2 = st.columns((2, 3)) 
        gini1.subheader("Gini Coefficient")
        g1, g2 = st.columns((2, 3))

        if path.is_file() == True:
            df_gini_list = pd.read_csv(name_dataframe)
            #df_gini_list.drop("Unnamed: 0", axis=1, inplace=True)

            g1.markdown("Individual Gini-Coefficient:")
            g1.dataframe(df_gini_list)
            total_gini = df_gini_list["gini"].mean()
            total_gini = round(total_gini, 3)      

            graph = "png_gini_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".png"
            gini_graph = Image.open(graph)
            g2.markdown("Graph:")
            g2.image(gini_graph)
            g1.write("The Gini-Coefficient is the most well-known measure of inequality. A Gini-Coefficient of zero means all holders have the same amount of cards. A Gini-Coefficient of one means one holder has all cards. The lower the Gini coefficient, the more equal the holders are. The current total Gini-Coefficient equals: " + str(total_gini)+ ".")
        
        else:
            column_names = ["Name", "address", "quantity", "percentage"]
            df_holders = pd.DataFrame(columns = column_names)

            column_names = ["Name", "x", "points"]
            df_gini = pd.DataFrame(columns = column_names)

            column_names = ["Name", "gini"]
            df_gini_list = pd.DataFrame(columns = column_names)

            for names in official_rare_pepes:
                page_counter = 100
                page = 1
                
                while page_counter > 0:

                    url = "https://xchain.io/api/holders/" + names + "/" + str(page) + "/100"
                    headers = {'content-type': 'application/json'}
                    auth = HTTPBasicAuth('rpc', '1234')

                    response= requests.post(url, headers=headers, auth=auth)
                    response = response.json()

                    page = page + 1
                    page_counter = 0

                    for data in response["data"]:
                        page_counter = page_counter + 1

                        if "BURN" in data["address"]:
                            continue

                        elif "Burn" in data["address"]:
                            continue

                        else:
                            address = data["address"]
                            quantity = float(data["quantity"])
                            percentage = data["percentage"]     

                            df_holders.loc[df_holders.shape[0]] = [names, address, quantity, percentage]

                # Hier nach names referenzieren um einzelnen Gini Coefficient zu ermitteln
                holders_name = df_holders.loc[df_holders['Name'] == names]
                df_holders_sorted = holders_name["quantity"]
                df_holders_sorted = df_holders_sorted.sort_values()
                quantity = len(df_holders_sorted)
                quartiles = round(quantity / 5)
                
                # Method: https://planspace.org/2013/06/21/how-to-calculate-gini-coefficient-from-raw-data-in-python/

                def gini(list_of_values):
                    sorted_list = sorted(list_of_values)
                    height, area = 0, 0
                    for value in sorted_list:
                        height += value
                        area += height - value / 2.
                    fair_area = height * len(list_of_values) / 2.
                    return (fair_area - area) / fair_area

                gini_card = round(gini(df_holders_sorted),3)

                df_gini_list.loc[df_gini_list.shape[0]] = [names, gini_card]

                # Gini Coefficient: https://de.wikipedia.org/wiki/Gini-Koeffizient
                # Method: https://www.youtube.com/watch?v=LLEfsZYt9oI 

                first_q = df_holders_sorted[:(quartiles)].sum() / df_holders_sorted.sum()
                
                second_q = df_holders_sorted[:(quartiles*2)].sum() / df_holders_sorted.sum()
                
                third_q = df_holders_sorted[:(quartiles*3)].sum() / df_holders_sorted.sum()

                fourth_q = df_holders_sorted[:(quartiles*4)].sum() / df_holders_sorted.sum()

                fifth_q = df_holders_sorted.sum() / df_holders_sorted.sum()

                points = [0,first_q,second_q,third_q,fourth_q,fifth_q]
                x = [0,0.2,0.4,0.6,0.8,1.0]
                df = pd.DataFrame()
                df["Name"] = str(names)
                df["x"] = x
                df["points"] = points

                df_gini = df_gini.append(df, ignore_index=True)

            df_gini_list_name = "df_gini_list_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".csv"
            df_gini_list.to_csv(df_gini_list_name)

            g1.markdown("Individual Gini-Coefficient:")
            g1.dataframe(df_gini_list)
            total_gini = df_gini_list["gini"].mean()
            total_gini = round(total_gini, 3)        

            df_gini_name = "df_gini_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".csv"
            df_gini.to_csv(df_gini_name)

            graph = "png_gini_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".png"
            
            df_gini_total = df_gini.groupby(["x"]).mean()
            plt.close()
            plt.plot(x,df_gini_total["points"],"--o" )
            plt.plot(x,x,"--o" )
            plt.title("Card Distribution of Holders:")
            plt.savefig(graph)

            gini_graph = Image.open(graph)
            g2.markdown("Graph:")
            g2.image(gini_graph)
            g1.write("The Gini-Coefficient is the most well-known measure of inequality. A Gini-Coefficient of zero means all holders have the same amount of cards. A Gini-Coefficient of one means one holder has all cards. The lower the Gini coefficient, the more equal the holders are. The current total Gini-Coefficient equals: " + str(total_gini)+ ".")
        
        st.markdown("<hr/>", unsafe_allow_html=True)

    if volume_sold == True:

        vo1, vo2 = st.columns((2, 3)) 
        vo1.subheader("Volume sold")
        h1, h2 = st.columns((2, 3))

        name_dataframe = "df_volume_sold_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".csv"
        path_to_file = name_dataframe
        path = Path(path_to_file)

        if path.is_file() == True:
            df = pd.read_csv(name_dataframe)
            df_test = df[['Date','Volume sold']]
            h1.markdown("Data:")
            h1.dataframe(df_test)

            name_dataframe = "png_volume_sold_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".png"
            price = Image.open(name_dataframe)
            h2.markdown("Graph:")
            h2.image(price)
        
        else:

            if observation_time !="All":
                test = df_total
                test["Year"] = df_total["Date_Index"].str.split("-").str[0]
                test = test.loc[test['Year'] == str(observation_time)]
                df_total = test
            
            dict_total = {}

            for ind in df_total.index:
                price = df_total["Price in USD"][ind]
                date = df_total["Date_Index"][ind]

                if date in dict_total.keys():
                    dict_total[date] += price
                else:
                    dict_total[date] = price

            data_items = dict_total.items()
            data_list = list(data_items)

            df_new_total = pd.DataFrame(data_list)
            df_new_total = df_new_total.rename(columns={0: 'Date', 1: 'Volume sold'})
            df_new_total = df_new_total.sort_values(by=["Date"], ascending = False)
            name_dataframe = "df_volume_sold_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".csv"
            df_new_total.to_csv(name_dataframe)

            df = pd.read_csv(name_dataframe)
            df_test = df[['Date','Volume sold']]
            h1.markdown("Data:")
            h1.dataframe(df_test)

            h2.markdown("Graph:")
            df_test["time"] = pd.to_datetime(df_test["Date"])
            df_test.plot(x ='time', y='Volume sold', kind = 'line')

            name_dataframe = "png_volume_sold_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".png"
            plt.savefig(name_dataframe)
            price = Image.open(name_dataframe)
            h2.image(price)
        st.markdown("<hr/>", unsafe_allow_html=True)
        
    if bitcoin_index == True:

        bi1, bi2 = st.columns((2, 3)) 
        bi1.subheader("Benchmark Rare Pepe - Bitcoin")
        i1, i2 = st.columns((2, 2))

        df = pd.read_csv("_bitcoin-usd.csv")
        df_test = df[['timestamp','close']]
        df_test["time"] = pd.to_datetime(df_test["timestamp"],unit='s')
        df_test.rename(columns={"close":"Price in USD"},inplace=True)

        df_test.plot(x ='time', y='Price in USD', kind = 'line')
        plt.savefig('_bitcoin_time_series.png')

        test = Image.open('_bitcoin_time_series.png')
        i2.markdown("Bitcoin Time Series:")
        i2.image(test)

        name_dataframe = "png_market_cap_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".png"
        price = Image.open(name_dataframe)
        i1.markdown("Rare Pepe Market Cap Time Series:")
        i1.image(price)
        st.markdown("<hr/>", unsafe_allow_html=True)

    if xcp_index == True:

        xcp1, xc2 = st.columns((2, 3)) 
        xcp1.subheader("Benchmark Rare Pepe - XCP")
        j1, j2 = st.columns((2, 2))

        df = pd.read_csv("_xcp-usd.csv")
        df_test = df[['timestamp','close']]
        df_test["time"] = pd.to_datetime(df_test["timestamp"],unit='s')
        df_test.rename(columns={"close":"Price in USD"},inplace=True)

        df_test.plot(x ='time', y='Price in USD', kind = 'line')
        plt.savefig('_xcp_time_series.png')

        price = Image.open('_xcp_time_series.png')
        j2.markdown("XCP Time Series:")
        j2.image(price)

        name_dataframe = "png_market_cap_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".png"
        price = Image.open(name_dataframe)
        j1.markdown("Rare Pepe Market Cap Time Series:")
        j1.image(price)
        st.markdown("<hr/>", unsafe_allow_html=True)

    if pepecash_index == True:

        pepe1, pepe2 = st.columns((2, 3)) 
        pepe1.subheader("Benchmark Rare Pepe - Pepe Cash")
        k1, k2 = st.columns((2, 2))

        df = pd.read_csv("_pepecash-usd.csv")
        df_test = df[['timestamp','close']]
        df_test["time"] = pd.to_datetime(df_test["timestamp"],unit='s')
        df_test.rename(columns={"close":"Price in USD"},inplace=True)

        df_test.plot(x ='time', y='Price in USD', kind = 'line')
        plt.savefig('_pepecash_time_series.png')

        price = Image.open('_pepecash_time_series.png')
        k2.markdown("Pepecash Time Series:")
        k2.image(price)

        name_dataframe = "png_market_cap_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".png"
        price = Image.open(name_dataframe)
        k1.markdown("Rare Pepe Market Cap Time Series:")
        k1.image(price)
        st.markdown("<hr/>", unsafe_allow_html=True)

    if nasdaq_index == True:

        nas1, nas2 = st.columns((2, 3)) 
        nas1.subheader("Benchmark Rare Pepe - NASDAQ")
        l1, l2 = st.columns((2, 2))

        df = pd.read_csv("_nasdaq.csv")
        df_test = df[['timestamp','close']]
        df_test["time"] = pd.to_datetime(df_test["timestamp"],unit='s')
        df_test.rename(columns={"close":"Price in USD"},inplace=True)

        df_test.plot(x ='time', y='Price in USD', kind = 'line')
        plt.savefig('_nasdaq_time_series.png')

        price = Image.open('_nasdaq_time_series.png')
        l2.markdown("NASDAQ Time Series:")
        l2.image(price)

        name_dataframe = "png_market_cap_nd_no_max_" + str(card_supply) + "_" + str(number_transactions) + "_" + str(card_series) + "_" + str(observation_time) + ".png"
        price = Image.open(name_dataframe)
        l1.markdown("Rare Pepe Market Cap Time Series:")
        l1.image(price)
        st.markdown("<hr/>", unsafe_allow_html=True)

    if regression == True:

        re1, re2 = st.columns((5, 1)) 
        re1.subheader("Regression Analysis")
        re1.markdown("This regression is done with the dataset of all transactions for cards with maximum supply of 1000 and min 5 transactions.")
        n1,n2 = st.columns((5,1))

        # 1a. Einlesen des Datensatzes
        dataset = pd.read_csv("all_transactions_nd_no_max_1000_5_All_All.csv", usecols = ["Name", "Series", "Date" ,"Price in USD", "Quantity", "Supply","top_10", "total_holders"])
        dataset. rename(columns = {'Price in USD':'Price'}, inplace = True)
        dataset["Date"] = pd.to_datetime(dataset["Date"])
        #dataset['Series'] = pd.Categorical(dataset.Series)

        # 1b. Index setzen mit Karten und Datum (Panel Data)
        dataset = dataset.set_index(['Name','Date'])
        df = dataset

        # 1d. General correlation of the features
        n1.markdown("<hr/>", unsafe_allow_html=True)
        n1.markdown("1. Correlation of the used features")
        n1.dataframe(df[["Price","Series", "Quantity", "Supply","top_10", "total_holders"]].corr())
        

        # 2a. Perform PanelOLS
        # https://towardsdatascience.com/a-guide-to-panel-data-regression-theoretics-and-implementation-with-python-4c84c5055cf8 
        from linearmodels import PanelOLS
        import statsmodels.api as sm

        exog_vars = ["Quantity" , "Supply" , "Series" , "total_holders"]
        exog = sm.add_constant(dataset[exog_vars])
        mod = PanelOLS(dataset.Price, exog)

        pooledOLS_res = mod.fit(cov_type='clustered', cluster_entity=True)
        n1.markdown("<hr/>", unsafe_allow_html=True)
        n1.markdown("2. Output Panel OLS Regression Model")
        n1.markdown(pooledOLS_res.params)
        

        # 2b. Store values for checking homoskedasticity graphically
        fittedvals_pooled_OLS = pooledOLS_res.predict().fitted_values
        residuals_pooled_OLS = pooledOLS_res.resids

        # 3A. Homoskedasticity
        import matplotlib.pyplot as plt

        # 3A.1 Residuals-Plot for growing Variance Detection
        fig, ax = plt.subplots()
        ax.scatter(fittedvals_pooled_OLS, residuals_pooled_OLS, color = "blue")
        ax.axhline(0, color = 'r', ls = '--')
        ax.set_xlabel("Predicted Values", fontsize = 15)
        ax.set_ylabel("Residuals", fontsize = 15)
        ax.set_title("Homoskedasticity Test", fontsize = 30)
        plt.savefig("__Homoskedasticity.png")
        Homoskedasticity = Image.open('__Homoskedasticity.png')

        n1.markdown("<hr/>", unsafe_allow_html=True)
        n1.markdown("3. Homoskedasticity Test")
        n1.image(Homoskedasticity)

        # 3A.2 White-Test
        from statsmodels.stats.diagnostic import het_white, het_breuschpagan
        pooled_OLS_dataset = pd.concat([dataset, residuals_pooled_OLS], axis=1)
        exog = sm.tools.tools.add_constant(dataset['Price']).fillna(0)
        white_test_results = het_white(pooled_OLS_dataset["residual"], exog)
        labels = ["LM-Stat", "LM p-val", "F-Stat", "F p-val"]
        
        n1.markdown("<hr/>", unsafe_allow_html=True)
        n1.markdown("4. White Test: " + str(dict(zip(labels, white_test_results))))

        # 3A.3 Breusch-Pagan-Test
        breusch_pagan_test_results = het_breuschpagan(pooled_OLS_dataset["residual"], exog)
        labels = ["LM-Stat", "LM p-val", "F-Stat", "F p-val"] 
        n1.markdown("5. Breusch-Pagan: " + str(dict(zip(labels, breusch_pagan_test_results))))

        # 3.B Non-Autocorrelation
        # Durbin-Watson-Test
        from statsmodels.stats.stattools import durbin_watson

        # 1c. Check for serial correlation with lags
        from statsmodels.tsa.stattools import acf, pacf
        from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
        # Draw Plot
        fig, axes = plt.subplots(1,2,figsize=(16,3), dpi= 100)
        plot_acf(df["Price"].tolist(), lags=5, ax=axes[0])
        plot_pacf(df["Price"].tolist(), lags=5, ax=axes[1])
        plt.savefig("__autocorrelation.png")
        autocor = Image.open('__autocorrelation.png')
        n1.markdown("<hr/>", unsafe_allow_html=True)
        n1.markdown("6. Autocorrelation Test")
        n1.image(autocor)

        durbin_watson_test_results = durbin_watson(pooled_OLS_dataset["residual"]) 
        n1. markdown("Output Autocorrelation Test: " + str(durbin_watson_test_results))

    if dataset_analysis == True:
        if observation_time !="All":
            test = df_total
            test["Year"] = df_total["Date_Index"].str.split("-").str[0]
            test = test.loc[test['Year'] == str(observation_time)]
            df_total_time = test
        else:
            df_total_time = df_total

        st.subheader("Dataset: ")
        st.write("Transaction: " + str(len(df_total_time)))
        st.dataframe(df_total_time)

        st.markdown("<hr/>", unsafe_allow_html=True)

    # Execution Time
    st.subheader("Metadata:")
    end_time = datetime.now()
    execution_time = end_time - begin_time
    st.caption("Runtime: " + str(execution_time))
    st.caption("Current Date: " + current_month)
    st.caption("Load Date: " + load_month)
