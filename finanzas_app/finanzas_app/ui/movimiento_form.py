from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock

from services.categoria_service import listar_categorias, crear_categoria, eliminar_categoria, actualizar_categoria
from services.movimiento_service import registrar_movimiento, listar_movimientos, eliminar_movimiento
from services.resumen_service import obtener_resumen
from services.grafico_service import obtener_gastos_por_categoria
from services.pdf_service import generar_pdf

from matplotlib import pyplot as plt


import os
import sys
from kivy.lang import Builder

def resource_path(relative_path):
    """Devuelve la ruta absoluta para .py y .exe"""
    try:
        # Si estamos en un .exe
        base_path = sys._MEIPASS
    except AttributeError:
        # Si estamos en modo desarrollo
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Ajusta la ruta relativa 
kv_path = resource_path(os.path.join("ui", "movimiento_form.kv"))
Builder.load_file(kv_path)
#Builder.load_file(resource_path("ui/movimiento_form.kv"))
#Builder.load_file("ui/movimiento_form.kv")



class MovimientoForm(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Clock.schedule_once garantiza que el arbol de widgets este
        # completamente construido antes de manipularlo (fix boton bloqueado)
        Clock.schedule_once(self._init_ui, 0)

    def _init_ui(self, dt):
        self._panel_abierto = False
        self._panel_widget = None
        # Referencia al BoxLayout padre (contenedor del ScrollView)
        # lo buscamos a través de un widget que sí existe en ids
        self._contenedor_principal = self.ids.box_movimientos.parent
        self.cargar_categorias()
        self.actualizar_dashboard()
        self.actualizar_lista()

    # =========================
    # CATEGORÍAS
    # =========================
    def cargar_categorias(self):
        categorias = listar_categorias()
        self.mapa_categorias = {
            f"{nombre} ({tipo})": id_categoria
            for id_categoria, nombre, tipo in categorias
        }
        self.ids.spinner_categoria.values = list(self.mapa_categorias.keys())

    def _construir_panel_categorias(self):
        """Construye el panel de categorías como widget independiente."""
        from kivy.uix.textinput import TextInput as TI
        from kivy.uix.spinner import Spinner as Sp

        panel = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=5
        )

        # Fila para añadir nueva categoría
        fila_nueva = BoxLayout(size_hint_y=None, height=45, spacing=5)
        self._txt_cat_nombre = TI(hint_text="Nombre categoría")
        self._spinner_cat_tipo = Sp(
            text="ingreso",
            values=["ingreso", "gasto"],
            size_hint_x=0.5
        )
        btn_añadir = Button(text="Añadir", size_hint_x=0.4)
        btn_añadir.bind(on_press=lambda x: self.crear_categoria())
        fila_nueva.add_widget(self._txt_cat_nombre)
        fila_nueva.add_widget(self._spinner_cat_tipo)
        fila_nueva.add_widget(btn_añadir)
        panel.add_widget(fila_nueva)

        # Filas de categorías existentes
        categorias = listar_categorias()
        for id_cat, nombre, tipo in categorias:
            fila = BoxLayout(size_hint_y=None, height=40, spacing=5)
            fila.add_widget(Label(text=f"{nombre} ({tipo})", color=(0, 0, 0, 1)))
            btn_editar = Button(text="Editar", size_hint_x=0.3)
            btn_eliminar = Button(text="Eliminar", size_hint_x=0.3)
            btn_editar.bind(on_press=lambda x, i=id_cat: self.editar_categoria(i))
            btn_eliminar.bind(on_press=lambda x, i=id_cat: self.eliminar_categoria(i))
            fila.add_widget(btn_editar)
            fila.add_widget(btn_eliminar)
            panel.add_widget(fila)

        # Calcular height total
        panel.height = sum(
            c.height for c in panel.children
        ) + panel.spacing * (len(panel.children) - 1)

        return panel

    def cargar_lista_categorias(self):
        """Si el panel está abierto, lo reconstruye con datos frescos."""
        if not getattr(self, '_panel_abierto', False):
            return
        if self._panel_widget and self._panel_widget.parent:
            idx = self._contenedor_principal.children.index(self._panel_widget)
            self._contenedor_principal.remove_widget(self._panel_widget)
            self._panel_widget = self._construir_panel_categorias()
            self._contenedor_principal.add_widget(self._panel_widget, index=idx)

    def crear_categoria(self):
        if not hasattr(self, '_txt_cat_nombre') or self._txt_cat_nombre is None:
            return
        nombre = self._txt_cat_nombre.text.strip()
        tipo = self._spinner_cat_tipo.text
        if not nombre:
            self.mostrar_mensaje("Error", "El nombre no puede estar vacío")
            return
        try:
            crear_categoria(nombre, tipo)
            self._txt_cat_nombre.text = ""
            self.cargar_lista_categorias()
            self.cargar_categorias()
        except Exception as e:
            self.mostrar_mensaje("Error", str(e))

    def eliminar_categoria(self, id_categoria):
        try:
            eliminar_categoria(id_categoria)
            self.cargar_lista_categorias()
            self.cargar_categorias()
        except Exception as e:
            self.mostrar_mensaje("Error", str(e))

    def editar_categoria(self, id_categoria):
        cat = next((c for c in listar_categorias() if c[0] == id_categoria), None)
        if not cat:
            return
        popup_layout = BoxLayout(orientation="vertical", spacing=10, padding=10)
        txt_nombre = TextInput(text=cat[1])
        spinner_tipo = Spinner(text=cat[2], values=["ingreso", "gasto"])
        btn_guardar = Button(text="Guardar", size_hint_y=None, height=40)
        popup_layout.add_widget(txt_nombre)
        popup_layout.add_widget(spinner_tipo)
        popup_layout.add_widget(btn_guardar)
        popup = Popup(title="Editar categoría", content=popup_layout, size_hint=(0.8, 0.5))

        def guardar_edicion(x):
            try:
                actualizar_categoria(id_categoria, txt_nombre.text, spinner_tipo.text)
                popup.dismiss()
                self.cargar_lista_categorias()
                self.cargar_categorias()
            except Exception as e:
                self.mostrar_mensaje("Error", str(e))

        btn_guardar.bind(on_press=guardar_edicion)
        popup.open()

    def toggle_categorias(self):
        if not self._panel_abierto:
            # ABRIR: construir el panel e insertarlo en el árbol
            self._panel_widget = self._construir_panel_categorias()
            # Insertarlo justo después del botón "Editar categorías"
            # En Kivy el índice 0 es el último hijo, así que calculamos
            # la posición del botón de editar y lo insertamos antes del
            # siguiente elemento (los filtros)
            btn_editar = None
            for child in self._contenedor_principal.children:
                if hasattr(child, 'text') and child.text == "Editar categorías":
                    btn_editar = child
                    break
            if btn_editar:
                idx = self._contenedor_principal.children.index(btn_editar)
                self._contenedor_principal.add_widget(self._panel_widget, index=idx)
            else:
                self._contenedor_principal.add_widget(self._panel_widget)
            self._panel_abierto = True
        else:
            # CERRAR: eliminar el panel del árbol completamente
            if self._panel_widget and self._panel_widget.parent:
                self._contenedor_principal.remove_widget(self._panel_widget)
            self._panel_widget = None
            self._panel_abierto = False

    # =========================
    # MENSAJES
    # =========================
    def mostrar_mensaje(self, titulo, mensaje):
        Popup(
            title=titulo,
            content=Label(text=mensaje),
            size_hint=(0.8, 0.4)
        ).open()

    # =========================
    # GUARDAR MOVIMIENTO
    # =========================
    def guardar_movimiento(self):
        try:
            fecha = self.ids.txt_fecha.text
            cantidad = self.ids.txt_cantidad.text
            descripcion = self.ids.txt_descripcion.text
            categoria_texto = self.ids.spinner_categoria.text

            if categoria_texto == "Seleccionar categoría":
                raise ValueError("Debe seleccionar una categoría")

            id_categoria = self.mapa_categorias[categoria_texto]
            registrar_movimiento(fecha, cantidad, descripcion, id_categoria)

            self.ids.txt_fecha.text = ""
            self.ids.txt_cantidad.text = ""
            self.ids.txt_descripcion.text = ""
            self.ids.spinner_categoria.text = "Seleccionar categoría"

            self.actualizar_dashboard()
            self.actualizar_lista()
            self.mostrar_mensaje("OK", "Movimiento guardado")

        except Exception as e:
            self.mostrar_mensaje("Error", str(e))

    # =========================
    # DASHBOARD
    # =========================
    def actualizar_dashboard(self):
        resumen = obtener_resumen()
        self.ids.lbl_ingresos.text = f"{resumen['ingresos']:.2f} €"
        self.ids.lbl_gastos.text = f"{resumen['gastos']:.2f} €"
        self.ids.lbl_balance.text = f"{resumen['balance']:.2f} €"

    # =========================
    # LISTADO + FILTROS (RF4)
    # =========================
    def actualizar_lista(self):
        mes = self.ids.txt_mes.text.strip() or None
        tipo = self.ids.spinner_tipo.text
        if tipo == "Todos":
            tipo = None

        movimientos = listar_movimientos(mes=mes, tipo=tipo)
        contenedor = self.ids.box_movimientos
        contenedor.clear_widgets()

        if not movimientos:
            contenedor.add_widget(Label(text="Sin movimientos", size_hint_y=None, height=40))
            return

        for m in movimientos:
            id_mov, fecha, cantidad, descripcion, categoria, tipo_mov = m
            signo = "+" if tipo_mov == "ingreso" else "-"
            card = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                height=130,
                padding=10,
                spacing=5
            )

            with card.canvas.before:
                Color(0.95, 0.95, 0.95, 1)
                rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[12])

            # FIX: captura rect en el closure con r=rect
            card.bind(pos=lambda i, v, r=rect: setattr(r, "pos", i.pos),
                      size=lambda i, v, r=rect: setattr(r, "size", i.size))

            color_importe = (0, 0.6, 0, 1) if tipo_mov == "ingreso" else (0.85, 0.15, 0.15, 1)

            card.add_widget(Label(
                text=f"{fecha}  |  {categoria}",
                color=(0.3, 0.3, 0.3, 1),
                halign="left", valign="middle",
                text_size=(None, None)
            ))
            card.add_widget(Label(
                text=descripcion or "—",
                color=(0, 0, 0, 1),
                halign="left", valign="middle",
                text_size=(None, None)
            ))
            card.add_widget(Label(
                text=f"{signo}{float(cantidad):.2f} €",
                color=color_importe,
                font_size=18,
                bold=True,
                halign="left", valign="middle",
                text_size=(None, None)
            ))

            btn = Button(
                text="Eliminar",
                size_hint_y=None,
                height=35,
                background_color=(0.9, 0.3, 0.3, 1)
            )
            btn.bind(on_press=lambda x, mid=id_mov: self.borrar_movimiento(mid))

            card.add_widget(btn)
            contenedor.add_widget(card)

    # =========================
    # ELIMINAR MOVIMIENTO
    # =========================
    def borrar_movimiento(self, id_movimiento):
        try:
            eliminar_movimiento(id_movimiento)
            self.actualizar_dashboard()
            self.actualizar_lista()
        except Exception as e:
            self.mostrar_mensaje("Error", str(e))

    # =========================
    # GRÁFICO
    # =========================
    def mostrar_grafico(self):
        datos = obtener_gastos_por_categoria()
        if not datos:
            self.mostrar_mensaje("Sin datos", "No hay gastos")
            return
        categorias = [d[0] for d in datos]
        totales = [d[1] or 0 for d in datos]

        plt.pie(totales, labels=categorias, autopct="%1.1f%%")
        plt.title("Gastos por categoría")
        plt.axis("equal")
        plt.show()

    # =========================
    # PDF
    # =========================
    def exportar_pdf(self):
        try:
            ruta = generar_pdf()
            self.mostrar_mensaje("PDF", ruta)
        except Exception as e:
            self.mostrar_mensaje("Error", str(e))


class FinanzasApp(App):
    def build(self):
        return MovimientoForm()