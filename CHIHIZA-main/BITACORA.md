# CHIHIZA — Bitácora de Proyecto

## Información General

- **Proyecto:** CHIHIZA International — Sitio web de inversión inmobiliaria ecológica
- **Países:** Colombia, Costa Rica, Panamá
- **Stack:** HTML5, CSS3, JavaScript vanilla (sin frameworks)
- **Repo:** https://github.com/CHIHIZASTUDIO/CHIHIZA.git (main)
- **Email:** chihizaestudio@gmail.com
- **WhatsApp:** +57 321 993 1029
- **Última sesión:** 26 de julio de 2026

---

## Estructura del Sitio

```
├── index.html              — Página principal (Hero + Founder Teaser + How it Works + Form + FAQ)
├── about.html              — About + Team unificado (Why We Exist, Emiliano, María, Julián, Credentials)
├── process.html            — Our Process (7 pasos: Discovery → Territory → Masterplan → Architecture → Engineering → Construction → Delivery)
├── research.html           — Research (5 tesis, "From Research to Practice")
├── projects.html           — Catálogo de proyectos (solo Montvento)
├── contact.html            — Contacto
├── guide.html              — Guía "Beyond Buying Property" (lead capture, free after registration)
├── legacy.html             — Marco Legal de Inversión (lead capture, free after registration)
├── projects/
│   └── montvento.html      — Montvento Case Study 001 (deepened: Problem, Design Decisions, What We Learned)
├── assets/
│   ├── css/styles.css      — Estilos globales (~3880 líneas)
│   ├── js/main.js          — Lógica principal
│   ├── favicon.svg         — Favicon
│   ├── images/bg/          — 16 imágenes de fondo (img-1 a img-16)
│   ├── CHIHIZA Secure Investment Framework.pdf
│   └── guide.pdf
├── tools/
│   ├── CHIHIZA_DISCOVERY_V2.html    — Herramienta de descubrimiento
│   ├── CHIHIZA_DUE_DILIGENCE.html   — Due diligence terrain
│   ├── CHIHIZA_FINANCIAL_MODEL.html — Modelo financiero
│   └── digital-twin-campestre/       — Digital Twin (HTML+CSS+JS)
└── proyectos/              — Imágenes de proyectos
    ├── montvento/          — 5 imágenes de Montvento
    ├── team/
    │   └── emiliano.png    — Foto real de Emiliano
    ├── about-hero.png
    └── images-back/        — Imágenes fuente para backgrounds
```

---

## Paleta de Colores

| Variable | Color | Uso |
|---|---|---|
| `--bg` | `#f8f7f4` | Fondo principal (warm white) |
| `--bg-warm` | `#f3f1ec` | Secciones alternas |
| `--accent` | `#6b8f71` | Sage green (botones, tags, links) |
| `--text` | `#2c2c2c` | Texto principal |
| `--text-secondary` | `#5a5a55` | Texto secundario |
| Hot pink | `#ff0055` | Botón play (parpadeante) |
| WhatsApp green | `#25d366` | Float de WhatsApp |
| Fuchsia | `#d946ef` | Reserva (no activo) |

## Tipografía

- **Display:** Playfair Display (títulos, logo)
- **Body:** Inter (texto general)
- **Mono:** Courier New (botón play)

---

## Historial de Commits (Sesión 24 jul 2026)

| Hash | Descripción |
|---|---|
| `cc7e820` | Comprehensive mobile fixes: divider parallax, slider swipe, play button, spacing, hero bgs |
| `46cbbd9` | 16 images redistributed: hero bgs, dividers across all pages, CTA bgs |
| `567ba10` | Reverted section-bg approach, now using 4 full-width image dividers between sections |
| `d85f8c0` | 10 background images distributed across all pages (no repeats) |
| `f84bcb5` | Fix email: chihizaestudio@gmail.com |
| `3976b6b` | Play button: circle, hot pink #ff0055, blink animation, no text |
| `bda9a30` | START button moved into header nav (fuchsia, no more overlap) |
| `79211ad` | Remove WhatsApp nav-cta, START button now fuchsia |
| `256abf1` | START button fixed top-right (orange, console style) + WhatsApp nav green |

### Commits anteriores (pre-sesión)

