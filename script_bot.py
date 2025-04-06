import time
import random
import os
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import google.generativeai as genai
import re

load_dotenv("key.env")

INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
models = genai.list_models()

print("Modelele disponibile:")
for model in models:
    print(f"- {model.name}")
model = genai.GenerativeModel('models/gemini-1.5-pro-001')

chromedriver_autoinstaller.install()

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
)

service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

def remove_non_bmp_chars(text):
    return ''.join(char for char in text if ord(char) <= 0xFFFF)

def login_instagram():
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(random.uniform(1, 2))
    WebDriverWait(driver, 4).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Allow all cookies')]"))).click()

    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")

    username_input.send_keys(INSTAGRAM_USERNAME)
    time.sleep(random.uniform(2, 3))
    password_input.send_keys(INSTAGRAM_PASSWORD)
    time.sleep(random.uniform(2, 3))
    password_input.send_keys(Keys.RETURN)

    time.sleep(random.uniform(9, 10))

def get_all_conversations():
    driver.get("https://www.instagram.com/direct/inbox/")

    try:
        try:
            cookie_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))
            )
            cookie_button.click()

        except NoSuchElementException:
            print()

        WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@role='button']")))

        conversation_containers = driver.find_elements(By.XPATH,
                                                       "//div[contains(@class, 'x9f619') and contains(@class, 'xjbqb8w') and contains(@class, 'x78zum5') and contains(@class, 'x168nmei') and contains(@class, 'x13lgxp2') and contains(@class, 'x5pf9jr') and contains(@class, 'xo71vjh') and contains(@class, 'x1uhb9sk') and contains(@class, 'x1plvlek') and contains(@class, 'xryxfnj') and contains(@class, 'x1c4vz4f') and contains(@class, 'x2lah0s') and contains(@class, 'x1q0g3np') and contains(@class, 'xqjyukv') and contains(@class, 'x6s0dn4') and contains(@class, 'x1oa3qoh') and contains(@class, 'x1nhvcw1')]")

        all_conversations = []

        for container in conversation_containers:
            elements = container.find_elements(By.XPATH,
                                               ".//span[contains(@class, 'x1lliihq') and contains(@class, 'x193iq5w') and contains(@class, 'x6ikm8r') and contains(@class, 'x10wlt62') and contains(@class, 'xlyipyv') and contains(@class, 'xuxw1ft')]")

            conversation_data = [element.text.strip() for element in elements]

            all_conversations.append(conversation_data)

        filtered_texts = []

        for conversation in all_conversations:
            texts = [conversation[i] for i in range(len(conversation)) if i % 2 == 0]

            filtered_texts.extend(texts)

        all_conversations = [conversation[i] for conversation in all_conversations for i in range(len(conversation)) if
                             i % 2 == 0]
        lista_filtrata = [all_conversations[i] for i in range(len(all_conversations)) if i % 2 == 0]
        print("Lista de nume:")
        for i, nume in enumerate(lista_filtrata):
            print(f"{i + 1}. {nume}")

        selected_index = int(input("Introdu numărul corespunzător numelui pe care vrei să-l selectezi: ")) - 1

        print(len(conversation_containers))
        if 0 <= selected_index < len(lista_filtrata):
            selected_container = conversation_containers[selected_index * 2]

            selected_container.click()
            print(f"Conversația cu {lista_filtrata[selected_index]} a fost deschisă.")
            return lista_filtrata[selected_index]

        else:
            print("Index invalid. Te rog să introduci un număr valid.")

    except Exception as e:
        print("Eroare la obținerea conversațiilor:", e)
        return []

def get_last_received_message():
    time.sleep(1)
    try:
        mesaje = driver.find_elements(By.XPATH,
                                      "//div[contains(@class, 'html-div') and contains(@class, 'xexx8yu') and text() != '']")


        if mesaje:
            ultimul_mesaj = mesaje[-1].text.strip()
            return ultimul_mesaj
        else:
            return None
    except Exception as e:
        print(f"Eroare la citirea ultimului mesaj: {e}")
        return None

def write_message(conversation_name):
    conversatie = get_full_conversation(conversation_name)
    prompt = "\n".join(conversatie)

    prompt = prompt + ("Continua conversatia in mod natural")

    WebDriverWait(driver, 2).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@aria-placeholder='Message...']"))
    )

    response = model.generate_content(prompt)
    mesaj = response.text

    mesaj = remove_non_bmp_chars(mesaj)
    camp_mesaj = driver.find_element(By.XPATH, "//div[@aria-placeholder='Message...']")
    for char in mesaj:
        camp_mesaj.send_keys(char)
        time.sleep(0.001)
    time.sleep(1)
    camp_mesaj.send_keys(Keys.RETURN)
    with open(f"conversatii/{conversation_name}.txt", "a", encoding="utf-8") as file:
        file.write(f"Bot: {mesaj}\n")

    print(f"Mesaj trimis: {mesaj}")

def ultimul_mesaj(conversation_name):
    try:
        with open(f"conversatii/{conversation_name}.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()

            bot_messages = [line.strip() for line in lines if line.startswith("Bot:")]

            if bot_messages:
                last_message = bot_messages[-1][len("Bot: "):].strip()
                return last_message
            else:
                return ""
    except FileNotFoundError:
        print(f"Fișierul {conversation_name}.txt nu a fost găsit.")
        return ""
    except Exception as e:
        print(f"Eroare la citirea fișierului: {e}")
        return ""

def auto_reply(nume_persoana):
    time.sleep(10)
    if get_last_received_message() != ultimul_mesaj(nume_persoana):
        with open(f"conversatii/{nume_persoana}.txt", "a", encoding="utf-8") as file:
            file.write(f"{get_last_received_message()} \n")
            time.sleep(5)
            write_message(nume_persoana)

def get_full_conversation(conversation_name):
    try:
        with open(f"conversatii/{conversation_name}.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()

            conversation = [line.strip() for line in lines]
            return conversation
    except FileNotFoundError:
        print(f"Fișierul {conversation_name}.txt nu a fost găsit.")
        return []
    except Exception as e:
        print(f"Eroare la citirea fișierului: {e}")
        return []

running = True
def check_stop():
    global running
    user_input = input("Apasă 'q' pentru a opri procesul: ")
    if user_input.lower() == 'q':
        running = False
        print("Procesul a fost oprit.")

login_instagram()

nume_persoana = get_all_conversations()

def handle_action(option):
    if option == 1:
        write_message(nume_persoana)
    elif option == 2:
        while True:
            auto_reply(nume_persoana)

    elif option == 3:
        time.sleep(3)
        driver.quit()
    else:
        print("Invalid option")

while True:
    try:
        option = int(input("Enter 1 for write_message, 2 for auto_reply: "))
        handle_action(option)
        if option == 3:
            break
    except ValueError:
        print("Please enter a valid number (1 or 2 or 3).")
