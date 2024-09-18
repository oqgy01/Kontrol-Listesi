import requests
from bs4 import BeautifulSoup
url = "https://docs.google.com/spreadsheets/d/1AP9EFAOthh5gsHjBCDHoUMhpef4MSxYg6wBN0ndTcnA/edit#gid=0"
response = requests.get(url)
html_content = response.content
soup = BeautifulSoup(html_content, "html.parser")
first_cell = soup.find("td", {"class": "s2"}).text.strip()
if first_cell != "Aktif":
    exit()
first_cell = soup.find("td", {"class": "s1"}).text.strip()
print(first_cell)



import pandas as pd
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
from io import BytesIO
import os
import numpy as np
import shutil
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.chrome.service import Service
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from selenium.common.exceptions import TimeoutException, WebDriverException
import xml.etree.ElementTree as ET
import warnings
from colorama import init, Fore, Style
import openpyxl
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from collections import Counter
import requests
import io
warnings.filterwarnings("ignore")
import tkinter as tk
from tkinter import simpledialog
import chromedriver_autoinstaller
pd.options.mode.chained_assignment = None



chromedriver_autoinstaller.install()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--log-level=1') 
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  
driver = webdriver.Chrome(options=chrome_options)

login_url = "https://task.haydigiy.com/kullanici-giris/?ReturnUrl=%2Fadmin"
driver.get(login_url)

email_input = driver.find_element("id", "EmailOrPhone")
email_input.send_keys("mustafa_kod@haydigiy.com")

password_input = driver.find_element("id", "Password")
password_input.send_keys("123456")
password_input.send_keys(Keys.RETURN)

driver.maximize_window()


desired_page_url = "https://task.haydigiy.com/admin/product/list/"
driver.get(desired_page_url)

#Kategori Dahil Alan
category_select = Select(driver.find_element("id", "AdvancedFilterIds"))

#Kategori ID'si (Fiyata Hamle)
category_select.select_by_value("40")

#Seçiniz Kısmının Tikini Kaldırma
all_remove_buttons = driver.find_elements(By.XPATH, "//span[@class='select2-selection__choice__remove']")
second_remove_button = all_remove_buttons[0]
second_remove_button.click()

# "SearchMinStock" input alanına 3 değerini girin
search_min_stock_input = driver.find_element(By.ID, "SearchMinStock")
driver.execute_script("arguments[0].style.display = 'block';", search_min_stock_input)
search_min_stock_input.clear()
search_min_stock_input.send_keys("3")

#Ara Butonuna Tıklama
search_button = driver.find_element(By.ID, "search-products")
search_button.click()
search_button.click()

# "data-role" attribute'u "dropdownlist" olan select elementi bulun
dropdown_element = driver.find_element(By.CSS_SELECTOR, "select[data-role='dropdownlist']")

# JavaScript kullanarak elementi görünür yapın
driver.execute_script("arguments[0].style.display = 'block';", dropdown_element)

# Select sınıfını kullanarak elementi seçin ve değerini değiştirin
dropdown = Select(dropdown_element)
dropdown.select_by_value("100")

time.sleep(2)

# Tarihleri saklamak için bir liste oluştur
tarihler = []

# Ana döngü: bir sonraki sayfaya geçilene kadar devam eder
while True:
    # Sayfadaki tüm metin öğelerini bul ve tarih içerenleri listeye ekle
    metin_elements = driver.find_elements(By.XPATH, "//*[text()]")
    for metin_element in metin_elements:
        # Metin öğesinin içeriğini al
        metin = metin_element.text.strip()
        # Eğer metin bir tarih formatına uyuyorsa, tarihi listeye ekle
        try:
            tarih = datetime.strptime(metin, "%d.%m.%Y %H:%M:%S").strftime("%d.%m.%Y")
            tarihler.append(tarih)
        except ValueError:
            pass  # Metin bir tarih değilse, geç

    try:
        # "Bir sonraki sayfaya git" butonunu bul
        next_page_button = driver.find_element(By.XPATH, "//a[@class='k-link k-pager-nav' and @aria-label='Bir sonraki sayfaya git']")
        
        # Eğer buton tıklanabilirse, ikinci sayfaya geç
        if "k-state-disabled" not in next_page_button.get_attribute("class"):
            next_page_button.click()
            time.sleep(2) # Sayfa yüklenene kadar bekleyin
        else:
            # Buton tıklanabilir değilse, döngüyü sonlandır
            break
    except NoSuchElementException:
        # "Bir sonraki sayfaya git" butonu bulunamazsa, en son sayfadayız, döngüyü sonlandır
        break

# Tarihlerin kaç kez tekrarlandığını bul
tekrar_sayisi = {}
for tarih in tarihler:
    tekrar_sayisi[tarih] = tarihler.count(tarih)

