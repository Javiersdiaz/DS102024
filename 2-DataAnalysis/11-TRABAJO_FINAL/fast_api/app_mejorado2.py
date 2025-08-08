import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Cargar modelo NLP
modelo_nlp = SentenceTransformer('distiluse-base-multilingual-cased-v2')

# Configuración de la app
st.set_page_config(page_title="¿Qué hacer con los niños?", page_icon="🎈")
st.title("🎈 ¿Qué hacer con los niños?")
st.subheader("Encuentra actividades inclusivas y divertidas para tu familia")

# Cargar datos
data = pd.read_csv('actividades_familiares_españa_v3.csv')

# Limpiar columnas
data['necesidad_especial'] = data['necesidad_especial'].fillna('No especificado')
data['precio'] = data['precio'].fillna('No especificado')
data['categoria'] = data['categoria'].fillna('Sin categoría')
data['descripcion'] = data['descripcion'].fillna('')

# Panel lateral (filtros)
st.sidebar.header("💬 Tus preferencias")
edad_usuario = st.sidebar.slider('Edad del niño/a', 1, 16, 6)
ciudad_usuario = st.sidebar.selectbox('Ubicación', options=data['ubicacion'].dropna().unique())

opciones_diversidad = data['necesidad_especial'].dropna().unique()
diversidad_funcional = st.sidebar.selectbox('Diversidad funcional', options=['Todos'] + list(opciones_diversidad))

opciones_precio = data['precio'].dropna().unique()
filtro_precio = st.sidebar.selectbox('Tipo de precio', options=['Todos'] + list(opciones_precio))

opciones_categoria = data['categoria'].dropna().unique()
filtro_categoria = st.sidebar.selectbox('Categoría de actividad', options=['Todas'] + list(opciones_categoria))

consulta_texto = st.sidebar.text_input('Describe qué te gustaría hacer:', 'Actividad tranquila en casa')

# Botón de búsqueda
if st.sidebar.button('🔍 Buscar actividades'):
    # Aplicar filtros
    filtro = (data['edad_minima'] <= edad_usuario) & (data['ubicacion'] == ciudad_usuario)

    if diversidad_funcional != 'Todos':
        filtro &= data['necesidad_especial'].str.lower().str.contains(diversidad_funcional.lower(), na=False)

    if filtro_precio != 'Todos':
        filtro &= data['precio'].str.lower().str.contains(filtro_precio.lower(), na=False)

    if filtro_categoria != 'Todas':
        filtro &= (data['categoria'] == filtro_categoria)

    actividades_filtradas = data[filtro].reset_index(drop=True)

    if actividades_filtradas.empty:
        st.error("⚠️ No se encontraron actividades que cumplan con tus criterios. Prueba cambiando algún filtro.")
    else:
        # Calcular similitud semántica
        descripciones = actividades_filtradas['descripcion'].tolist()
        embeddings_actividades = modelo_nlp.encode(descripciones, convert_to_tensor=True)
        embedding_consulta = modelo_nlp.encode([consulta_texto], convert_to_tensor=True)

        similitudes = cosine_similarity(embedding_consulta, embeddings_actividades)[0]
        actividades_filtradas['similitud'] = similitudes

        # Ordenar por similitud y eliminar duplicados
        resultados = actividades_filtradas.sort_values(by='similitud', ascending=False)
        resultados_unicos = resultados.drop_duplicates(subset='nombre_evento').reset_index(drop=True)

        # Seleccionar top 3 actividades distintas
        top_3 = resultados_unicos.head(3)

        # Mostrar actividad recomendada con descripción
        actividad_recomendada = top_3.iloc[0]
        st.success(f"🎯 Actividad recomendada: {actividad_recomendada['nombre_evento']}")
        st.markdown(f"📝 *{actividad_recomendada['descripcion']}*")

        # Mostrar otras dos sugerencias si existen
        if len(top_3) > 1:
            st.write("📋 Otras opciones que podrían interesarte:")
            st.dataframe(top_3.iloc[1:][['nombre_evento', 'categoria', 'descripcion', 'precio', 'necesidad_especial']])
        else:
            st.info("Solo encontramos una actividad que se ajuste bien a tu búsqueda.")
