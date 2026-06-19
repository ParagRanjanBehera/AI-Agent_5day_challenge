# BigQuery Release Notes Explorer & Twitter Composer

A premium, glassmorphic dark-themed web application built with **Python Flask** and **Vanilla HTML, JavaScript, and CSS**. This explorer fetches Google Cloud's official BigQuery release notes Atom feed, structures updates dynamically, and allows users to compose and publish tweets directly to X (formerly Twitter) with a built-in character constraint tool.

---

## 🌟 Key Features

*   **Premium Visual Experience:** Modern dark-mode interface featuring subtle gradients, glassmorphism, responsive grids, and micro-animations.
*   **Structured Parsing:** Breaks down complex, multi-item daily release notes into distinct individual cards with color-coded category badges (`Feature`, `Announcement`, `Issue`, `Deprecation`, `General`).
*   **Search & Dynamic Filters:** Instant search by keywords or dates, combined with quick category filters.
*   **Intelligent Caching:** Implements robust in-memory caching to avoid hitting Google Cloud rate limits, with a manual refresh button featuring a sleek spinner loader.
*   **Interactive Twitter Composer:** 
    *   Draft posts with pre-filled content, date, type, and source links.
    *   Dynamic circular progress ring tracker matching the **280-character limit**.
    *   Quick-insert buttons for common hashtags (`#BigQuery`, `#GCP`, `#GoogleCloud`).
*   **Multi-Select Publishing:** Select multiple updates to automatically compile into a consolidated summary.

---

## 🛠️ Tech Stack

*   **Backend:** Python 3.9+, Flask, Requests (HTTP calls), BeautifulSoup4 (HTML parser)
*   **Frontend:** Vanilla HTML5, Vanilla CSS3 (Glassmorphism & animations), JavaScript (ES6+, DOM Manipulation)
*   **Assets:** Google Fonts (Inter), FontAwesome 6 (Icons)

---

## 🚀 Getting Started

### 1. Clone the repository & enter the folder
```bash
git clone https://github.com/ParagRanjanBehera/AI-Agent_5day_challenge.git
cd AI-Agent_5day_challenge
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the development server
```bash
python app.py
```

### 4. Open in browser
Navigate to **[http://localhost:5000](http://localhost:5000)** in your web browser.

---

## 📁 Repository Structure

```
AI-Agent_5day_challenge/
├── app.py                   # Flask backend & XML parsing engine
├── requirements.txt         # Package dependencies
├── .gitignore               # Ignored local environments & caches
├── README.md                # Project documentation
└── templates/
    └── index.html           # Glassmorphic user interface & tweet composer
```

---

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).
