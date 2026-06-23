import wx

from views.main_frame import MainFrame
from views.splash_screen import SplashScreen


class RepairDeskApp(wx.App):
    """
    Aplicación principal de RepairDesk.
    """

    def OnInit(self):
        """
        Muestra el splash screen al iniciar la aplicación.
        """

        # Crear y mostrar splash screen
        self.splash = SplashScreen()
        self.splash.Show()

        # Esperar 2 segundos antes de abrir la ventana principal
        wx.CallLater(
            2000,
            self.mostrar_ventana_principal
        )

        return True

    def mostrar_ventana_principal(self):
        """
        Cierra el splash screen y abre la ventana principal.
        """

        # Cerrar splash
        self.splash.Destroy()

        # Crear ventana principal
        self.frame = MainFrame()

        # Mostrar ventana principal
        self.frame.Show()


if __name__ == "__main__":

    # Crear aplicación
    app = RepairDeskApp()

    # Iniciar bucle principal
    app.MainLoop()