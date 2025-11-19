from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.contrib.auth import authenticate, login, get_user_model
import json


import json

class LoginAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        if not user:
            return Response({'detail':'Credenciales inválidas'}, status=401)
        refresh = RefreshToken.for_user(user)  # esto falla si user no es un User de Django
        # Si usas SimpleUser (no Django User), genera token manual:
        payload = {
            'user_id': str(user.id),
            'email': user.email,
            'rol': user.rol,
        }
        # mejor: crear tokens manuales
        refresh = RefreshToken()
        refresh['user_id'] = str(user.id)
        refresh['email'] = user.email
        refresh['rol'] = user.rol
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        })

# Create your views here.

from django.http import HttpResponse
from .qr import generar_qr_para_equipo
from .models import Equipos

def ver_qr_equipo(request, pk):
    equipo = Equipos.objects.get(pk=pk)
    qr_image = generar_qr_para_equipo(equipo)

    # Si tienes el archivo guardado:
    if hasattr(equipo, 'qr_image') and equipo.qr_image:
        with open(equipo.qr_image.path, 'rb') as f:
            return HttpResponse(f.read(), content_type='image/png')

    # Si solo generas el QR temporalmente:
    import qrcode
    from io import BytesIO
    img = qrcode.make(equipo.codigo_qr or str(equipo.id))
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return HttpResponse(buffer.getvalue(), content_type='image/png')

# Vista principal (index)
def index(request):
    return render(request, 'frontend/index.html')

# API Views
User = get_user_model()

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.auth import login, get_user_model
from django.db import connection
import json

User = get_user_model()


@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    try:
        data = json.loads(request.body)
        correo = data.get('correo', '').strip()
        password = data.get('password', '')
        
        print(f"🔍 Intento de login con correo: {correo}")
        
        if not correo or not password:
            return JsonResponse({
                'success': False,
                'message': 'Correo y contraseña son requeridos'
            }, status=400)
        
        # Verificar credenciales directamente en PostgreSQL
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, nombre, apellido, correo, rol
                FROM usuarios
                WHERE correo = %s 
                AND activo = true
                AND password_hash = crypt(%s, password_hash)
            """, [correo, password])
            
            result = cursor.fetchone()
            
            if result:
                user_id, nombre, apellido, email, rol = result
                
                try:
                    # Obtener el objeto user
                    user = User.objects.raw(
                        "SELECT * FROM usuarios WHERE id = %s",
                        [user_id]
                    )[0]
                    
                    # Iniciar sesión
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                    
                    print("✓ Login exitoso")
                    return JsonResponse({
                        'success': True,
                        'message': 'Login exitoso',
                        'user': {
                            'id': str(user_id),
                            'nombre': nombre,
                            'apellido': apellido,
                            'email': email,
                            'rol': rol
                        }
                    })
                except (IndexError, Exception) as e:
                    print(f"✗ Error al obtener usuario: {e}")
                    return JsonResponse({
                        'success': False,
                        'message': 'Error al autenticar'
                    }, status=500)
            else:
                print("✗ Credenciales inválidas")
                return JsonResponse({
                    'success': False,
                    'message': 'Credenciales inválidas'
                }, status=401)
            
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': 'Error del servidor'
        }, status=500)

@require_http_methods(["GET"])
def listar_equipos(request):
    # Por ahora devuelve datos de ejemplo
    # Luego lo conectarás con tu modelo
    equipos = []
    return JsonResponse({'equipos': equipos})

@require_http_methods(["GET"])
def listar_reparaciones(request):
    reparaciones = []
    return JsonResponse({'reparaciones': reparaciones})

@require_http_methods(["GET"])
def listar_repuestos(request):
    repuestos = []
    return JsonResponse({'repuestos': repuestos})

def dashboard(request):
    return render(request, 'frontend/dashboard.html')