"""
terminal uzerinden fastapi ile sürekli sohbet (post atarak)
api endpointi: /chat
"""
import requests # HTTP istekleri gondermek icin kullanacagimiz kutuphane

#api adresi
API_URL = "http://localhost:8000/chat" #fastapi uygulamamiz localde 8000 portunda calisiyor ve endpointimiz /chat

#baslangic bilgileri
name = input("Adiniz: ")
age = input("Yasiniz: ")
print("\nDoktor asistanina hosgeldiniz! Sorularinizi sorabilirsiniz. Cikmak icin 'exit' yaziniz.")

#bir dongu ile kullanicidan mesaj al ve API ye gonder
while True:

    user_message = input(f"{name}: ")
    if user_message.lower() == "exit":
        print("Gorusmek uzere!")
        break

    #API ye POST istegi gonder
    payload = {
        "name": name,
        "age": int(age),
        "message": user_message
    }

    try:
        # fastapi sunucusuna post istegi atalim, 30 saniye bekleyelim 
        res = requests.post(API_URL, json=payload, timeout=30)

        # eger istek basariliysa (200), yanit icinde responce kodu yazdirilir
        if res.status_code == 200:
            print(f"Doktor Asistanı: {res.json()['response']}")
        else:
            print("hata", res.status_code, res.text)
    except requests.exceptions.RequestException as e:
        print("Baglanti hatasi: ", e)

