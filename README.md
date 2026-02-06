# 🥩 MeatOrder Manager

**MeatOrder Manager** ist eine Django‑Webanwendung zur **Bestell‑, Kunden‑ und Rundenverwaltung für den Fleischverkauf**.
Die App eignet sich für kleinere Betriebe, Direktvermarkter oder Vereine, die wiederkehrende Bestellrunden organisieren.

---

## 🚀 Features

* 📦 **Bestellrunden verwalten** (aktiv / abgeschlossen)
* 👥 **Kundenverwaltung**
* 🥩 **Produktverwaltung**
* 📝 **Bestellungen anlegen, bearbeiten & löschen**
* 📊 **Übersicht pro Runde**
* 🔐 **Django Admin‑Backend**
* 🧼 Saubere Projektstruktur (ohne sensible Daten im Repo)

---

## 🛠️ Tech‑Stack

* **Backend:** Python, Django
* **Frontend:** Django Templates (HTML)
* **Datenbank:** SQLite (lokal, nicht im Repository)
* **Versionsverwaltung:** Git & GitHub

---

## ⚙️ Installation & Setup

### 1️⃣ Repository klonen

```bash
git clone https://github.com/Mueco34/meatorder-manager.git
cd meatorder-manager
```

### 2️⃣ Virtuelle Umgebung erstellen & aktivieren

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Abhängigkeiten installieren

```bash
python -m pip install -r requirements.txt
```

### 4️⃣ Datenbank migrieren

```bash
python manage.py migrate
```

### 5️⃣ Superuser erstellen (optional, empfohlen)

```bash
python manage.py createsuperuser
```

### 6️⃣ Entwicklungsserver starten

```bash
python manage.py runserver
```

➡️ Aufruf im Browser: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🔐 Datenschutz & Sicherheit

* ❌ **Keine echte Datenbank im Repository**
* ❌ **Keine Kundendaten auf GitHub**
* ✔️ `db.sqlite3` ist durch `.gitignore` ausgeschlossen
* ✔️ Sensible Konfigurationen können über `.env` erfolgen

Dieses Repository enthält **ausschließlich Quellcode**.

---

## 🧪 Demo & Weiterentwicklung

Für Präsentationen oder Demos können **Fake‑Daten** genutzt werden.
Echte Kundendaten sollten ausschließlich lokal oder auf einem geschützten Server gespeichert werden.

Geplante Erweiterungen:

* 📤 Export (CSV / PDF)
* 📈 Auswertungen pro Runde
* 🌐 Deployment‑Setup
* 👤 Rollen & Benutzerrechte

---

## 📄 Lizenz

Dieses Projekt dient als **Referenz‑ und Lernprojekt**.
Eine kommerzielle Nutzung kann individuell geklärt werden.

---

## 👨‍💻 Autor

**Mücahid Akargöl**
Junior Softwareentwickler

GitHub: [https://github.com/Mueco34](https://github.com/Mueco34)

---

✨ *Feedback, Ideen und Verbesserungsvorschläge sind jederzeit willkommen!*
