# ArtRider - Plataforma de Gestión para Equipos de Sonido

Este proyecto implementa una solución web completa para la gestión y renta de equipos de sonido y DJ. El sistema ha sido desarrollado bajo una arquitectura de software modular, separando estrictamente la lógica de negocio (Backend Django) de la interfaz de usuario (Frontend Angular).

Este proyecto fue generado utilizando [Angular CLI](https://github.com/angular/angular-cli) versión 20.3.7 para el cliente y Django Rest Framework para el servidor.

---

## 🏗 Arquitectura MVC (Model-View-Controller)

Aunque se utilizan tecnologías modernas orientadas a servicios (API REST), el proyecto respeta los principios fundamentales del patrón MVC solicitado en la asignatura de Ingeniería Web:

### 1. Modelo (Model) - `backend/users/models.py`
Representa la estructura de datos y las reglas de negocio.
- Se utilizó el ORM de Django para mapear las clases a la base de datos relacional.
- **Ubicación:** Carpeta `backend/users/models.py`.

### 2. Controlador (Controller) - `backend/users/views.py`
Gestiona la lógica de las peticiones entrantes.
- Actúa como intermediario, recibiendo las solicitudes HTTP (GET, POST), validando datos a través de los *Serializers* y comunicándose con los Modelos.
- **Ubicación:** Carpeta `backend/users/views.py`.

### 3. Vista (View) - Frontend (Angular)
La capa de presentación está totalmente desacoplada en la carpeta `frontend/`.
- El backend entrega datos en formato JSON.
- El frontend (Angular) consume estos datos y renderiza las vistas HTML para el usuario final.
- **Ubicación:** Carpeta `frontend/src/`.

---

## 📂 Estructura del Proyecto

El repositorio está organizado como un monorepositorio con dos directorios principales:

```text
/
├── backend/               # LÓGICA DE SERVIDOR (Django)
│   ├── users/             # Módulo de Usuarios (MVC)
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/              # INTERFAZ DE USUARIO (Angular)
│   ├── src/               # Componentes y Vistas
│   ├── angular.json
│   └── package.json
│
├── .gitignore
└── README.md
```
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

## 🧪 Endpoints y Pruebas

### Verificar API (Backend)
Puede probar la conexión del patrón MVC directamente en el navegador o Postman:

* **Admin Panel:** `http://127.0.0.1:8000/admin/`
* **API Users:** `http://127.0.0.1:8000/users/`

### Comandos de Angular (Frontend)
Si desea ejecutar tareas de mantenimiento en el frontend, utilice los siguientes comandos dentro de la carpeta `frontend/`:

* **Generar componentes:** `ng generate component component-name`
* **Build de producción:** `ng build` (Los artefactos se guardarán en `dist/`)
* **Unit Tests:** `ng test` (vía Karma)
* **End-to-End Tests:** `ng e2e`

Para más información sobre Angular CLI, visite [Angular CLI Overview and Command Reference](https://angular.dev/tools/cli).