| Hash | Descripción |
|---|---|
| `varios` | Rewrite all 11 HTML pages (inline CSS removed, SEO, lazy load) |
| `varios` | Full CSS rewrite: white theme, shadow system, responsive |
| `varios` | main.js rewrite: IntersectionObserver, counters, toast, lightbox |
| `varios` | Copy 4 team tools into tools/ folder, white theme applied |
| `varios` | THE PROCESS panel with 4 tools (Discovery, Due Diligence, Digital Twin, Financial Model) |
| `varios` | Delete dead files (5 stubs, old CSS/JS, .bak) |
| `varios` | OG tags, Twitter Cards, canonical URLs on all pages |
| `varios` | Breadcrumbs on project pages, nav fix |
| `varios` | Email capture forms on guide.html and legacy.html |

---

## Lo que Hicimos en Esta Sesión

### 1-5: Cambios Anteriores (Ver abajo)
- Botón Play circular, hot pink, blink animation
- Email actualizado a chihizaestudio@gmail.com
- Sistema de 16 imágenes de fondo distribuidas
- Fix móvil integral

### 6. Reescritura Mayor de Contenido (Basado en Crítica Experta 7.8/10)
**Contexto:** Análisis de experto identificó problemas clave: hero vende dinero no deseo, sin identidad de marca clara, testimonios falsos, equipo inventado, GEA no es protagonista, demasiado texto sin imagen.

**Cambios en index.html:**
- **Hero:** Reescrito con narrativa emocional ("Architecture born from the forest") en vez de métricas financieras. Imagen fullscreen con texto mínimo.
- **GEA como protagonista:** Sección expandida con Biomimicry, Local Materials, Living Architecture. Layout editorial de dos columnas.
- **Eliminados:** Testimonios falsos, equipo inventado ("Architecture Team", "Operations Team")
- **Formulario simplificado:** Solo 5 campos: Name, Email, WhatsApp, Budget Range, Book a Conversation
- **Nuevo orden:** Hero → GEA → Divisor → Projects → Divisor → How it Works → Form → FAQ → Divisor → CTA
- **Copy emocional:** "We don't design buildings. We design ecosystems." / "Places where architecture meets the wild" / "From vision to reality"
- **Meta tags actualizados:** Title y description reflejan identidad arquitectónica, no inversión

**Estructura eliminada:**
- ❌ Stats animados (inversión promedio, ROI, retorno)
- ❌ 3 Simple Steps (vendía dinero, no vida)
- ❌ Testimonios (3 inventados)
- ❌ Team grid (18 miembros genéricos)
- ❌ Sección de "Sectors" (5 sectores = demasiadas opciones)

**Nueva estructura:**
- ✅ Hero emocional (fullscreen image)
- ✅ GEA + Biomimicry + Local Materials + Living Architecture
- ✅ Projects slider (mantenido)
- ✅ How it Works (3 pasos: Discover, Connect, Create)
- ✅ Contact form (5 campos simplificados)
- ✅ FAQ (5 preguntas, reducido de 10)
- ✅ CTA con imagen de fondo

### 7. FASE 1: Evidencia + Confianza (Basado en Crítica 8.3/10)
**Contexto:** Segunda crítica identificó: afirmaciones sin evidencia, sin personas, sin prueba social, sin fundador visible, GEA/MOX/HOM son abstractos, Legal promete de más.

**Cambios en index.html:**
- **GEA Workflow Diagram:** Diagrama SVG de 5 pasos (Survey → Design → Source → Build → Live) con iconos animados
- **GEA Pillar Cards:** 3 tarjetas visuales con SVG ilustrativos (landscape, factory, people)
- **Social Proof:** Sección con logos de alianzas + testimonial real
- **Founder Teaser:** Sección de 2 columnas con foto + narrativa + link a founders.html
- **Nav actualizado:** Agregado "Founder" en todas las páginas
- **Footer actualizado:** Agregado link a Founder en todos los footers

**Nuevo archivo: founders.html**
- Hero fullscreen con foto del fundador
- Narrativa personal ("I started CHIHIZA because...")
- Timeline visual (2012 → Today)
- Credenciales: Educación, Reconocimientos, Publicaciones, Afiliaciones
- CTA contextual ("Let's design something together")

