# Librerías necesarias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Configuración general
sns.set(style='whitegrid')
np.random.seed(42)  # Reproducibilidad

# Definimos listas de productos, categorías y sucursales
productos = ['Laptop', 'Celular', 'Tablet', 'Audífonos', 'Mouse', 'Teclado', 'Monitor']
categorias = {
    'Laptop': 'Computación',
    'Celular': 'Telefonía',
    'Tablet': 'Computación',
    'Audífonos': 'Accesorios',
    'Mouse': 'Accesorios',
    'Teclado': 'Accesorios',
    'Monitor': 'Computación'
}
sucursales = ['CDMX', 'Guadalajara', 'Monterrey', 'Puebla']

# Generar 500 registros aleatorios
n = 500
fechas = [datetime(2024, 1, 1) + timedelta(days=np.random.randint(0, 180)) for _ in range(n)]
productos_venta = np.random.choice(productos, size=n)
cantidades = np.random.randint(1, 5, size=n)
precios_unitarios = [np.random.randint(100, 2000) for _ in range(n)]
sucursales_venta = np.random.choice(sucursales, size=n)

# Crear DataFrame
df = pd.DataFrame({
    'Fecha': fechas,
    'Producto': productos_venta,
    'Cantidad': cantidades,
    'Precio Unitario': precios_unitarios,
    'Sucursal': sucursales_venta
})

# Agregar categoría y total de venta
df['Categoría'] = df['Producto'].map(categorias)
df['Total Venta'] = df['Cantidad'] * df['Precio Unitario']

# Vista general
df.info()
df.head()

# KPIs generales
print("🔸 Total de ventas ($):", df['Total Venta'].sum())
print("🔸 Total de productos vendidos:", df['Cantidad'].sum())
print("🔸 Ticket promedio ($):", round(df['Total Venta'].mean(), 2))


ventas_por_dia = df.groupby('Fecha')['Total Venta'].sum()

plt.figure(figsize=(12,5))
ventas_por_dia.plot()
plt.title('Ventas por Día')
plt.xlabel('Fecha')
plt.ylabel('Total de Ventas ($)')
plt.grid(True)
plt.tight_layout()
plt.show()

# Por cantidad
productos_top = df.groupby('Producto')['Cantidad'].sum().sort_values(ascending=False)

plt.figure(figsize=(8,5))
productos_top.plot(kind='bar', color='skyblue')
plt.title('Top productos por cantidad vendida')
plt.ylabel('Unidades vendidas')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Por ingresos
productos_ingresos = df.groupby('Producto')['Total Venta'].sum().sort_values(ascending=False)

plt.figure(figsize=(8,5))
productos_ingresos.plot(kind='bar', color='orange')
plt.title('Top productos por ingresos generados')
plt.ylabel('Total de ventas ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

ventas_por_sucursal = df.groupby('Sucursal')['Total Venta'].sum().sort_values()

plt.figure(figsize=(6,4))
ventas_por_sucursal.plot(kind='barh', color='mediumseagreen')
plt.title('Ventas por Sucursal')
plt.xlabel('Total de ventas ($)')
plt.tight_layout()
plt.show()


# Extraer mes y día
df['Mes'] = df['Fecha'].dt.to_period('M')
df['Día Semana'] = df['Fecha'].dt.day_name()

# Ventas por mes
ventas_por_mes = df.groupby('Mes')['Total Venta'].sum()

plt.figure(figsize=(10,5))
ventas_por_mes.plot(marker='o', color='steelblue')
plt.title('Ventas por Mes')
plt.xlabel('Mes')
plt.ylabel('Total de Ventas ($)')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# Ventas por día de la semana
orden_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
ventas_dia_semana = df.groupby('Día Semana')['Total Venta'].sum().reindex(orden_dias)

plt.figure(figsize=(8,4))
ventas_dia_semana.plot(kind='bar', color='salmon')
plt.title('Ventas por Día de la Semana')
plt.ylabel('Total de Ventas ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


#ventas por ciudad
pivot_ciudad_producto = pd.pivot_table(df, values='Cantidad',
                                       index='Producto',
                                       columns='Sucursal',
                                       aggfunc='sum',
                                       fill_value=0)

pivot_ciudad_producto.plot(kind='bar', figsize=(10,6))
plt.title('Unidades vendidas por Producto y Sucursal')
plt.ylabel('Cantidad')
plt.xticks(rotation=45)
plt.legend(title='Sucursal')
plt.tight_layout()
plt.show()

# matriz de correlacion
corr_matrix = df[['Cantidad', 'Precio Unitario', 'Total Venta']].corr()

plt.figure(figsize=(6,4))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Matriz de Correlación')
plt.tight_layout()
plt.show()

#guardar datos
df.to_excel('ventas_simuladas.xlsx', index=False)