# Sonuçları bir metin dosyasına yaz
with io.open("Kontrol Listesi.txt", "w") as dosya:
    dosya.write("Resimsiz Ürünler\n\n")
    for tarih, tekrar in tekrar_sayisi.items():
        dosya.write(f"{tarih} - {tekrar}\n")

# Tüm tarihleri teke düşür
tarihler_tek = list(set(tarihler))

driver.quit()












# İndirilecek dosyanın URL'si
url = "https://task.haydigiy.com/FaprikaReturnXls/30WGD6/1/"

# İstek gönder
response = requests.get(url)

# Dosyayı kaydet
with open("indirilen_dosya.xlsx", "wb") as file:
    file.write(response.content)


# Excel dosyasını oku
df = pd.read_excel("indirilen_dosya.xlsx")

# Korunacak sütunlar
columns_to_keep = ["Id", "OlusturulmaTarihi"]

# Silinecek sütunları belirle
columns_to_drop = [col for col in df.columns if col not in columns_to_keep]

# Belirtilen sütunları sil
df.drop(columns=columns_to_drop, inplace=True)

# Tüm tabloda yenilenenleri kaldır
df.drop_duplicates(inplace=True)

# OlusturulmaTarihi sütunundaki saat verilerini temizle
df["OlusturulmaTarihi"] = pd.to_datetime(df["OlusturulmaTarihi"], format='%d.%m.%Y %H:%M:%S').dt.date

# Liste içerisindeki yenilenenlerin sayısını hesapla
yenilenen_sayilari = Counter(df["OlusturulmaTarihi"])

# Tekil tarihleri al
tekil_tarihler = list(set(df["OlusturulmaTarihi"]))

# Kontrol Listesi.txt dosyasına yaz
with io.open("Kontrol Listesi.txt", "a") as dosya:
    dosya.write("\nBekleyen İadeler\n")
    for tarih in tekil_tarihler:
        yenilenen_sayisi = yenilenen_sayilari[tarih]
        dosya.write(f"{tarih} - {yenilenen_sayisi} \n")

        












def download_and_merge_excel(url1, url2, url3):
    # İlk Excel dosyasını indir
    response1 = requests.get(url1)
    with open('excel1.xlsx', 'wb') as f1:
        f1.write(response1.content)

    # İkinci Excel dosyasını indir
    response2 = requests.get(url2)
    with open('excel2.xlsx', 'wb') as f2:
        f2.write(response2.content)

    # Üçüncü Excel dosyasını indir
    response3 = requests.get(url3)
    with open('excel3.xlsx', 'wb') as f3:
        f3.write(response3.content)

    # İki Excel dosyasını birleştir
    df1 = pd.read_excel('excel1.xlsx')
    df2 = pd.read_excel('excel2.xlsx')
    df3 = pd.read_excel('excel3.xlsx')

    merged_df = pd.concat([df1, df2, df3], ignore_index=True)

    # Birleştirilmiş dosyaları yeni bir Excel'e yaz
    merged_df.to_excel('UrunListesi.xlsx', index=False)

    # İndirilen Excel dosyalarını sil 
    os.remove('excel1.xlsx')
    os.remove('excel2.xlsx')
    os.remove('excel3.xlsx')

if __name__ == "__main__":
    url1 = "https://task.haydigiy.com/FaprikaXls/ZU4HUQ/1/"
    url2 = "https://task.haydigiy.com/FaprikaXls/ZU4HUQ/2/"
    url3 = "https://task.haydigiy.com/FaprikaXls/ZU4HUQ/3/"

    download_and_merge_excel(url1, url2, url3)

# Birleştirilmiş Excel dosyasını oku
df_merged = pd.read_excel('UrunListesi.xlsx')



# Excel dosyasını oku
df = pd.read_excel("UrunListesi.xlsx")

# DataFrame'i yeni bir dosyaya yaz
df.to_excel("UrunListesi2.xlsx", index=False)



# Excel dosyasını oku
df = pd.read_excel("UrunListesi.xlsx")

# "UrunAdi", "Aciklama", "MetaAciklama" sütunlarını dışındaki tüm sütunları sil
df = df[["UrunAdi", "Aciklama", "MetaAciklama"]]

# Tüm tabloda yenilenenleri kaldır
df = df.drop_duplicates()


# Temizlenmiş verileri "YenilenmemişUrunListesi.xlsx" dosyasına yaz
df.to_excel("UrunListesi.xlsx", index=False)


# Excel dosyasını oku
df = pd.read_excel("UrunListesi.xlsx")

# "Aciklama" sütununda boş olan hücrelerin sayısını al
bos_hucre_sayisi = df["Aciklama"].isnull().sum()

