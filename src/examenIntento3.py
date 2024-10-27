import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar el archivo CSV
df = pd.read_csv('./data/hotel_bookings.csv')

# Ver los tipos de columnas
print(df.dtypes)


# Verificar si hay duplicados
duplicados = df.duplicated()

# Contar el número de duplicados
num_duplicados = duplicados.sum()
print(f"Número de registros duplicados: {num_duplicados}")

# Si hay duplicados, puedes eliminarlos
if num_duplicados > 0:
    df = df.drop_duplicates()
   
# Imprimir la cantidad de registros que quedaron
num_registros_quedaron = len(df)
print(f"Número de registros que quedaron: {num_registros_quedaron}")


# Ajustar tipos de datos de acuerdo al diccionario proporcionado
df['hotel'] = df['hotel'].astype('object')
df['is_canceled'] = df['is_canceled'].astype('int64')
df['lead_time'] = df['lead_time'].astype('int64')
df['arrival_date_year'] = df['arrival_date_year'].astype('int64')
df['arrival_date_month'] = df['arrival_date_month'].astype('object')
df['arrival_date_week_number'] = df['arrival_date_week_number'].astype('int64')
df['arrival_date_day_of_month'] = df['arrival_date_day_of_month'].astype('int64')
df['stays_in_weekend_nights'] = df['stays_in_weekend_nights'].astype('int64')
df['stays_in_week_nights'] = df['stays_in_week_nights'].astype('int64')
df['adults'] = df['adults'].astype('int64')
df['children'] = df['children'].astype('float64')
df['babies'] = df['babies'].astype('int64')
df['meal'] = df['meal'].astype('object')
df['country'] = df['country'].astype('object')
df['market_segment'] = df['market_segment'].astype('object')
df['distribution_channel'] = df['distribution_channel'].astype('object')
df['is_repeated_guest'] = df['is_repeated_guest'].astype('int64')
df['previous_cancellations'] = df['previous_cancellations'].astype('int64')
df['previous_bookings_not_canceled'] = df['previous_bookings_not_canceled'].astype('int64')
df['reserved_room_type'] = df['reserved_room_type'].astype('object')
df['assigned_room_type'] = df['assigned_room_type'].astype('object')
df['booking_changes'] = df['booking_changes'].astype('int64')
df['deposit_type'] = df['deposit_type'].astype('object')
df['agent'] = df['agent'].astype('float64')
df['company'] = df['company'].astype('float64')
df['days_in_waiting_list'] = df['days_in_waiting_list'].astype('int64')
df['customer_type'] = df['customer_type'].astype('object')
df['adr'] = df['adr'].astype('float64')
df['required_car_parking_spaces'] = df['required_car_parking_spaces'].astype('int64')
df['total_of_special_requests'] = df['total_of_special_requests'].astype('int64')
df['reservation_status'] = df['reservation_status'].astype('object')
df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'], errors='coerce')

# Verificar los tipos de datos después de los ajustes
print("\nTipos de datos después de ajustes:")
print(df.dtypes)

# Listar columnas categóricas
columnas_categoricas = ['hotel', 'meal', 'country', 'market_segment', 
                         'distribution_channel', 'reserved_room_type', 
                         'assigned_room_type', 'deposit_type', 
                         'customer_type', 'reservation_status']

# Verificar valores únicos en las columnas categóricas
for col in columnas_categoricas:
    print(f"Valores únicos en la columna '{col}':")
    print(df[col].unique())

# Verificar formato de fecha
def verificar_fechas(df, fecha_col):
    fechas_invalidas = df[~df[fecha_col].dt.strftime('%Y-%m-%d').str.match(r'^\d{4}-\d{2}-\d{2}')]
    return fechas_invalidas

fechas_inconsistentes = verificar_fechas(df, 'reservation_status_date')
print("\nFechas inconsistentes en 'reservation_status_date':")
print(fechas_inconsistentes[['reservation_status_date']])

# Intentar convertir la columna 'reservation_status_date' al formato datetime
df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'], format='%Y-%m-%d', errors='coerce')

# Identificar fechas que no fueron convertidas correctamente
fechas_invalidas = df[df['reservation_status_date'].isna()]

