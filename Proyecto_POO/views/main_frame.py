import wx

from views.nueva_reparacion_dialog import NuevaReparacionDialog
from models.reparacion import Reparacion
from views.detalle_reparacion_frame import DetalleReparacionFrame

class MainFrame(wx.Frame):
    """
    Ventana principal de RepairDesk.

    Desde esta ventana se visualizan las reparaciones
    registradas y se accede a las principales
    funcionalidades del sistema.
    """

    def __init__(self):

        super().__init__(
            parent=None,
            title="RepairDesk",
            size=(900, 600)
        )

        # Configuración inicial de la ventana
        self.crear_menu()
        
        # Lista temporal de reparaciones
        self.reparaciones = []
        
        # Contador temporal de órdenes
        self.proximo_numero = 1

        # Panel principal de la ventana
        panel = wx.Panel(self)

        # Contenedor principal
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Encabezado
        titulo = wx.StaticText(
            panel,
            label="Reparaciones registradas"
        )

        fuente = wx.Font(
            12,
            wx.FONTFAMILY_DEFAULT,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD
        )

        titulo.SetFont(fuente)

        # Tabla principal de reparaciones
        self.lista = wx.ListCtrl(
            panel,
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )

        # Definición de columnas
        self.lista.InsertColumn(
            0,
            "Orden",
            width=120
        )

        self.lista.InsertColumn(
            1,
            "Cliente",
            width=180
        )

        self.lista.InsertColumn(
            2,
            "Equipo",
            width=180
        )

        self.lista.InsertColumn(
            3,
            "Estado",
            width=120
        )

        # Organización visual
        sizer.Add(
            titulo,
            0,
            wx.ALL,
            10
        )

        sizer.Add(
            self.lista,
            1,
            wx.EXPAND | wx.ALL,
            10
        )

        panel.SetSizer(sizer)

        # Evento de doble clic sobre una reparación
        self.lista.Bind(
            wx.EVT_LIST_ITEM_ACTIVATED,
            self.on_abrir_detalle
        )

        # Centrar ventana
        self.Centre()

    def on_abrir_detalle(self, event):
        """
        Abre la ventana de detalle de una reparación.
        """

        indice = event.GetIndex()

        reparacion = self.reparaciones[indice]

        ventana = DetalleReparacionFrame(
            self,
            reparacion,
            indice
        )

        ventana.Show()

    def crear_menu(self):
        """
        Crea la barra de menús principal.
        """

        barra_menu = wx.MenuBar()

        # Menú Archivo
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

        # Menú Ayuda
        menu_ayuda = wx.Menu()

        item_acerca = menu_ayuda.Append(
            wx.ID_ABOUT,
            "Acerca de"
        )

        # Agregar menús a la barra
        barra_menu.Append(
            menu_archivo,
            "Archivo"
        )

        barra_menu.Append(
            menu_ayuda,
            "Ayuda"
        )

        self.SetMenuBar(barra_menu)

        # Eventos del menú
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
        """
        Abre la ventana para registrar una nueva reparación.
        """

        dialog = NuevaReparacionDialog(self)

        if dialog.ShowModal() == wx.ID_OK:

            datos = dialog.obtener_datos()

            numero_orden = f"RD-2026-{self.proximo_numero:03d}"

            reparacion = Reparacion(
                numero_orden,
                datos["cliente"],
                datos["equipo"],
                datos["serie"],
                datos["problema"]
            )
            # Guardar en memoria
            self.reparaciones.append(reparacion)
            
            self.agregar_reparacion_lista(reparacion)

            self.proximo_numero += 1

        dialog.Destroy()

    def agregar_reparacion_lista(self, reparacion):
        """
        Agrega una reparación al ListCtrl.
        """

        indice = self.lista.InsertItem(
            self.lista.GetItemCount(),
            reparacion.numero_orden
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

        self.lista.SetItem(
            indice,
            3,
            reparacion.estado
        )

    def on_salir(self, event):
        """
        Cierra la aplicación.
        """

        self.Close()