# "Kontrol Listesi.txt" dosyasına yaz
with io.open("Kontrol Listesi.txt", "a") as dosya:
    dosya.write("\nÖzelliksiz Ürün Adedi: " + str(bos_hucre_sayisi) + "\n")













# Excel dosyasını oku
df = pd.read_excel("UrunListesi.xlsx")

# "Aciklama" sütununu sil
df.drop(columns=["Aciklama"], inplace=True)

# "MetaAciklama" sütununda "Birbirinden şık" ile başlayan ve boş olmayan hücreleri filtrele
df = df[df["MetaAciklama"].str.startswith("Birbirinden şık", na=False) | df["MetaAciklama"].isnull()]

# Temizlenmiş verileri "TemizlenmisUrunListesi.xlsx" dosyasına yaz
df.to_excel("UrunListesi.xlsx", index=False)


# Excel dosyasını oku
df = pd.read_excel("UrunListesi.xlsx")

# "UrunAdi" sütunundaki verilerin adedini al
urun_adi_adedi = len(df["UrunAdi"])

# "Kontrol Listesi.txt" dosyasına yaz
with io.open("Kontrol Listesi.txt", "a") as dosya:
    dosya.write("Bana Urunu Anlat Verisi Olmayan Urun Adedi: " + str(urun_adi_adedi) + "\n")










# Dosyaların adlarını listeye al
dosya_listesi = ["indirilen_dosya.xlsx", "UrunListesi.xlsx"]

# Her dosyayı silelim
for dosya in dosya_listesi:
    try:
        os.remove(dosya)
        print(f"{dosya} başarıyla silindi.")
    except FileNotFoundError:
        print(f"{dosya} dosyası bulunamadı.")
    except Exception as e:
        print(f"{dosya} dosyası silinirken bir hata oluştu: {e}")









# Excel dosyasını oku
df = pd.read_excel("UrunListesi2.xlsx")


# "UrunAdi", "Aciklama", "MetaAciklama" sütunlarını dışındaki tüm sütunları sil
df = df[["ModelKodu", "UrunAdi", "Kategori", "Ozellik", "VaryasyonN11Kodu", "MorhipoKodu", "VaryasyonMorhipoKodu", "HepsiBuradaKodu", "VaryasyonHepsiBuradaKodu", "Marka"]]

# Tüm tabloda yenilenenleri kaldır
df = df.drop_duplicates()


# Temizlenmiş verileri "YenilenmemişUrunListesi.xlsx" dosyasına yaz
df.to_excel("UrunListesi2.xlsx", index=False)





# "UrunListesi2.xlsx" dosyasını oku
df = pd.read_excel("UrunListesi2.xlsx")

# "Marka" sütununda "GRL" içermeyen hücreleri say
grl_icermeyen_urun_sayisi = df[~df["Marka"].str.contains("GRL", na=False)].shape[0]

# "Kontrol Listesi.txt" dosyasına ekle
with io.open("Kontrol Listesi.txt", "a", encoding="utf-8") as file:
    file.write("GRL Markasi Olmayan Urunler: {}\n".format(grl_icermeyen_urun_sayisi))










# "UrunListesi2.xlsx" dosyasını oku
df = pd.read_excel("UrunListesi2.xlsx")

# "Kategori" sütununda boş olan hücreleri say
kategorisiz_urun_sayisi = df["Kategori"].isna().sum()

# "Kontrol Listesi.txt" dosyasına ekle
with io.open("Kontrol Listesi.txt", "a", encoding="utf-8") as file:
    file.write("Kategorisiz Urunler: {}\n".format(kategorisiz_urun_sayisi))








# "UrunListesi2.xlsx" dosyasını oku
df = pd.read_excel("UrunListesi2.xlsx")

# "Kategori" sütununda boş olan hücreleri say
kategorisiz_urun_sayisi = df["VaryasyonN11Kodu"].isna().sum()

# "Kontrol Listesi.txt" dosyasına ekle
with io.open("Kontrol Listesi.txt", "a", encoding="utf-8") as file:
    file.write("Kac Gundur Satista Verisi Girilmemis Urunler: {}\n".format(kategorisiz_urun_sayisi))








# "UrunListesi2.xlsx" dosyasını oku
df = pd.read_excel("UrunListesi2.xlsx")

# "Kategori" sütununda boş olan hücreleri say
kategorisiz_urun_sayisi = df["MorhipoKodu"].isna().sum()

# "Kontrol Listesi.txt" dosyasına ekle
with io.open("Kontrol Listesi.txt", "a", encoding="utf-8") as file:
    file.write("Ortalama Satis Adedi Verisi Girilmemis Urunler: {}\n".format(kategorisiz_urun_sayisi))







