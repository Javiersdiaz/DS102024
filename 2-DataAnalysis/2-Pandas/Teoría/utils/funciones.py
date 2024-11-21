import pandas as pd

class Display(object):
    """Mostrar la representación HTML de varios objetos"""
    template = """<div style="float: left; padding: 10px;">
    <p style='font-family:"Courier New", Courier, monospace'>{0}</p>{1}
    </div>"""
    
    def __init__(self, *args, context=None):
        # Si no se pasa un contexto, se usa el entorno local por defecto
        if context is None:
            context = globals()
        
        # Convertir los nombres de variables a objetos reales si son cadenas
        self.args = [eval(a, context) if isinstance(a, str) else a for a in args]
        self.arg_names = [a if isinstance(a, str) else repr(a) for a in args]
        
    def _repr_html_(self):
        return '\n'.join(self.template.format(name, obj._repr_html_())
                         for name, obj in zip(self.arg_names, self.args))
    
    def __repr__(self):
        return '\n\n'.join(name + '\n' + repr(obj)
                           for name, obj in zip(self.arg_names, self.args))

def make_df(cols:str, ind:list[int]) -> pd.DataFrame:
    """Crear rápidamente un DataFrame"""
    data = {c: [str(c) + str(i) for i in ind]
            for c in cols}
    return pd.DataFrame(data, ind)

import numpy as np
from scipy import stats

def analisis_estadistico(datos):
    """
    Realiza un análisis estadístico de una lista de números.
    
    Parámetros:
        datos (list o array-like): Lista de números para analizar.
    
    Devuelve:
        dict: Diccionario con las estadísticas calculadas.
    """
    if not datos:
        raise ValueError("La lista de datos no puede estar vacía.")
    
    analisis = {
        "media": np.mean(datos),
        "mediana": np.median(datos),
        "moda": stats.mode(datos, keepdims=False)[0],
        "desviacion_estandar": np.std(datos, ddof=1),  # ddof=1 para la muestra
        "conteo": len(datos),
        "maximo": np.max(datos),
        "minimo": np.min(datos),
        "percentil_25": np.percentile(datos, 25),
        "percentil_50": np.percentile(datos, 50),  # Equivalente a la mediana
        "percentil_75": np.percentile(datos, 75),
    }
    
    return analisis

# Ejemplo de uso
datos = [1, 2, 2, 3, 4, 5, 5, 5, 6, 7]
resultado = analisis_estadistico(datos)
print(resultado)



import pandas as pd
import numpy as np

def categorizar_columnas(df):
    """
    Clasifica las columnas de un DataFrame según su tipo de datos en categorías:
    Cualitativos Nominales, Cualitativos Ordinales, Cuantitativos Discretos,
    Cuantitativos Continuos, Binarios e Índices.
    
    Parámetros:
        df (pd.DataFrame): DataFrame a analizar.
    
    Devuelve:
        dict: Diccionario con listas de nombres de columnas categorizadas.
    """
    categorias = {
        "cualitativos_nominales": [],
        "cualitativos_ordinales": [],
        "cuantitativos_discretos": [],
        "cuantitativos_continuos": [],
        "binarios": [],
        "indices": []
    }
    
    # Verificar índices
    if isinstance(df.index, pd.RangeIndex) or isinstance(df.index, pd.Int64Index):
        categorias["indices"].append("index")
    elif isinstance(df.index, pd.MultiIndex):
        categorias["indices"].extend(df.index.names)
    
    for col in df.columns:
        serie = df[col]
        
        # Clasificar cualitativos
        if pd.api.types.is_categorical_dtype(serie) or serie.dtype == "object":
            unique_values = serie.nunique()
            if unique_values == 2:
                categorias["binarios"].append(col)
            elif serie.cat.ordered if pd.api.types.is_categorical_dtype(serie) else False:
                categorias["cualitativos_ordinales"].append(col)
            else:
                categorias["cualitativos_nominales"].append(col)
        
        # Clasificar cuantitativos
        elif pd.api.types.is_numeric_dtype(serie):
            if np.issubdtype(serie.dtype, np.integer):
                if serie.nunique() == 2:
                    categorias["binarios"].append(col)
                else:
                    categorias["cuantitativos_discretos"].append(col)
            elif np.issubdtype(serie.dtype, np.floating):
                categorias["cuantitativos_continuos"].append(col)
        
        # Si no se clasifica
        else:
            categorias["cualitativos_nominales"].append(col)
    
    return categorias