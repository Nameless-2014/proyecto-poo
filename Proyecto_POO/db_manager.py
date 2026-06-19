import sqlite3
from datetime import datetime
from models.reparacion import Reparacion

# NUEVO: Clase DatabaseManager que centraliza toda la gestión de la base de datos SQLite
class DatabaseManager:
    """
    Gestiona todas las operaciones con la base de datos SQLite para RepairDesk.
    Utiliza sentencias preparadas para prevenir inyección SQL.
    """
    
    def __init__(self, db_path="taller_pc.db"):
        # NUEVO: Ruta de la base de datos
        self.db_path = db_path
        # NUEVO: Inicializar las tablas al crear la instancia
        self._inicializar_base_de_datos()
    
    def _inicializar_base_de_datos(self):
        """
        NUEVO: Crea las tablas de clientes y equipos si no existen.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # NUEVO: Tabla de Clientes con estructura relacional
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dni TEXT UNIQUE NOT NULL,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    telefono TEXT
                )
            ''')
            
            # NUEVO: Tabla de Equipos vinculada a clientes mediante foreign key
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS equipos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_id INTEGER NOT NULL,
                    num_serie TEXT NOT NULL,
                    modelo_marca TEXT NOT NULL,
                    falla_reportada TEXT,
                    diagnostico TEXT DEFAULT '',
                    observaciones TEXT DEFAULT '',
                    estado TEXT DEFAULT 'Pendiente',
                    fecha_ingreso TEXT NOT NULL,
                    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
                )
            ''')
            
            conn.commit()
        finally:
            conn.close()
    
    def insertar_reparacion(self, dni, nombre, apellido, telefono, num_serie, modelo_marca, falla):
        """
        NUEVO: Inserta un nuevo cliente y su equipo. Maneja el ID de cliente automáticamente.
        Retorna el objeto Reparacion con el ID de equipos generado.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # NUEVO: Insertar o ignorar cliente (uso de INSERT OR IGNORE con sentencia preparada)
            cursor.execute('''
                INSERT OR IGNORE INTO clientes (dni, nombre, apellido, telefono) 
                VALUES (?, ?, ?, ?)
            ''', (dni, nombre, apellido, telefono))
            
            # NUEVO: Obtener el ID del cliente usando sentencia preparada
            cursor.execute("SELECT id FROM clientes WHERE dni = ?", (dni,))
            cliente_result = cursor.fetchone()
            
            if not cliente_result:
                raise Exception("No se pudo obtener el ID del cliente")
            
            cliente_id = cliente_result[0]
            
            # NUEVO: Registrar el equipo vinculado al cliente_id
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")
            cursor.execute('''
                INSERT INTO equipos (cliente_id, num_serie, modelo_marca, falla_reportada, fecha_ingreso)
                VALUES (?, ?, ?, ?, ?)
            ''', (cliente_id, num_serie, modelo_marca, falla, fecha_actual))
            
            # NUEVO: Obtener el ID del equipo recién insertado
            equipo_id = cursor.lastrowid
            
            conn.commit()
            
            # NUEVO: Retornar objeto Reparacion con todos los datos incluido el ID
            return Reparacion(
                equipo_id=equipo_id,
                cliente=f"{nombre} {apellido}",
                equipo=modelo_marca,
                serie=num_serie,
                problema=falla,
                estado="Pendiente",
                diagnostico="",
                observaciones=""
            )
            
        except sqlite3.Error as e:
            conn.rollback()
            raise Exception(f"Error al insertar reparación: {e}")
        finally:
            conn.close()
    
    def obtener_todas_reparaciones(self):
        """
        NUEVO: Obtiene todas las reparaciones con JOIN entre clientes y equipos.
        Retorna una lista de objetos Reparacion.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # NUEVO: Sentencia con JOIN para combinar datos de cliente y equipo
            cursor.execute('''
                SELECT e.id, c.nombre, c.apellido, e.modelo_marca, e.num_serie, 
                       e.estado, e.falla_reportada, e.diagnostico, e.observaciones
                FROM equipos e
                JOIN clientes c ON e.cliente_id = c.id
                ORDER BY e.fecha_ingreso DESC
            ''')
            
            resultados = cursor.fetchall()
            reparaciones = []
            
            # NUEVO: Convertir cada fila en objeto Reparacion
            for fila in resultados:
                equipo_id, nombre, apellido, modelo, serie, estado, falla, diagnostico, observaciones = fila
                reparacion = Reparacion(
                    equipo_id=equipo_id,
                    cliente=f"{nombre} {apellido}",
                    equipo=modelo,
                    serie=serie,
                    problema=falla,
                    estado=estado,
                    diagnostico=diagnostico,
                    observaciones=observaciones
                )
                reparaciones.append(reparacion)
            
            return reparaciones
        finally:
            conn.close()
    
    def buscar_reparaciones(self, criterio):
        """
        NUEVO: Busca reparaciones por DNI, Apellido o Número de Serie usando sentencias preparadas.
        Retorna una lista de objetos Reparacion que coinciden con el criterio.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # NUEVO: Sentencia preparada con LIKE para búsqueda flexible
            parametro = f"%{criterio}%"
            cursor.execute('''
                SELECT e.id, c.nombre, c.apellido, e.modelo_marca, e.num_serie, 
                       e.estado, e.falla_reportada, e.diagnostico, e.observaciones, c.dni
                FROM equipos e
                JOIN clientes c ON e.cliente_id = c.id
                WHERE c.dni LIKE ? OR c.apellido LIKE ? OR c.nombre LIKE ? OR e.num_serie LIKE ?
                ORDER BY e.fecha_ingreso DESC
            ''', (parametro, parametro, parametro, parametro))
            
            resultados = cursor.fetchall()
            reparaciones = []
            
            # NUEVO: Convertir resultados a objetos Reparacion
            for fila in resultados:
                equipo_id, nombre, apellido, modelo, serie, estado, falla, diagnostico, observaciones, dni = fila
                reparacion = Reparacion(
                    equipo_id=equipo_id,
                    cliente=f"{nombre} {apellido}",
                    equipo=modelo,
                    serie=serie,
                    problema=falla,
                    estado=estado,
                    diagnostico=diagnostico,
                    observaciones=observaciones
                )
                reparaciones.append(reparacion)
            
            return reparaciones
        finally:
            conn.close()
    
    def actualizar_reparacion(self, equipo_id, estado, diagnostico, observaciones):
        """
        NUEVO: Actualiza el estado, diagnóstico y observaciones de una reparación.
        Utiliza sentencia preparada con el equipo_id como identificador único.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # NUEVO: UPDATE usando sentencia preparada con equipo_id
            cursor.execute('''
                UPDATE equipos
                SET estado = ?, diagnostico = ?, observaciones = ?
                WHERE id = ?
            ''', (estado, diagnostico, observaciones, equipo_id))
            
            conn.commit()
            
            # NUEVO: Retornar True si se actualizó alguna fila
            return cursor.rowcount > 0
            
        except sqlite3.Error as e:
            conn.rollback()
            raise Exception(f"Error al actualizar reparación: {e}")
        finally:
            conn.close()
    
    def obtener_reparacion_por_id(self, equipo_id):
        """
        NUEVO: Obtiene una reparación específica por su ID de equipo.
        Retorna un objeto Reparacion o None si no existe.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # NUEVO: Sentencia preparada para obtener reparación por ID
            cursor.execute('''
                SELECT e.id, c.nombre, c.apellido, e.modelo_marca, e.num_serie, 
                       e.estado, e.falla_reportada, e.diagnostico, e.observaciones
                FROM equipos e
                JOIN clientes c ON e.cliente_id = c.id
                WHERE e.id = ?
            ''', (equipo_id,))
            
            resultado = cursor.fetchone()
            
            if not resultado:
                return None
            
            # NUEVO: Convertir resultado a objeto Reparacion
            equipo_id, nombre, apellido, modelo, serie, estado, falla, diagnostico, observaciones = resultado
            return Reparacion(
                equipo_id=equipo_id,
                cliente=f"{nombre} {apellido}",
                equipo=modelo,
                serie=serie,
                problema=falla,
                estado=estado,
                diagnostico=diagnostico,
                observaciones=observaciones
            )
        finally:
            conn.close()
