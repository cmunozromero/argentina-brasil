import os
import requests

# Configura tu clave API de Chatly
CHATLY_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI4Y2UyNjhkNC1kNjMyLTQ3YjEtYWE5NC0zYjc2ZmMzNDljODciLCJpbnRlZ3JpdHlDaGVjayI6ZmFsc2UsImJhc2VVcmwiOiIiLCJwcm9kdWN0VmFsaURGb3IiOiJDSEFUTFkiLCJpc0FkbWluIjpmYWxzZSwiaWF0IjoxNzY1NjE2MzExLCJleHAiOjE3NjU2Mzc5MTEsInN1YiI6IjhjZTI2OGQ0LWQ2MzItNDdiMS1hYTk0LTNiNzZmYzM0OWM4NyIsImp0aSI6IjgyNWExZmJmLWM1ZDMtNDFhNS1iYTc4LWJkYjNjM2M5N2IxZiJ9.bWplMfnFDk3224z8FcMix3ZIFAAqfsZQrbQp-U4_W-4'  # Cambia a tu clave API de Chatly

# Leer imágenes desde carpetas locales
def get_photos_from_local_directory(base_directory):
    photos_by_day = {}
    for day_folder in os.listdir(base_directory):
        day_path = os.path.join(base_directory, day_folder)
        if os.path.isdir(day_path):
            photos = []
            for file_name in os.listdir(day_path):
                if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):  # Filtrar tipos de archivo de imagen
                    photo_path = os.path.join(day_path, file_name)
                    photos.append(photo_path)
            if photos:
                photos_by_day[day_folder] = photos
    return photos_by_day

