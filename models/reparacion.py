class Reparacion:
    """
    Molde para crear los objetos de cada reparación. 
    Lo armamos como una clase para mantener los datos ordenados en memoria 
    antes de mandarlos a la base de datos o mostrarlos en la tabla.
    """
    def __init__(
        self,
        equipo_id, # MODIFICADO: Cambiamos numero_orden por equipo_id para que coincida con el ID de SQLite
        cliente,
        equipo,
        serie,
        problema,
        estado="Pendiente", # Valores por defecto para que no tire error al instanciar
        diagnostico="",
        observaciones=""
    ):

        # Guardamos los atributos de la instancia
        self.equipo_id = equipo_id 
        self.cliente = cliente
        self.equipo = equipo
        self.serie = serie
        self.problema = problema
        self.estado = estado
        self.diagnostico = diagnostico
        self.observaciones = observaciones