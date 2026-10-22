# Aplicación de Gestión de Ingresos y Gastos Personales

**Autor:** Miguel David González Bobes  
**Ciclo:** Desarrollo de Aplicaciones Multiplataforma (2DAM)  
**Curso:** 2025–2026  
**Tecnologías:** Python 3.12.10 · Kivy · SQLite · Matplotlib · ReportLab

---

## Descripción

Aplicación de escritorio con interfaz gráfica orientada a móvil que permite registrar, categorizar y visualizar movimientos económicos personales. Incluye dashboard financiero en tiempo real, filtros por mes y tipo, gráficos estadísticos y exportación a PDF.

---

## Requisitos del sistema

| Componente | Versión utilizada |
|---|---|
| Python | **3.12.10** (versión exacta de desarrollo) |
| Sistema operativo | Windows 11 |
| pip | 24.x o superior |

> ⚠️ **Importante:** Kivy tiene compatibilidad limitada con versiones de Python muy recientes. Se recomienda usar exactamente **Python 3.12.10** para garantizar el funcionamiento correcto.

---

## Instalación paso a paso (Windows 11)

### Paso 1 — Descargar e instalar Python 3.12.10

1. Ir a https://www.python.org/downloads/release/python-31210/
2. Descargar **Windows installer (64-bit)**
3. Ejecutar el instalador:
   - ✅ Marcar **"Add Python to PATH"**
   - ✅ Marcar **"Install for all users"** (recomendado)
4. Verificar la instalación abriendo una terminal (CMD o PowerShell):

```cmd
python --version
```
Debe mostrar: `Python 3.12.10`

---

### Paso 2 — Descomprimir el proyecto

Descomprime el archivo `.zip` del proyecto en una carpeta de tu elección, por ejemplo:

```
C:\Proyectos\finanzas_app\
```

Abre una terminal (CMD o PowerShell) y navega a esa carpeta:

```cmd
cd C:\Proyectos\finanzas_app
```

---

### Paso 3 — Crear el entorno virtual

```cmd
python -m venv venv
```

Activar el entorno virtual:

```cmd
venv\Scripts\activate
```

Verás que el prompt cambia a `(venv)`. **Todos los pasos siguientes deben ejecutarse con el entorno activado.**

---

### Paso 4 — Actualizar pip

```cmd
python -m pip install --upgrade pip
```

---

### Paso 5 — Instalar dependencias de Kivy (requisitos previos)

Kivy en Windows requiere instalar primero sus dependencias de sistema:

```cmd
pip install kivy[base] kivy_examples --pre --extra-index-url https://kivy.org/downloads/simple/
```

Si la línea anterior da error, prueba la instalación estable:

```cmd
pip install kivy
```

---

### Paso 6 — Instalar kivy-garden y los widgets necesarios

```cmd
pip install kivy-garden
```

Si el proyecto usa algún widget de garden (como `garden.matplotlib`), instálalo con:

```cmd
garden install matplotlib
```

> 💡 Si al ejecutar la app aparece un error `No module named 'kivy_garden.xxx'`, instala el widget concreto con `garden install xxx`.

---

### Paso 7 — Instalar el resto de dependencias

```cmd
pip install matplotlib reportlab
```

---

### Paso 8 — Verificar todas las instalaciones

```cmd
python -c "import kivy; print('Kivy:', kivy.__version__)"
python -c "import matplotlib; print('Matplotlib:', matplotlib.__version__)"
python -c "import reportlab; print('ReportLab:', reportlab.Version)"
python -c "import sqlite3; print('SQLite: OK')"
```

Todas deben ejecutarse sin error.

---

## Ejecución

Con el entorno virtual activado, desde la raíz del proyecto:

```cmd
python main.py
```

La base de datos `finanzas.db` se crea automáticamente en la carpeta `data/` al primer arranque, incluyendo las siguientes categorías predefinidas:

| Categoría | Tipo |
|---|---|
| Salario | Ingreso |
| Ventas | Ingreso |
| Comida | Gasto |
| Transporte | Gasto |
| Vivienda | Gasto |
| Ocio | Gasto |
| Salud | Gasto |

