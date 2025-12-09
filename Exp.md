# ArtRider - Plataforma de Gestión para Equipos de Sonido

Este proyecto implementa una solución web completa para la gestión y renta de equipos de sonido y DJ. El sistema ha sido desarrollado bajo una arquitectura de software modular, separando estrictamente la lógica de negocio, la interfaz de usuario y el manejo de datos.

## Arquitectura MVC (Model-View-Controller)

Aunque se utilizan tecnologías modernas (Django Rest Framework y Angular), el proyecto respeta los principios fundamentales del patrón MVC solicitado en la asignatura de Ingeniería Web:

### 1. Modelo (Model) - `backend/users/models.py`
Representa la estructura de datos y las reglas de negocio.
- Se utilizó el ORM de Django para mapear las clases a la base de datos relacional.
- Ubicación: Carpeta `DjangoArtRdier/users/models.py`.

### 2. Controlador (Controller) - `backend/users/views.py`
Gestiona la lógica de las peticiones entrantes.
- Actúa como intermediario, recibiendo las solicitudes HTTP (GET, POST), validando datos a través de los *Serializers* y comunicándose con los Modelos.
- Ubicación: Carpeta `DjangoArtRdier/users/views.py`.

### 3. Vista (View) - Frontend (Angular)
La capa de presentación está totalmente desacoplada.
- El backend entrega datos en formato JSON (API REST).
- El frontend (Angular) consume estos datos y renderiza las vistas HTML para el usuario final.
- Configuración de UI: Archivos en la carpeta `src/`.

---

## 🛠 Tecnologías Utilizadas

* **Backend:** Python 3 + Django 5 (Django Rest Framework).
* **Frontend:** Angular + TypeScript.
* **Base de Datos:** SQLite (Entorno de desarrollo).
* **Autenticación:** Tokens JWT / Sistema de auth nativo.

---

## 🚀 Instrucciones de Ejecución

Este proyecto consta de dos partes: Backend y Frontend. Siga estos pasos para iniciar el sistema:

### Paso 1: Iniciar el Backend (Django)

1.  Abra una terminal y navegue a la carpeta del servidor:
    ```bash
    cd DjangoArtRdier
    ```
2.  Cree y active el entorno virtual (opcional pero recomendado):
    ```bash
    python -m venv venv
    # En Windows:
    .\venv\Scripts\activate
    # En Mac/Linux:
    source venv/bin/activate
    ```
3.  Instale las dependencias:
    ```bash
    pip install -r requirements.txt
    ```
4.  Ejecute las migraciones y encienda el servidor:
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```
    *El backend estará corriendo en: `http://127.0.0.1:8000/`*

### Paso 2: Iniciar el Frontend (Angular)

1.  Abra una **nueva terminal** en la raíz del proyecto (donde está este README).
2.  Instale las dependencias de Node:
    ```bash
    npm install
    ```
3.  Inicie el servidor de desarrollo:
    ```bash
    ng serve
    # O si no tiene Angular CLI global:
    npm start
    ```
    *La aplicación web estará disponible en: `http://localhost:4200/`*

---

## 📂 Estructura del Proyecto

```text
/
├── DjangoArtRdier/        # LÓGICA DE SERVIDOR (Backend)
│   ├── users/             # Módulo de Usuarios (MVC implementado)
│   │   ├── models.py      # Modelos de datos
│   │   ├── views.py       # Controladores (API Logic)
│   │   ├── serializers.py # Transformación de datos
│   │   └── urls.py        # Rutas de la API
│   ├── manage.py
│   └── requirements.txt
│
├── src/                   # INTERFAZ DE USUARIO (Frontend)
│   ├── app/               # Componentes de Angular
│   └── assets/            # Imágenes y recursos estáticos
├── package.json
└── README.md
```
## 🧪 Endpoints de Prueba (API)
  Puede probar la conexión del patrón MVC directamente en el navegador o Postman:

  Admin Panel: http://127.0.0.1:8000/admin/

  API Users: http://127.0.0.1:8000/users/ (Dependiendo de la configuración de rutas en urls.py)