if not fechas_invalidas.empty:
    print("\nFechas que no están en el formato 'YYYY-MM-DD':")
    print(fechas_invalidas[['reservation_status_date']])

    # Convertir en una fecha especifica si no estan en el formato date
    df['reservation_status_date'].fillna(pd.to_datetime('2015-01-01'), inplace=True)


# Verificar valores fuera de rango para columnas numéricas
def verificar_valores_fuera_de_rango(df):
    inconsistencias = {}
    if df['lead_time'].min() < 0:
        inconsistencias['lead_time'] = df[df['lead_time'] < 0]

    if df['adults'].min() < 0:
        inconsistencias['adults'] = df[df['adults'] < 0]

    if df['children'].min() < 0:
        inconsistencias['children'] = df[df['children'] < 0]

    if df['babies'].min() < 0:
        inconsistencias['babies'] = df[df['babies'] < 0]

    if df['stays_in_weekend_nights'].min() < 0:
        inconsistencias['stays_in_weekend_nights'] = df[df['stays_in_weekend_nights'] < 0]

    if df['stays_in_week_nights'].min() < 0:
        inconsistencias['stays_in_week_nights'] = df[df['stays_in_week_nights'] < 0]

    return inconsistencias

inconsistencias_numericas = verificar_valores_fuera_de_rango(df)
for col, registros in inconsistencias_numericas.items():
    print(f"\nRegistros inconsistentes en '{col}':")
    print(registros)

# Verificar valores categóricos
def verificar_valores_categoricos(df):
    categoricos = ['hotel', 'meal', 'country', 'market_segment', 'distribution_channel', 'customer_type', 'reservation_status']
    inconsistencias_categoricas = {}
    
    for col in categoricos:
        valores_unicos = df[col].unique()
        # Puedes definir valores esperados según el contexto
        print(f"\nValores únicos en '{col}': {valores_unicos}")
        
    return inconsistencias_categoricas

inconsistencias_categoricas = verificar_valores_categoricos(df)

# Conclusión
print("\nVerificación completada. Revisa las inconsistencias reportadas.")
    

# Identificar y contar valores faltantes por columna
valores_faltantes = df.isnull().sum()
print("Valores faltantes por columna:")
print(valores_faltantes[valores_faltantes > 0])

# Rellenar valores faltantes basados en el tipo de dato
for col in df.columns:
    if df[col].dtype == 'object':
        # Para columnas categóricas, rellenar con el valor más común o un marcador
        df[col].fillna(df[col].mode()[0], inplace=True)  # Rellenar con el valor más frecuente
    elif df[col].dtype == 'float64':
        # Para columnas numéricas (float), rellenar con la media
        df[col].fillna(df[col].mean(), inplace=True)
    elif df[col].dtype == 'int64':
        # Para columnas numéricas (int), rellenar con 0
        df[col].fillna(0, inplace=True)
    elif df[col].dtype == 'datetime64[ns]':
        # Para columnas de fecha, rellenar con una fecha específica (por ejemplo, 1 de enero de 1900)
        df[col].fillna(pd.to_datetime('1900-01-01'), inplace=True)

# Verificar nuevamente valores faltantes después de rellenar
valores_faltantes_post = df.isnull().sum()
print("\nValores faltantes después de rellenar:")
print(valores_faltantes_post[valores_faltantes_post > 0])

# Aquí, seleccionamos solo las columnas numéricas
numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns

# Convertir valores negativos a positivos
df[numerical_cols] = df[numerical_cols].abs()


# Definir límites razonables para cada columna
def corregir_datos_inusuales(df):
    # Establecer límites
    max_stays = 30  # Estancia máxima de 30 noches
    max_lead_time = 365  # Máximo lead time de un año
    max_adults = 10  # Máximo de adultos por reserva
    max_children = 5  # Máximo de niños por reserva
    max_babies = 5  # Máximo de bebés por reserva
    max_required_parking_spaces = 5  # Máximo de espacios de estacionamiento

    # Identificar y corregir valores anómalos
    df.loc[df['stays_in_weekend_nights'] > max_stays, 'stays_in_weekend_nights'] = None
    df.loc[df['stays_in_week_nights'] > max_stays, 'stays_in_week_nights'] = None
    df.loc[df['lead_time'] > max_lead_time, 'lead_time'] = None
    df.loc[df['adults'] > max_adults, 'adults'] = None
    df.loc[df['children'] > max_children, 'children'] = None
    df.loc[df['babies'] > max_babies, 'babies'] = None
    df.loc[df['required_car_parking_spaces'] > max_required_parking_spaces, 'required_car_parking_spaces'] = None

    return df

