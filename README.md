# 🕷️ Scrapper Chatbot Services

Este proyecto proporciona una API REST construida con Flask que permite realizar scraping de contenido web para alimentar un chatbot. 
La arquitectura está diseñada para ser modular y escalable, facilitando la integración de nuevos contextos y fuentes de datos.

---

## 📁 Estructura del Proyecto

scrapper_chatbot_services/
├── app/
│ ├── init.py
│ ├── routes.py
│ └── utils.py
├── context/
│ └── [archivos de contexto]
├── .gitignore
├── Dockerfile
├── requirements.txt
└── run.py

- `app/`: Contiene la lógica principal de la aplicación, incluyendo las rutas y funciones auxiliares.
- `context/`: Almacena archivos relacionados con diferentes contextos para el scraping.
- `run.py`: Punto de entrada para ejecutar la aplicación Flask.
- `Dockerfile`: Configuración para construir una imagen Docker de la aplicación.
- `requirements.txt`: Lista de dependencias necesarias para ejecutar la aplicación.

---

## 🚀 Instalación y Ejecución

### 🔧 Requisitos Previos

- Python 3.9 o superior
- Git
- (Opcional) Docker y Docker Compose

### 📥 Clonar el Repositorio

```bash
git clone https://github.com/JehielL/scrapper_chatbot_services.git
cd scrapper_chatbot_services
🐍 Configurar el Entorno Virtual
En Linux/macOS:
python3 -m venv venv
source venv/bin/activate
En Windows:
python -m venv venv
venv\Scripts\activate
📦 Instalar las Dependencias
pip install -r requirements.txt
▶️ Ejecutar la Aplicación
bash

python run.py
La aplicación estará disponible en http://127.0.0.1:5000

🐳 Uso con Docker (Opcional)
📦 Construir la Imagen Docker
docker build -t scrapper_chatbot_services .
🚀 Ejecutar el Contenedor
docker run -d -p 5000:5000 scrapper_chatbot_services

La API estará accesible en http://localhost:5000

📡 Endpoints Principales
GET /scrape: Inicia el proceso de scraping para una URL específica.

GET /contextos: Devuelve la lista de contextos disponibles.

POST /set_contexto: Permite establecer un nuevo contexto para el scraping.

⚠️ Nota: La implementación detallada de estos endpoints se encuentra en app/routes.py.

🧪 Pruebas
Actualmente, no se han implementado pruebas automatizadas. Se recomienda utilizar herramientas como pytest para agregar pruebas unitarias y de integración en el futuro.

🤝 Contribuciones
Las contribuciones son bienvenidas. Por favor, sigue los siguientes pasos:

Haz un fork del repositorio.

Crea una nueva rama (git checkout -b feature/nueva-funcionalidad).

Realiza tus cambios y haz commits descriptivos.

Envía un pull request detallando los cambios realizados.

📄 Licencia

