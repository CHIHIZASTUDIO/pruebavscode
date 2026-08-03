# CHIHIZA Website - Cambios Realizados

## 2026-07-24

### Slider Horizontal Automático (index.html)
- Se reemplazó la lista vertical de proyectos por un carrusel horizontal automático
- 5 proyectos con cards que se deslizan de izquierda a derecha (loop infinito)
- Pausa al hacer hover sobre las cards
- Cards duplicadas para lograr el loop sin saltos
- CSS en `assets/css/styles.css` (.projects-slider, .slider-track, .slider-card)
- Botón "View All Projects" que lleva a projects.html

### Página de Proyectos (projects.html)
- Catálogo completo con filtro por país (All / Colombia / Costa Rica / Panama)
- 5 proyectos: Natautá, Río Frío, El Mirador, CostaVerde, Nosara
- Grid de cards con badges de país, precio e IRR

### Nav Actualizado (5 páginas)
- index.html, about.html, contact.html, legacy.html, guide.html
- Nuevo orden: Home → Projects → About → Legal → Guide → Contact → WhatsApp

### THE PROCESS - Panel de Herramientas del Equipo
- Botón flotante naranja en esquina inferior izquierda
- Color: gradiente #ff6b35 → #f7931e
- Al hacer click se despliega un panel hacia arriba con overlay oscuro
- 4 herramientas en orden:
  1. DISCOVERY → CHIHIZA_DISCOVERY_V2.html
  2. DUE DILIGENCE → CHIHIZA_DUE_DILIGENCE.html
  3. DIGITAL TWIN → digital-twin-campestre/index.html
  4. FINANCIAL MODEL → CHIHIZA_FINANCIAL_MODEL.html
- CSS en `assets/css/styles.css` (.team-tools-*)
- JS inline en index.html

### Archivos Modificados
- `index.html` - Slider + Nav + Team Tools Panel + JS
- `projects.html` - Creada desde cero
- `assets/css/styles.css` - Slider CSS + Team Tools CSS
- `about.html` - Nav actualizado
- `contact.html` - Nav actualizado
- `legacy.html` - Nav actualizado
- `guide.html` - Nav actualizado