# Corregir datos inusuales
df = corregir_datos_inusuales(df)

# Verificar los valores corregidos
print("\nValores corregidos en el DataFrame:")
print(df.describe(include='all'))


# Configurar el estilo del histograma de hotel y anho
sns.set(style="whitegrid")

# Crear un gráfico de barras de hotel en función de arrival_date_year
plt.figure(figsize=(12, 6))
ax = sns.countplot(data=df, x='arrival_date_year', hue='hotel', palette='pastel')
plt.title('Frecuencia de Tipos de Hotel por Año de Llegada')
plt.xlabel('Año de Llegada')
plt.ylabel('Frecuencia')
plt.legend(title='Tipo de Hotel')

# Añadir descripción de resultados
total_registros = len(df)
for p in ax.patches:
    height = p.get_height()
    ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., height),
                ha='center', va='bottom', fontsize=10, color='black')
    
plt.text(0.5, 0.95, f'Total de registros: {total_registros}', 
         ha='center', va='center', transform=ax.transAxes, fontsize=12, 
         bbox=dict(facecolor='white', alpha=0.5))

plt.show()

#En el grafico se puede observar una mayor cantidad de registros en el anho 2017 siendo la del City Hotel con una mayor cantidad de concurrencia 
#y la de menor concurrencia se da en el 2015 tambien en City Hotel


# Configurar el estilo del grafico de barras entre anho y mes
sns.set(style="whitegrid")

# Contar los registros por año y mes de llegada
df['arrival_date_month'] = pd.Categorical(df['arrival_date_month'], 
                                           categories=["January", "February", "March", "April", 
                                                       "May", "June", "July", "August", 
                                                       "September", "October", "November", "December"],
                                           ordered=True)
grouped_data = df.groupby(['arrival_date_year', 'arrival_date_month'], observed=True).size().reset_index(name='counts')

# Crear el gráfico de barras
plt.figure(figsize=(12, 6))
ax = sns.barplot(data=grouped_data, x='arrival_date_month', y='counts', hue='arrival_date_year', palette='pastel')
plt.title('Frecuencia de Registros por Mes y Año de Llegada')
plt.xlabel('Mes de Llegada')
plt.ylabel('Frecuencia')
plt.legend(title='Año de Llegada')
plt.xticks(rotation=45)

# Añadir descripción de cada barra
for p in ax.patches:
    height = p.get_height()
    ax.annotate(f'{height}', (p.get_x() + p.get_width() / 2., height),
                ha='center', va='bottom', fontsize=10, color='black')

plt.show()
#se puede observar una mayor cantidad de concurrencia en el mes de Mayo del 2017 y la menor cantidad en noviembre del 2015

#Grafico Box Plots entre tipo de hotel y la tarifa diaria promedio
plt.figure(figsize=(12, 6))
ax = sns.boxplot(data=df, x='hotel', y='adr')
plt.title('Box Plot de ADR por Tipo de Hotel')
plt.xlabel('Tipo de Hotel')
plt.ylabel('ADR')

# Agregar descripciones a cada caja
for i, hotel_type in enumerate(df['hotel'].unique()):
    # Calcular la mediana de 'adr' para cada tipo de hotel
    median_value = df[df['hotel'] == hotel_type]['adr'].median()
    # Contar el número de registros para cada tipo de hotel
    count_value = df[df['hotel'] == hotel_type].shape[0]
    
    # Añadir texto al boxplot correspondiente
    ax.annotate(f'Mediana: {median_value:.2f}\nRegistros: {count_value}', 
                xy=(i, median_value), 
                xytext=(i, median_value + 5),  # Ajustar posición del texto
                ha='center', 
                fontsize=10, 
                color='black',
                bbox=dict(boxstyle='round,pad=0.3', edgecolor='none', facecolor='lightgrey'))

