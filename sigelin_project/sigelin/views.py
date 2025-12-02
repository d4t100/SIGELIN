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
# PÁGINAS HTML - Acceso libre
# ============================================================================

def index(request):
    """Página de login"""
    return render(request, 'frontend/index.html')

def dashboard(request):
    """Dashboard principal"""
    return render(request, 'frontend/dashboard.html')

def equipos(request):
    """Página de equipos"""
    return render(request, 'frontend/Equipos.html')

def reparaciones(request):
    """Página de reparaciones"""
    return render(request, 'frontend/Reparaciones.html')

def inventario(request):
    """Página de inventario"""
    return render(request, 'frontend/Inventario.html')

def reportes(request):
    """Página de reportes"""
    return render(request, 'frontend/Reportes.html')


# ============================================================================
# AUTENTICACIÓN
# ============================================================================

@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    """Login de usuarios"""
    try:
        data = json.loads(request.body)
        correo = data.get('correo', '').strip()
        password = data.get('password', '')
        
        if not correo or not password:
            return JsonResponse({
                'success': False,
                'message': 'Correo y contraseña son requeridos'
            }, status=400)
        
        user = authenticate(request, username=correo, password=password)
        
        if user:
            login(request, user)
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
            return JsonResponse({
                'success': False,
                'message': 'Credenciales inválidas'
            }, status=401)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Error del servidor'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def logout_view(request):
    """Cerrar sesión"""
    logout(request)
    return JsonResponse({
        'success': True,
        'message': 'Sesión cerrada'
    })


# ============================================================================
# API ENDPOINTS - SIN AUTENTICACIÓN (Por ahora)
# ============================================================================

@csrf_exempt
@require_http_methods(["GET"])
def listar_equipos(request):
    """Lista todos los equipos"""
    try:
        from sigelin.models import Equipos
        equipos = list(Equipos.objects.filter(activo=True).values())
        return JsonResponse({'equipos': equipos})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def listar_reparaciones(request):
    """Lista todas las reparaciones"""
    try:
        from sigelin.models import Reparaciones
        reparaciones = list(Reparaciones.objects.values())
        return JsonResponse({'reparaciones': reparaciones})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def listar_repuestos(request):
    """Lista todos los repuestos"""
    try:
        from sigelin.models import Repuestos
        repuestos = list(Repuestos.objects.filter(activo=True).values())
        return JsonResponse({'repuestos': repuestos})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ============================================================================
# QR
# ============================================================================

def ver_qr_equipo(request, pk):
    """Genera código QR para un equipo"""
    try:
        from sigelin.models import Equipos
        equipo = Equipos.objects.get(pk=pk)
        data = f"http://localhost:8000/equipos/{pk}/qr/"
        img = qrcode.make(data)
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        return HttpResponse(buffer.getvalue(), content_type='image/png')
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}', status=500)
    
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