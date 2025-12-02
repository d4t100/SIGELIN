/**
 * Sistema de autenticación con sesiones Django
 * Versión mejorada con mejor manejo de navegación
 */

const API_BASE = 'http://localhost:8000/api';

// Clase para manejar la autenticación
class AuthManager {
    constructor() {
        this.user = null;
        this.checkInterval = null;
    }

    // Inicializar el sistema de autenticación
    async init() {
        await this.checkSession();
        this.startSessionCheck();
    }

    // Verificar si hay sesión activa
    async checkSession() {
        try {
            const response = await fetch(`${API_BASE}/auth/check/`, {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer session_active'
                }
            });

            if (response.ok) {
                const data = await response.json();
                if (data.authenticated) {
                    this.user = data.user;
                    this.saveUserToStorage(data.user);
                    return true;
                }
            }
            
            this.clearUserData();
            return false;
        } catch (error) {
            console.error('Error verificando sesión:', error);
            this.clearUserData();
            return false;
        }
    }

    // Iniciar sesión
    async login(correo, password) {
        try {
            const response = await fetch(`${API_BASE}/auth/login/`, {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ correo, password })
            });

            const data = await response.json();

            if (data.success) {
                this.user = data.user;
                this.saveUserToStorage(data.user);
                this.startSessionCheck();
                return { success: true, user: data.user };
            } else {
                return { success: false, message: data.message };
            }
        } catch (error) {
            console.error('Error en login:', error);
            return { success: false, message: 'Error de conexión' };
        }
    }

    // Cerrar sesión
    async logout() {
        try {
            await fetch(`${API_BASE}/auth/logout/`, {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
        } catch (error) {
            console.error('Error en logout:', error);
        } finally {
            this.clearUserData();
            this.stopSessionCheck();
            window.location.href = '/';
        }
    }

    // Guardar usuario en localStorage (solo como cache)
    saveUserToStorage(user) {
        localStorage.setItem('sigelin_user', JSON.stringify(user));
        localStorage.setItem('sigelin_authenticated', 'true');
        localStorage.setItem('sigelin_token', 'session_active');
    }

    // Obtener usuario desde localStorage
    getUserFromStorage() {
        try {
            const userData = localStorage.getItem('sigelin_user');
            return userData ? JSON.parse(userData) : null;
        } catch {
            return null;
        }
    }

    // Limpiar datos de usuario
    clearUserData() {
        this.user = null;
        localStorage.removeItem('sigelin_user');
        localStorage.removeItem('sigelin_authenticated');
        localStorage.removeItem('sigelin_token');
    }

    // Verificar sesión cada 5 minutos
    startSessionCheck() {
        if (this.checkInterval) return;
        
        this.checkInterval = setInterval(async () => {
            const isValid = await this.checkSession();
            if (!isValid && window.location.pathname !== '/') {
                alert('Tu sesión ha expirado. Serás redirigido al login.');
                window.location.href = '/';
            }
        }, 5 * 60 * 1000); // 5 minutos
    }

    // Detener verificación de sesión
    stopSessionCheck() {
        if (this.checkInterval) {
            clearInterval(this.checkInterval);
            this.checkInterval = null;
        }
    }

    // Obtener usuario actual
    getUser() {
        return this.user || this.getUserFromStorage();
    }

    // Verificar si está autenticado
    isAuthenticated() {
        return localStorage.getItem('sigelin_authenticated') === 'true';
    }

    // Proteger página (requiere autenticación)
    async requireAuth(redirectToLogin = true) {
        // Si ya sabemos que está autenticado, no hacer otra verificación
        if (this.isAuthenticated() && this.getUserFromStorage()) {
            return true;
        }

        const isAuth = await this.checkSession();
        if (!isAuth && redirectToLogin) {
            window.location.href = '/';
            return false;
        }
        return isAuth;
    }
}

// Instancia global
const auth = new AuthManager();

// Función para hacer fetch autenticado
async function apiFetch(endpoint, options = {}) {
    const defaultOptions = {
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        }
    };

    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            ...options,
            ...defaultOptions
        });

        if (response.status === 401) {
            auth.clearUserData();
            if (window.location.pathname !== '/') {
                alert('Sesión expirada. Inicia sesión nuevamente.');
                window.location.href = '/';
            }
            throw new Error('No autorizado');
        }

        return response;
    } catch (error) {
        console.error('Error en apiFetch:', error);
        throw error;
    }
}

// Función de logout global
function logout() {
    auth.logout();
}

// Exportar para uso global
window.auth = auth;
window.apiFetch = apiFetch;
window.logout = logout;
window.API_BASE = API_BASE;

// Marcar enlaces activos en el menú
function markActiveLink() {
    const currentPath = window.location.pathname;
    const links = document.querySelectorAll('aside a, nav a');
    
    links.forEach(link => {
        link.classList.remove('active');
        const href = link.getAttribute('href');
        
        if (href && (currentPath === href || currentPath.endsWith(href))) {
            link.classList.add('active');
        }
    });
}

// Ejecutar al cargar
document.addEventListener('DOMContentLoaded', () => {
    markActiveLink();
});