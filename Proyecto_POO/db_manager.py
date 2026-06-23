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
        self.db_path = db_path
        self._inicializar_base_de_datos()
    
    def _inicializar_base_de_datos(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dni TEXT UNIQUE NOT NULL,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    telefono TEXT
                )
            ''')
            
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
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO clientes (dni, nombre, apellido, telefono) 
                VALUES (?, ?, ?, ?)
            ''', (dni, nombre, apellido, telefono))
            
            cursor.execute("SELECT id FROM clientes WHERE dni = ?", (dni,))
            cliente_result = cursor.fetchone()
            
            if not cliente_result:
                raise Exception("No se pudo obtener el ID del cliente")
            
            cliente_id = cliente_result[0]
            
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")
            cursor.execute('''
                INSERT INTO equipos (cliente_id, num_serie, modelo_marca, falla_reportada, fecha_ingreso)
                VALUES (?, ?, ?, ?, ?)
            ''', (cliente_id, num_serie, modelo_marca, falla, fecha_actual))
            
            equipo_id = cursor.lastrowid
            conn.commit()
            
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
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT e.id, c.nombre, c.apellido, e.modelo_marca, e.num_serie, 
                       e.estado, e.falla_reportada, e.diagnostico, e.observaciones
                FROM equipos e
                JOIN clientes c ON e.cliente_id = c.id
                ORDER BY e.fecha_ingreso DESC
            ''')
            
            resultados = cursor.fetchall()
            reparaciones = []
            
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
        Busca reparaciones por DNI, Apellido, Nombre, Número de Serie, Estado o Número de Orden.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            parametro = f"%{criterio}%"
            
            # Agregamos OR e.estado LIKE ? y OR e.id LIKE ? para incluir estado y orden en el filtro
            cursor.execute('''
                SELECT e.id, c.nombre, c.apellido, e.modelo_marca, e.num_serie, 
                       e.estado, e.falla_reportada, e.diagnostico, e.observaciones, c.dni
                FROM equipos e
                JOIN clientes c ON e.cliente_id = c.id
                WHERE c.dni LIKE ? 
                   OR c.apellido LIKE ? 
                   OR c.nombre LIKE ? 
                   OR e.num_serie LIKE ?
                   OR e.estado LIKE ?
                   OR e.id LIKE ?
                ORDER BY e.fecha_ingreso DESC
            ''', (parametro, parametro, parametro, parametro, parametro, parametro)) # Ahora son 6 parámetros
            
            resultados = cursor.fetchall()
            reparaciones = []
            
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
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE equipos
                SET estado = ?, diagnostico = ?, observaciones = ?
                WHERE id = ?
            ''', (estado, diagnostico, observaciones, equipo_id))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except sqlite3.Error as e:
            conn.rollback()
            raise Exception(f"Error al actualizar reparación: {e}")
        finally:
            conn.close()
    
    def obtener_reparacion_por_id(self, equipo_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
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

    # NUEVO METODO PARA ELIMINAR
    def eliminar_reparacion(self, equipo_id):
        """
        Elimina un registro de reparación específico de la base de datos.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM equipos WHERE id = ?', (equipo_id,))
            conn.commit()
        except sqlite3.Error as e:
            conn.rollback()
            raise Exception(f"Error al eliminar reparación: {e}")
        finally:
            conn.close()