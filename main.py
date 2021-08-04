from tkinter import *
from tkinter import messagebox, Menu
import requests
import json
import sqlite3

pycrypto = Tk()
pycrypto.title("My Crypto Portfolio")
pycrypto.iconbitmap("favicon.ico")

con = sqlite3.connect('coin.db')
cursorObj = con.cursor()
cursorObj.execute("CREATE TABLE IF NOT EXISTS coin(id INTEGER PRIMARY KEY, Symbol TEXT, amount INTEGER, price REAL)")
con.commit()

cursorObj.execute("REPLACE INTO coin VALUES(1, 'BTC', 2, 38000)")
con.commit()
cursorObj.execute("REPLACE INTO coin VALUES(2, 'ETH', 4, 2040)")
con.commit()
cursorObj.execute("REPLACE INTO coin VALUES(3, 'USDT', 5, 10)")
con.commit()
cursorObj.execute("REPLACE INTO coin VALUES(4, 'ADA', 10, 30)")
con.commit()

def reset():
    for cell in pycrypto.winfo_children():
        cell.destroy()
    app_nav()
    app_header()
    my_portfolio()

def app_nav():
    def clear_all():
        cursorObj.execute("DELETE FROM coin")
        con.commit()

        messagebox.showinfo("Portfolio Notifications", "Portfolio Cleared - Add New Coins!")
        reset()
    
    def close_app():
        pycrypto.destroy()

    menu = Menu(pycrypto)
    file_item = Menu(menu)
    file_item.add_command(label='Clear Portfolio', command=clear_all)
    file_item.add_command(label='Close App', command=close_app)
    menu.add_cascade(label='File', menu=file_item)
    pycrypto.config(menu=menu)

