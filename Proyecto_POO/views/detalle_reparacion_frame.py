import wx


class DetalleReparacionFrame(wx.Frame):
    """
    Ventana que muestra los detalles de una reparación.
    """

    def __init__(
        self,
        main_frame,
        reparacion,
        indice
    ):

        super().__init__(
            parent=None,
            title=f"Detalle - {reparacion.numero_orden}",
            size=(700, 600)
        )

        # Ventana principal
        self.main_frame = main_frame

        # Reparación seleccionada
        self.reparacion = reparacion

        # Índice dentro de la tabla
        self.indice = indice

        # Guardar referencia a la reparación
        self.reparacion = reparacion

        # Panel principal
        panel = wx.Panel(self)

        # Contenedor principal
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Título
        titulo = wx.StaticText(
            panel,
            label="Detalle de reparación"
        )

        fuente = wx.Font(
            12,
            wx.FONTFAMILY_DEFAULT,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD
        )

        titulo.SetFont(fuente)

        sizer.Add(
            titulo,
            0,
            wx.ALL,
            10
        )

        # Información básica
        sizer.Add(
            wx.StaticText(
                panel,
                label=f"Orden: {reparacion.numero_orden}"
            ),
            0,
            wx.LEFT | wx.RIGHT | wx.BOTTOM,
            10
        )

        sizer.Add(
            wx.StaticText(
                panel,
                label=f"Cliente: {reparacion.cliente}"
            ),
            0,
            wx.LEFT | wx.RIGHT | wx.BOTTOM,
            10
        )

        sizer.Add(
            wx.StaticText(
                panel,
                label=f"Equipo: {reparacion.equipo}"
            ),
            0,
            wx.LEFT | wx.RIGHT | wx.BOTTOM,
            10
        )

        sizer.Add(
            wx.StaticText(
                panel,
                label=f"Serie: {reparacion.serie}"
            ),
            0,
            wx.LEFT | wx.RIGHT | wx.BOTTOM,
            10
        )

        sizer.Add(
            wx.StaticText(
                panel,
                label=f"Problema informado: {reparacion.problema}"
            ),
            0,
            wx.LEFT | wx.RIGHT | wx.BOTTOM,
            10
        )

        # Estado de la reparación
        sizer.Add(
            wx.StaticText(
                panel,
                label="Estado:"
            ),
            0,
            wx.LEFT | wx.RIGHT | wx.TOP,
            10
        )

        self.cmb_estado = wx.ComboBox(
            panel,
            choices=[
                "Pendiente",
                "En diagnóstico",
                "Reparando",
                "Finalizado",
                "Entregado"
            ],
            style=wx.CB_READONLY
        )

        self.cmb_estado.SetValue(reparacion.estado)

        sizer.Add(
            self.cmb_estado,
            0,
            wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM,
            10
        )

        # Diagnóstico técnico
        sizer.Add(
            wx.StaticText(
                panel,
                label="Diagnóstico:"
            ),
            0,
            wx.LEFT | wx.RIGHT | wx.TOP,
            10
        )

        self.txt_diagnostico = wx.TextCtrl(
            panel,
            style=wx.TE_MULTILINE
        )

        # Mostrar diagnóstico existente
        self.txt_diagnostico.SetValue(
            reparacion.diagnostico
        )

        sizer.Add(
            self.txt_diagnostico,
            1,
            wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM,
            10
        )

        # Observaciones
        sizer.Add(
            wx.StaticText(
                panel,
                label="Observaciones:"
            ),
            0,
            wx.LEFT | wx.RIGHT | wx.TOP,
            10
        )

        self.txt_observaciones = wx.TextCtrl(
            panel,
            style=wx.TE_MULTILINE
        )

        # Mostrar observaciones existentes
        self.txt_observaciones.SetValue(
            reparacion.observaciones
        )

        sizer.Add(
            self.txt_observaciones,
            1,
            wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM,
            10
        )

        # Botón guardar
        btn_guardar = wx.Button(
            panel,
            label="Guardar cambios"
        )
        
        btn_guardar.Bind(
            wx.EVT_BUTTON,
            self.on_guardar
        )

        sizer.Add(
            btn_guardar,
            0,
            wx.ALIGN_RIGHT | wx.ALL,
            10
        )

        panel.SetSizer(sizer)

    def on_guardar(self, event):
        """
        Guarda los cambios realizados en la reparación.
        """

        # Actualizar estado
        self.reparacion.estado = (
            self.cmb_estado.GetValue()
        )

        # Actualizar tabla principal
        self.main_frame.lista.SetItem(
            self.indice,
            3,
            self.reparacion.estado
        )

        wx.MessageBox(
            "Cambios guardados correctamente.",
            "RepairDesk",
            wx.OK | wx.ICON_INFORMATION
        )

        self.Centre()