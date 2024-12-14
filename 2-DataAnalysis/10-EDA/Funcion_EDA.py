class DataAnalyzer:
    """
    Clase para realizar análisis exploratorio y visualización de datos.
    """
    def __init__(self):
        """
        Inicializa el objeto DataAnalyzer.
        """
        self.data = None

    def load_data(self, path: str) -> None:
        """
        Carga los datos desde un archivo CSV o Excel.
        
        Args:
            path (str): Ruta del archivo.
        """
        try:
            if path.endswith('.csv'):
                self.data = pd.read_csv(path)
            elif path.endswith('.xlsx') or path.endswith('.xls'):
                self.data = pd.read_excel(path)
            else:
                raise ValueError("El formato de archivo no es compatible. Use CSV o Excel.")
            print("Datos cargados exitosamente.")
        except Exception as e:
            print(f"Error al cargar los datos: {e}")

    def get_info(self, visual: bool = True) -> None:
        """
        Muestra información básica del dataset de manera visual usando pandas.
        
        Args:
            visual (bool): Si es True, muestra la información de forma visual.
        """
        if self.data is None:
            print("No hay datos cargados. Use el método load_data primero.")
            return

        # Información básica
        dimensiones = pd.DataFrame({
            "Descripción": ["Filas", "Columnas"],
            "Valor": [self.data.shape[0], self.data.shape[1]]
        })

        tipos_datos = pd.DataFrame({
            "Columna": self.data.columns,
            "Tipo": self.data.dtypes.values
        })

        memoria = pd.DataFrame({
            "Descripción": ["Memoria utilizada (MB)"],
            "Valor": [round(self.data.memory_usage(deep=True).sum() / 1_048_576, 2)]
        })

        resumen_estadistico = self.data.describe(include='all').transpose()

        # Imprimir información visualmente
        if visual:
            print("\nDimensiones:")
            display(dimensiones)
            
            print("\nTipos de datos:")
            display(tipos_datos)
            
            print("\nMemoria utilizada:")
            display(memoria)
            
            print("\nResumen estadístico:")
            display(resumen_estadistico)
        else:
            # Alternativa en caso de querer obtener los datos en formato texto
            print("Dimensiones:")
            print(dimensiones.to_string(index=False))
            
            print("\nTipos de datos:")
            print(tipos_datos.to_string(index=False))
            
            print("\nMemoria utilizada:")
            print(memoria.to_string(index=False))
            
            print("\nResumen estadístico:")
            print(resumen_estadistico.to_string())

    def describe_numeric(self, visual: bool = True) -> pd.DataFrame:
        """
        Análisis estadístico detallado de variables numéricas.

        Args:
            visual (bool): Si es True, muestra los resultados como tabla.

        Retorna:
            pd.DataFrame: Estadísticas como media, mediana, moda, desviación estándar,
                          cuartiles, asimetría y curtosis.
        """
        if self.data is None:
            print("No hay datos cargados. Use el método load_data primero.")
            return None

        numeric_data = self.data.select_dtypes(include=['number'])
        if numeric_data.empty:
            print("No hay variables numéricas en el dataset.")
            return None

        analysis = pd.DataFrame({
            "Media": numeric_data.mean(),
            "Mediana": numeric_data.median(),
            "Moda": numeric_data.mode().iloc[0],
            "Desviación Estándar": numeric_data.std(),
            "Cuartil 25%": numeric_data.quantile(0.25),
            "Cuartil 75%": numeric_data.quantile(0.75),
            "Asimetría": numeric_data.skew(),
            "Curtosis": numeric_data.kurt()
        })

        if visual:
            print("\nAnálisis Estadístico de Variables Numéricas:")
            display(analysis)
        return analysis