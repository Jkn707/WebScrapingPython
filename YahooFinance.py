import requests
from bs4 import BeautifulSoup

url = "https://finance.yahoo.com/crypto/"

class Crypto:
    def __init__(self, symbol, name, price, change, percent_change, market_cap):
        self.symbol = symbol
        self.name = name
        self.price = price
        self.change = change
        self.percent_change = percent_change
        self.market_cap = market_cap

class Scraper:
    def __init__(self, url):
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")
        self.all_cryptos = soup.find_all("tr", {"class": "simpTblRow"})


class Compiler:
    def __init__(self, crypto_bunch):
        self.crypto_bunch = crypto_bunch

    def compile(self):
        cryptos = []
        for crypto in self.crypto_bunch:
            symbol = crypto.find("a", {"class": "Fw(600) C($linkColor)"}).text
            name = crypto.find("td", {"aria-label": "Name"}).text
            price = crypto.find("td", {"aria-label": "Price (Intraday)"}).text
            change = crypto.find("td", {"aria-label": "Change"}).text
            percent_change = crypto.find("td", {"aria-label": "% Change"}).text
            market_cap = crypto.find("td", {"aria-label": "Market Cap"}).text

            cryptos.append(Crypto(symbol, name, price, change, percent_change, market_cap))
            
        return cryptos

class Printer:
    def __init__(self, cryptos):
        self.cryptos = cryptos

    def print_cryptos(self):
        #create 2d list of cryptos
        cryptos_list = []
        cryptos_list.append(["Symbol", "Name", "Price(USD)", "Change(USD)", "% Change", "Market Cap(USD)"])
        cryptos_list.append(["------", "----", "-----------", "----------", "--------", "---------------"])
        for crypto in self.cryptos:
            cryptos_list.append([crypto.symbol, crypto.name, crypto.price, crypto.change, crypto.percent_change, crypto.market_cap])
        #print organized list
        for crypto in cryptos_list:
            print("{:<10} {:<30} {:<20} {:<20} {:<20} {:<20}".format(*crypto))

class Formatter:
    def __init__(self, cryptos):
        self.cryptos = cryptos

    def priceFormatter(self):
        for crypto in self.cryptos:
            crypto.price = float(crypto.price.replace(",", ""))
        return self.cryptos
    
    def percentFormatter(self):
        for crypto in self.cryptos:
            crypto.percent_change = float(crypto.percent_change.replace("%", ""))
        return self.cryptos


class Sorter:
    def __init__(self, cryptos):
        self.cryptos = cryptos
    
    def ordenar_por_precio(self, choice = None):
        cryptos_copy = self.cryptos.copy()
        cryptos_copy = Formatter(cryptos_copy).priceFormatter()
        def swapPrices():
            if  choice == None:
                newChoice = input("¿Desea ordenar de mayor a menor? (y/n): ")
            else:
                newChoice = choice

            if newChoice.lower() == "y":
                for i in range(len(cryptos_copy)-1):
                    for j in range(len(cryptos_copy)-1):
                        if cryptos_copy[j].price < cryptos_copy[j+1].price:
                            cryptos_copy[j], cryptos_copy[j+1] = cryptos_copy[j+1], cryptos_copy[j]
            else:
                for i in range(len(cryptos_copy)-1):
                    for j in range(len(cryptos_copy)-1):
                        if cryptos_copy[j].price > cryptos_copy[j+1].price:
                            cryptos_copy[j], cryptos_copy[j+1] = cryptos_copy[j+1], cryptos_copy[j]
            return cryptos_copy
        cryptos_copy = swapPrices()
        Printer(cryptos_copy).print_cryptos()
    
    def ordenar_por_porcentaje(self):
        cryptos_copy = self.cryptos.copy()
        cryptos_copy = Formatter(cryptos_copy).percentFormatter()
        def swapPercentages():
            for i in range(len(cryptos_copy)-1):
                for j in range(len(cryptos_copy)-1):
                    if cryptos_copy[j].percent_change < cryptos_copy[j+1].percent_change:
                        cryptos_copy[j], cryptos_copy[j+1] = cryptos_copy[j+1], cryptos_copy[j]
            return cryptos_copy
        cryptos_copy = swapPercentages()
        Printer(cryptos_copy).print_cryptos()

class Finder:
    def __init__(self, cryptos):
        self.cryptos = cryptos
    
    def look_for_crypto(self):
        name = input("Ingrese el nombre o el símbolo de la criptomoneda: ")
        for crypto in self.cryptos:
            if name.lower() in crypto.name.lower() or name.lower() in crypto.symbol.lower():
                Printer([crypto]).print_cryptos()
                return
        print("No se encontró la criptomoneda")
        choice = input("¿Desea buscar otra criptomoneda? (y/n): ")
        if choice.lower() == "y":
            self.look_for_crypto()
        else:
            return
    
    def top_N_positives(self):
        N = int(input("Ingrese la cantidad de criptomonedas que desea ver: "))

        def show_positivechange():
            positives = list(filter(lambda x: float(x.change) > 0, self.cryptos))
            return positives[:N]

        def most_expensive(positiveCryptos):
            Sorter(positiveCryptos).ordenar_por_precio("y")

        most_expensive(show_positivechange())

class Menu:
    def show_menu():
        print("1. Ver todas las criptomonedas")
        print("2. Ordenar por precio")
        print("3. Ordenar por porcentaje de cambio")
        print("4. Buscar criptomoneda")
        print("5. Ver las N criptomonedas más caras con cambio positivo")
        print("6. Salir")
        choice = input("Ingrese una opción: ")
        return choice
    
class System:
    def __init__(self):
        self.cryptos = []
        self.scraper = Scraper(url)
    
    def run(self):
        self.cryptos = Compiler(self.scraper.all_cryptos).compile()
        cryptos_copy = self.cryptos.copy()
        while True:
            choice = Menu.show_menu()
            match choice:
                case "1":
                    Printer(cryptos_copy).print_cryptos()
                    cryptos_copy = Compiler(self.scraper.all_cryptos).compile()
                case "2":
                    Sorter(cryptos_copy).ordenar_por_precio()
                    cryptos_copy = Compiler(self.scraper.all_cryptos).compile()
                case "3":
                    Sorter(cryptos_copy).ordenar_por_porcentaje()
                    cryptos_copy = Compiler(self.scraper.all_cryptos).compile()
                case "4":
                    Finder(cryptos_copy).look_for_crypto()
                    cryptos_copy = Compiler(self.scraper.all_cryptos).compile()
                case "5":
                    Finder(cryptos_copy).top_N_positives()
                    cryptos_copy = Compiler(self.scraper.all_cryptos).compile()
                case "6":
                    exit()
                case _:
                    print("Opción inválida")
                    continue

if __name__ == "__main__":
    System().run()


    





  