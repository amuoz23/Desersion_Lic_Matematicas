import pandas as pd
import numpy as np


def verificar_columna_numerica(df, columna, verbose=True):
    """
    Verifica si una columna contiene solo datos numéricos.
    
    Args:
        df (pd.DataFrame): DataFrame que contiene los datos
        columna (str): Nombre de la columna a verificar
        verbose (bool): Si True, muestra información detallada
    
    Returns:
        dict: Diccionario con información sobre la verificación:
            - 'es_numerica': bool, True si todos los datos son numéricos
            - 'tipo_dato': tipo de dato de la columna
            - 'valores_no_numericos': lista de valores no numéricos encontrados
            - 'cantidad_no_numericos': cantidad de valores no numéricos
            - 'indices_no_numericos': índices donde están los valores no numéricos
    
    Raises:
        ValueError: Si la columna no existe en el DataFrame
    """
    
    # Verificar que la columna existe
    if columna not in df.columns:
        raise ValueError(f"La columna '{columna}' no existe en el DataFrame. "
                        f"Columnas disponibles: {list(df.columns)}")
    
    # Obtener la serie
    serie = df[columna]
    
    # Información inicial
    resultado = {
        'es_numerica': False,
        'tipo_dato': str(serie.dtype),
        'valores_no_numericos': [],
        'cantidad_no_numericos': 0,
        'indices_no_numericos': [],
        'total_valores': len(serie),
        'valores_nulos': serie.isnull().sum(),
        'indices_nulos': serie[serie.isnull()].index.tolist()
    }
    
    # Si el tipo ya es numérico (int, float)
    if pd.api.types.is_numeric_dtype(serie):
        resultado['es_numerica'] = True
        
        if verbose:
            print(f"✓ La columna '{columna}' es numérica")
            print(f"  - Tipo de dato: {resultado['tipo_dato']}")
            print(f"  - Total de valores: {resultado['total_valores']}")
            print(f"  - Valores nulos: {resultado['valores_nulos']}")
        
        return resultado
    
    # Si no es numérico, intentar convertir y encontrar problemas
    valores_no_numericos = []
    indices_no_numericos = []
    
    for idx, valor in serie.items():
        # Ignorar valores nulos (NaN, None)
        if pd.isnull(valor):
            continue
        
        # Intentar convertir a número
        try:
            # Limpiar espacios si es string
            if isinstance(valor, str):
                valor = valor.strip()
            
            # Intentar conversión a float
            float(valor)
        except (ValueError, TypeError):
            valores_no_numericos.append(valor)
            indices_no_numericos.append(idx)
    
    # Actualizar resultado
    resultado['valores_no_numericos'] = valores_no_numericos
    resultado['cantidad_no_numericos'] = len(valores_no_numericos)
    resultado['indices_no_numericos'] = indices_no_numericos
    resultado['es_numerica'] = len(valores_no_numericos) == 0
    
    # Mostrar información si verbose está activado
    if verbose:
        if resultado['es_numerica']:
            print(f"✓ La columna '{columna}' contiene solo datos numéricos")
            print(f"  - Tipo de dato actual: {resultado['tipo_dato']} (puede convertirse a numérico)")
            print(f"  - Total de valores: {resultado['total_valores']}")
            print(f"  - Valores nulos: {resultado['valores_nulos']}")
            
            # Mostrar detalles de valores nulos si existen
            if resultado['valores_nulos'] > 0:
                print(f"\n{'='*70}")
                print(f"DETALLE DE VALORES NULOS:")
                print(f"{'='*70}")
                print(f"Índices con valores nulos: {resultado['indices_nulos']}")
                print(f"{'='*70}")
        else:
            print(f"✗ La columna '{columna}' NO es completamente numérica")
            print(f"  - Tipo de dato: {resultado['tipo_dato']}")
            print(f"  - Total de valores: {resultado['total_valores']}")
            print(f"  - Valores nulos: {resultado['valores_nulos']}")
            print(f"  - Valores no numéricos encontrados: {resultado['cantidad_no_numericos']}")
            
            # Mostrar detalles de valores nulos si existen
            if resultado['valores_nulos'] > 0:
                print(f"\n{'='*70}")
                print(f"DETALLE DE VALORES NULOS:")
                print(f"{'='*70}")
                print(f"Índices con valores nulos: {resultado['indices_nulos']}")
                print(f"{'='*70}")
            
            # Mostrar detalles de valores no numéricos
            print(f"\n{'='*70}")
            print(f"DETALLE DE VALORES NO NUMÉRICOS:")
            print(f"{'='*70}")
            print(f"{'Índice':<10} {'Valor':<30} {'Tipo':<20}")
            print(f"{'-'*70}")
            
            # Mostrar TODOS los valores no numéricos
            for idx, val in zip(indices_no_numericos, valores_no_numericos):
                # Truncar valores muy largos
                val_str = str(val)[:27] + '...' if len(str(val)) > 30 else str(val)
                tipo_val = type(val).__name__
                print(f"{idx:<10} {val_str:<30} {tipo_val:<20}")
            
            print(f"{'='*70}")
    
    return resultado


