import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os

# --- Resumidor con GPT (OpenAI) ---
def resumir_texto_con_gpt(texto_largo, openai_client, max_tokens=600):
    prompt = (
        "Resume el siguiente texto conservando los datos, hechos y descripciones clave, "
        "de forma clara y útil, sin perder contexto relevante. Limítalo a máximo 4-5 párrafos breves:\n\n"
        f"{texto_largo}\n\nResumen:"
    )
    try:
        response = openai_client.chat.completions.create(
            model=os.getenv('OPEN_API_MODEL', 'gpt-3.5-turbo'),
            messages=[
                {"role": "system", "content": "Eres un experto en resumen de textos web."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.2
        )
        resumen = response.choices[0].message.content.strip()
        return resumen
    except Exception as e:
        print(f"❌ Error resumiendo con OpenAI: {e}")
        return texto_largo[:max_tokens * 8]

# --- Función para limitar texto bruto ---
def limitar_texto(texto, max_chars=5000):
    return texto[:max_chars]

# --- Guardar resultado como archivo ---
def save_to_txt(text, filename="output.txt", directory="/chatbotv2025/myapp/context/"):
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)

# --- Scraper optimizado ---
def scrape_url_to_text(url, max_paragraphs=20):
    response = requests.get(url, timeout=20)
    soup = BeautifulSoup(response.content, "html.parser")
    for tag in soup(["script", "style", "noscript", "footer", "nav", "form", "input"]):
        tag.decompose()
    lines, seen = [], set()
    # Títulos relevantes
    for tag in soup.find_all(["h1", "h2", "h3"]):
        text = tag.get_text().strip()
        if text and text not in seen:
            lines.append(f"## {text.upper()} ##")
            seen.add(text)
    # Primeros párrafos principales
    for p in soup.find_all("p")[:max_paragraphs]:
        text = p.get_text().strip()
        if text and text not in seen:
            lines.append(text)
            seen.add(text)
    return '\n'.join(lines)

# --- Crawling + Scraping + Resumen GPT (si hace falta) ---
def crawl_and_scrape(url, max_pages=20, max_chars=16500, openai_client=None):
    visited, to_visit, domain = set(), [url], urlparse(url).netloc
    full_content = []
    while to_visit and len(visited) < max_pages:
        current_url = to_visit.pop(0)
        if current_url in visited: continue
        try:
            print(f"🔍 Visitando: {current_url}")
            formatted_text = scrape_url_to_text(current_url)
            full_content.append(f"---- {current_url} ----\n{formatted_text}")
            visited.add(current_url)
            # Busca más links internos (limitados)
            response = requests.get(current_url, timeout=10)
            soup = BeautifulSoup(response.content, "html.parser")
            for tag in soup(["script", "style", "noscript", "footer", "nav"]):
                tag.decompose()
            for link in soup.find_all("a", href=True):
                absolute_url = urljoin(current_url, link["href"])
                parsed = urlparse(absolute_url)
                if parsed.netloc == domain and absolute_url not in visited and absolute_url.startswith("http"):
                    to_visit.append(absolute_url)
        except Exception as e:
            print(f"⚠️ Error al visitar {current_url}: {e}")

    result_text = "\n\n".join(full_content)
    # Limita en bruto por si acaso
    if len(result_text) > max_chars:
        print(f"⚠️ Texto excede {max_chars} caracteres. Resumiendo con GPT...")
        if openai_client:
            result_text = resumir_texto_con_gpt(result_text, openai_client, max_tokens=700)
        else:
            result_text = limitar_texto(result_text, max_chars)
    return result_text