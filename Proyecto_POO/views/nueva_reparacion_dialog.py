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

        # Panel principal
        panel = wx.Panel(self)

        # Contenedor principal
        sizer_principal = wx.BoxSizer(wx.VERTICAL)

        # Campos del formulario
        self.txt_cliente = wx.TextCtrl(panel)
        self.txt_equipo = wx.TextCtrl(panel)
        self.txt_serie = wx.TextCtrl(panel)

        self.txt_problema = wx.TextCtrl(
            panel,
            style=wx.TE_MULTILINE
        )

        # Formulario
        formulario = wx.FlexGridSizer(
            rows=4,
            cols=2,
            vgap=10,
            hgap=10
        )

        formulario.Add(
            wx.StaticText(panel, label="Cliente:"),
            0,
            wx.ALIGN_CENTER_VERTICAL
        )

        formulario.Add(
            self.txt_cliente,
            1,
            wx.EXPAND
        )

        formulario.Add(
            wx.StaticText(panel, label="Equipo:"),
            0,
            wx.ALIGN_CENTER_VERTICAL
        )

        formulario.Add(
            self.txt_equipo,
            1,
            wx.EXPAND
        )

        formulario.Add(
            wx.StaticText(panel, label="N° Serie:"),
            0,
            wx.ALIGN_CENTER_VERTICAL
        )

        formulario.Add(
            self.txt_serie,
            1,
            wx.EXPAND
        )

        formulario.Add(
            wx.StaticText(panel, label="Problema:"),
            0,
            wx.ALIGN_TOP
        )

        formulario.Add(
            self.txt_problema,
            1,
            wx.EXPAND
        )

        formulario.AddGrowableCol(1, 1)
        formulario.AddGrowableRow(3, 1)

        # Botones
        btn_aceptar = wx.Button(
            panel,
            wx.ID_OK,
            "Aceptar"
        )

        btn_cancelar = wx.Button(
            panel,
            wx.ID_CANCEL,
            "Cancelar"
        )

        sizer_botones = wx.BoxSizer(wx.HORIZONTAL)

        sizer_botones.Add(
            btn_aceptar,
            0,
            wx.RIGHT,
            10
        )

        sizer_botones.Add(
            btn_cancelar,
            0
        )

        # Organización visual
        sizer_principal.Add(
            formulario,
            1,
            wx.ALL | wx.EXPAND,
            15
        )

        sizer_principal.Add(
            sizer_botones,
            0,
            wx.ALL | wx.ALIGN_RIGHT,
            15
        )

        panel.SetSizer(sizer_principal)

        self.Centre()
    
    def obtener_datos(self):
        """
        Devuelve los datos ingresados en el formulario.
        """

        return {
            "cliente": self.txt_cliente.GetValue(),
            "equipo": self.txt_equipo.GetValue(),
            "serie": self.txt_serie.GetValue(),
            "problema": self.txt_problema.GetValue()
        }