# 🟥 TAPPX 🟥


Este programa compara artículos y videos basándose en el contenido de texto y las categorías IAB (Interactive Advertising Bureau). El objetivo es generar un archivo JSON con los resultados de las comparaciones, donde se asigna a cada artículo un ranking de los tres videos más similares.

# Requisitos 🛠
  - Python 3.7 o superior 🐍
  - Librerías: rake_nltk, nltk, pandas, spacy, sklearn 🤖
  - Ejecutar el siguiente comando para instalar los requisitos:
  
  ```
  pip install -r requirements.txt
  ```
  
# Funcionamiento ⚙️

El programa realiza las siguientes tareas:
  1.  Limpia el texto de los artículos y videos eliminando etiquetas Jinja2, puntuación, números y palabras vacías (stop words), y convierte las palabras a sus formas base (lemmas) usando la librería spaCy. `remove_jinja2_tags()` `clean_text()`
  2.  Extrae palabras clave del texto utilizando Rake. `get_keywords2()`
  3.  Compara las categorías IAB de los artículos y videos. `compare_topics()`
  4.  Calcula la similitud del coseno entre los textos y las palabras clave utilizando la función TfidfVectorizer de sklearn. `temp_comp()`
  5.  Combina las similitudes en un único puntaje y guarda el resultado en un diccionario.
  6.  Limpia los resultados manteniendo solo los tres videos con mayor puntuación para cada artículo.
  7.  Escribe los resultados en un archivo JSON llamado 'tappx.json'.

# Uso ✊🏽
  - Asegúrese de tener instaladas las dependencias necesarias (rake_nltk, nltk, pandas, spacy, sklearn).
  - Coloque los archivos 'articles.json' y 'videos.json' en el mismo directorio que el script.
  - Ejecute el script con el comando python script.py.
  - Se creará un archivo 'tappx.json' en el directorio con los resultados de las comparaciones.

# Definicion del score 💥

Como se han utilizado diferentes tipos de similitudes, se realiza un cálculo para ponderar cada una de los scores, para cada articulo se encontraran todas las puntuaciones y que, si se quisiera, nos mostrarian el top 3, top 5 o top x. Cuánto mayor sea el score, mayor similitud habrá entre el articulo y los textos.

Al final, el programa crea un archivo JSON que contiene los tres videos más similares a cada artículo según la similitud del coseno y las categorías IAB.
