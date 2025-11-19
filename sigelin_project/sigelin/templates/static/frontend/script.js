// Llamadas al backend Django (asumiendo API en /api/)
async function cargarResumen() {
  try {
    const [equipos, reparaciones, repuestos] = await Promise.all([
      fetch("/api/equipos/"),
      fetch("/api/reparaciones/"),
      fetch("/api/repuestos/"),
      fetch('http://localhost:8000/api/login/'),
      fetch('/api/login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        correo: correo, // Necesitarías modificar la vista en Django
        password: password
    })
})
    ]);

    const equiposData = await equipos.json();
    const reparacionesData = await reparaciones.json();
    const repuestosData = await repuestos.json();

    document.getElementById("equipos-count").textContent = equiposData.length;
    document.getElementById("reparaciones-count").textContent =
      reparacionesData.filter((r) => r.estado === "pendiente").length;
    document.getElementById("repuestos-bajo-stock").textContent =
      repuestosData.filter((r) => r.cantidad <= r.stock_minimo).length;
  } catch (error) {
    console.error("Error al cargar datos:", error);
    document.getElementById("dashboard-cards").innerHTML =
      "<p>Error al conectar con el servidor.</p>";
  }
}

document.addEventListener("DOMContentLoaded", cargarResumen);
