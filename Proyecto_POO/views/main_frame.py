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
        super().__init__(parent=None, title="RepairDesk", size=(900, 600))

        base_path = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_path, "..", "assets", "IcoDesk.ico")
        self.SetIcon(wx.Icon(icon_path, wx.BITMAP_TYPE_ICO))

        self.crear_menu()
        
        self.db = DatabaseManager()
        self.reparaciones = self.db.obtener_todas_reparaciones()

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        titulo = wx.StaticText(panel, label="Reparaciones registradas")
        fuente = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        titulo.SetFont(fuente)

        self.txt_buscar = wx.SearchCtrl(panel, style=wx.TE_PROCESS_ENTER)
        self.txt_buscar.SetDescriptiveText("Buscar por cliente, equipo o serie...")
        self.txt_buscar.Bind(wx.EVT_TEXT, self.on_buscar)

        self.lista = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self.lista.InsertColumn(0, "Orden", width=120)
        self.lista.InsertColumn(1, "Cliente", width=180)
        self.lista.InsertColumn(2, "Equipo", width=180)
        self.lista.InsertColumn(3, "Estado", width=120)

        for rep in self.reparaciones:
            self.agregar_reparacion_lista(rep)

        sizer.Add(titulo, 0, wx.ALL, 10)
        sizer.Add(self.txt_buscar, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        sizer.Add(self.lista, 1, wx.EXPAND | wx.ALL, 10)

        panel.SetSizer(sizer)

        self.lista.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_abrir_detalle)
        # NUEVO: Detectar el clic derecho en un elemento de la lista
        self.lista.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.on_click_derecho)
        
        self.Centre()

    def on_buscar(self, event):
        criterio = self.txt_buscar.GetValue()
        self.reparaciones = self.db.buscar_reparaciones(criterio)
        
        self.lista.DeleteAllItems()
        for rep in self.reparaciones:
            self.agregar_reparacion_lista(rep)

    def on_abrir_detalle(self, event):
        indice = event.GetIndex()
        reparacion = self.reparaciones[indice]
        ventana = DetalleReparacionFrame(self, reparacion, indice)
        ventana.Show()

    # NUEVO: Menú contextual al hacer clic derecho
    def on_click_derecho(self, event):
        self.indice_seleccionado = event.GetIndex()
        
        menu = wx.Menu()
        item_eliminar = menu.Append(wx.ID_ANY, "Eliminar")
        self.Bind(wx.EVT_MENU, self.on_eliminar_reparacion, item_eliminar)
        
        self.PopupMenu(menu)
        menu.Destroy()

    # NUEVO: Lógica de eliminación con confirmación
    def on_eliminar_reparacion(self, event):
        if not hasattr(self, 'indice_seleccionado'):
            return
            
        reparacion = self.reparaciones[self.indice_seleccionado]
        
        # Cartel de confirmación (wx.YES_NO genera los botones Sí y No)
        respuesta = wx.MessageBox(
            "¿Estás seguro que deseas eliminar al cliente/equipo? Esta acción no se puede revertir.",
            "Confirmar eliminación",
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION
        )
        
        if respuesta == wx.YES:
            try:
                # Borramos de SQLite
                self.db.eliminar_reparacion(reparacion.equipo_id)
                
                # Borramos de la lista en memoria
                del self.reparaciones[self.indice_seleccionado]
                
                # Borramos de la pantalla visualmente
                self.lista.DeleteItem(self.indice_seleccionado)
                
                wx.MessageBox("Cliente eliminado con éxito.", "Eliminado", wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"Error al eliminar en la base de datos: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def crear_menu(self):
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

            try:
                nueva_rep = self.db.insertar_reparacion(
                    dni=f"S/D-{datos['cliente'][:3]}",
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
        codigo_orden = f"RD-2026-{reparacion.equipo_id:03d}"

        indice = self.lista.InsertItem(self.lista.GetItemCount(), codigo_orden)
        self.lista.SetItem(indice, 1, reparacion.cliente)
        self.lista.SetItem(indice, 2, reparacion.equipo)
        self.lista.SetItem(indice, 3, reparacion.estado)

    def on_salir(self, event):
        self.Close()