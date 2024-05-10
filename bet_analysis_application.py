import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import os

# Varsayılan değer
DEFAULT_MAC_SAYISI = 7

def takim_bilgilerini_cek(takim):
    clear_screen()
    # Web sitesinden verileri çek
    url = f"https://www.sporx.com/{takim}-fiksturu-ve-mac-sonuclari"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Maç sonuçlarını bul
    maclar = soup.find_all("tr")
    galibiyet_sayisi = 0
    toplam_gol = 0
    son_mac_skoru = None
    for mac in maclar:
        skor_element = mac.find("a", class_="d-block rounded bg-sporx text-white fw-bolder py-1 px-1 text-nowrap")
        if skor_element:
            skor = skor_element.get_text(strip=True)
            gol_sayisi = skor.split("-")
            if len(gol_sayisi) == 2 and gol_sayisi[0].strip() and gol_sayisi[1].strip():
                try:
                    attigi_gol = int(gol_sayisi[0])
                    gol_sayisi_g2 = int(gol_sayisi[1])
                except ValueError:
                    continue
                ev_sahibi = mac.find("td", class_="text-start w-25").find("a").get_text(strip=True)
                deplasman = mac.find("td", class_="text-end w-25").find("a").get_text(strip=True)
                if takim.lower() == turkce_karakter_degistir(ev_sahibi.lower()):
                    toplam_gol += attigi_gol
                    if attigi_gol > gol_sayisi_g2:
                        galibiyet_sayisi += 1
                    son_mac_skoru = f"{ev_sahibi} {skor} {deplasman}\n"
                elif takim.lower() == turkce_karakter_degistir(deplasman.lower()):
                    toplam_gol += gol_sayisi_g2
                    if attigi_gol < gol_sayisi_g2:
                        galibiyet_sayisi += 1
                    son_mac_skoru = f"Son Maç: {ev_sahibi} {skor} {deplasman}\n"
    if galibiyet_sayisi == 0:
        messagebox.showerror("Hata", f"{takim.capitalize()} takımı için bilgi bulunamadı.")
        return None, None, None
    else:
        return galibiyet_sayisi, toplam_gol, son_mac_skoru


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def turkce_karakter_degistir(takim_ad):
    takim_ad = takim_ad.replace("ı", "i")
    takim_ad = takim_ad.replace("ç", "c")
    takim_ad = takim_ad.replace("ş", "s")
    takim_ad = takim_ad.replace("ğ", "g")
    takim_ad = takim_ad.replace("ü", "u")
    takim_ad = takim_ad.replace("ö", "o")
    return takim_ad.replace(" ", "-")  # Boşlukları '-' ile değiştir


def tahmini_mac_sonucu(gol_tahmini):
    takim1_gol = int(gol_tahmini)
    takim2_gol = takim1_gol - 1 if takim1_gol > 0 else 0  # Takım2'nin gol sayısını belirle
    takim1 = turkce_karakter_degistir(takim1_entry.get())
    takim2 = turkce_karakter_degistir(takim2_entry.get())
    return f"Tahmini maç sonucu: {takim1.capitalize()} {takim1_gol} - {takim2_gol} {takim2.capitalize()} "


