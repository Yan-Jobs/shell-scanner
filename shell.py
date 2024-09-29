import requests, argparse, sys, time
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Back, Style, init
import os

init(autoreset=True)

ap = argparse.ArgumentParser(description="Web Shell Tarayıcı")
ap.add_argument("-url", required=True, help="Tarama yapılacak URL")
ap.add_argument("-list", required=True, help="Şifre listesi dosyası")
ap.add_argument("-time", required=True, help="Eş zamanlı iş parçacığı sayısı")
args = vars(ap.parse_args())

def zaman():
    t = time.localtime()
    simdi = time.strftime("%H:%M:%S", t)
    return simdi

def arac(u, sifre):
    host = "http://"+u+"/"+liste_sifre

    req = requests.get(host).status_code
    if req == 200:
        print(Fore.GREEN + "[BAŞARILI] " + Fore.WHITE + "{:<55} Durum: ".format(host) + Fore.GREEN + "{:<20}".format(req))
    else:
        print(Fore.RED + "[BAŞARISIZ] " + Fore.WHITE + "{:<55} Durum: ".format(host) + Fore.RED + "{:<20}".format(req))

def bf(u):
   try:
       sifre = args["list"]
       with ThreadPoolExecutor(max_workers=int(args["time"])) as executor:
           with open(sifre, "r") as sifre_liste:
               for liste_sifre in sifre_liste:
                   liste_sifre = liste_sifre.replace("\n", "")
                   executor.submit(arac, u, liste_sifre)

   except requests.exceptions.ConnectionError as e:
       print(Fore.RED + "[HATA] " + Fore.WHITE + " Bağlantı hatası.")
   except Exception as e:
       print(Fore.RED + "[HATA] " + Fore.WHITE + " Bir sorun oluştu: {}".format(e))

def ana():
    try:
        if len(sys.argv) < 2:
            print(ap.usage())
        else:
            os.system("clear")
            os.system("cls")
            print(Fore.CYAN + "[+] " + Fore.YELLOW + " Tarama Başlatılıyor {}".format(zaman()))
            time.sleep(1)
            print(Fore.CYAN + "[+] " + Fore.YELLOW + " Lütfen biraz bekleyin...\n")
            u = args["url"]
            bf(u)
            print("\n" + Fore.CYAN + "[+] " + Fore.GREEN + " Tarama Tamamlandı. {}".format(zaman()))
            time.sleep(5)
            os.system("clear")
            os.system("cls")
            print("")
            print(Fore.CYAN + "[#] " + Fore.BLUE + " İyi Günler!")
            print(Style.RESET_ALL)
    except KeyboardInterrupt as e:
        print(Fore.RED + "[!] " + Fore.WHITE + " Programdan Çıkıldı")

if __name__ == '__main__':
   ana()
