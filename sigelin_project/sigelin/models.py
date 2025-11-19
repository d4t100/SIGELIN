from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class Auditoria(models.Model):
    id = models.UUIDField(primary_key=True)
    tabla = models.CharField(max_length=50)
    operacion = models.CharField(max_length=20)
    id_registro = models.UUIDField(blank=True, null=True)
    usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, blank=True, null=True)
    datos_anteriores = models.JSONField(blank=True, null=True)
    datos_nuevos = models.JSONField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auditoria'
        db_table_comment = 'Registro de auditorÝa de todas las operaciones crÝticas del sistema'


class ComprasRepuesto(models.Model):
    id = models.UUIDField(primary_key=True)
    nro_orden = models.CharField(unique=True, max_length=50, blank=True, null=True)
    fecha_solicitud = models.DateTimeField(blank=True, null=True)
    fecha_aprobacion = models.DateTimeField(blank=True, null=True)
    fecha_recepcion = models.DateTimeField(blank=True, null=True)
    estado = models.TextField(blank=True, null=True)  # This field type is a guess.
    proveedor = models.CharField(max_length=150, blank=True, null=True)
    contacto_proveedor = models.CharField(max_length=255, blank=True, null=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    id_solicitante = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_solicitante', blank=True, null=True)
    id_aprobador = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_aprobador', related_name='comprasrepuesto_id_aprobador_set', blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'compras_repuesto'


class DetalleCompra(models.Model):
    id = models.UUIDField(primary_key=True)
    id_compra = models.ForeignKey(ComprasRepuesto, models.DO_NOTHING, db_column='id_compra')
    id_repuesto = models.ForeignKey('Repuestos', models.DO_NOTHING, db_column='id_repuesto')
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detalle_compra'


class DetalleReparacion(models.Model):
    id = models.UUIDField(primary_key=True)
    id_reparacion = models.ForeignKey('Reparaciones', models.DO_NOTHING, db_column='id_reparacion')
    id_repuesto = models.ForeignKey('Repuestos', models.DO_NOTHING, db_column='id_repuesto')
    cantidad_usada = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detalle_reparacion'


class Equipos(models.Model):
    id = models.UUIDField(primary_key=True)
    codigo_qr = models.CharField(unique=True, max_length=100)
    nombre = models.CharField(max_length=150)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    nro_serie = models.CharField(unique=True, max_length=100, blank=True, null=True)
    estado = models.TextField(blank=True, null=True)  # This field type is a guess.
    fecha_adquisicion = models.DateField(blank=True, null=True)
    valor_compra = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    garantia_meses = models.IntegerField(blank=True, null=True)
    proveedor = models.CharField(max_length=150, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    especificaciones = models.JSONField(blank=True, null=True)
    id_ubicacion = models.ForeignKey('Ubicaciones', models.DO_NOTHING, db_column='id_ubicacion', blank=True, null=True)
    id_responsable = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_responsable', blank=True, null=True)
    activo = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'equipos'
        db_table_comment = 'Registro de todos los equipos del laboratorio con su informaci¾n y estado'


class HistorialUbicacion(models.Model):
    id = models.UUIDField(primary_key=True)
    id_equipo = models.ForeignKey(Equipos, models.DO_NOTHING, db_column='id_equipo')
    id_ubicacion_anterior = models.ForeignKey('Ubicaciones', models.DO_NOTHING, db_column='id_ubicacion_anterior', blank=True, null=True)
    id_ubicacion_nueva = models.ForeignKey('Ubicaciones', models.DO_NOTHING, db_column='id_ubicacion_nueva', related_name='historialubicacion_id_ubicacion_nueva_set', blank=True, null=True)
    fecha_cambio = models.DateTimeField(blank=True, null=True)
    motivo = models.CharField(max_length=255, blank=True, null=True)
    id_usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'historial_ubicacion'


class Incidencias(models.Model):
    id = models.UUIDField(primary_key=True)
    nro_incidencia = models.CharField(unique=True, max_length=50, blank=True, null=True)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_reporte = models.DateTimeField(blank=True, null=True)
    fecha_asignacion = models.DateTimeField(blank=True, null=True)
    fecha_resolucion = models.DateTimeField(blank=True, null=True)
    estado = models.TextField(blank=True, null=True)  # This field type is a guess.
    prioridad = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_equipo = models.ForeignKey(Equipos, models.DO_NOTHING, db_column='id_equipo', blank=True, null=True)
    id_reportante = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_reportante')
    id_asignado = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_asignado', related_name='incidencias_id_asignado_set', blank=True, null=True)
    solucion = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    archivos_adjuntos = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'incidencias'
        db_table_comment = 'Reportes de problemas o fallas en equipos'


class Reparaciones(models.Model):
    id = models.UUIDField(primary_key=True)
    nro_reparacion = models.CharField(unique=True, max_length=50, blank=True, null=True)
    fecha_inicio = models.DateTimeField(blank=True, null=True)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    descripcion_problema = models.TextField()
    descripcion_solucion = models.TextField(blank=True, null=True)
    diagnostico = models.TextField(blank=True, null=True)
    costo_mano_obra = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    costo_repuestos = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    costo_total = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    estado = models.TextField(blank=True, null=True)  # This field type is a guess.
    prioridad = models.TextField(blank=True, null=True)  # This field type is a guess.
    tiempo_estimado_horas = models.IntegerField(blank=True, null=True)
    id_equipo = models.ForeignKey(Equipos, models.DO_NOTHING, db_column='id_equipo')
    id_tecnico = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_tecnico', blank=True, null=True)
    id_supervisor = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_supervisor', related_name='reparaciones_id_supervisor_set', blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reparaciones'
        db_table_comment = 'Historial de reparaciones realizadas a los equipos'


class Reportes(models.Model):
    id = models.UUIDField(primary_key=True)
    tipo = models.TextField()  # This field type is a guess.
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    fecha_generacion = models.DateTimeField(blank=True, null=True)
    formato = models.CharField(max_length=20, blank=True, null=True)
    parametros = models.JSONField(blank=True, null=True)
    url_archivo = models.CharField(max_length=500, blank=True, null=True)
    tamanio_bytes = models.BigIntegerField(blank=True, null=True)
    id_usuario = models.ForeignKey('Usuarios', models.DO_NOTHING, db_column='id_usuario')
    descargas = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reportes'


class Repuestos(models.Model):
    id = models.UUIDField(primary_key=True)
    codigo = models.CharField(unique=True, max_length=50)
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    tipo = models.TextField()  # This field type is a guess.
    marca = models.CharField(max_length=100, blank=True, null=True)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    cantidad_actual = models.IntegerField(blank=True, null=True)
    stock_minimo = models.IntegerField(blank=True, null=True)
    stock_maximo = models.IntegerField(blank=True, null=True)
    unidad_medida = models.CharField(max_length=20, blank=True, null=True)
    precio_referencia = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    compatible_con = models.JSONField(blank=True, null=True)
    ubicacion_bodega = models.CharField(max_length=100, blank=True, null=True)
    activo = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'repuestos'
        db_table_comment = 'Inventario de repuestos y materiales disponibles'


class Sesiones(models.Model):
    id = models.UUIDField(primary_key=True)
    user = models.ForeignKey('Usuarios', models.DO_NOTHING)
    refresh_token = models.CharField(max_length=500)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    expira_en = models.DateTimeField()
    activo = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sesiones'


class Ubicaciones(models.Model):
    id = models.UUIDField(primary_key=True)
    nombre_sala = models.CharField(max_length=100)
    piso = models.IntegerField()
    edificio = models.CharField(max_length=50)
    capacidad = models.IntegerField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ubicaciones'
        unique_together = (('nombre_sala', 'edificio'),)


class Usuarios(models.Model):
    id = models.UUIDField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.CharField(unique=True, max_length=255)
    password_hash = models.CharField(max_length=255, db_column='password_hash')  # ← Cambiar aquí
    rol = models.TextField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    activo = models.BooleanField(blank=True, null=True)
    token_2fa = models.CharField(max_length=255, blank=True, null=True)
    ultimo_acceso = models.DateTimeField(blank=True, null=True)
    intentos_fallidos = models.IntegerField(blank=True, null=True)
    bloqueado_hasta = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuarios'


class SimpleUserManager(BaseUserManager):
    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})

class SimpleUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100, blank=True)
    apellido = models.CharField(max_length=100, blank=True)
    correo = models.EmailField(max_length=255, unique=True)
    password_hash = models.CharField(max_length=255, db_column='password_hash')
    rol = models.TextField(blank=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    activo = models.BooleanField(default=True)
    token_2fa = models.CharField(max_length=255, blank=True, null=True)
    ultimo_acceso = models.DateTimeField(blank=True, null=True)
    intentos_fallidos = models.IntegerField(default=0, blank=True, null=True)
    bloqueado_hasta = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    
    # Campos requeridos por PermissionsMixin
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = SimpleUserManager()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = []
    
    # IMPORTANTE: Decirle a Django que NO use el campo password
    password = None  # Desactivar el campo password de Django

    class Meta:
        managed = False
        db_table = 'usuarios'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.correo

    # Estos métodos no se usan porque autenticamos manualmente
    def set_password(self, raw_password):
        pass

    def check_password(self, raw_password):
        return False