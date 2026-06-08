class Reparacion:
    """
    Representa una reparación registrada dentro del sistema.
    Almacena los datos principales de una computadora
    ingresada al taller.
    """
    def __init__(
        self,
        numero_orden,
        cliente,
        equipo,
        serie,
        problema,
        estado="Pendiente",
        diagnostico="",
        observaciones=""
    ):

        self.numero_orden = numero_orden
        self.cliente = cliente
        self.equipo = equipo
        self.serie = serie
        self.problema = problema
        self.estado = estado
        self.diagnostico = diagnostico
        self.observaciones = observaciones