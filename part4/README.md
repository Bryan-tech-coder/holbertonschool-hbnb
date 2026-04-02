# Part 4 - Simple Web Client (HBnB)

Instrucciones (en español) para ejecutar y dejar la interfaz lista para evaluación:

Requisitos
- Python 3
- Tu API (part3) corriendo en http://127.0.0.1:5002
- `flask-cors` instalado en el entorno del API (se añadió en part3/app/__init__.py)

1) Descargar una imagen libre (Unsplash) y guardarla en `part4/images/hbnb.jpg`

Puedes usar este comando para descargar una imagen gratuita (ejemplo de Unsplash):

```bash
mkdir -p part4/images
curl -L -o part4/images/hbnb.jpg "https://images.unsplash.com/photo-1505691723518-36a0a1f0c4b6?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
```

(La URL anterior apunta a una imagen de muestra de Unsplash; verifica la licencia antes de usarla en producción.)

2) Servir el frontend (evitar abrir archivos con file://)

```bash
# desde la raíz del repo
python -m http.server --directory part4 8000
# Abrir en el navegador:
# http://localhost:8000
```

3) Ejecutar el API (part3)

Asegúrate de activar tu entorno virtual y ejecutar la app API (ejemplo):

```bash
# desde la carpeta part3
source ../.venv/bin/activate  # adapta a tu entorno
python run.py
```

4) Verificar comportamiento esperado
- Visitar `/login.html`, iniciar sesión con credenciales válidas.
- Tras login se guardará un `token` en cookie y redirige a `index.html`.
- `index.html` muestra la lista de lugares (debes tener el API corriendo).
- Usa el filtro de precio para probar el filtrado cliente-side.
- Abre `place.html?id=<PLACE_ID>` para ver detalles; si estás autenticado, verás el formulario de reviews.

Notas importantes
- Ya se habilitó CORS en `part3/app/__init__.py` para `"/api/*"` (modo desarrollo). En producción restringe orígenes.
- El código del frontend (`part4/scripts.js`) contiene comentarios en español para explicar cada función.

Si quieres, puedo:
- Añadir imágenes por cada `place` y mostrarlas automáticamente si el API las provee.
- Mejorar la UI y mensajes de error.
- Preparar un commit y un `README` más detallado para entregar.

Instrucciones para preparar un commit listo para entrega:

```bash
# Añadir cambios
git add part4/
# Commit con mensaje corto y claro
git commit -m "part4: cliente web mejorado - logo, hero, imágenes resueltas desde API, estilos"
# (opcional) crear branch y push
git checkout -b feat/part4-frontend
git push origin feat/part4-frontend
```

