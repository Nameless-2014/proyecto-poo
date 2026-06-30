import wx
from datetime import datetime

class ComprobantePrintout(wx.Printout):
    """
    Clase que hereda de wx.Printout para dibujar manualmente 
    el comprobante usando un Device Context (DC).
    """
    def __init__(self, reparacion, estado_actual, diagnostico_actual):
        super().__init__("Comprobante de Reparación")
        self.reparacion = reparacion
        self.estado_actual = estado_actual
        self.diagnostico_actual = diagnostico_actual

    def OnPrintPage(self, page):
        """
        Este método es llamado por el sistema para dibujar la página.
        """
        dc = self.GetDC()

        #corrige la escala porque se veia muy chiquito el comprobante al imprimirlo como PDF
        ppi_pantalla = self.GetPPIScreen()
        ppi_impresora = self.GetPPIPrinter()
        escala_x = ppi_impresora[0] / ppi_pantalla[0]
        escala_y = ppi_impresora[1] / ppi_pantalla[1]
        dc.SetUserScale(escala_x, escala_y)
        
        # Configurar las fuentes que vamos a usar como "pinceles"
        fuente_titulo = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        fuente_normal = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        fuente_chica = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL)

        codigo_orden = f"RD-2026-{self.reparacion.equipo_id:03d}"
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")

        # Configurar coordenadas iniciales (X, Y)
        x_margin = 50
        y_pos = 50
        salto_linea = 30

        # --- TÍTULO ---
        dc.SetFont(fuente_titulo)
        dc.DrawText("REPAIR DESK - SERVICIO TÉCNICO", x_margin, y_pos)
        y_pos += salto_linea * 2

        # --- CABECERA ---
        dc.SetFont(fuente_normal)
        dc.DrawText(f"Fecha: {fecha_actual}", x_margin, y_pos)
        y_pos += salto_linea
        dc.DrawText(f"Orden N°: {codigo_orden}", x_margin, y_pos)
        y_pos += salto_linea * 2

        # --- DATOS CLIENTE ---
        dc.SetFont(fuente_titulo)
        dc.DrawText("DATOS DEL CLIENTE", x_margin, y_pos)
        y_pos += salto_linea
        dc.SetFont(fuente_normal)
        dc.DrawText(f"Cliente: {self.reparacion.cliente}", x_margin, y_pos)
        y_pos += salto_linea * 2

        # --- DATOS EQUIPO ---
        dc.SetFont(fuente_titulo)
        dc.DrawText("DATOS DEL EQUIPO", x_margin, y_pos)
        y_pos += salto_linea
        dc.SetFont(fuente_normal)
        dc.DrawText(f"Equipo: {self.reparacion.equipo}", x_margin, y_pos)
        y_pos += salto_linea
        dc.DrawText(f"N° Serie: {self.reparacion.serie}", x_margin, y_pos)
        y_pos += salto_linea
        dc.DrawText(f"Falla: {self.reparacion.problema}", x_margin, y_pos)
        y_pos += salto_linea * 2

        # --- ESTADO ---
        dc.SetFont(fuente_titulo)
        dc.DrawText("ESTADO ACTUAL", x_margin, y_pos)
        y_pos += salto_linea
        dc.SetFont(fuente_normal)
        dc.DrawText(f"Estado: {self.estado_actual}", x_margin, y_pos)
        y_pos += salto_linea
        dc.DrawText(f"Diagnóstico: {self.diagnostico_actual}", x_margin, y_pos)
        y_pos += salto_linea * 3

        # --- PIE DE PÁGINA ---
        dc.SetFont(fuente_chica)
        dc.DrawText("Conserve este comprobante para retirar su equipo.", x_margin, y_pos)
        y_pos += 20
        dc.DrawText("¡Gracias por confiar en nosotros!", x_margin, y_pos)

        return True # Devuelve True indicando que la página se dibujó con éxito

    def HasPage(self, pageNum):
        # Como es un comprobante simple, solo tenemos la página 1
        return pageNum == 1

    def GetPageInfo(self):
        # (minPage, maxPage, pageFrom, pageTo)
        return (1, 1, 1, 1)