---

## Estructura del proyecto

```
finanzas_app/
├── main.py                        # Punto de entrada de la aplicación
├── README.md                      # Este archivo
├── data/                          # Generada automáticamente al ejecutar
│   └── finanzas.db                # Base de datos SQLite
├── database/
│   └── db.py                      # Conexión y esquema de la base de datos
├── ui/
│   ├── movimiento_form.py         # Lógica de la interfaz principal
│   └── movimiento_form.kv         # Definición de la UI en lenguaje KV
└── services/
    ├── categoria_service.py       # CRUD de categorías
    ├── movimiento_service.py      # CRUD de movimientos con filtros
    ├── resumen_service.py         # Cálculo de totales financieros
    ├── grafico_service.py         # Consultas para el gráfico
    └── pdf_service.py             # Generación de informes PDF
```

---

## Funcionalidades

| Función | Descripción |
|---|---|
| Dashboard financiero | Muestra ingresos, gastos y balance en tiempo real |
| Registrar movimiento | Añade ingresos o gastos con fecha, cantidad, descripción y categoría |
| Eliminar movimiento | Elimina cualquier movimiento desde el listado |
| Filtrar movimientos | Filtra por mes (YYYY-MM) y por tipo (ingreso / gasto / todos) |
| Gestión de categorías | Crear, editar y eliminar categorías (panel desplegable) |
| Gráfico de gastos | Gráfico de tarta por categoría con Matplotlib |
| Exportar PDF | Genera `informe_financiero.pdf` con tabla y resumen |

---

## Archivos generados durante el uso

| Archivo | Ubicación | Descripción |
|---|---|---|
| `finanzas.db` | `data/` | Base de datos con categorías y movimientos |
| `informe_financiero.pdf` | Raíz del proyecto | Informe exportado al pulsar el botón PDF |

---

## Dependencias completas

| Paquete | Uso |
|---|---|
| `kivy` | Framework de interfaz gráfica |
| `kivy-garden` | Widgets adicionales de Kivy |
| `matplotlib` | Generación del gráfico de tarta |
| `reportlab` | Generación del PDF |
| `sqlite3` | Base de datos local (incluido en Python) |

---

## Solución de problemas comunes

| Error | Causa probable | Solución |
|---|---|---|
| `ModuleNotFoundError: No module named 'kivy'` | Kivy no instalado o entorno virtual no activado | Activar venv y ejecutar `pip install kivy` |
| `ModuleNotFoundError: No module named 'reportlab'` | ReportLab no instalado | `pip install reportlab` |
| `ModuleNotFoundError: No module named 'matplotlib'` | Matplotlib no instalado | `pip install matplotlib` |
| `PermissionError` al generar PDF | El PDF está abierto en otro programa | Cerrar el PDF antes de exportar de nuevo |
| Pantalla negra o en blanco al arrancar | Conflicto con drivers gráficos y OpenGL | Ejecutar `set KIVY_GL_BACKEND=angle_sdl2` antes de `python main.py` |
| `garden: command not found` | kivy-garden no instalado | `pip install kivy-garden` |
| La app no arranca con Python 3.13+ | Kivy no es compatible aún | Usar exactamente Python **3.12.10** |

---

## Nota sobre la pantalla negra en Windows (OpenGL)

En algunos equipos con Windows 11 y tarjetas gráficas integradas (Intel HD/Iris), Kivy puede mostrar una pantalla negra. Si ocurre, ejecuta antes de lanzar la app:

```cmd
set KIVY_GL_BACKEND=angle_sdl2
python main.py
```

O crea un archivo `.env` en la raíz o añade esta línea al principio de `main.py`:

```python
import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
```

---

## Notas técnicas

- La BD usa claves foráneas con `ON DELETE RESTRICT`: no se puede eliminar una categoría con movimientos asociados.
- El índice `idx_movimientos_fecha` acelera las consultas filtradas por mes.
- La arquitectura sigue el patrón por capas: **UI → Servicios → Base de datos**.
- La variable `KIVY_NO_CONSOLELOG=1` puede añadirse al entorno para suprimir logs de consola de Kivy en producción.
