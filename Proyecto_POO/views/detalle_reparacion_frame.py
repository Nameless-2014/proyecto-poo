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
        # MODIFICADO: Generamos el código de orden visual usando el ID real de la base de datos
        # Así mantenemos el formato original (Ej: RD-2026-001)
        codigo_orden = f"RD-2026-{reparacion.equipo_id:03d}"

        super().__init__(
            parent=None,
            title=f"Detalle - {codigo_orden}",
            size=(700, 600)
        )

        self.main_frame = main_frame
        self.reparacion = reparacion
        self.indice = indice

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        titulo = wx.StaticText(panel, label="Detalle de reparación")
        fuente = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        titulo.SetFont(fuente)

        sizer.Add(titulo, 0, wx.ALL, 10)

        # MODIFICADO: Actualizamos la etiqueta para mostrar el nuevo código de orden
        sizer.Add(wx.StaticText(panel, label=f"Orden: {codigo_orden}"), 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        sizer.Add(wx.StaticText(panel, label=f"Cliente: {reparacion.cliente}"), 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        sizer.Add(wx.StaticText(panel, label=f"Equipo: {reparacion.equipo}"), 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        sizer.Add(wx.StaticText(panel, label=f"Serie: {reparacion.serie}"), 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)
        sizer.Add(wx.StaticText(panel, label=f"Problema informado: {reparacion.problema}"), 0, wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        sizer.Add(wx.StaticText(panel, label="Estado:"), 0, wx.LEFT | wx.RIGHT | wx.TOP, 10)

        self.cmb_estado = wx.ComboBox(
            panel,
            choices=["Pendiente", "En diagnóstico", "Reparando", "Finalizado", "Entregado"],
            style=wx.CB_READONLY
        )
        self.cmb_estado.SetValue(reparacion.estado)
        sizer.Add(self.cmb_estado, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        sizer.Add(wx.StaticText(panel, label="Diagnóstico:"), 0, wx.LEFT | wx.RIGHT | wx.TOP, 10)

        self.txt_diagnostico = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        self.txt_diagnostico.SetValue(reparacion.diagnostico)
        sizer.Add(self.txt_diagnostico, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        sizer.Add(wx.StaticText(panel, label="Observaciones:"), 0, wx.LEFT | wx.RIGHT | wx.TOP, 10)

        self.txt_observaciones = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        self.txt_observaciones.SetValue(reparacion.observaciones)
        sizer.Add(self.txt_observaciones, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        btn_guardar = wx.Button(panel, label="Guardar cambios")
        btn_guardar.Bind(wx.EVT_BUTTON, self.on_guardar)
        sizer.Add(btn_guardar, 0, wx.ALIGN_RIGHT | wx.ALL, 10)

        panel.SetSizer(sizer)

    def on_guardar(self, event):
        """
        Guarda los cambios realizados en la reparación y los manda a SQLite.
        """
        nuevo_estado = self.cmb_estado.GetValue()
        nuevo_diagnostico = self.txt_diagnostico.GetValue()
        nuevas_observaciones = self.txt_observaciones.GetValue()

        try:
            # NUEVO: Le pedimos a la conexión de base de datos que ya tenemos en MainFrame que haga el UPDATE
            self.main_frame.db.actualizar_reparacion(
                self.reparacion.equipo_id,
                nuevo_estado,
                nuevo_diagnostico,
                nuevas_observaciones
            )

            # Si SQLite guardó bien, actualizamos el objeto en memoria para que la tabla principal no quede desfasada
            self.reparacion.estado = nuevo_estado
            self.reparacion.diagnostico = nuevo_diagnostico
            self.reparacion.observaciones = nuevas_observaciones

            # Actualizamos visualmente el ListCtrl de la ventana principal
            self.main_frame.lista.SetItem(self.indice, 3, self.reparacion.estado)

            wx.MessageBox("Cambios guardados correctamente en la base de datos.", "RepairDesk", wx.OK | wx.ICON_INFORMATION)
            
            # MODIFICADO: Cerramos la ventana automáticamente después de guardar para que sea más cómodo
            self.Close()

        except Exception as e:
            # En caso de que falle la escritura en el archivo local de la DB
            wx.MessageBox(f"Error al guardar en la base de datos: {e}", "Error", wx.OK | wx.ICON_ERROR)