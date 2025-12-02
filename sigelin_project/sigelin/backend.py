"""
Backend de autenticación personalizado para SIGELIN
Valida contraseñas hasheadas con crypt() de PostgreSQL
"""
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db import connection
import hashlib

User = get_user_model()


class PostgresCryptBackend(ModelBackend):
    """
    Backend que autentica contra la tabla usuarios de PostgreSQL
    usando el hash crypt() almacenado en password_hash
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Autentica un usuario verificando su contraseña contra PostgreSQL
        
        Args:
            username: El correo electrónico del usuario
            password: La contraseña en texto plano
        
        Returns:
            Usuario autenticado o None
        """
        print("=" * 80)
        print("🔐 BACKEND DE AUTENTICACIÓN PERSONALIZADO")
        print(f"📧 Correo: {username}")
        print(f"🔑 Password length: {len(password) if password else 0}")
        
        if not username or not password:
            print("❌ Username o password vacío")
            print("=" * 80)
            return None
        
        try:
            # Buscar el usuario por correo
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id, nombre, apellido, correo, password_hash, rol, activo
                    FROM usuarios
                    WHERE correo = %s AND activo = true
                """, [username])
                
                row = cursor.fetchone()
                
                if not row:
                    print(f"❌ Usuario no encontrado: {username}")
                    print("=" * 80)
                    return None
                
                user_id, nombre, apellido, correo, password_hash, rol, activo = row
                
                print(f"✅ Usuario encontrado:")
                print(f"   ID: {user_id}")
                print(f"   Nombre: {nombre} {apellido}")
                print(f"   Rol: {rol}")
                print(f"   Hash length: {len(password_hash) if password_hash else 0}")
                
                # Verificar la contraseña usando crypt() de PostgreSQL
                cursor.execute("""
                    SELECT password_hash = crypt(%s, password_hash) AS match
                    FROM usuarios
                    WHERE correo = %s
                """, [password, username])
                
                result = cursor.fetchone()
                password_matches = result[0] if result else False
                
                print(f"🔐 Verificación de contraseña: {'✅ VÁLIDA' if password_matches else '❌ INVÁLIDA'}")
                
                if not password_matches:
                    print("=" * 80)
                    return None
                
                # Obtener o crear el usuario en el modelo Django
                try:
                    user = User.objects.get(id=user_id)
                    print(f"✅ Usuario Django encontrado: {user.correo}")
                except User.DoesNotExist:
                    # Crear el usuario si no existe
                    print(f"⚠️ Usuario Django no existe, creando...")
                    user = User.objects.create(
                        id=user_id,
                        correo=correo,
                        nombre=nombre,
                        apellido=apellido,
                        rol=rol,
                        activo=activo,
                        is_active=activo,
                        is_staff=(rol == 'administrador'),
                        is_superuser=(rol == 'administrador')
                    )
                    print(f"✅ Usuario Django creado: {user.correo}")
                
                print("✅ Autenticación exitosa")
                print("=" * 80)
                return user
                
        except Exception as e:
            print(f"❌ ERROR EN AUTENTICACIÓN: {str(e)}")
            import traceback
            traceback.print_exc()
            print("=" * 80)
            return None
    
    def get_user(self, user_id):
        """
        Obtiene un usuario por su ID
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None