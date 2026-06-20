import wx
import os


class SplashScreen(wx.Frame):
    """
    Pantalla de inicio de RepairDesk.

    Muestra una imagen de presentación antes
    de abrir la ventana principal.
    """

    def __init__(self):

        super().__init__(
            parent=None,
            title="RepairDesk",

            # Ventana sin bordes
            style=wx.FRAME_NO_TASKBAR
            | wx.STAY_ON_TOP
            | wx.BORDER_NONE
        )

        # Panel principal
        panel = wx.Panel(self)

        # Fondo negro por si la imagen tarda en cargar
        panel.SetBackgroundColour(wx.BLACK)

        # --------------------------------------------------
        # Ruta absoluta de la carpeta Proyecto_POO
        # --------------------------------------------------

        ruta_base = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        # --------------------------------------------------
        # Ruta de la imagen splash
        # --------------------------------------------------

        ruta_imagen = os.path.join(
            ruta_base,
            "assets",
            "RepairDeskSplash.png"
        )

        # --------------------------------------------------
        # Verificación para depuración
        # --------------------------------------------------

        print(f"[Splash] Imagen: {ruta_imagen}")
        print(f"[Splash] Existe: {os.path.exists(ruta_imagen)}")

        # --------------------------------------------------
        # Si la imagen no existe
        # --------------------------------------------------

        if not os.path.exists(ruta_imagen):

            mensaje = wx.StaticText(
                panel,
                label="No se encontró RepairDeskSplash.png"
            )

            sizer_error = wx.BoxSizer(wx.VERTICAL)

            sizer_error.AddStretchSpacer()

            sizer_error.Add(
                mensaje,
                0,
                wx.ALIGN_CENTER
            )

            sizer_error.AddStretchSpacer()

            panel.SetSizer(sizer_error)

            self.Centre()

            return

        # --------------------------------------------------
        # Cargar imagen
        # --------------------------------------------------

        imagen = wx.Image(
            ruta_imagen,
            wx.BITMAP_TYPE_PNG
        )

        # --------------------------------------------------
        # Tamaño original de la imagen
        # --------------------------------------------------

        ancho = imagen.GetWidth()
        alto = imagen.GetHeight()

        print(
            f"[Splash] Imagen original: {ancho}x{alto}"
        )

        # --------------------------------------------------
        # Escalar manteniendo proporción
        # --------------------------------------------------

        ancho_maximo = 700
        alto_maximo = 400

        factor = min(
            ancho_maximo / ancho,
            alto_maximo / alto
        )

        nuevo_ancho = int(ancho * factor)
        nuevo_alto = int(alto * factor)

        imagen = imagen.Scale(
            nuevo_ancho,
            nuevo_alto,
            wx.IMAGE_QUALITY_HIGH
        )

        # --------------------------------------------------
        # Crear bitmap
        # --------------------------------------------------

        bitmap = wx.StaticBitmap(
            panel,
            wx.ID_ANY,
            wx.Bitmap(imagen)
        )

        # --------------------------------------------------
        # Layout principal
        # --------------------------------------------------

        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(
            bitmap,
            1,
            wx.ALIGN_CENTER | wx.ALL,
            0
        )

        panel.SetSizer(sizer)

        # --------------------------------------------------
        # Ajustar tamaño real de la ventana
        # --------------------------------------------------

        self.SetClientSize(
            (nuevo_ancho, nuevo_alto)
        )

        # Centrar splash
        self.Centre()