# Generar contenido HTML directamente con la API de Chatly
def generate_html_content_chatly(day, text, photos):
    api_url = 'https://api.chatly.com/v1/generate'  # Cambia esto a la URL correcta de Chatly
    headers = {
        'Authorization': f'Bearer {CHATLY_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    # Crear un prompt para el modelo Claude-Sonnet
    prompt = f"""Genera una página HTML completa lista para guardar como dia{day}.html para mi diario de viaje con un diseño visual moderno y atractivo.
        - Contenido: utiliza este texto: "{text}".
        - Imágenes: {', '.join(photos) if photos else 'sin imágenes'} (usa estos paths como placeholders; déjalos tal cual para que yo los reemplace).

        Características del diseño:
        - Diseño moderno con gradientes, sombras y animaciones.
        - Header con título del día, subtítulo y ubicación.
        - Secciones bien organizadas con iconos temáticos.
        - Cajas destacadas (highlight-box) para información importante (vuelos, restaurantes, etc.).
        - Story-box para anécdotas especiales.
        - Grid de fotos cuando haya múltiples imágenes; fotos dentro de wrappers tipo "photo-wrapper" con efecto polaroid (rotación ligera).
        - Citas destacadas en "quote-box".
        - Footer con información del viaje.
        - Navegación flotante en la esquina inferior derecha con flechas (← 🏠 →) y enlaces a día anterior, inicio y siguiente (usa '#' como placeholder).
        - Responsive y optimizado para impresión.
        - Fuentes: Playfair Display para títulos, Lato para texto (incluye enlaces a Google Fonts).
        - Paleta de colores acorde al destino del día (elige colores adecuados según el día).

        Estructura requerida:
        - Header con gradiente temático.
        - Secciones divididas por decorative-line.
        - Texto justificado y bien espaciado.
        - Highlight-box para datos importantes.
        - Story-box para anécdotas divertidas.
        - Grid de fotos cuando corresponda.
        - Quote al final con reflexión del día.

        Instrucciones adicionales:
        - Marca claramente en el HTML los lugares donde debo reemplazar las imágenes (por ejemplo con atributos data-placeholder o comentarios).
        - Asegúrate de que el HTML incluya todo el CSS necesario (en la cabecera dentro de <style>) y que sea listo para usar.
        - Incluye los enlaces a Google Fonts para Playfair Display y Lato.
        - Usa clases descriptivas (header, highlight-box, story-box, photo-wrapper, decorative-line, quote-box, floating-nav).

        Salida esperada: devuelve exclusivamente el código HTML completo listo para guardar como dia{day}.html. No incluyas explicaciones ni texto adicional fuera del HTML."""
    
    response = requests.post(api_url, headers=headers, json={'prompt': prompt, 'model': 'claude-sonnet'})
    if response.status_code == 200:
        response_data = response.json()
        return response_data['generated_text']  # Ajusta esto según la respuesta de Chatly
    else:
        print(f"Error al generar contenido para {day}: {response.status_code} - {response.text}")
        return f"<h2>{day}</h2><p>No se pudo generar contenido.</p>"

# Guardar el contenido HTML en un archivo
def save_html_file(day, html_content):
    # Hacer que el directorio de salida sea relativo al directorio donde está este archivo Python
    script_dir = os.path.abspath(os.path.dirname(__file__))
    directory = os.path.join(script_dir, 'ia', str(day), 'html')
    os.makedirs(directory, exist_ok=True)  # Crea el directorio si no existe
    file_path = os.path.join(directory, f'{day}.html')
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

# Función principal
def main():
    # Hacer que la ruta base sea relativa al directorio donde está este archivo Python
    script_dir = os.path.abspath(os.path.dirname(__file__))
    base_directory = os.path.join(script_dir, 'AI_GENERATION_FOTOS')  # Cambiado a ruta relativa
    photos_by_day = get_photos_from_local_directory(base_directory)

    # Ejemplo de textos para los días
    texts = {
        '5': 'Este dia teniamos libre por la mañana hasta las 15:00 de la tarde que nos venian a recoger para el avion a el calafate. María vio una ruta de senderismo hasta el lago esmeralda que era muy famoso. Fuimos con un uber, pasamos el control policial de ushuaia y lo pararon para preguntarle por el carné, era un coche de los que no tenian matriculas fisicas. Nos estuvo contando que estaban haciendo un cambio en las matriculas para que la matricula se heredase entre coches. Cuando nos dejo en el comienzo de la ruta nos extrañó no ver a nadie en el parking, y nos dijo el chico que la gente solia empezar la ruta mas alla de las 9 de la mañana y eran las 8 y poco. El comienzo de la ruta estaba helado y no llevamos crampones, empezaba bien. No solo con eso, despues de pasar el primer tramo empezamos a ver qué está todo embarrado y tenemos que ir sorteandolo. No nos rendimos porque confiamos en que mejoraría, y asi fue. Aunque aun quedaba un rato de barro y hielo luego todo mejoró, vinieron una vistas increibles y lo disfrutamos mushisimo, llegamos al lago despues de 2 horas de caminata, estaba congelado y nos estuvimos haciendo fotos. Nos comimos el salchicion y las regañas que noa compramos el dia anterior y nos volvimos. Pillamos un taxi de vuelta y nos dejo en el hotel. Cuando llegamos al hotel nos entro hambre y nos pedimos una hamburgesa y unos espaguettis bolognesa, ibamos buscando una sopa de pollo o algo por El Estilo y nos entro hambre. A las 14.00 nos pasaban a buscar para coger el vuelo a el calafate. Teniamos 1 hora de de vuelo y fue todo bien. Cuando llegamos estabamos un poco perdidos porque no nos estaban esperando en la salida, tardaron unos 15 minutos en llegar y nos llevaron al hotel. Hasta ahora el mejor hotel que hemos tenido, Alto Calafate, con spa incluido y una sala de juegos. Nos cambiamos y bajamos al spa, yo ese dia estaba empezando a ponerme malo y tenia muchas ganas de relajarme en el spa y Maria me hizo una ahogadilla mientras estaba flotando y me entró agua por la nariz, cosa que detesto y me enfadé, luego le tire yo agua a los ojos de lama manera por estar enfadado y le hice una ahogadilla a ella y discutimos sobre mi reaccion. Que me sale ser vengativo y quiero dejar de ser asi. Luego cenamos ahi en el hotel, ya que quedaba lejos del pueblo, me pedi un estofado de cordero muy bueno y maria un salmon a la plancha, para ir a lo seguro, pero sabia mucho a limón... Pedimos un launch box para el dia siguiente de un bocata de milanesa.',
    }

    for day, text in texts.items():
        photos = photos_by_day.get(day, [])
        html_content = generate_html_content_chatly(day, text, photos)
        save_html_file(day, html_content)
    
    print("Diarios generados en la estructura de carpetas.")

if __name__ == "__main__":
    main()