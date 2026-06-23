import wx
import os
from datetime import datetime

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

       
        sizer_botones = wx.BoxSizer(wx.HORIZONTAL)
        
        btn_comprobante = wx.Button(panel, label="Generar Comprobante")
        btn_comprobante.Bind(wx.EVT_BUTTON, self.on_generar_comprobante)
        
        btn_guardar = wx.Button(panel, label="Guardar cambios")
        btn_guardar.Bind(wx.EVT_BUTTON, self.on_guardar)
        
        sizer_botones.Add(btn_comprobante, 0, wx.RIGHT, 10)
        sizer_botones.Add(btn_guardar, 0, wx.LEFT, 0)

        sizer.Add(sizer_botones, 0, wx.ALIGN_RIGHT | wx.ALL, 10)

        panel.SetSizer(sizer)

    def on_guardar(self, event):
        """
        Guarda los cambios realizados en la reparación y los manda a SQLite.
        """
        nuevo_estado = self.cmb_estado.GetValue()
        nuevo_diagnostico = self.txt_diagnostico.GetValue()
        nuevas_observaciones = self.txt_observaciones.GetValue()

        try:
            self.main_frame.db.actualizar_reparacion(
                self.reparacion.equipo_id,
                nuevo_estado,
                nuevo_diagnostico,
                nuevas_observaciones
            )

            self.reparacion.estado = nuevo_estado
            self.reparacion.diagnostico = nuevo_diagnostico
            self.reparacion.observaciones = nuevas_observaciones

           
            estado_visual = nuevo_estado

            if nuevo_estado == "Pendiente":
                estado_visual = "⏳ Pendiente"
            elif nuevo_estado == "En diagnóstico":
                estado_visual = "🔍 En diagnóstico"
            elif nuevo_estado == "Reparando":
                estado_visual = "🔧 Reparando"
            elif nuevo_estado == "Finalizado":
                estado_visual = "✅ Finalizado"
            elif nuevo_estado == "Entregado":
                estado_visual = "📦 Entregado"

            self.main_frame.lista.SetItem(
                self.indice,
                3,
                estado_visual
            )

            wx.MessageBox("Cambios guardados correctamente en la base de datos.", "RepairDesk", wx.OK | wx.ICON_INFORMATION)
            self.Close()

        except Exception as e:
            wx.MessageBox(f"Error al guardar en la base de datos: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def on_generar_comprobante(self, event):
        """
        Genera un comprobante en formato .txt y lo abre automáticamente.
        """
        codigo_orden = f"RD-2026-{self.reparacion.equipo_id:03d}"
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")

        ticket = f"""
=========================================
          REPAIR DESK - SERVICIO TÉCNICO
=========================================
Fecha: {fecha_actual}
Orden N°: {codigo_orden}
-----------------------------------------
DATOS DEL CLIENTE
Cliente: {self.reparacion.cliente}
-----------------------------------------
DATOS DEL EQUIPO
Equipo: {self.reparacion.equipo}
N° Serie: {self.reparacion.serie}
Problema: {self.reparacion.problema}
-----------------------------------------
ESTADO ACTUAL
Estado: {self.cmb_estado.GetValue()}
Diagnóstico: {self.txt_diagnostico.GetValue() if self.txt_diagnostico.GetValue() else 'S/D'}
=========================================
Conserve este comprobante para retirar
su equipo. ¡Gracias por confiar en nosotros!
=========================================
"""
        nombre_archivo = f"Comprobante_{codigo_orden}.txt"

        try:
            with open(nombre_archivo, "w", encoding="utf-8") as file:
                file.write(ticket)
            os.startfile(nombre_archivo)
        except Exception as e:
            wx.MessageBox(f"Error al generar el comprobante: {e}", "Error", wx.OK | wx.ICON_ERROR)