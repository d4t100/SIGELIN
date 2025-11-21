from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout, get_user_model
import json
import qrcode
from io import BytesIO

User = get_user_model()

# ============================================================================
# AUTENTICACIÓN
# ============================================================================

def index(request):
    """Renderiza la página de login"""
    return render(request, 'frontend/index.html')


def dashboard(request):
    """Renderiza el dashboard"""
    return render(request, 'frontend/dashboard.html')


@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    """
    Login de usuarios
    Espera JSON con: correo y password
    """
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
        
        # Intentar autenticar
        user = authenticate(request, username=correo, password=password)
        
        if user:
            login(request, user)
            print("✓ Login exitoso")
            return JsonResponse({
                'success': True,
                'message': 'Login exitoso',
                'user': {
                    'id': str(user.id),
                    'nombre': getattr(user, 'nombre', ''),
                    'apellido': getattr(user, 'apellido', ''),
                    'email': user.email,
                    'correo': user.email,
                    'rol': getattr(user, 'rol', '')
                }
            })
        else:
            print("✗ Credenciales inválidas")
            return JsonResponse({
                'success': False,
                'message': 'Credenciales inválidas'
            }, status=401)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'JSON inválido'
        }, status=400)
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': 'Error del servidor'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def logout_view(request):
    """Cierra la sesión del usuario"""
    logout(request)
    return JsonResponse({
        'success': True,
        'message': 'Sesión cerrada'
    })


@csrf_exempt
@require_http_methods(["GET"])
def auth_check(request):
    """
    Verifica si el usuario tiene una sesión válida
    """
    auth_header = request.headers.get('Authorization', '')
    
    if not auth_header or auth_header != 'Bearer session_active':
        return JsonResponse({
            'authenticated': False,
            'message': 'No hay sesión válida'
        }, status=401)
    
    if request.user and request.user.is_authenticated:
        return JsonResponse({
            'authenticated': True,
            'user': {
                'id': str(request.user.id),
                'nombre': getattr(request.user, 'nombre', ''),
                'apellido': getattr(request.user, 'apellido', ''),
                'email': request.user.email,
                'rol': getattr(request.user, 'rol', '')
            }
        })
    
    return JsonResponse({
        'authenticated': False,
        'message': 'Sesión expirada'
    }, status=401)


# ============================================================================
# QR Y EQUIPOS
# ============================================================================

def ver_qr_equipo(request, pk):
    """
    Genera y devuelve un código QR para un equipo específico
    """
    try:
        from sigelin.models import Equipos
        
        equipo = Equipos.objects.get(pk=pk)
        
        # Crear datos del QR
        data = f"http://localhost:8000/equipos/{pk}/qr/"
        
        # Generar código QR
        img = qrcode.make(data)
        
        # Convertir a bytes
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        return HttpResponse(buffer.getvalue(), content_type='image/png')
        
    except Exception as e:
        print(f"Error generando QR: {e}")
        return HttpResponse(f'Error: {str(e)}', status=500)


# ============================================================================
# API ENDPOINTS
# ============================================================================

@require_http_methods(["GET"])
def listar_equipos(request):
    """Lista todos los equipos"""
    try:
        from sigelin.models import Equipos
        equipos = list(Equipos.objects.filter(activo=True).values())
        return JsonResponse({'equipos': equipos})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def listar_reparaciones(request):
    """Lista todas las reparaciones"""
    try:
        from sigelin.models import Reparaciones
        reparaciones = list(Reparaciones.objects.values())
        return JsonResponse({'reparaciones': reparaciones})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def listar_repuestos(request):
    """Lista todos los repuestos"""
    try:
        from sigelin.models import Repuestos
        repuestos = list(Repuestos.objects.filter(activo=True).values())
        return JsonResponse({'repuestos': repuestos})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)