def verificar_multiples_columnas(df, columnas=None, verbose=True):
    """
    Verifica múltiples columnas del DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame a verificar
        columnas (list): Lista de columnas a verificar. Si es None, verifica todas
        verbose (bool): Si True, muestra información detallada
    
    Returns:
        dict: Diccionario con resultados por columna
    """
    if columnas is None:
        columnas = df.columns.tolist()
    
    resultados = {}
    
    if verbose:
        print("=" * 60)
        print("VERIFICACIÓN DE COLUMNAS NUMÉRICAS")
        print("=" * 60 + "\n")
    
    for col in columnas:
        if verbose:
            print(f"\n--- Columna: {col} ---")
        
        resultado = verificar_columna_numerica(df, col, verbose=verbose)
        resultados[col] = resultado
    
    # Resumen final
    if verbose:
        print("\n" + "=" * 60)
        print("RESUMEN")
        print("=" * 60)
        
        numericas = [col for col, res in resultados.items() if res['es_numerica']]
        no_numericas = [col for col, res in resultados.items() if not res['es_numerica']]
        
        print(f"\n✓ Columnas numéricas ({len(numericas)}):")
        for col in numericas:
            print(f"  - {col}")
        
        if no_numericas:
            print(f"\n✗ Columnas NO numéricas ({len(no_numericas)}):")
            for col in no_numericas:
                cant = resultados[col]['cantidad_no_numericos']
                print(f"  - {col} ({cant} valores problemáticos)")
    
    return resultados


def verificar_multiples_columnas(df, columnas=None, verbose=True):
    """
    Verifica múltiples columnas del DataFrame.
    """
    if columnas is None:
        columnas = df.columns.tolist()
    
    resultados = {}
    
    if verbose:
        print("=" * 60)
        print("VERIFICACIÓN DE COLUMNAS NUMÉRICAS")
        print("=" * 60 + "\n")
    
    for col in columnas:
        if verbose:
            print(f"\n--- Columna: {col} ---")
        
        resultado = verificar_columna_numerica(df, col, verbose=verbose)
        resultados[col] = resultado
    
    # Resumen final
    if verbose:
        print("\n" + "=" * 60)
        print("RESUMEN")
        print("=" * 60)
        
        numericas = [col for col, res in resultados.items() if res['es_numerica']]
        no_numericas = [col for col, res in resultados.items() if not res['es_numerica']]
        
        print(f"\n✓ Columnas numéricas ({len(numericas)}):")
        for col in numericas:
            print(f"  - {col}")
        
        if no_numericas:
            print(f"\n✗ Columnas NO numéricas ({len(no_numericas)}):")
            for col in no_numericas:
                cant = resultados[col]['cantidad_no_numericos']
                print(f"  - {col} ({cant} valores problemáticos)")
    
    return resultados



