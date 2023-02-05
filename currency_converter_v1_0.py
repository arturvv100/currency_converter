#Currency converter scrap currency conversion rates to PLN from NBP website
#You can use this rates to convert PLN to other currency using current rates 

#scraping NBP conversion rates
import requests, bs4
link = 'https://www.nbp.pl/home.aspx?f=/kursy/kursya.html'
res = requests.get(link)
res.text
soup = bs4.BeautifulSoup(res.text,'lxml')
link_nbp = soup.select('.center a')[0]['href']
res = requests.get(link_nbp)
res.text
soup = bs4.BeautifulSoup(res.text, 'xml')
data_nbp = soup.data_publikacji.contents[0]
waluty = soup.find_all('pozycja')
kursy_nbp = {}
for i in waluty:
    kursy_nbp[i.kod_waluty.contents[0]] = round(float(i.kurs_sredni.contents[0].replace(',','.'))*int(i.przelicznik.contents[0]),4)
kursy_nbp['EUR']
wybor_walut = list(kursy_nbp.keys())


#GUI
from tkinter import *

def check():
    inpt = entry.get()
    if inpt.isdigit() and float(inpt) > 0:
        return float(inpt)
    else:
        return 0
    
def convert():
    x = round(check()*kursy_nbp[currency_menu.var.get()],2)
    label2.config(text=x)
    
    
class Menu:
    def __init__(self, master):
        self.master = master
        self.frame = Frame(self.master)
    
        self.values = wybor_walut
        self.var = StringVar(value = self.values[0])
        self.optionMenu = OptionMenu(self.frame, self.var, *self.values)
        self.optionMenu.pack()
        self.frame.pack(expand = True, fill = BOTH,pady=5)

root = Tk()
root.title('Currency converter v1.0')
root.geometry("250x120")

label = Label(root, text=f'Kurs NBP z dnia {data_nbp}', font=20, fg='blue')
label.pack(fill='x')

frame = Frame(root)
frame.pack()

leftframe = Frame(frame)
leftframe.pack(side=LEFT)

rightframe = Frame(frame)
rightframe.pack(side=RIGHT)

bottomframe = Frame(root)
bottomframe.pack(side=BOTTOM)


label = Label(leftframe, text='PLN')
label.pack(expand=True,pady=6)

entry = Entry(leftframe, width = 10, justify=CENTER)
entry.pack(expand=True)

currency_menu = Menu(rightframe)

label2 = Label(rightframe, text='',width = 10, justify=CENTER, bg='white')
label2.pack(expand=True)

convert_button = Button(bottomframe, text='Przelicz')
convert_button.pack(fill='x',pady=5)

convert_button.config(command=convert)

root.mainloop()