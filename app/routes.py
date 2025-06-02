# app/routes.py

from flask import Blueprint, request, jsonify, current_app
from app.scraper import crawl_and_scrape
from app.utils import save_to_txt
import jwt

routes_bp = Blueprint('routes', __name__)


@routes_bp.route('/scrape', methods=['GET'])
def scrape():
    url = request.args.get("url")
    token_header = request.headers.get("Authorization")

    if not url:
        return jsonify({"error": "Parametro 'url' requerido"}), 400
    if not token_header:
        return jsonify({"error": "Token JWT requerido en Authorization"}), 401

    token = token_header.split(" ")[1] if token_header.startswith("Bearer ") else token_header

    try:
        # Validar y decodificar el JWT
        print(f"🔐 SECRET KEY EN USO: {current_app.config.get('JWT_SECRET_KEY')}")

        decoded = jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
        propietario_id = decoded.get("user_id")
        if not propietario_id:
            return jsonify({"error": "JWT no contiene 'user_id'"}), 400

        # Ejecutar el scraping
        content = crawl_and_scrape(url, max_pages=10)

        # Guardar el resultado como archivo de contexto del propietario
        filename = f"{propietario_id}_context.txt"
        save_to_txt(content, filename)

        return jsonify({
            "message": "Contenido guardado con éxito",
            "archivo": filename,
            "propietario_id": propietario_id
        }), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expirado"}), 401
    except jwt.InvalidTokenError as e:
        return jsonify({"error": f"Token inválido: {str(e)}"}), 401
    except Exception as e:
        current_app.logger.error(f"❌ Error en /scrape: {e}", exc_info=True)
        return jsonify({"error": f"Error interno: {str(e)}"}), 500


@routes_bp.route('/contextos', methods=['GET'])
def listar_contextos():
    import os
    import re

    token_header = request.headers.get("Authorization")
    if not token_header:
        return jsonify({"error": "Token JWT requerido"}), 401

    token = token_header.split(" ")[1] if token_header.startswith("Bearer ") else token_header

    try:
        decoded = jwt.decode(token, current_app.config["JWT_SECRET_KEY"], algorithms=["HS256"])
        propietario_id = decoded.get("user_id")
        if not propietario_id:
            return jsonify({"error": "JWT no contiene 'user_id'"}), 400

        context_dir = current_app.config.get("CONTEXTS_DIR", "/chatbotv2025/myapp/context/")
        if not os.path.exists(context_dir):
            return jsonify({"contextos": []})

        archivos = os.listdir(context_dir)
        contextos_usuario = []

        for archivo in archivos:
            if archivo.startswith(f"{propietario_id}_") and archivo.endswith(".txt"):
                nombre = re.sub(f"^{propietario_id}_", "", archivo).replace(".txt", "")
                contextos_usuario.append({
                    "archivo": archivo,
                    "nombre": nombre
                })

        return jsonify({"contextos": contextos_usuario}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expirado"}), 401
    except jwt.InvalidTokenError as e:
        return jsonify({"error": f"Token inválido: {str(e)}"}), 401
    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500
