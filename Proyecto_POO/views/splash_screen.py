import wx


class SplashScreen(wx.Frame):
    """
    Pantalla de inicio de RepairDesk.

    Se muestra durante unos segundos antes de abrir
    la ventana principal de la aplicación.
    """

    def __init__(self):

        super().__init__(
            parent=None,
            title="RepairDesk",
            size=(450, 250)
        )

        # Panel principal
        panel = wx.Panel(self)

        # Contenedor principal
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Título de la aplicación
        titulo = wx.StaticText(
            panel,
            label="RepairDesk"
        )

        # Configurar fuente del título
        fuente_titulo = titulo.GetFont()
        fuente_titulo.SetPointSize(20)
        fuente_titulo.SetWeight(wx.FONTWEIGHT_BOLD)

        titulo.SetFont(fuente_titulo)

        # Subtítulo
        subtitulo = wx.StaticText(
            panel,
            label="Sistema de Gestión de Reparaciones"
        )

        # Texto de carga
        texto_carga = wx.StaticText(
            panel,
            label="Cargando..."
        )

        # Espacio superior
        sizer.AddStretchSpacer()

        # Agregar título
        sizer.Add(
            titulo,
            0,
            wx.ALIGN_CENTER
        )

        # Agregar subtítulo
        sizer.Add(
            subtitulo,
            0,
            wx.ALIGN_CENTER | wx.TOP,
            10
        )

        # Agregar texto de carga
        sizer.Add(
            texto_carga,
            0,
            wx.ALIGN_CENTER | wx.TOP,
            25
        )

        # Espacio inferior
        sizer.AddStretchSpacer()

        # Asociar sizer al panel
        panel.SetSizer(sizer)

        # Recalcular distribución visual
        panel.Layout()

        # Centrar ventana en pantalla
        self.Centre()