plt.show()

#Grafico Violin de Noches de Estancia y tipo de comida

plt.figure(figsize=(12, 6))
ax = sns.violinplot(data=df, x='meal', y='stays_in_week_nights')
plt.title('Violin Plot de Noches de Estancia en Semana por Tipo de Comida')
plt.xlabel('Tipo de Comida')
plt.ylabel('Noches de Estancia en Semana')

# Agregar descripciones a cada violín
for i, meal_type in enumerate(df['meal'].unique()):
    # Calcular la media de 'stays_in_week_nights' para cada tipo de comida
    mean_value = df[df['meal'] == meal_type]['stays_in_week_nights'].mean()
    # Contar el número de registros para cada tipo de comida
    count_value = df[df['meal'] == meal_type].shape[0]
    
    # Añadir texto al violín correspondiente
    ax.annotate(f'Media: {mean_value:.1f}\nRegistros: {count_value}', 
                xy=(i, mean_value), 
                xytext=(i, mean_value + 1),  # Ajustar posición del texto
                ha='center', 
                fontsize=10, 
                color='black',
                bbox=dict(boxstyle='round,pad=0.3', edgecolor='none', facecolor='lightgrey'))

plt.show()

#Analisis Adicional

# Filtrar solo columnas numéricas
numeric_columns = df.select_dtypes(include=['int64', 'float64'])

# Obtener resumen estadístico
summary_stats = numeric_columns.describe()

# Calcular el rango intercuartílico
iqr = numeric_columns.quantile(0.75) - numeric_columns.quantile(0.25)

# Añadir IQR al resumen
summary_stats.loc['IQR'] = iqr

print(summary_stats)

"""
Resumen Estadístico

is_canceled:

Media: 0.27
Desviación Estándar: 0.45
Mínimo: 0
Máximo: 1
Interpretación: Aproximadamente el 27.5% de las reservas fueron canceladas, ya que este es un indicador binario.


lead_time:

Media: 77.58 días
Desviación Estándar: 81.27 días
Mínimo: 0 días
Máximo: 365 días
Interpretación: El tiempo promedio de antelación para realizar una reserva es de alrededor de 78 días, con una gran variabilidad.


arrival_date_year:

Media: 2016.21
Desviación Estándar: 0.69
Mínimo: 2015
Máximo: 2017
Interpretación: La mayoría de las llegadas son en los años 2016 y 2017.


arrival_date_week_number:

Media: 26.84
Desviación Estándar: 13.67
Mínimo: 1
Máximo: 53
Interpretación: La media indica que las llegadas tienden a concentrarse alrededor de la semana 27 del año, pero hay llegadas en todas las semanas.
days_in_waiting_list:

Media: 0.75 días
Desviación Estándar: 10.02 días
Mínimo: 0 días
Máximo: 391 días
Interpretación: La mayoría de las reservas no están en lista de espera, pero hay algunas excepcionales que pueden tardar hasta 391 días.

adr (Average Daily Rate):

Media: 106.34
Desviación Estándar: 55.01
Mínimo: 0
Máximo: 5400
Interpretación: La tarifa diaria promedio es de aproximadamente $106.34, aunque hay algunos registros atípicos muy altos que podrían influir en esta media.


required_car_parking_spaces:

Media: 0.08
Desviación Estándar: 0.28
Mínimo: 0
Máximo: 3
Interpretación: La mayoría de las reservas no requieren espacios de estacionamiento, con solo unos pocos que requieren más de uno.


total_of_special_requests:

Media: 0.70
Desviación Estándar: 0.83
Mínimo: 0
Máximo: 5
Interpretación: En promedio, los clientes hacen menos de una solicitud especial, aunque algunos hacen hasta cinco.
"""
#FUENTES: mi principal fuente fueron las clases que estan en la plataforma pero tambien estuve utilizando recursos de otras paginas
# https://aprendeconalf.es/docencia/python/manual/pandas/ 
# https://joserzapata.github.io/courses/python-ciencia-datos/visualizacion/
# https://www.kaggle.com/code/hernanlarapadilla/an-lisis-multivariante-y-ciencia-de-datos
# https://joserzapata.github.io/courses/python-ciencia-datos/visualizacion/seaborn/

