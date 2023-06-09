import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from bs4 import BeautifulSoup
import requests
import pandas as pd
import tkinter as tk
from tkinter.ttk import Button, Label, Progressbar
from threading import Thread
import time
kitap_isimler = []
indirimli_fiyatlar = []
normal_fiyatlar = []

print("Made by Melis İldireci...")
def veri_cek_ve_yaz():
    progress_bar.start()
    for i in range(1, 3):
        soup = BeautifulSoup(requests.get(f'https://www.bkmkitap.com/edebiyat-kitaplari?pg={i}').content, 'html.parser')
        isimler = soup.find_all('a', class_='fl col-12 text-description detailLink')
        indirimliler = soup.find_all('div', class_='col col-12 currentPrice')
        normaller = soup.find_all('div', class_='text-line discountedPrice')

        for indirimli, normal, isim in zip(indirimliler, normaller, isimler):
            fiyat = normal.text.strip().split('\n')[0].replace('TL', '').replace('.', '').replace(',', '.').strip()
            indirimli = indirimli.text.replace('TL', '').replace('.', '').replace(',', '.').strip()

            fiyat = float(fiyat)
            indirimli = float(indirimli)

            print(isim.text.strip(), fiyat, indirimli, i)

            indirimli_fiyatlar.append(indirimli)
            normal_fiyatlar.append(fiyat)
            kitap_isimler.append(isim.text.strip())

    label.config(text="Verilerin çekilme işlemi bitti.")
    print("veriler çekildi")
    progress_bar.stop()

    # Verileri bir DataFrame'e dönüştürme
    data = {
        'Kitap İsmi': kitap_isimler,
        'Fiyat': normal_fiyatlar,
        'İndirimli Fiyat': indirimli_fiyatlar,
        '%': [(indirimli / fiyat) * 100 for indirimli, fiyat in zip(indirimli_fiyatlar, normal_fiyatlar)]
    }

    df = pd.DataFrame(data)

    # Excel dosyasına yazma
    df.to_excel('kitap_fiyatlari.xlsx', index=False)


def grafikleri_oluştur_ve_goster():
    # Grafik 1: Çizgi Grafiği
    plt.figure(figsize=(12, 8))
    plt.plot(indirimli_fiyatlar, label='İndirimli Fiyatlar', marker='o', linewidth=2, markersize=6)
    plt.plot(normal_fiyatlar, label='Normal Fiyatlar', marker='s', linewidth=2, markersize=6)
    plt.xlabel('Kitap İndeksi')
    plt.ylabel('Fiyat')
    plt.title('Kitap Fiyatları')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Grafik 2: Dağılım Grafiği
    plt.figure(figsize=(12, 8))
    sns.scatterplot(x=range(len(indirimli_fiyatlar)), y=indirimli_fiyatlar, label='İndirimli Fiyatlar')
    sns.scatterplot(x=range(len(normal_fiyatlar)), y=normal_fiyatlar, label='Normal Fiyatlar')
    plt.xlabel('Kitap İndeksi')
    plt.ylabel('Fiyat')
    plt.title('Kitap Fiyatları')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Grafik 3: KDE plot
    plt.figure(figsize=(12, 8))
    sns.kdeplot(indirimli_fiyatlar, label='İndirimli Fiyatlar')
    sns.kdeplot(normal_fiyatlar, label='Normal Fiyatlar')
    plt.xlabel('Fiyat')
    plt.ylabel('Yoğunluk')
    plt.title('Kitap Fiyatları')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Pasta Grafiği
    plt.figure(figsize=(12, 8))
    labels = ['İndirimli Fiyatlar', 'Normal Fiyatlar']
    sizes = [sum(indirimli_fiyatlar), sum(normal_fiyatlar)]
    explode = (0.1, 0)  # Dilimler arasındaki boşluğu ayarlamak için kullanılır
    colors = ['#FF7676', '#76D7FF']  # Dilimlerin renkleri
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')  # Daire şeklinde görüntülemek için
    plt.title('Toplam Fiyat Dağılımı piechart')
    plt.show()

    # Veri sayısı
    n = len(indirimli_fiyatlar)

    # X ekseni için indeksler
    indeksler = np.arange(n)

    # 3D çubuk grafik
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # İndirimli fiyatlar
    ax.bar(indeksler, indirimli_fiyatlar, zs=0, zdir='y', alpha=0.8, label='İndirimli Fiyatlar')

    # Normal fiyatlar
    ax.bar(indeksler, normal_fiyatlar, zs=1, zdir='y', alpha=0.8, label='Normal Fiyatlar')

    # Eksen etiketleri
    ax.set_xlabel('Kitap İndeksi')
    ax.set_ylabel('Fiyat')
    ax.set_zlabel('Yoğunluk')

    # Başlık
    plt.title('Kitap Fiyatları')

    # Görselleştirme
    plt.legend()
    plt.show()


def retrieve_data():
    label.config(text="Veriler çekiliyor...")
    label.config(text="Made by Melis İldireci")
    progress_bar.start()  # Start the progress bar
    thread = Thread(target=veri_cek_ve_yaz)  # Veri çekme işlemini alt işlem olarak başlat
    thread.start()
    print("veriler çekiliyor!")
    time.sleep(6)



def create_graphs():
    label.config(text="Grafikler oluşturuldu.")
    grafikleri_oluştur_ve_goster()

    print("grafikler oluşturuldu")
    time.sleep(5)

window = tk.Tk()
window.title("Kitap Fiyatları Analizi Melis İldireci")
window.geometry("450x250")

label = Label(window, text="Veri çek düğmesine daha sonra grafik oluşturmak için ilgili düğmeye tıklayın.")
label.pack(pady=10)

button_retrieve = Button(window, text="Veri Çek", command=retrieve_data)
button_retrieve.pack(pady=5)

button_graphs = Button(window, text="Grafikleri Oluştur", command=create_graphs)
button_graphs.pack(pady=5)

progress_bar = Progressbar(window, mode='indeterminate')
progress_bar.pack(pady=10)

window.mainloop()