**Lead Capture (Guide + Legal):**
- Formulario ampliado: Name, Email, Country (antes solo email)
- Gate antes del PDF download
- "Free. No spam. We respect your privacy."

**Legal Page reescrita:**
- Título: "What we can prove — not what we promise"
- Separación clara: "What we document" vs "What we're building"
- Items en desarrollo marcados con opacity + "In development"
- Eliminados items que no existen (05-08 original)

**Proyecto Natauta reestructurado:**
- Narrativa sensorial ("Where the forest breathes")
- Descripción emocional (olor, sonido, luz)
- Sidebar expandido con "Experience"
- Copy vende vida, no ficha técnica

**CSS additions:**
- `.gea-workflow` — Diagrama de flujo horizontal
- `.gea-pillar-card` — Tarjetas visuales con SVG
- `.social-proof` — Sección de prueba social
- `.founder-teaser` — Sección del fundador
- `.founder-timeline` — Timeline visual
- `.credentials-grid` — Grid de credenciales
- `.lead-capture-form` — Formulario de captura

### 8. Información Real del Fundador + Página Research
**Contexto:** El usuario proporcionó biografía real y tesis de maestría.

**Cambios en founders.html:**
- **Hero:** Nombre real "Emiliano Pérez"
- **Narrativa:** Biografía completa del usuario (6 párrafos)
- **Timeline:** Reescrito con etapas reales (Formation → Exploration → Foundation → Methodology → Expansion → Today)
- **Credentials:** 
  - Research: Link a tesis Universidad Distrital
  - Affiliations: Universidad Distrital, Green Building Council, Sustainable Building Council
  - Focus Areas: Ecological Community Design, Modular Construction, Territorial Planning, Environmental Stewardship
  - Countries: Colombia, Costa Rica, Panama
- **CTA:** WhatsApp message personalizado "Hi Emiliano, I read your story..."

**Nuevo archivo: research.html**
- Hero: "What is sustainable rural housing?"
- **Thesis Card:** Tesis UNIOESTE completa (autor, advisor, universidad, programa, fecha, páginas)
- **Download:** Link directo al PDF de la tesis
- **Abstract:** Resumen de la investigación
- **Key Findings:** 4 hallazgos principales
- **Methodology Connection:** Cómo la investigación se conecta con CHIHIZA
- **Academic Repository:** Lista de investigaciones (UDistrital + UNIOESTE)
- **CTA:** "See these principles in action"