# "UrunListesi2.xlsx" dosyasını oku
df = pd.read_excel("UrunListesi2.xlsx")

# "Kategori" sütununda boş olan hücreleri say
kategorisiz_urun_sayisi = df["VaryasyonMorhipoKodu"].isna().sum()

# "Kontrol Listesi.txt" dosyasına ekle
with io.open("Kontrol Listesi.txt", "a", encoding="utf-8") as file:
    file.write("Diger Depodaki Adetler Verisi Girilmemis Urunler: {}\n".format(kategorisiz_urun_sayisi))









# "UrunListesi2.xlsx" dosyasını oku
df = pd.read_excel("UrunListesi2.xlsx")

# "Kategori" sütununda boş olan hücreleri say
kategorisiz_urun_sayisi = df["HepsiBuradaKodu"].isna().sum()

# "Kontrol Listesi.txt" dosyasına ekle
with io.open("Kontrol Listesi.txt", "a", encoding="utf-8") as file:
    file.write("Goruntulenme Adedi Verisi Girilmemis Urunler: {}\n".format(kategorisiz_urun_sayisi))









# "UrunListesi2.xlsx" dosyasını oku
df = pd.read_excel("UrunListesi2.xlsx")

# "Kategori" sütununda boş olan hücreleri say
kategorisiz_urun_sayisi = df["VaryasyonHepsiBuradaKodu"].isna().sum()

# "Kontrol Listesi.txt" dosyasına ekle
with io.open("Kontrol Listesi.txt", "a", encoding="utf-8") as file:
    file.write("Raf Omru Verisi Girilmemis Urunler: {}\n".format(kategorisiz_urun_sayisi))









# "UrunListesi2.xlsx" dosyasını oku
df = pd.read_excel("UrunListesi2.xlsx")

# "Ozellik" sütununda "Renk Seçiniz" metnini içermeyen hücreleri say
renk_seciniz_olmayan_urun_sayisi = df["Ozellik"].apply(lambda x: "Renk Seçiniz" not in str(x)).sum()

# "Kontrol Listesi.txt" dosyasına ekle
with io.open("Kontrol Listesi.txt", "a", encoding="utf-8") as file:
    file.write("Renk Seciniz Ozelligi Olmayan Urunler: {}\n".format(renk_seciniz_olmayan_urun_sayisi))










# "UrunListesi2.xlsx" dosyasını oku
df = pd.read_excel("UrunListesi2.xlsx")

# "Ozellik" sütununda "Renk Seçiniz" metnini içermeyen hücreleri say
renk_seciniz_olmayan_urun_sayisi = df["Ozellik"].apply(lambda x: "Kategori Seçiniz" not in str(x)).sum()

# "Kontrol Listesi.txt" dosyasına ekle
with io.open("Kontrol Listesi.txt", "a", encoding="utf-8") as file:
    file.write("Kategori Seciniz Ozelligi Olmayan Urunler: {}\n".format(renk_seciniz_olmayan_urun_sayisi))








# Excel dosyasını oku
df = pd.read_excel("UrunListesi2.xlsx")

# "UrunAdi" sütunundaki her bir verinin " - " karakterinden sonraki kısmını temizle
df["UrunAdi"] = df["UrunAdi"].apply(lambda x: x.split(" - ")[1] if " - " in x else x)









# "UrunListesi2.xlsx" dosyasını oku
df = pd.read_excel("UrunListesi2.xlsx")

# "UrunAdi" sütunundaki her bir verinin " - " karakterinden sonraki kısmını temizle
df["UrunAdi"] = df["UrunAdi"].apply(lambda x: x.split(" - ")[1] if " - " in x else x)

# "ModelKodu" sütunundaki verilerden "m1." metnini temizle
df["ModelKodu"] = df["ModelKodu"].str.replace("m1.", "")

# "ModelKodu" ve "UrunAdi" sütunlarını karşılaştır ve eşleşmeyenleri say
eslesmeyen_urun_sayisi = (df["ModelKodu"] != df["UrunAdi"]).sum()

# "Kontrol Listesi.txt" dosyasına ekle
with io.open("Kontrol Listesi.txt", "a", encoding="utf-8") as file:
    file.write("Model Kodu ile Urun Kodu Tutmayan Urunler: {}\n".format(eslesmeyen_urun_sayisi))



















# Dosyaların adlarını listeye al
dosya_listesi = ["UrunListesi2.xlsx"]

# Her dosyayı silelim
for dosya in dosya_listesi:
    try:
        os.remove(dosya)
        print(f"{dosya} başarıyla silindi.")
    except FileNotFoundError:
        print(f"{dosya} dosyası bulunamadı.")
    except Exception as e:
        print(f"{dosya} dosyası silinirken bir hata oluştu: {e}")