def iki_takimli_analiz():
    takim1 = turkce_karakter_degistir(takim1_entry.get())
    takim2 = turkce_karakter_degistir(takim2_entry.get())
    mac_sayisi = int(mac_sayisi_entry.get())

    if not takim1 or not takim2:
        messagebox.showerror("Hata", "Lütfen takımları girin.")
        return
    sonuc = ""
    takim1_bilgilerini_cek = takim_bilgilerini_cek(takim1)
    if takim1_bilgilerini_cek is None:
        return
    galibiyet_sayisi_g1, gol_sayisi_g1, son_mac_skoru_g1 = takim1_bilgilerini_cek
    takim2_bilgilerini_cek = takim_bilgilerini_cek(takim2)
    if takim2_bilgilerini_cek is None:
        return
    galibiyet_sayisi_g2, gol_sayisi_g2, son_mac_skoru_g2 = takim2_bilgilerini_cek

    sonuc += f"{takim1.capitalize()}\nGalibiyet Sayısı:{galibiyet_sayisi_g1}\nGol Sayısı:{gol_sayisi_g1}\n{son_mac_skoru_g1}\n\n"
    sonuc += f"{takim2.capitalize()}\nGalibiyet Sayısı:{galibiyet_sayisi_g2}\nGol Sayısı:{gol_sayisi_g2}\n{son_mac_skoru_g2}\n\n"

    if galibiyet_sayisi_g1 is not None and galibiyet_sayisi_g2 is not None:
        if galibiyet_sayisi_g1 > galibiyet_sayisi_g2:
            sonuc += f"{takim1.capitalize()} Takım {takim2.capitalize()} simülasyona göre yendi!\n"
        elif galibiyet_sayisi_g1 < galibiyet_sayisi_g2:
            sonuc += f"{takim2.capitalize()} Takım {takim1.capitalize()} simülasyona göre yendi!\n"
        else:
            sonuc += f"İki takım arasındaki maç simülasyona göre berabere bitti\n"

    # Gol sayısı tahmini
    if galibiyet_sayisi_g1 is not None and galibiyet_sayisi_g2 is not None:
        takim1_son_mac_gol = son_mac_bilgilerini_cek(takim1, mac_sayisi)
        takim2_son_mac_gol = son_mac_bilgilerini_cek(takim2, mac_sayisi)

        if len(takim1_son_mac_gol) < mac_sayisi or len(takim2_son_mac_gol) < mac_sayisi:
            messagebox.showerror("Hata", "Gol tahmini yapmak için yeterli veri bulunamadı.")
            return

        ortalama_gol_takim1 = sum(takim1_son_mac_gol) / len(takim1_son_mac_gol)
        ortalama_gol_takim2 = sum(takim2_son_mac_gol) / len(takim2_son_mac_gol)

        # Tahmin edilen gol sayısını hesapla
        ortalama_gol = (ortalama_gol_takim1 + ortalama_gol_takim2) / 2
        gol_tahmini = ortalama_gol + 0.25 if takim1_son_mac_gol[-1] > takim2_son_mac_gol[-1] else ortalama_gol

        sonuc += f"Maçta Muhtemelen {gol_tahmini:.2f} gol olacak.\n"

        # Maç sonucunu tahmin et
        tahmini_sonuc = tahmini_mac_sonucu(gol_tahmini)
        sonuc += tahmini_sonuc

    sonuc_label.config(text=sonuc)
def son_mac_bilgilerini_cek(takim, mac_sayisi):
    url = f"https://www.sporx.com/{takim}-fiksturu-ve-mac-sonuclari"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    maclar = soup.find_all("tr")
    son_mac_gol_sayilari = []
    mac_sayaci = 0

    for mac in maclar:
        skor_element = mac.find("a", class_="d-block rounded bg-sporx text-white fw-bolder py-1 px-1 text-nowrap")
        if skor_element:
            skor = skor_element.get_text(strip=True)
            gol_sayisi = skor.split("-")
            if len(gol_sayisi) == 2 and gol_sayisi[0].strip() and gol_sayisi[1].strip():
                try:
                    gol_sayisi_g1 = int(gol_sayisi[0])
                    gol_sayisi_g2 = int(gol_sayisi[1])
                    son_mac_gol_sayilari.append(gol_sayisi_g1)
                    son_mac_gol_sayilari.append(gol_sayisi_g2)
                    mac_sayaci += 1
                except ValueError:
                    continue
                if mac_sayaci >= mac_sayisi:
                    break
    return son_mac_gol_sayilari
# Arayüz
root = tk.Tk()
root.title("Futbol Analiz Programı")

frame = ttk.Frame(root)
frame.grid(row=0, column=0, padx=10, pady=10)

takim1_label = ttk.Label(frame, text="Ev Sahibi Takım:")
takim1_label.grid(row=0, column=0, sticky="w")

takim1_entry = ttk.Entry(frame)
takim1_entry.grid(row=0, column=1, padx=5, pady=5)

takim2_label = ttk.Label(frame, text="Deplasman Takım:")
takim2_label.grid(row=1, column=0, sticky="w")

takim2_entry = ttk.Entry(frame)
takim2_entry.grid(row=1, column=1, padx=5, pady=5)

mac_sayisi_label = ttk.Label(frame, text="Gol analizi için kullanılacak son maç sayısı:")
mac_sayisi_label.grid(row=2, column=0, sticky="w")

mac_sayisi_entry = ttk.Entry(frame)
mac_sayisi_entry.insert(0, DEFAULT_MAC_SAYISI)  # Varsayılan değeri göster
mac_sayisi_entry.grid(row=2, column=1, padx=5, pady=5)

analiz_button = ttk.Button(frame, text="Analiz Yap", command=iki_takimli_analiz)
analiz_button.grid(row=3, column=0, columnspan=2, pady=10)

sonuc_label = ttk.Label(frame, text="")
sonuc_label.grid(row=4, column=0, columnspan=2)

root.mainloop()

