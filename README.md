# InstagramChatBot
Această aplicație automatizează interacțiunea cu Instagram Direct folosind Selenium și Gemini API. Permite logarea într-un cont de Instagram, extragerea conversațiilor și generarea de răspunsuri automate pe baza unui script. Mesajele sunt salvate într-un fișier pentru gestionarea conversațiilor.

Prerequisite
Înainte de a începe, asigură-te că ai instalate următoarele dependențe:

Python 3.x
Selenium
Gemini API
WebDriver pentru browserul tău (ex: ChromeDriver)
Instalarea Dependențelor
Instalează dependențele necesare folosind pip:

pip install -r requirements.txt
Asigură-te că ai adăugat WebDriver-ul (de exemplu, ChromeDriver) în PATH-ul tău sau poți specifica calea completă în scriptul script_bot.py.

Configurarea Fișierului key.env
Înainte de a rula scriptul, trebuie să creezi un fișier .env (sau key.env) pentru a configura datele necesare contului tău de Instagram și cheia pentru API.

Creează un fișier numit key.env în directorul principal al aplicației tale.

Adaugă următoarele variabile în fișierul key.env:

INSTAGRAM_USERNAME=contul_tau_instagram
INSTAGRAM_PASSWORD=parola_ta_instagram
GEMINI_API_KEY=cheia_ta_api
Asigură-te că înlocuiești valorile corespunzătoare pentru contul tău de Instagram și cheia API. Aceste informații sunt esențiale pentru autentificarea și interacțiunea cu serviciile necesare.

Cum să rulezi scriptul script_bot.py
Asigură-te că fișierul key.env a fost creat corect și conține datele necesare.

Lansează scriptul folosind comanda de mai jos:
python script_bot.py
Scriptul va citi automat datele din fișierul key.env, se va conecta la Instagram și va extrage conversațiile.

Interacțiunea cu Scriptul din Consolă
Aplicația este concepută să ruleze complet din consolă și să interacționeze cu utilizatorul. Odată ce scriptul este pornit:

Se va face logarea automat pe Instagram.

Vei vedea în consolă mesajele extrase din conversațiile tale Instagram Direct.

Pe baza unui script predefinit, botul va genera răspunsuri automate și le va trimite înapoi.

Toate conversațiile și răspunsurile vor fi salvate într-un fișier log pentru a putea gestiona istoricul mesajelor.

Exemple de Comenzi
Aplicația rulează complet în fundal și nu necesită interacțiune directă, dar poate fi configurată pentru a personaliza mesajele automate.

Începe botul automatizat:

python script_bot.py
Modifică scriptul de răspunsuri:
Modifică scriptul care răspunde automat în fișierul response_script.py (dacă este disponibil). Acest fișier poate fi modificat pentru a schimba comportamentul botului.

Răspunsuri Automate
Aplicația utilizează Gemini API pentru a genera răspunsuri automate. Dacă este configurat corect, botul va analiza mesajele din Instagram și va răspunde pe baza unui algoritm predefinit.

Depanare
Eroare de autentificare Instagram: Asigură-te că datele din fișierul key.env sunt corecte.

WebDriver nu este găsit: Verifică dacă ai instalat corect WebDriver-ul pentru browserul pe care îl folosești.

Pentru orice alte întrebări, nu ezita să deschizi un issue pe GitHub sau să contactezi dezvoltatorul.

Licență
Acest proiect este licențiat sub licența MIT. Vezi fișierul LICENSE pentru mai multe detalii.

În acest README:
Cum să configurezi contul și cheia API în fișierul .env.

Cum să rulezi scriptul din consolă.

Informații despre interacțiunea cu scriptul și gestionarea conversațiilor.

Asta ar trebui să ofere tot ce ai nevoie pentru ca utilizatorii să poată rula aplicația și să înțeleagă cum să configureze corect fișierele și mediul.