def my_portfolio():
    api_request = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=300&convert=USD&CMC_PRO_API_KEY=835aac78-75c8-44f2-8a2e-cc25c19a1830")
    api = json.loads(api_request.content)

    cursorObj.execute("SELECT * FROM coin")
    coins = cursorObj.fetchall()

    def font_color(amount):
        if amount > 0:
            return "green"
        else:
            return "red"

    def insert_coin():
        cursorObj.execute("INSERT INTO coin(symbol, price, amount) VALUES(?, ?, ?)", (symbol_txt.get(), price_txt.get(), amount_txt.get()))
        con.commit()
        reset()
        messagebox.showinfo("Portfolio Notifications", "Coin Added Successfully!")
    
    def update_coin():
        cursorObj.execute("UPDATE coin SET symbol=?, price=?, amount=? WHERE id=?", (symbol_update.get(), price_update.get(), amount_update.get(), portid_update.get()))
        con.commit()
        reset()
        messagebox.showinfo("Portfolio Notifications", "Coin Updated Successfully!")

    def delete_coin():
        cursorObj.execute("DELETE FROM coin WHERE id=?", (portid_delete.get(),))
        con.commit()
        reset()
        messagebox.showinfo("Portfolio Notifications", "Coin Deleted!")

    total_pl = 0
    coin_row = 1
    total_current_value = 0
    total_amount_paid = 0

    for i in range(0,300):
        for coin in coins:
            if api['data'][i]['symbol'] == coin[1]:
                total_paid = coin[2] * coin[3]
                current_value = coin[2] * api['data'][i]['quote']['USD']['price']
                pl_percoin = api['data'][i]['quote']['USD']['price'] - coin[3]
                total_pl_coin = pl_percoin * coin[2]

                total_pl += total_pl_coin
                total_current_value += current_value
                total_amount_paid += total_paid

                port_id = Label(pycrypto, text= coin[0], bg='#F3F4F6', fg='black', font="Lato 12 bold", padx="5", pady="6", borderwidth=2, relief="groove")
                port_id.grid(row=coin_row, column=0, sticky=N+S+W+E)
                
                name = Label(pycrypto, text= api["data"][i]["symbol"], bg='#F3F4F6', fg='black', font="Lato 12 bold", padx="5", pady="6", borderwidth=2, relief="groove")
                name.grid(row=coin_row, column=1, sticky=N+S+W+E)

                price_coin = Label(pycrypto, text="${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]), bg='#F3F4F6', fg='black', font="Lato 12 bold", padx="5", pady="6", borderwidth=2, relief="groove")
                price_coin.grid(row=coin_row, column=2, sticky=N+S+W+E)

                no_coin = Label(pycrypto, text= coin[2], bg='#F3F4F6', fg='black', font="Lato 12 bold", padx="5", pady="6", borderwidth=2, relief="groove")
                no_coin.grid(row=coin_row, column=3, sticky=N+S+W+E)

                amount_paid = Label(pycrypto, text= "${0:.2f}".format(total_paid), bg='#F3F4F6', fg='black', font="Lato 12 bold", padx="5", pady="6", borderwidth=2, relief="groove")
                amount_paid.grid(row=coin_row, column=4, sticky=N+S+W+E)

                current_val = Label(pycrypto, text= "${0:.2f}".format(current_value), bg='#F3F4F6', fg='black', font="Lato 12 bold", padx="5", pady="6", borderwidth=2, relief="groove")
                current_val.grid(row=coin_row, column=5, sticky=N+S+W+E)

                pl_per_coin = Label(pycrypto, text= "${0:.2f}".format(pl_percoin), bg='#F3F4F6', fg=font_color(float("{0:.2f}".format(pl_percoin))), font="Lato 12 bold", padx="5", pady="6", borderwidth= 2, relief="groove")
                pl_per_coin.grid(row=coin_row, column=6, sticky=N+S+W+E)

                tot_pl = Label(pycrypto, text= "${0:.2f}".format(total_pl_coin), bg='#F3F4F6', fg=font_color(float("{0:.2f}".format(total_pl_coin))), font="Lato  12 bold", padx="5", pady="6", borderwidth=2, relief="groove")
                tot_pl.grid(row=coin_row, column=7, sticky=N+S+W+E)

                coin_row += 1

    #Insert Data
    symbol_txt = Entry(pycrypto, borderwidth=3, relief="groove")   
    symbol_txt.grid(row = coin_row + 1, column = 1)

    price_txt = Entry(pycrypto, borderwidth=3, relief="groove")   
    price_txt.grid(row = coin_row + 1, column = 2)

    amount_txt = Entry(pycrypto, borderwidth=3, relief="groove")   
    amount_txt.grid(row = coin_row + 1, column = 3)  

    add_coin = Button(pycrypto, text= "Add Coin", bg='#0E2049',command= insert_coin, fg= "white", font="Lato  12 bold", padx="5", pady="6", borderwidth=2, relief="groove")
    add_coin.grid(row=coin_row +1, column=4, sticky=N+S+W+E)

    #Update Data
    portid_update = Entry(pycrypto, borderwidth=3, relief="groove")   
    portid_update.grid(row = coin_row + 2, column = 0)

    symbol_update = Entry(pycrypto, borderwidth=3, relief="groove")   
    symbol_update.grid(row = coin_row + 2, column = 1)

    price_update = Entry(pycrypto, borderwidth=3, relief="groove")   
    price_update.grid(row = coin_row + 2, column = 2)

    amount_update = Entry(pycrypto, borderwidth=3, relief="groove")   
    amount_update.grid(row = coin_row + 2, column = 3)  

    update_coin_text = Button(pycrypto, text= "Update Coin", bg='#0E2049',command= update_coin, fg= "white", font="Lato  12 bold", padx="5", pady="6", borderwidth=2, relief="groove")
    update_coin_text.grid(row=coin_row +2, column=4, sticky=N+S+W+E)

    #Delete coin
    portid_delete = Entry(pycrypto, borderwidth=3, relief="groove")   
    portid_delete.grid(row = coin_row + 3, column = 0)

    delete_coin_text = Button(pycrypto, text= "Delete Coin", bg='#0E2049',command= delete_coin, fg= "white", font="Lato  12 bold", padx="5", pady="6", borderwidth=2, relief="groove")
    delete_coin_text.grid(row=coin_row +3, column=4, sticky=N+S+W+E)



                     

    total_ap = Label(pycrypto, text="${0:.2f}".format(total_amount_paid), bg='#F3F4F6', fg='black', font="Lato  12 bold", padx="5", pady="6", borderwidth=2, relief="groove")
    total_ap.grid(row=coin_row, column=4, sticky=N+S+W+E)

    total_cv = Label(pycrypto, text="${0:.2f}".format(total_current_value), bg='#F3F4F6', fg='black', font="Lato  12 bold", padx="5", pady="6", borderwidth=2, relief="groove")
    total_cv.grid(row=coin_row, column=5, sticky=N+S+W+E)

    total_pl = Label(pycrypto, text= "${0:.2f}".format(total_pl), bg='#F3F4F6', fg=font_color(float("{0:.2f}".format(total_pl))), font="Lato  12 bold", padx="5", pady="6", borderwidth=2, relief="groove")
    total_pl.grid(row=coin_row, column=7, sticky=N+S+W+E)

    api = ""
    refresh = Button(pycrypto, text= "Refresh", bg='#0E2049',command=reset, fg= "white", font="Lato  12 bold", padx="5", pady="6", borderwidth=2, relief="groove")
    refresh.grid(row=coin_row +1, column=7, sticky=N+S+W+E)


def app_header():

    port_id = Label(pycrypto, text='Portfolio ID', bg='#0E2049', fg='white', font="Lato 12 bold", padx="5", pady="6", borderwidth=2, relief="groove")
    port_id.grid(row=0, column=0, sticky=N+S+W+E)

    name = Label(pycrypto, text='Coin Name', bg='#0E2049', fg='white', font="Lato 12 bold", padx="5", pady="6", borderwidth=2, relief="groove")
    name.grid(row=0, column=1, sticky=N+S+W+E)

    price_coin = Label(pycrypto, text='Price', bg='#0E2049', fg='white', font="Lato 12 bold", padx="5", pady="6", borderwidth=2, relief="groove")
    price_coin.grid(row=0, column=2, sticky=N+S+W+E)

    no_coin = Label(pycrypto, text='Coin Owned', bg='#0E2049', fg='white', font="Lato 12 bold", padx="5", pady="6", borderwidth=2, relief="groove")
    no_coin.grid(row=0, column=3, sticky=N+S+W+E)

    amount_paid = Label(pycrypto, text='Total Amount paid', bg='#0E2049', fg='white', font="Lato 12 bold", padx="5", pady="6", borderwidth=2, relief="groove")
    amount_paid.grid(row=0, column=4, sticky=N+S+W+E)

    current_val = Label(pycrypto, text='Current Value', bg='#0E2049', fg='white', font="Lato 12 bold", padx="5", pady="6", borderwidth=2, relief="groove")
    current_val.grid(row=0, column=5, sticky=N+S+W+E)

    pl_per_coin = Label(pycrypto, text='P/L Per Coin', bg='#0E2049', fg='white', font="Lato 12 bold", padx="5", pady="6", borderwidth=2, relief="groove")
    pl_per_coin.grid(row=0, column=6, sticky=N+S+W+E)

    tot_pl = Label(pycrypto, text='Total P/L with Coin', bg='#0E2049', fg='white', font="Lato 12 bold", padx="5", pady="6", borderwidth=2, relief="groove")
    tot_pl.grid(row=0, column=7, sticky=N+S+W+E)

app_nav()
app_header()
my_portfolio()

pycrypto.mainloop()

cursorObj.close()
con.close()
print("Program Completed!")



      