import wx

class NuevaReparacionDialog(wx.Dialog):
    """
    Ventana utilizada para registrar una nueva reparación.
    """

    def __init__(self, parent):
        super().__init__(
            parent,
            title="Nueva reparación",
            size=(600, 400)
        )

        panel = wx.Panel(self)
        sizer_principal = wx.BoxSizer(wx.VERTICAL)
        self.txt_dni = wx.TextCtrl(panel)
        self.txt_cliente = wx.TextCtrl(panel)
        self.txt_equipo = wx.TextCtrl(panel)
        self.txt_serie = wx.TextCtrl(panel)
        self.txt_problema = wx.TextCtrl(panel, style=wx.TE_MULTILINE)

        formulario = wx.FlexGridSizer(rows=5, cols=2, vgap=10, hgap=10)

        formulario.Add(wx.StaticText(panel, label="DNI:"), 0, wx.ALIGN_CENTER_VERTICAL)
        formulario.Add(self.txt_dni, 1, wx.EXPAND)

        formulario.Add(wx.StaticText(panel, label="Cliente:"), 0, wx.ALIGN_CENTER_VERTICAL)
        formulario.Add(self.txt_cliente, 1, wx.EXPAND)

        formulario.Add(wx.StaticText(panel, label="Equipo:"), 0, wx.ALIGN_CENTER_VERTICAL)
        formulario.Add(self.txt_equipo, 1, wx.EXPAND)

        formulario.Add(wx.StaticText(panel, label="N° Serie:"), 0, wx.ALIGN_CENTER_VERTICAL)
        formulario.Add(self.txt_serie, 1, wx.EXPAND)

        formulario.Add(wx.StaticText(panel, label="Problema:"), 0, wx.ALIGN_TOP)
        formulario.Add(self.txt_problema, 1, wx.EXPAND)

        formulario.AddGrowableCol(1, 1)
        formulario.AddGrowableRow(3, 1)

        # MODIFICADO: Le sacamos el wx.ID_OK automático para poder controlarlo nosotros
        btn_aceptar = wx.Button(panel, label="Aceptar")
        btn_aceptar.Bind(wx.EVT_BUTTON, self.on_aceptar)

        btn_cancelar = wx.Button(panel, wx.ID_CANCEL, "Cancelar")

        sizer_botones = wx.BoxSizer(wx.HORIZONTAL)
        sizer_botones.Add(btn_aceptar, 0, wx.RIGHT, 10)
        sizer_botones.Add(btn_cancelar, 0)

        sizer_principal.Add(formulario, 1, wx.ALL | wx.EXPAND, 15)
        sizer_principal.Add(sizer_botones, 0, wx.ALL | wx.ALIGN_RIGHT, 15)

        panel.SetSizer(sizer_principal)
        self.Centre()
    
    def on_aceptar(self, event):
        """
        Valida que los campos no estén vacíos antes de guardar.
        """
        dni = self.txt_dni.GetValue().strip()
        cliente = self.txt_cliente.GetValue().strip()
        equipo = self.txt_equipo.GetValue().strip()
        serie = self.txt_serie.GetValue().strip()
        problema = self.txt_problema.GetValue().strip()

        # Validación estricta
        if not dni or not cliente or not equipo or not serie or not problema:
            wx.MessageBox(
                "Hay campos sin completar. Debe rellenar todos los campos antes de guardar.", 
                "Error de validación", 
                wx.OK | wx.ICON_WARNING
            )
            return  # Corta la ejecución acá y no cierra la ventana

        # Si todo está bien, cierra la ventana mandando la señal de OK
        self.EndModal(wx.ID_OK)

    def obtener_datos(self):
        """
        Devuelve los datos limpios de espacios en blanco a los costados.
        """
        return {
            "dni": self.txt_dni.GetValue().strip(),
            "cliente": self.txt_cliente.GetValue().strip(),
            "equipo": self.txt_equipo.GetValue().strip(),
            "serie": self.txt_serie.GetValue().strip(),
            "problema": self.txt_problema.GetValue().strip()
        }