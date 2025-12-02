/**
 * Sistema de autenticación SIGELIN - Versión Corregida
 */

const API_BASE = 'http://localhost:8000/api';

// Clase para manejar la autenticación
class AuthManager {
    constructor() {
        this.user = null;
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
            window.location.href = '/';
        }
    }

    // Guardar usuario en localStorage
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

    // Obtener usuario actual
    getUser() {
        return this.user || this.getUserFromStorage();
    }

    // Verificar si está autenticado (solo revisa localStorage)
    isAuthenticated() {
        const isAuth = localStorage.getItem('sigelin_authenticated') === 'true';
        const hasUser = this.getUserFromStorage() !== null;
        return isAuth && hasUser;
    }

    // Proteger página - SOLO revisa localStorage, NO redirige automáticamente
    requireAuth() {
        const currentPath = window.location.pathname;
        
        // Si estamos en la página de login, no hacer nada
        if (currentPath === '/' || currentPath === '/index.html') {
            return false;
        }
        
        // Verificar autenticación
        if (!this.isAuthenticated()) {
            console.log('❌ No autenticado, redirigiendo al login...');
            window.location.href = '/';
            return false;
        }
        
        console.log('✅ Usuario autenticado');
        return true;
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
            alert('Sesión expirada. Inicia sesión nuevamente.');
            window.location.href = '/';
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
    if (confirm('¿Seguro que deseas cerrar sesión?')) {
        auth.logout();
    }
}

// Marcar enlace activo
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

// Exportar para uso global
window.auth = auth;
window.apiFetch = apiFetch;
window.logout = logout;
window.API_BASE = API_BASE;

// NO ejecutar requireAuth automáticamente
console.log('🔐 Sistema de autenticación cargado');