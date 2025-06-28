# PyVueFinance

Nowoczesna platforma do analizy portfela inwestycyjnego: Python (Django + DRF) + Vue 3 + Vuetify.

## Stack

- Backend: Django, Django REST Framework (DRF)
- Frontend: Vue 3, Vuetify
- Repozytorium: Git
- Środowisko wirtualne: venv

## Struktura katalogów

- `/backend` – API Django + logika biznesowa
- `/frontend` – interfejs użytkownika (SPA)
- `.env.example` – przykładowe zmienne środowiskowe

## Uruchamianie

1. Skonfiguruj `venv` i zależności Python/Django (`backend/requirements.txt`)
2. Zainstaluj frontend (`npm install` w `frontend/`)
3. Odpal backend: `python manage.py runserver`
4. Odpal frontend: `npm run dev` w `frontend/`