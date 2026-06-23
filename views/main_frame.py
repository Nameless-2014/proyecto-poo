import wx
import os

from views.nueva_reparacion_dialog import NuevaReparacionDialog
from models.reparacion import Reparacion
from views.detalle_reparacion_frame import DetalleReparacionFrame
from db_manager import DatabaseManager


class MainFrame(wx.Frame):
    """
    Ventana principal de RepairDesk.
    Conectada a SQLite pero manteniendo la interfaz original.
    """

    def __init__(self):
        super().__init__(
            parent=None,
            title="RepairDesk v1.0.0",
            size=(1000, 650)
        )

        # --------------------------------------------------
        # ICONO DE LA APLICACIÓN
        # --------------------------------------------------

        base_path = os.path.dirname(os.path.abspath(__file__))

        icon_path = os.path.join(
            base_path,
            "..",
            "assets",
            "IcoDesk.ico"
        )

        if os.path.exists(icon_path):
            self.SetIcon(
                wx.Icon(
                    icon_path,
                    wx.BITMAP_TYPE_ICO
                )
            )

        self.crear_menu()

        # --------------------------------------------------
        # BASE DE DATOS
        # --------------------------------------------------

        self.db = DatabaseManager()

        self.reparaciones = (
            self.db.obtener_todas_reparaciones()
        )

        # --------------------------------------------------
        # PANEL PRINCIPAL
        # --------------------------------------------------

        panel = wx.Panel(self)

        sizer = wx.BoxSizer(wx.VERTICAL)

        # --------------------------------------------------
        # CABECERA VISUAL
        # --------------------------------------------------

        cabecera = wx.Panel(panel)

        cabecera.SetBackgroundColour(
            "#003366"
        )

        sizer_cabecera = wx.BoxSizer(
            wx.HORIZONTAL
        )

        logo_path = os.path.join(
            base_path,
            "..",
            "assets",
            "IcoDesk.png"
        )

        if os.path.exists(logo_path):

            imagen_logo = wx.Image(
                logo_path
            )

            imagen_logo = imagen_logo.Scale(
                64,
                64,
                wx.IMAGE_QUALITY_HIGH
            )

            logo = wx.StaticBitmap(
                cabecera,
                bitmap=wx.Bitmap(imagen_logo)
            )

            sizer_cabecera.Add(
                logo,
                0,
                wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                15
            )

        textos = wx.BoxSizer(
            wx.VERTICAL
        )

        titulo_app = wx.StaticText(
            cabecera,
            label="RepairDesk"
        )

        fuente_titulo = wx.Font(
            20,
            wx.FONTFAMILY_DEFAULT,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD
        )

        titulo_app.SetFont(
            fuente_titulo
        )

        titulo_app.SetForegroundColour(
            wx.WHITE
        )

        subtitulo = wx.StaticText(
            cabecera,
            label="Sistema de Gestión de Reparaciones"
        )

        subtitulo.SetForegroundColour(
            "#D6E4FF"
        )

        textos.Add(
            titulo_app
        )

        textos.Add(
            subtitulo
        )

        sizer_cabecera.Add(
            textos,
            0,
            wx.ALIGN_CENTER_VERTICAL
        )

        cabecera.SetSizer(
            sizer_cabecera
        )

        # --------------------------------------------------
        # BUSCADOR
        # --------------------------------------------------

        self.txt_buscar = wx.SearchCtrl(
            panel,
            style=wx.TE_PROCESS_ENTER
        )

        self.txt_buscar.SetDescriptiveText(
            "Buscar cliente, equipo o número de serie..."
        )

        self.txt_buscar.SetMinSize(
            (-1, 28)
        )

        self.txt_buscar.Bind(
            wx.EVT_TEXT,
            self.on_buscar
        )

        # --------------------------------------------------
        # TABLA DE REPARACIONES
        # --------------------------------------------------

        self.lista = wx.ListCtrl(
            panel,
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )

        self.lista.InsertColumn(
            0,
            "Orden",
            width=120
        )

        self.lista.InsertColumn(
            1,
            "Cliente",
            width=240
        )

        self.lista.InsertColumn(
            2,
            "Equipo",
            width=320
        )

        self.lista.InsertColumn(
            3,
            "Estado",
            width=180
        )

        self.lista.SetFont(
            wx.Font(
                10,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL
            )
        )

        # --------------------------------------------------
        # CARGAR REPARACIONES
        # --------------------------------------------------

        for rep in self.reparaciones:

            self.agregar_reparacion_lista(
                rep
            )

        # --------------------------------------------------
        # CONTADOR
        # --------------------------------------------------

        self.lbl_total = wx.StaticText(
            panel,
            label=f"Total de reparaciones: {len(self.reparaciones)}"
        )

        # --------------------------------------------------
        # LAYOUT
        # --------------------------------------------------

        sizer.Add(
            cabecera,
            0,
            wx.EXPAND
        )

        sizer.Add(
            self.txt_buscar,
            0,
            wx.EXPAND | wx.ALL,
            15
        )

        sizer.Add(
            self.lista,
            1,
            wx.EXPAND | wx.LEFT | wx.RIGHT,
            10
        )

        sizer.Add(
            self.lbl_total,
            0,
            wx.ALL,
            10
        )

        panel.SetSizer(
            sizer
        )

        # --------------------------------------------------
        # EVENTOS
        # --------------------------------------------------

        self.lista.Bind(
            wx.EVT_LIST_ITEM_ACTIVATED,
            self.on_abrir_detalle
        )

        self.lista.Bind(
            wx.EVT_LIST_ITEM_RIGHT_CLICK,
            self.on_click_derecho
        )

        self.Centre()

    def on_buscar(self, event):

        criterio = self.txt_buscar.GetValue()

        self.reparaciones = (
            self.db.buscar_reparaciones(
                criterio
            )
        )

        self.lista.DeleteAllItems()

        for rep in self.reparaciones:

            self.agregar_reparacion_lista(
                rep
            )

    def on_abrir_detalle(self, event):

        indice = event.GetIndex()

        reparacion = self.reparaciones[
            indice
        ]

        ventana = DetalleReparacionFrame(
            self,
            reparacion,
            indice
        )

        ventana.Show()

    def on_click_derecho(self, event):

        self.indice_seleccionado = (
            event.GetIndex()
        )

        menu = wx.Menu()

        item_eliminar = menu.Append(
            wx.ID_ANY,
            "Eliminar"
        )

        self.Bind(
            wx.EVT_MENU,
            self.on_eliminar_reparacion,
            item_eliminar
        )

        self.PopupMenu(menu)

        menu.Destroy()

    def on_eliminar_reparacion(self, event):

        if not hasattr(
            self,
            "indice_seleccionado"
        ):
            return

        reparacion = self.reparaciones[
            self.indice_seleccionado
        ]

        respuesta = wx.MessageBox(
            "¿Estás seguro que deseas eliminar al cliente/equipo? Esta acción no se puede revertir.",
            "Confirmar eliminación",
            wx.YES_NO
            | wx.NO_DEFAULT
            | wx.ICON_QUESTION
        )

        if respuesta == wx.YES:

            try:

                self.db.eliminar_reparacion(
                    reparacion.equipo_id
                )

                del self.reparaciones[
                    self.indice_seleccionado
                ]

                self.lista.DeleteItem(
                    self.indice_seleccionado
                )

                self.lbl_total.SetLabel(
                    f"Total de reparaciones: {self.lista.GetItemCount()}"
                )

                wx.MessageBox(
                    "Cliente eliminado con éxito.",
                    "Eliminado",
                    wx.OK | wx.ICON_INFORMATION
                )

            except Exception as e:

                wx.MessageBox(
                    f"Error al eliminar en la base de datos: {e}",
                    "Error",
                    wx.OK | wx.ICON_ERROR
                )

    def crear_menu(self):

        barra_menu = wx.MenuBar()

        menu_archivo = wx.Menu()

        self.item_nuevo = menu_archivo.Append(
            wx.ID_NEW,
            "Nueva reparación"
        )

        menu_archivo.AppendSeparator()

        item_salir = menu_archivo.Append(
            wx.ID_EXIT,
            "Salir"
        )

        menu_ayuda = wx.Menu()

        item_manual = menu_ayuda.Append(
            wx.ID_ANY,
            "Manual de uso"
        )

        item_acerca = menu_ayuda.Append(
            wx.ID_ABOUT,
            "Acerca de"
        )

        self.Bind(
            wx.EVT_MENU,
            self.on_acerca_de,
            item_acerca
        )
        
        self.Bind(
            wx.EVT_MENU,
            self.on_manual,
            item_manual
        )
        
        barra_menu.Append(
            menu_archivo,
            "Archivo"
        )

        barra_menu.Append(
            menu_ayuda,
            "Ayuda"
        )

        self.SetMenuBar(
            barra_menu
        )

        self.Bind(
            wx.EVT_MENU,
            self.on_salir,
            item_salir
        )

        self.Bind(
            wx.EVT_MENU,
            self.on_nueva_reparacion,
            self.item_nuevo
        )

    def on_nueva_reparacion(self, event):

        dialog = NuevaReparacionDialog(
            self
        )

        if dialog.ShowModal() == wx.ID_OK:

            datos = dialog.obtener_datos()

            try:

                nueva_rep = (
                    self.db.insertar_reparacion(
                        dni=f"S/D-{datos['cliente'][:3]}",
                        nombre=datos["cliente"],
                        apellido="",
                        telefono="",
                        num_serie=datos["serie"],
                        modelo_marca=datos["equipo"],
                        falla=datos["problema"]
                    )
                )

                self.reparaciones.append(
                    nueva_rep
                )

                self.agregar_reparacion_lista(
                    nueva_rep
                )

            except Exception as e:

                wx.MessageBox(
                    f"Error al guardar en la base de datos: {e}",
                    "Error",
                    wx.OK | wx.ICON_ERROR
                )

        dialog.Destroy()

    def agregar_reparacion_lista(
        self,
        reparacion
    ):

        codigo_orden = (
            f"RD-2026-{reparacion.equipo_id:03d}"
        )

        indice = self.lista.InsertItem(
            self.lista.GetItemCount(),
            codigo_orden
        )

        self.lista.SetItem(
            indice,
            1,
            reparacion.cliente
        )

        self.lista.SetItem(
            indice,
            2,
            reparacion.equipo
        )

        estado = reparacion.estado

        if estado == "Pendiente":
            estado = "⏳ Pendiente"

        elif estado == "En diagnóstico":
            estado = "🔍 En diagnóstico"

        elif estado == "Reparando":
            estado = "🔧 Reparando"

        elif estado == "Finalizado":
            estado = "✅ Finalizado"

        elif estado == "Entregado":
            estado = "📦 Entregado"

        self.lista.SetItem(
            indice,
            3,
            estado
        )

        if hasattr(
            self,
            "lbl_total"
        ):
            self.lbl_total.SetLabel(
                f"Total de reparaciones: {self.lista.GetItemCount()}"
            )

    def on_salir(self, event):

        self.Close()
        
    def on_acerca_de(self, event):
        """
        Muestra información sobre la aplicación.
        """

        mensaje = (
            "RepairDesk v1.0.0\n\n"
            "Sistema de Gestión de Reparaciones Informáticas.\n\n"
            "Permite registrar, consultar, modificar y "
            "administrar reparaciones de equipos.\n\n"
            "Tecnologías utilizadas:\n"
            "- Python\n"
            "- wxPython\n"
            "- SQLite\n\n"
            "Desarrollado por "
            "Torres Marco & Imolesi Cristopher."
        )

        wx.MessageBox(
            mensaje,
            "Acerca de RepairDesk",
            wx.OK | wx.ICON_INFORMATION
        )
        
    def on_manual(self, event):
        """
        Muestra una guía rápida de uso.
        """

        mensaje = (
            "MANUAL DE USO - REPAIRDESK\n\n"
            "1. Para registrar una reparación:\n"
            "   Archivo → Nueva reparación.\n\n"
            "2. Para buscar una reparación:\n"
            "   Utilice la barra de búsqueda.\n\n"
            "3. Para ver o editar detalles:\n"
            "   Haga doble clic sobre una reparación.\n\n"
            "4. Para cambiar el estado:\n"
            "   Abra el detalle y guarde los cambios.\n\n"
            "5. Para eliminar una reparación:\n"
            "   Clic derecho sobre el registro y seleccione Eliminar."
        )

        wx.MessageBox(
            mensaje,
            "Manual de uso",
            wx.OK | wx.ICON_INFORMATION
        )