**CSS additions:**
- `.research-card` — Tarjeta principal de tesis
- `.research-badge` — Badges (Master's Thesis, Open Access, Creative Commons)
- `.research-meta` — Grid de metadata
- `.research-abstract` — Resumen de investigación
- `.research-methods` — Lista de métodos
- `.research-findings-grid` — Grid de hallazgos
- `.research-connection` — Conexión investigación-CHIHIZA
- `.research-list` — Lista de investigaciones

**Nav actualizado:** Agregado "Research" en todas las páginas
**Footer actualizado:** Agregado link a Research en todos los footers

---

## Funcionalidades del Sitio

### Principal (index.html) — Versión Editorial/Emocional
- Hero fullscreen con imagen de fondo + narrativa emocional
- **GEA Workflow Diagram** (5 pasos SVG animados)
- **GEA Pillar Cards** (3 tarjetas visuales: Architecture, Manufacturing, Life)
- **Social Proof** (logos + testimonial)
- **Founder Teaser** (foto + narrativa + link)
- Slider de proyectos con scroll infinito (5 proyectos)
- How it Works: 3 pasos (Discover, Connect, Create)
- Formulario simplificado (5 campos → WhatsApp)
- FAQ accordion (5 preguntas)
- CTA con imagen de fondo
- THE PROCESS (panel lateral con 4 herramientas)
- WhatsApp float
- **Eliminados:** Stats animados, testimonios, team grid, sectores

### Herramientas de Equipo (tools/)
1. **Discovery** — Screening de oportunidades de inversión
2. **Due Diligence** — Análisis de terreno y evaluación de riesgo
3. **Digital Twin** — Ficha técnica y configuración paramétrica
4. **Financial Model** — Proyecciones, IRR, rendimientos

### Páginas Secundarias
- **About:** Hero con imagen, valores, stats, CTA
- **Founder:** Hero fullscreen, narrativa personal, timeline visual, credenciales, CTA (NUEVO)
- **Projects:** Filtros por país, catálogo con cards, CTA
- **Contact:** Formulario + métodos de contacto (WhatsApp, email, calendario)
- **Guide:** Hero, contenido, sidebar con lead capture (Name, Email, Country), descarga PDF
- **Legacy:** Hero, framework legal (solo demostrable), lead capture, descarga PDF
- **5 projetos individuales:** Hero, galería, narrativa sensorial, ubicación, CTA

### Componentes Reutilizables
- Header fijo con scroll effect
- Menú hamburger móvil (fullscreen overlay)
- Botón play parpadeante
- WhatsApp float
- Toast notifications
- Lightbox de imágenes
- Breadcrumbs
- Lead capture forms (Name, Email, Country)
- Fade-in on scroll (IntersectionObserver)
- **GEA Workflow Diagram** (5 pasos SVG animados)
- **GEA Pillar Cards** (3 tarjetas visuales con SVG)
- **Social Proof** (logos + testimonial)
- **Founder Teaser** (2 columnas: foto + narrativa)
- **Founder Timeline** (timeline visual vertical)
- **Credentials Grid** (4 cards: Educación, Reconocimientos, Publicaciones, Afiliaciones)

---

## Notas Técnicas

### CSS
- Variables CSS para colores, sombras, tipografía
- Sistema de sombras (xs → xl)
- Grid layouts responsive (1-2-4 columnas)
- Animaciones: fade-in, blink-glow, slide (slider)
- Media queries: 1024px, 768px, 480px
- **GEA Workflow** (flexbox horizontal, SVG animados)
- **GEA Pillar Cards** (grid 3 columnas, hover effects)
- **Social Proof** (flex logos, testimonial card)
- **Founder Teaser** (grid 2 columnas)
- **Founder Timeline** (vertical line + dots)
- **Credentials Grid** (grid 2 columnas)
- **Lead Capture Form** (vertical stack, select custom)

### JavaScript
- IIFE auto-ejecutable (sin globals innecesarios)
- IntersectionObserver para lazy loading y fade-in
- Smooth scroll para anchors
- Contadores animados con ease-out cubic
- Lightbox para galerías
- Toast notifications
- FAQ accordion
- Filtros de proyectos por país
- Team tools panel (slide-out)
- Mobile menu toggle

### Performance
- `loading="lazy"` en todas las imágenes
- Ancho/alto explícito en todas las imágenes (prevenir layout shift)
- `font-display: swap` en Google Fonts
- CSS/JS minificado (producción)
- Imágenes optimizadas (WebP donde es posible)

### SEO
- Title y meta description en todas las páginas
- Open Graph tags (og:title, og:description, og:image, og:url)
- Twitter Cards
- Canonical URLs
- Structured headings (h1 → h2 → h3)
- Alt text en todas las imágenes

---

## Próximos Pasos Pendientes

### Completado ✅
- [x] Hero emocional/editorial (no métricas financieras)
- [x] GEA como protagonista con sección expandida
- [x] Eliminar testimonios falsos
- [x] Eliminar equipo inventado
- [x] Simplificar formulario (5 campos)
- [x] Reordenar secciones (Hero → GEA → Projects → How it Works → Form → FAQ → CTA)
- [x] Rewrite copy emocional en todas las secciones
- [x] Actualizar meta tags con identidad arquitectónica
- [x] GEA Workflow Diagram (5 pasos SVG animados)
- [x] GEA Pillar Cards (3 tarjetas visuales con SVG)
- [x] Social Proof section (logos + testimonial)
- [x] Founder Teaser en index.html
- [x] founders.html (hero, narrativa, timeline, credenciales)
- [x] Lead capture en Guide y Legal (Name, Email, Country)
- [x] Legal page reescrita (solo prometer lo demostrable)
- [x] Proyecto Natauta reestructurado como "destino"
- [x] Nav link Founder en todas las páginas
- [x] Footer link Founder en todas las páginas
- [x] Biografía real del fundador (Emiliano Pérez)
- [x] research.html (tesis UNIOESTE + UDistrital)
- [x] Nav link Research en todas las páginas
- [x] Footer link Research en todas las páginas
- [x] Unificación About+Team (about.html absorbe founders.html)
- [x] Eliminación de founders.html
- [x] Nuevo process.html (7 pasos metodológicos)
- [x] Nav simplificada: eliminado "Team", agregado "Process"
- [x] Footer simplificado: About + Process
- [x] Montvento profundizado: Problem, Design Decisions, What We Learned
- [x] Research conectado con "This directly led to..." en cada tesis
- [x] Guide: "Free Download" → "Free After Registration"
- [x] Legacy: "Free Download" → "Free After Registration"
- [x] Contact: Proyectos dropdown actualizado (solo Montvento)
- [x] Costa Rica/Panamá eliminados de todos los dropdowns

### Pendiente (Requiere Contenido del Usuario)
- [ ] **Foto real de Emiliano** (ya en proyectos/team/emiliano.png, integrada en about.html)
- [ ] **Foto real de María** (pendiente)
- [ ] **Foto real de Julián David** (pendiente)
- [ ] **Fotos reales de obra/proceso** (reemplazar renders en Montvento)
- [ ] **Video corto de proceso** (futuro)
- [ ] **Documentos legales reales** (verificar PDF exists)

### Pendiente (Código)
- [ ] Verificar responsive en todos los breakpoints
- [ ] Actualizar BITACORA con hash del commit
- [ ] Agregar CSS para process.html timeline si es necesario

### 9. FASE 3: Estructura Unificada + Profundización (Basado en Crítica 9.1/10 — 26 jul 2026)
**Contexto:** Tercera crítica experta identificó: demasiadas páginas (8 para empresa pequeña), About y Team separados sin razón, falta de "Why We Founders", Projects vacíos, Guide contradicción ("free download" vs formulario), Legal sobrepromete.

**Cambios estructurales:**
- **Unificación About+Team:** about.html absorbe founders.html → página unificada con "Why We Exist" + 3 perfiles + credenciales + quote blocks. founders.html eliminado.
- **Nuevo: process.html:** Timeline visual de 7 pasos (Discovery → Territory Analysis → Masterplan → Architecture → Engineering → Construction → Delivery). Cada paso con narrativa editorial y contexto de metodología CHIHIZA.
- **Nav simplificada:** Home | Projects | About | Process | Research | Legal | Guide | Contact (eliminado "Team" link de todas las páginas)
- **Footer simplificado:** About + Process reemplazan About Us + Team

**Profundización Montvento (Case Study 001):**
- Nuevo: "The Problem" — desafíos reales del sitio (pendiente, sol, viento, acceso, suelo)
- Nuevo: "Design Decisions" — decisiones específicas (orientación, aleros, ventilación, materiales, cimentación)
- Nuevo: "What We Learned" — 4 lecciones concretas (sitio sabe mejor, materiales locales no son compromiso, diseño pasivo funciona, restricciones producen creatividad)
- Cada lección conectada con investigaciones específicas del equipo

**Investigación conectada con decisiones:**
- Cada tesis en research.html ahora tiene línea "This directly led to..." con fondo sage green y borde izquierdo
- Emiliano UNIOESTE → política de 50km
- Emiliano UDistrital → diseño climático responsive en Montvento
- María → framework de integración comunitaria
- Julián UDistrital → framework de viabilidad financiera
- Julián UniAgustiniana → filosofía de diseño centrada en humanos

**Correcciones de contenido:**
- Guide: "Free Download" → "Free After Registration" (hero tag + meta description)
- Legacy: "Free Download" → "Free After Registration"
- Contact: Proyectos dropdown actualizado (solo Montvento + General + Partnership)
- Guide/Legacy: Eliminados Costa Rica y Panamá de dropdown de países
- Index: Founder teaser link apunta a about.html (no founders.html)

### FASE 2 (Futuro)
- [ ] Case studies por proyecto (antes/después, datos reales)
- [ ] Behind the scenes (proceso de diseño)
- [ ] Video institucional (drone footage + entrevista)
- [ ] Blog section para contenido de autoridad
- [ ] Analytics (Google Analytics / Plausible)
- [ ] Optimizar tamaño de imágenes (actualmente ~2.5MB cada una)
- [ ] Minificar CSS/JS para producción
- [ ] Agregar analytics (Google Analytics / Plausible)
- [ ] Configurar dominio chihiza.com
