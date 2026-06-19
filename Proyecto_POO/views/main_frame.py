import wx

# Reutilizamos las vistas y moldes originales de mi compañero
from views.nueva_reparacion_dialog import NuevaReparacionDialog
from models.reparacion import Reparacion
from views.detalle_reparacion_frame import DetalleReparacionFrame

# NUEVO: Importamos el motor de base de datos que armamos
from db_manager import DatabaseManager

class MainFrame(wx.Frame):
    """
    Ventana principal de RepairDesk.
    Conectada a SQLite pero manteniendo la interfaz original.
    """

    def __init__(self):
        super().__init__(parent=None, title="RepairDesk", size=(900, 600))

        self.crear_menu()
        
        # NUEVO: Inicializamos la conexión a la base de datos local
        self.db = DatabaseManager()
        
        # MODIFICADO: En vez de arrancar con self.reparaciones = [], traemos el historial real de SQLite
        self.reparaciones = self.db.obtener_todas_reparaciones()

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        titulo = wx.StaticText(panel, label="Reparaciones registradas")
        fuente = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        titulo.SetFont(fuente)

        # NUEVO: Agregamos la barra de búsqueda para cumplir con los requisitos
        self.txt_buscar = wx.SearchCtrl(panel, style=wx.TE_PROCESS_ENTER)
        self.txt_buscar.SetDescriptiveText("Buscar por cliente, equipo o serie...")
        self.txt_buscar.Bind(wx.EVT_TEXT, self.on_buscar)

        # REQUISITO LISTCTRL: Tabla principal de reparaciones (Mantenemos la de mi compañero)
        self.lista = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.lista.InsertColumn(0, "Orden", width=120)
        self.lista.InsertColumn(1, "Cliente", width=180)
        self.lista.InsertColumn(2, "Equipo", width=180)
        self.lista.InsertColumn(3, "Estado", width=120)

        # NUEVO: Llenamos la tabla con lo que recuperamos de la base de datos
        for rep in self.reparaciones:
            self.agregar_reparacion_lista(rep)

        # Organización visual (sumamos el buscador al medio)
        sizer.Add(titulo, 0, wx.ALL, 10)
        sizer.Add(self.txt_buscar, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        sizer.Add(self.lista, 1, wx.EXPAND | wx.ALL, 10)

        panel.SetSizer(sizer)

        self.lista.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_abrir_detalle)
        self.Centre()

    def on_buscar(self, event):
        """
        NUEVO: Filtra la tabla consultando a la base de datos en tiempo real al escribir.
        """
        criterio = self.txt_buscar.GetValue()
        self.reparaciones = self.db.buscar_reparaciones(criterio)
        
        self.lista.DeleteAllItems() # Limpiamos la vista actual
        for rep in self.reparaciones:
            self.agregar_reparacion_lista(rep)

    def on_abrir_detalle(self, event):
        indice = event.GetIndex()
        reparacion = self.reparaciones[indice]
        ventana = DetalleReparacionFrame(self, reparacion, indice)
        ventana.Show()

    def crear_menu(self):
        """
        Mantenemos la estructura de menús original intacta.
        """
        barra_menu = wx.MenuBar()
        menu_archivo = wx.Menu()
        
        self.item_nuevo = menu_archivo.Append(wx.ID_NEW, "Nueva reparación")
        menu_archivo.AppendSeparator()
        item_salir = menu_archivo.Append(wx.ID_EXIT, "Salir")
        
        menu_ayuda = wx.Menu()
        item_acerca = menu_ayuda.Append(wx.ID_ABOUT, "Acerca de")

        barra_menu.Append(menu_archivo, "Archivo")
        barra_menu.Append(menu_ayuda, "Ayuda")
        self.SetMenuBar(barra_menu)

        self.Bind(wx.EVT_MENU, self.on_salir, item_salir)
        self.Bind(wx.EVT_MENU, self.on_nueva_reparacion, self.item_nuevo)

    def on_nueva_reparacion(self, event):
        dialog = NuevaReparacionDialog(self)

        if dialog.ShowModal() == wx.ID_OK:
            datos = dialog.obtener_datos()

            # MODIFICADO: Guardamos en SQLite en vez de la memoria temporal.
            # Como el formulario solo pide 'Cliente' todo junto, lo mandamos a 'nombre' 
            # y ponemos 'S/D' (Sin Datos) en el DNI porque es obligatorio para la BD.
            try:
                nueva_rep = self.db.insertar_reparacion(
                    dni=f"S/D-{datos['cliente'][:3]}", # Parche temporal para que el DNI no choque como duplicado
                    nombre=datos["cliente"], 
                    apellido="", 
                    telefono="", 
                    num_serie=datos["serie"], 
                    modelo_marca=datos["equipo"], 
                    falla=datos["problema"]
                )
                
                self.reparaciones.append(nueva_rep)
                self.agregar_reparacion_lista(nueva_rep)
            except Exception as e:
                wx.MessageBox(f"Error al guardar en la base de datos: {e}", "Error", wx.OK | wx.ICON_ERROR)

        dialog.Destroy()

    def agregar_reparacion_lista(self, reparacion):
        """
        REQUISITO LISTCTRL: Función encargada de inyectar los datos en la grilla.
        """
        # MODIFICADO: Mantenemos el formato original de mi compañero pero con el ID real de SQLite
        codigo_orden = f"RD-2026-{reparacion.equipo_id:03d}"

        indice = self.lista.InsertItem(self.lista.GetItemCount(), codigo_orden)
        self.lista.SetItem(indice, 1, reparacion.cliente)
        self.lista.SetItem(indice, 2, reparacion.equipo)
        self.lista.SetItem(indice, 3, reparacion.estado)

    def on_salir(self, event):
        self.Close()