"""
================================================================================
PRESUPUESTO DE OBRA DETALLADO - VIVIENDA CAMPESTRE MINIMALISTA
================================================================================
Genera presupuesto completo en CSV con precios de Homecenter Colombia (2026)

Basado en ficha técnica:
- Terreno: 13m x 10m (130 m²)
- Edificio: 120 m² (2 niveles)
- Estructura: Block, losa armada
- Acabados: Minimalistas

Ejecutar: python presupuesto_obra.py
Genera: PRESUPUESTO_OBRA.csv (abrir en Excel)
================================================================================
"""

import csv
import os
from datetime import datetime

# ============================================================================================
# PARÁMETROS DEL PROYECTO (Desde TXT)
# ============================================================================================
PROYECTO = {
    'nombre': 'Vivienda Campestre Minimalista',
    'codigo': 'VC-2026-001',
    'ubicacion': 'Zona Periurbana, Colombia',
    'area_total': 120,  # m²
    'niveles': 2,
    'area_nivel1': 70,
    'area_nivel2': 50,
    'altura nivel': 2.8,
    'altura_total': 5.6,
    'largo_terreno': 13,
    'ancho_terreno': 10,
}

# ============================================================================================
# PRECIOS HOMECENTER COLOMBIA 2026 (COP) - Actualizados
# ============================================================================================
# Nota: Precios referenciales aproximados. Varían según sucursal y promociones.

PRECIOS = {
    # ============================================
    # 1. MOVIMIENTO DE TIERRA Y Preparación
    # ============================================
    'limpieza_terreno': {'unit': 'm²', 'price': 3500, 'desc': 'Limpieza y desmonte de terreno'},
    'nivelacion': {'unit': 'm²', 'price': 5500, 'desc': 'Nivelación manual del terreno'},
    'excavacion': {'unit': 'm³', 'price': 28000, 'desc': 'Excavación manual para cimentación'},
    'relleno': {'unit': 'm³', 'price': 18000, 'desc': 'Relleno y compactación'},
    'relleno_exportar': {'unit': 'm³', 'price': 35000, 'desc': 'Exportación de excedentes'},
    
    # ============================================
    # 2. CIMIENTOS
    # ============================================
    'concreto_f210': {'unit': 'm³', 'price': 285000, 'desc': 'Concreto f210 para zapatas'},
    'concreto_f280': {'unit': 'm³', 'price': 320000, 'desc': 'Concreto f280 para losas'},
    'acero_420x': {'unit': 'kg', 'price': 4800, 'desc': 'Acero de refuerzo 420x (varilla #4)'},
    'acero_240x': {'unit': 'kg', 'price': 4500, 'desc': 'Acero de refuerzo 240x (estribos)'},
    'malla_6x6_4mm': {'unit': 'm²', 'price': 18500, 'desc': 'Malla electrosoldada 6x6 #4'},
    'malla_6x6_5mm': {'unit': 'm²', 'price': 24000, 'desc': 'Malla electrosoldada 6x6 #5'},
    'formato_100x30': {'unit': 'pza', 'price': 8500, 'desc': 'Formato para zapata 100x30cm'},
    'formato_100x40': {'unit': 'pza', 'price': 11000, 'desc': 'Formato para zapata 100x40cm'},
    'formato_viga': {'unit': 'ml', 'price': 12000, 'desc': 'Formato para viga de amarre'},
    'polietileno': {'unit': 'm²', 'price': 2800, 'desc': 'Polietileno 200 micrones'},
    
    # ============================================
    # 3. ESTRUCTURA - LOSAS
    # ============================================
    'losa_maciza': {'unit': 'm²', 'price': 95000, 'desc': 'Losa maciza armada (concreto + acero + formatos)'},
    'losa_aligerada': {'unit': 'm²', 'price': 78000, 'desc': 'Losa aligerada con bovedilla'},
    'bovedilla': {'unit': 'pza', 'price': 3200, 'desc': 'Bovedilla de arcilla 24cm'},
    'bovedilla_12': {'unit': 'pza', 'price': 2100, 'desc': 'Bovedilla de arcilla 12cm'},
    'viga_cimentacion': {'unit': 'ml', 'price': 65000, 'desc': 'Viga de cimentación armada'},
    
    # ============================================
    # 4. MUROS - BLOCK
    # ============================================
    'block_14x20x40': {'unit': 'pza', 'price': 3200, 'desc': 'Block estructural 14x20x40cm'},
    'block_14x20x30': {'unit': 'pza', 'price': 2800, 'desc': 'Block estructural 14x20x30cm'},
    'block_9x20x40': {'unit': 'pza', 'price': 2400, 'desc': 'Block de divide 9x20x40cm'},
    'block_9x14x40': {'unit': 'pza', 'price': 2100, 'desc': 'Block divisorio 9x14x40cm'},
    'mortero_1': {'unit': 'bulto', 'price': 14500, 'desc': 'Mortero 1 (cemento + arena) 50kg'},
    'cemento_50kg': {'unit': 'bulto', 'price': 32000, 'desc': 'Cemento Portland 50kg (Cementos Argos)'},
    'arena_gruesa': {'unit': 'm³', 'price': 85000, 'desc': 'Arena gruesa para concreto'},
    'arena_fina': {'unit': 'm³', 'price': 75000, 'desc': 'Arena fina para mortero'},
    'piedra_chancada': {'unit': 'm³', 'price': 72000, 'desc': 'Piedra chancada #4'},
    'grava_3_4': {'unit': 'm³', 'price': 68000, 'desc': 'Grava 3/4 pulgada'},
    'varilla_3_8': {'unit': 'ml', 'price': 4200, 'desc': 'Varilla nervada 3/8" (10ft)'},
    'varilla_1_2': {'unit': 'ml', 'price': 7800, 'desc': 'Varilla nervada 1/2" (10ft)'},
    'alambre_18': {'unit': 'kg', 'price': 6500, 'desc': 'Alambre galvanizado #18'},
    'escombro': {'unit': 'm³', 'price': 55000, 'desc': 'Escombro reciclado para relleno'},
    
    # ============================================
    # 5. CUBIERTA
    # ============================================
    'impermeabilizante': {'unit': 'gal', 'price': 125000, 'desc': 'Impermeabilizante líquido (1 gal = 4m²)'},
    'malla_fibra': {'unit': 'm²', 'price': 4500, 'desc': 'Malla de fibra para impermeabilización'},
    'panel_techo': {'unit': 'm²', 'price': 45000, 'desc': 'Panel sandwich para cubierta (opcional)'},
    'canalón': {'unit': 'ml', 'price': 18000, 'desc': 'Canalón plástico 4 pulgadas'},
    'bajante': {'unit': 'ml', 'price': 15000, 'desc': 'Bajante plástico 3 pulgadas'},
    'tapa_canalon': {'unit': 'pza', 'price': 8000, 'desc': 'Tapa y rejilla canalón'},
    
    # ============================================
    # 6. INSTALACIONES ELÉCTRICAS
    # ============================================
    'cable_10': {'unit': 'ml', 'price': 2800, 'desc': 'Cable THW #10 (iluminación)'},
    'cable_6': {'unit': 'ml', 'price': 4500, 'desc': 'Cable THW #6 (tomas)'},
    'cable_4': {'unit': 'ml', 'price': 6200, 'desc': 'Cable THW #4 (A/C)'},
    'conduit_3_4': {'unit': 'ml', 'price': 3200, 'desc': 'Conduit PVC 3/4 pulgadas'},
    'conduit_1_2': {'unit': 'ml', 'price': 2100, 'desc': 'Conduit PVC 1/2 pulgada'},
    'caja_4x2': {'unit': 'pza', 'price': 2800, 'desc': 'Caja eléctrica 4x2 pulgadas'},
    'caja_6x6': {'unit': 'pza', 'price': 8500, 'desc': 'Caja de paso 6x6 pulgadas'},
    'tomacorriente': {'unit': 'pza', 'price': 12000, 'desc': 'Tomacorriente doble polarizado'},
    'interruptor': {'unit': 'pza', 'price': 9500, 'desc': 'Interruptor simple'},
    'panel_electrico': {'unit': 'pza', 'price': 185000, 'desc': 'Panel eléctrico 12 circuitos'},
    'breaker_20a': {'unit': 'pza', 'price': 18000, 'desc': 'Breaker termomagnético 20A'},
    'breaker_30a': {'unit': 'pza', 'price': 22000, 'desc': 'Breaker termomagnético 30A'},
    'breaker_diferencial': {'unit': 'pza', 'price': 85000, 'desc': 'Breaker diferencial 30mA'},
    'luminaria_led': {'unit': 'pza', 'price': 28000, 'desc': 'Plafón LED empotrado 18W'},
    'luminaria_ext': {'unit': 'pza', 'price': 45000, 'desc': 'Luminaria exterior LED 30W'},
    'interruptor_tactil': {'unit': 'pza', 'price': 65000, 'desc': 'Interruptor táctil dimmer'},
    
    # ============================================
    # 7. INSTALACIONES SANITARIAS
    # ============================================
    'tubo_pvc_4': {'unit': 'ml', 'price': 8500, 'desc': 'Tubo PVC sanitario 4"'},
    'tubo_pvc_2': {'unit': 'ml', 'price': 5500, 'desc': 'Tubo PVC sanitario 2"'},
    'tubo_cobre_1_2': {'unit': 'ml', 'price': 18000, 'desc': 'Tubo cobre agua fría 1/2"'},
    'tubo_cobre_3_4': {'unit': 'ml', 'price': 28000, 'desc': 'Tubo cobre agua fría 3/4"'},
    'tubo_pex': {'unit': 'ml', 'price': 12000, 'desc': 'Tubo PEX alternativa a cobre'},
    'codo_pvc_4': {'unit': 'pza', 'price': 3500, 'desc': 'Codo PVC 4" 90°'},
    'codo_pvc_2': {'unit': 'pza', 'price': 2200, 'desc': 'Codo PVC 2" 90°'},
    'tee_pvc_4': {'unit': 'pza', 'price': 4500, 'desc': 'Tee PVC 4"'},
    'tee_pvc_2': {'unit': 'pza', 'price': 3200, 'desc': 'Tee PVC 2"'},
    'v_reguladora': {'unit': 'pza', 'price': 45000, 'desc': 'Válvula reguladora de presión'},
    'llave_paso': {'unit': 'pza', 'price': 28000, 'desc': 'Llave de paso 1/2"'},
    'rejilla_desagüe': {'unit': 'pza', 'price': 15000, 'desc': 'Rejilla desagüe piso 4"'},
    'sifon': {'unit': 'pza', 'price': 12000, 'desc': 'Sifón lavamanos'},
    'tapas_acceso': {'unit': 'pza', 'price': 8000, 'desc': 'Tapa de acceso PVC'},
    
    # ============================================
    # 8. SANITARIOS Y GRIFERÍA (Homecenter)
    # ============================================
    'inodoro': {'unit': 'pza', 'price': 380000, 'desc': 'Inodoro colgado Roca/Innobath'},
    'lavamanos': {'unit': 'pza', 'price': 185000, 'desc': 'Lavamanos sobreponer Roca'},
    'lavamanos_empotrado': {'unit': 'pza', 'price': 280000, 'desc': 'Lavamanos empotrado Roca'},
    'ducha': {'unit': 'jgo', 'price': 220000, 'desc': 'Set ducha termostática'},
    'grifo_lavamanos': {'unit': 'pza', 'price': 165000, 'desc': 'Grifo lavamanos monocomando'},
    'grifo_cocina': {'unit': 'pza', 'price': 280000, 'desc': 'Grifo cocina pull-out'},
    'llave paso_bano': {'unit': 'pza', 'price': 35000, 'desc': 'Llave de paso cromada'},
    'válvula_inodoro': {'unit': 'pza', 'price': 85000, 'desc': 'Válvula descarga inodoro'},
    'tanque_inodoro': {'unit': 'pza', 'price': 120000, 'desc': 'Tanca Inodoro Roca'},
    'asiento_inodoro': {'unit': 'pza', 'price': 95000, 'desc': 'Asiento inodoro blanco'},
    'toallero': {'unit': 'pza', 'price': 45000, 'desc': 'Toallero cromado'},
    'jabonero': {'unit': 'pza', 'price': 35000, 'desc': 'Jabonero embebido'},
    'portarrollos': {'unit': 'pza', 'price': 32000, 'desc': 'Portarrollos cromado'},
    'espejo_bano': {'unit': 'pza', 'price': 185000, 'desc': 'Espejo bañera con luz LED'},
    
    # ============================================
    # 9. COCINA
    # ============================================
    'gabinete_cocina': {'unit': 'ml', 'price': 650000, 'desc': 'Gabinete cocina modular (por ml vertical)'},
    'meson_cuarzo': {'unit': 'ml', 'price': 380000, 'desc': 'Mesón cuarzo (por ml)'},
    'meson_granito': {'unit': 'ml', 'price': 280000, 'desc': 'Mesón granito (por ml)'},
    'fregadero': {'unit': 'pza', 'price': 320000, 'desc': 'Fregadero acero inoxidable doble'},
    'campana_extraccion': {'unit': 'pza', 'price': 480000, 'desc': 'Campana extracción 60cm'},
    'horno': {'unit': 'pza', 'price': 850000, 'desc': 'Horno eléctrico empotrado'},
    'cooktop': {'unit': 'pza', 'price': 650000, 'desc': 'Cooktop 4 quemadores gas'},
    'refrigerador': {'unit': 'pza', 'price': 1800000, 'desc': 'Refrigerador No Frost 350L'},
    'lavavajillas': {'unit': 'pza', 'price': 1200000, 'desc': 'Lavavajillas 14 cubiertos'},
    
    # ============================================
    # 10. PISOS Y REVESTIMIENTOS
    # ============================================
    'porcelanato_60x60': {'unit': 'm²', 'price': 45000, 'desc': 'Porcelanato 60x60cm (Homecenter)'},
    'porcelanato_60x120': {'unit': 'm²', 'price': 68000, 'desc': 'Porcelanato 60x120cm'},
    'ceramica_bano': {'unit': 'm²', 'price': 32000, 'desc': 'Cerámica pared baño 25x40cm'},
    'deck_madera': {'unit': 'm²', 'price': 125000, 'desc': 'Deck madera treated o pinus'},
    'deck_composite': {'unit': 'm²', 'price': 185000, 'desc': 'Deck composite (WPC)'},
    'piedra_borde': {'unit': 'ml', 'price': 28000, 'desc': 'Bordeador piedra natural'},
    'cerámica_piso_ext': {'unit': 'm²', 'price': 38000, 'desc': 'Cerámica piso exterior antideslizante'},
    'adhesivo_piso': {'unit': 'bulto', 'price': 28000, 'desc': 'Adhesivo para porcelanato (20kg)'},
    'cemento_colla': {'unit': 'bulto', 'price': 22000, 'desc': 'Cemento cola (20kg)'},
    'cruzetas_2mm': {'unit': 'caja', 'price': 8000, 'desc': 'Cruzetas 2mm (100 pzas)'},
    'cruzetas_3mm': {'unit': 'caja', 'price': 8000, 'desc': 'Cruzetas 3mm (100 pzas)'},
    'boquilla_piso': {'unit': 'kg', 'price': 8500, 'desc': 'Boquilla para juntas de piso'},
    'silicona': {'unit': 'tube', 'price': 18000, 'desc': 'Silicona sanitaria transparente'},
    'perfil_t': {'unit': 'ml', 'price': 12000, 'desc': 'Perfil T aluminio juntas'},
    
    # ============================================
    # 11. PINTURA
    # ============================================
    'pintura_latex': {'unit': 'gal', 'price': 125000, 'desc': 'Pintura látex interior (Pintuco)'},
    'pintura_acrilica': {'unit': 'gal', 'price': 145000, 'desc': 'Pintura acrílica exterior (Pintuco)'},
    'pintura_templada': {'unit': 'gal', 'price': 185000, 'desc': 'Pintura templada techos'},
    'primer': {'unit': 'gal', 'price': 95000, 'desc': 'Primer sellador'},
    'masilla': {'unit': 'kg', 'price': 12000, 'desc': 'Masilla para paredes'},
    'lija': {'unit': 'pza', 'price': 3500, 'desc': 'Lija grano 120'},
    'cinta_juntas': {'unit': 'rollo', 'price': 18000, 'desc': 'Cinta para juntas de paneles'},
    'brocha': {'unit': 'pza', 'price': 15000, 'desc': 'Brocha 4 pulgadas'},
    'rodillo': {'unit': 'pza', 'price': 18000, 'desc': 'Rodillo 23cm'},
    
    # ============================================
    # 12. CARPINTERÍA
    # ============================================
    'puerta_interior': {'unit': 'pza', 'price': 285000, 'desc': 'Puerta interior melamina 2.10x0.80'},
    'puerta_interior_alta': {'unit': 'pza', 'price': 385000, 'desc': 'Puerta interior alta 2.40x0.90'},
    'puerta_principal': {'unit': 'pza', 'price': 1200000, 'desc': 'Puerta principal madera maciza'},
    'marco_puerta': {'unit': 'jgo', 'price': 85000, 'desc': 'Marco puerta completo'},
    'bisagra': {'unit': 'pza', 'price': 18000, 'desc': 'Bisagra acero inoxidable'},
    'cerradura': {'unit': 'pza', 'price': 65000, 'desc': 'Cerradura inoxidable'},
    'jaladera': {'unit': 'pza', 'price': 28000, 'desc': 'Jaladera aluminio'},
    'ventana_aluminio': {'unit': 'm²', 'price': 320000, 'desc': 'Ventana aluminio + vidrio (m²)'},
    'ventana_correiza': {'unit': 'm²', 'price': 280000, 'desc': 'Ventana correiza aluminio (m²)'},
    'vidrio_templado': {'unit': 'm²', 'price': 185000, 'desc': 'Vidrio templado 8mm'},
    'vidrio_laminado': {'unit': 'm²', 'price': 225000, 'desc': 'Vidrio laminado 6+6mm'},
    'perfileria_aluminio': {'unit': 'ml', 'price': 18000, 'desc': 'Perfil aluminio natural'},
    'sellador': {'unit': 'tube', 'price': 15000, 'desc': 'Sellador silicona neutra'},
    
    # ============================================
    # 13. ACABADOS ESPECIALES
    # ============================================
    'madera_pergola': {'unit': 'ml', 'price': 85000, 'desc': 'Madera tratada pérgola'},
    'baranda_acero': {'unit': 'ml', 'price': 180000, 'desc': 'Baranda acero + vidrio'},
    'baranda_madera': {'unit': 'ml', 'price': 125000, 'desc': 'Baranda madera treated'},
    'escalera': {'unit': 'pza', 'price': 4500000, 'desc': 'Escalera caracol acero (opcional)'},
    'escalera_moderna': {'unit': 'pza', 'price': 6500000, 'desc': 'Escalera moderna huella flotante'},
    
    # ============================================
    # 14. PUERTAS Y VENTANAS EXTRAS
    # ============================================
    'puerta_garaje': {'unit': 'pza', 'price': 1850000, 'desc': 'Puerta sectional garaje'},
    'puerta_correiza': {'unit': 'm²', 'price': 380000, 'desc': 'Puerta correiza aluminio + vidrio'},
    'porton': {'unit': 'pza', 'price': 2200000, 'desc': 'Portón vehicular metálico'},
    'reja': {'unit': 'm²', 'price': 185000, 'desc': 'Reja seguridad metálica'},
    
    # ============================================
    # 15. SOSTENIBILIDAD
    # ============================================
    'panel_solar': {'unit': 'pza', 'price': 1800000, 'desc': 'Panel solar fotovoltaico 400W'},
    'inversor_solar': {'unit': 'pza', 'price': 2500000, 'desc': 'Inversor solar 3kW'},
    'bateria_solar': {'unit': 'pza', 'price': 3500000, 'desc': 'Batería litio 5kWh'},
    'calentador_solar': {'unit': 'pza', 'price': 2800000, 'desc': 'Calentador solar 200L'},
    'cisterna': {'unit': 'pza', 'price': 1200000, 'desc': 'Cisterna polietileno 1000L'},
    'bomba_agua': {'unit': 'pza', 'price': 650000, 'desc': 'Bomba sumergible 1HP'},
    'tanque_gravedad': {'unit': 'pza', 'price': 450000, 'desc': 'Tanque gravedad 200L'},
    'filtro_agua': {'unit': 'pza', 'price': 285000, 'desc': 'Filtro agua potable 3 etapas'},
    
    # ============================================
    # 16. PAISAJISMO
    # ============================================
    'cesped_rollo': {'unit': 'm²', 'price': 28000, 'desc': 'Césped en rollo (grama)'},
    'tierra_vegetal': {'unit': 'm³', 'price': 65000, 'desc': 'Tierra vegetal preparada'},
    'arbol_grande': {'unit': 'pza', 'price': 350000, 'desc': 'Árbol grande (3-4m)'},
    'arbol_pequeno': {'unit': 'pza', 'price': 125000, 'desc': 'Árbol pequeño (1.5-2m)'},
    'arbusto': {'unit': 'pza', 'price': 35000, 'desc': 'Arbusto (40-60cm)'},
    'planta_acceso': {'unit': 'pza', 'price': 18000, 'desc': 'Planta de acceso (maceta)'},
    'maceta_grande': {'unit': 'pza', 'price': 85000, 'desc': 'Maceta fibra cemento grande'},
    'tubo_riego': {'unit': 'ml', 'price': 2800, 'desc': 'Tubo goteo 16mm'},
    'gotero': {'unit': 'pza', 'price': 800, 'desc': 'Gotero compensador'},
    'temporizador_riego': {'unit': 'pza', 'price': 185000, 'desc': 'Temporizador riego automático'},
    'grava_paisajismo': {'unit': 'm³', 'price': 85000, 'desc': 'Grava ornamental blanca'},
    'piedra_paisajismo': {'unit': 'kg', 'price': 3500, 'desc': 'Piedra ornamental rivera'},
    'sendero_piedra': {'unit': 'm²', 'price': 95000, 'desc': 'Sendero piedra natural'},
    'luminaria_jardin': {'unit': 'pza', 'price': 85000, 'desc': 'Luminaria jardín LED solar'},
    'luminaria_sendero': {'unit': 'pza', 'price': 45000, 'desc': 'Luminaria sendero baja'},
    
    # ============================================
    # 17. HERRAMIENTAS Y VARIOS
    # ============================================
    'andamio': {'unit': 'día', 'price': 25000, 'desc': 'Alquiler andamio tubular'},
    'mezcladora': {'unit': 'día', 'price': 85000, 'desc': 'Alquiler mezcladora 200L'},
    'compactadora': {'unit': 'día', 'price': 120000, 'desc': 'Alquiler compactadora'},
    'herramienta_menor': {'unit': 'global', 'price': 350000, 'desc': 'Herramienta menor (palas, picos, etc.)'},
    'proteccion_personal': {'unit': 'global', 'price': 180000, 'desc': 'Elementos de protección personal'},
    'limpieza_final': {'unit': 'global', 'price': 450000, 'desc': 'Limpieza final de obra'},
    
    # ============================================
    # 18. MANO DE OBRA (Referencia Colombia 2026)
    # ============================================
    'maestro_obra': {'unit': 'día', 'price': 120000, 'desc': 'Maestro de obra (jornada diaria)'},
    'oficial': {'unit': 'día', 'price': 85000, 'desc': 'Oficial de construcción'},
    'peon': {'unit': 'día', 'price': 55000, 'desc': 'Peón / ayudante'},
    'albañil': {'unit': 'día', 'price': 95000, 'desc': 'Albañil especializado'},
    'electricista': {'unit': 'día', 'price': 110000, 'desc': 'Electricista matriculado'},
    'plomero': {'unit': 'día', 'price': 105000, 'desc': 'Plomero especialista'},
    'carpintero': {'unit': 'día', 'price': 100000, 'desc': 'Carpintero'},
    'pintor': {'unit': 'día', 'price': 90000, 'desc': 'Pintor especializado'},
    'soldador': {'unit': 'día', 'price': 115000, 'desc': 'Soldador certificado'},
    'instalador_pisos': {'unit': 'día', 'price': 105000, 'desc': 'Instalador de pisos'},
}

# ============================================================================================
# PARTIDAS DE OBRA CON CANTIDADES CALCULADAS
# ============================================================================================

PARTIDAS = [
    # ============================================
    # 1. MOVIMIENTO DE TIERRA
    # ============================================
    {
        'partida': '1. MOVIMIENTO DE TIERRA',
        'items': [
            {'desc': 'Limpieza y desmonte del terreno', 'key': 'limpieza_terreno', 'qty': 130},
            {'desc': 'Nivelación general del terreno', 'key': 'nivelacion', 'qty': 130},
            {'desc': 'Excavación para zapatas (6 zapatas 1.2x0.8x0.4)', 'key': 'excavacion', 'qty': 2.3},
            {'desc': 'Relleno compactado alrededor de zapatas', 'key': 'relleno', 'qty': 4.5},
            {'desc': 'Exportación de excedentes', 'key': 'relleno_exportar', 'qty': 3},
        ]
    },
    
    # ============================================
    # 2. CIMIENTOS
    # ============================================
    {
        'partida': '2. CIMIENTOS Y ESTRUCTURA INFERIOR',
        'items': [
            {'desc': 'Concreto f210 para zapatas (6 zapatas)', 'key': 'concreto_f210', 'qty': 2.3},
            {'desc': 'Acero de refuerzo zapatas (varilla #4)', 'key': 'acero_420x', 'qty': 180},
            {'desc': 'Estribos acero 240x', 'key': 'acero_240x', 'qty': 45},
            {'desc': 'Formatos para zapatas', 'key': 'formato_100x40', 'qty': 6},
            {'desc': 'Concreto viga de amarre f210', 'key': 'concreto_f210', 'qty': 1.8},
            {'desc': 'Acero vigas de amarre', 'key': 'acero_420x', 'qty': 120},
            {'desc': 'Formatos vigas de amarre', 'key': 'formato_viga', 'qty': 18},
            {'desc': 'Polietileno bajo losas', 'key': 'polietileno', 'qty': 70},
            {'desc': 'Piedra chancada base', 'key': 'piedra_chancada', 'qty': 3.5},
            {'desc': 'Arena gruesa', 'key': 'arena_gruesa', 'qty': 4},
            {'desc': 'Grava 3/4', 'key': 'grava_3_4', 'qty': 5},
        ]
    },
    
    # ============================================
    # 3. ESTRUCTURA LOSAS
    # ============================================
    {
        'partida': '3. ESTRUCTURA - LOSAS',
        'items': [
            {'desc': 'Losa maciza nivel 1 (70 m²)', 'key': 'losa_maciza', 'qty': 70},
            {'desc': 'Losa maciza nivel 2 (50 m²)', 'key': 'losa_maciza', 'qty': 50},
            {'desc': 'Malla electrosoldada 6x6 #5', 'key': 'malla_6x6_5mm', 'qty': 120},
            {'desc': 'Acero refuerzo losas', 'key': 'acero_420x', 'qty': 480},
            {'desc': 'Concreto f280 para losas', 'key': 'concreto_f280', 'qty': 14.4},
            {'desc': 'Arena gruesa para concreto', 'key': 'arena_gruesa', 'qty': 7.2},
            {'desc': 'Grava 3/4 para concreto', 'key': 'grava_3_4', 'qty': 10.8},
        ]
    },
    
    # ============================================
    # 4. MUROS
    # ============================================
    {
        'partida': '4. MUROS EN BLOCK',
        'items': [
            {'desc': 'Block estructural 14x20x40 muros exteriores', 'key': 'block_14x20x40', 'qty': 950},
            {'desc': 'Block divide 9x20x40 muros interiores', 'key': 'block_9x20x40', 'qty': 380},
            {'desc': 'Mortero 1 para asentado (2 bultos/m²)', 'key': 'mortero_1', 'qty': 45},
            {'desc': 'Cemento Portland 50kg', 'key': 'cemento_50kg', 'qty': 65},
            {'desc': 'Arena fina para mortero', 'key': 'arena_fina', 'qty': 8},
            {'desc': 'Varilla #3/8 para amarre', 'key': 'varilla_3_8', 'qty': 85},
            {'desc': 'Alambre #18 para amarre', 'key': 'alambre_18', 'qty': 25},
            {'desc': 'Escombro relleno muros', 'key': 'escombro', 'qty': 6},
        ]
    },
    
    # ============================================
    # 5. CUBIERTA
    # ============================================
    {
        'partida': '5. CUBIERTA',
        'items': [
            {'desc': 'Impermeabilizante líquido (110m²)', 'key': 'impermeabilizante', 'qty': 28},
            {'desc': 'Malla fibra refuerzo', 'key': 'malla_fibra', 'qty': 110},
            {'desc': 'Canalón plástico 4"', 'key': 'canalón', 'qty': 24},
            {'desc': 'Bajante plástico 3"', 'key': 'bajante', 'qty': 8},
            {'desc': 'Tapas y rejillas canalón', 'key': 'tapa_canalon', 'qty': 4},
        ]
    },
    
    # ============================================
    # 6. INSTALACIONES ELÉCTRICAS
    # ============================================
    {
        'partida': '6. INSTALACIONES ELÉCTRICAS',
        'items': [
            {'desc': 'Conduit PVC 3/4"', 'key': 'conduit_3_4', 'qty': 180},
            {'desc': 'Conduit PVC 1/2"', 'key': 'conduit_1_2', 'qty': 120},
            {'desc': 'Cable THW #10 (iluminación)', 'key': 'cable_10', 'qty': 350},
            {'desc': 'Cable THW #6 (tomas)', 'key': 'cable_6', 'qty': 220},
            {'desc': 'Cable THW #4 (A/C)', 'key': 'cable_4', 'qty': 40},
            {'desc': 'Cajas eléctricas 4x2"', 'key': 'caja_4x2', 'qty': 28},
            {'desc': 'Cajas de paso 6x6"', 'key': 'caja_6x6', 'qty': 8},
            {'desc': 'Tomacorrientes dobles', 'key': 'tomacorriente', 'qty': 18},
            {'desc': 'Interruptores simples', 'key': 'interruptor', 'qty': 12},
            {'desc': 'Interruptores táctiles dimmer', 'key': 'interruptor_tactil', 'qty': 4},
            {'desc': 'Panel eléctrico 12 circuitos', 'key': 'panel_electrico', 'qty': 1},
            {'desc': 'Breakers termomagnéticos 20A', 'key': 'breaker_20a', 'qty': 8},
            {'desc': 'Breaker diferencial 30mA', 'key': 'breaker_diferencial', 'qty': 2},
            {'desc': 'Plafones LED empotrados 18W', 'key': 'luminaria_led', 'qty': 16},
            {'desc': 'Luminarias exteriores LED 30W', 'key': 'luminaria_ext', 'qty': 6},
        ]
    },
    
    # ============================================
    # 7. INSTALACIONES SANITARIAS
    # ============================================
    {
        'partida': '7. INSTALACIONES SANITARIAS',
        'items': [
            {'desc': 'Tubo PVC sanitario 4"', 'key': 'tubo_pvc_4', 'qty': 25},
            {'desc': 'Tubo PVC sanitario 2"', 'key': 'tubo_pvc_2', 'qty': 35},
            {'desc': 'Tubo cobre agua fría 1/2"', 'key': 'tubo_cobre_1_2', 'qty': 45},
            {'desc': 'Tubo cobre agua fría 3/4"', 'key': 'tubo_cobre_3_4', 'qty': 12},
            {'desc': 'Codos PVC 4" 90°', 'key': 'codo_pvc_4', 'qty': 15},
            {'desc': 'Codos PVC 2" 90°', 'key': 'codo_pvc_2', 'qty': 22},
            {'desc': 'Tees PVC 4"', 'key': 'tee_pvc_4', 'qty': 8},
            {'desc': 'Tees PVC 2"', 'key': 'tee_pvc_2', 'qty': 12},
            {'desc': 'Válvula reguladora presión', 'key': 'v_reguladora', 'qty': 1},
            {'desc': 'Llaves de paso 1/2"', 'key': 'llave_paso', 'qty': 6},
            {'desc': 'Rejillas desagüe piso 4"', 'key': 'rejilla_desagüe', 'qty': 5},
            {'desc': 'Sifones lavamanos', 'key': 'sifon', 'qty': 3},
        ]
    },
    
    # ============================================
    # 8. SANITARIOS Y GRIFERÍA
    # ============================================
    {
        'partida': '8. SANITARIOS Y GRIFERÍA',
        'items': [
            {'desc': 'Inodoros colgados Roca (2.5)', 'key': 'inodoro', 'qty': 3},
            {'desc': 'Lavamanos sobreponer Roca', 'key': 'lavamanos', 'qty': 2},
            {'desc': 'Lavamanos empotrado (principal)', 'key': 'lavamanos_empotrado', 'qty': 1},
            {'desc': 'Set ducha termostática', 'key': 'ducha', 'qty': 2},
            {'desc': 'Grifos lavamanos monocomando', 'key': 'grifo_lavamanos', 'qty': 3},
            {'desc': 'Grifo cocina pull-out', 'key': 'grifo_cocina', 'qty': 1},
            {'desc': 'Válvulas descarga inodoro', 'key': 'válvula_inodoro', 'qty': 3},
            {'desc': 'Tancas inodoro Roca', 'key': 'tanque_inodoro', 'qty': 3},
            {'desc': 'Asientos inodoro', 'key': 'asiento_inodoro', 'qty': 3},
            {'desc': 'Toalleros cromados', 'key': 'toallero', 'qty': 3},
            {'desc': 'Jaboneros embebidos', 'key': 'jabonero', 'qty': 3},
            {'desc': 'Portarrollos cromados', 'key': 'portarrollos', 'qty': 3},
            {'desc': 'Espejos bañera con LED', 'key': 'espejo_bano', 'qty': 2},
        ]
    },
    
    # ============================================
    # 9. COCINA
    # ============================================
    {
        'partida': '9. COCINA',
        'items': [
            {'desc': 'Gabinete cocina modular (3 ml verticales)', 'key': 'gabinete_cocina', 'qty': 3},
            {'desc': 'Mesón cuarzo (2.5 ml)', 'key': 'meson_cuarzo', 'qty': 2.5},
            {'desc': 'Fregadero acero inoxidable doble', 'key': 'fregadero', 'qty': 1},
            {'desc': 'Campana extracción 60cm', 'key': 'campana_extraccion', 'qty': 1},
            {'desc': 'Cooktop 4 quemadores gas', 'key': 'cooktop', 'qty': 1},
        ]
    },
    
    # ============================================
    # 10. PISOS
    # ============================================
    {
        'partida': '10. PISOS Y REVESTIMIENTOS',
        'items': [
            {'desc': 'Porcelanato 60x60cm interior (100m²)', 'key': 'porcelanato_60x60', 'qty': 100},
            {'desc': 'Cerámica pared baño (25m²)', 'key': 'ceramica_bano', 'qty': 25},
            {'desc': 'Deck madera exterior (8m²)', 'key': 'deck_madera', 'qty': 8},
            {'desc': 'Adhesivo porcelanato (5 bultos)', 'key': 'adhesivo_piso', 'qty': 5},
            {'desc': 'Cemento cola (3 bultos)', 'key': 'cemento_colla', 'qty': 3},
            {'desc': 'Cruzetas 2mm', 'key': 'cruzetas_2mm', 'qty': 3},
            {'desc': 'Boquilla para juntas', 'key': 'boquilla_piso', 'qty': 25},
            {'desc': 'Silicona sanitaria', 'key': 'silicona', 'qty': 8},
        ]
    },
    
    # ============================================
    # 11. PINTURA
    # ============================================
    {
        'partida': '11. PINTURA',
        'items': [
            {'desc': 'Pintura látex interior (Pintuco) - 5 gal', 'key': 'pintura_latex', 'qty': 5},
            {'desc': 'Pintura acrílica exterior - 3 gal', 'key': 'pintura_acrilica', 'qty': 3},
            {'desc': 'Pintura templada techos - 2 gal', 'key': 'pintura_templada', 'qty': 2},
            {'desc': 'Primer sellador - 2 gal', 'key': 'primer', 'qty': 2},
            {'desc': 'Masilla para paredes - 20 kg', 'key': 'masilla', 'qty': 20},
            {'desc': 'Lijas various', 'key': 'lija', 'qty': 25},
            {'desc': 'Brochas y rodillos', 'key': 'brocha', 'qty': 6},
        ]
    },
    
    # ============================================
    # 12. CARPINTERÍA
    # ============================================
    {
        'partida': '12. CARPINTERÍA Y ESTRUCTURAS',
        'items': [
            {'desc': 'Puertas interiores melamina 2.10x0.80', 'key': 'puerta_interior', 'qty': 5},
            {'desc': 'Puerta principal madera maciza', 'key': 'puerta_principal', 'qty': 1},
            {'desc': 'Marcos puerta completos', 'key': 'marco_puerta', 'qty': 6},
            {'desc': 'Bisagras acero inoxidable', 'key': 'bisagra', 'qty': 18},
            {'desc': 'Cerraduras inoxidables', 'key': 'cerradura', 'qty': 6},
            {'desc': 'Jaladeras aluminio', 'key': 'jaladera', 'qty': 12},
            {'desc': 'Ventanas aluminio + vidrio (18m²)', 'key': 'ventana_aluminio', 'qty': 18},
            {'desc': 'Vidrio templado 8mm (4m²)', 'key': 'vidrio_templado', 'qty': 4},
            {'desc': 'Perfilería aluminio natural', 'key': 'perfileria_aluminio', 'qty': 45},
        ]
    },
    
    # ============================================
    # 13. PUERTA GARAJE
    # ============================================
    {
        'partida': '13. PUERTA GARAJE Y SEGURIDAD',
        'items': [
            {'desc': 'Puerta sectional garaje', 'key': 'puerta_garaje', 'qty': 1},
            {'desc': 'Portón vehicular metálico', 'key': 'porton', 'qty': 1},
        ]
    },
    
    # ============================================
    # 14. SOSTENIBILIDAD
    # ============================================
    {
        'partida': '14. SISTEMAS SOSTENIBLES',
        'items': [
            {'desc': 'Paneles solares fotovoltaicos 400W (2 pzas)', 'key': 'panel_solar', 'qty': 2},
            {'desc': 'Inversor solar 3kW', 'key': 'inversor_solar', 'qty': 1},
            {'desc': 'Cisterna polietileno 1000L', 'key': 'cisterna', 'qty': 1},
            {'desc': 'Bomba sumergible 1HP', 'key': 'bomba_agua', 'qty': 1},
            {'desc': 'Tanque gravedad 200L', 'key': 'tanque_gravedad', 'qty': 1},
            {'desc': 'Filtro agua potable 3 etapas', 'key': 'filtro_agua', 'qty': 1},
        ]
    },
    
    # ============================================
    # 15. PAISAJISMO
    # ============================================
    {
        'partida': '15. PAISAJISMO',
        'items': [
            {'desc': 'Césped en rollo (80m²)', 'key': 'cesped_rollo', 'qty': 80},
            {'desc': 'Tierra vegetal preparada', 'key': 'tierra_vegetal', 'qty': 8},
            {'desc': 'Árboles grandes (3-4m)', 'key': 'arbol_grande', 'qty': 4},
            {'desc': 'Árboles pequeños (1.5-2m)', 'key': 'arbol_pequeno', 'qty': 8},
            {'desc': 'Arbustos (40-60cm)', 'key': 'arbusto', 'qty': 20},
            {'desc': 'Plantas de acceso (maceta)', 'key': 'planta_acceso', 'qty': 10},
            {'desc': 'Macetas fibra cemento grandes', 'key': 'maceta_grande', 'qty': 6},
            {'desc': 'Sistema riego goteo (tubos)', 'key': 'tubo_riego', 'qty': 120},
            {'desc': 'Goteros compensadores', 'key': 'gotero', 'qty': 45},
            {'desc': 'Temporizador riego automático', 'key': 'temporizador_riego', 'qty': 1},
            {'desc': 'Grava ornamental blanca', 'key': 'grava_paisajismo', 'qty': 3},
            {'desc': 'Senderos piedra natural (12m²)', 'key': 'sendero_piedra', 'qty': 12},
            {'desc': 'Luminarias jardín LED solar', 'key': 'luminaria_jardin', 'qty': 8},
            {'desc': 'Luminarias sendero bajas', 'key': 'luminaria_sendero', 'qty': 6},
        ]
    },
    
    # ============================================
    # 16. HERRAMIENTAS Y VARIOS
    # ============================================
    {
        'partida': '16. HERRAMIENTAS Y VARIOS',
        'items': [
            {'desc': 'Alquiler andamio tubular (2 meses)', 'key': 'andamio', 'qty': 60},
            {'desc': 'Alquiler mezcladora 200L', 'key': 'mezcladora', 'qty': 25},
            {'desc': 'Herramienta menor', 'key': 'herramienta_menor', 'qty': 1},
            {'desc': 'Elementos de protección personal', 'key': 'proteccion_personal', 'qty': 1},
            {'desc': 'Limpieza final de obra', 'key': 'limpieza_final', 'qty': 1},
        ]
    },
    
    # ============================================
    # 17. MANO DE OBRA
    # ============================================
    {
        'partida': '17. MANO DE OBRA',
        'items': [
            {'desc': 'Maestro de obra (120 días)', 'key': 'maestro_obra', 'qty': 120},
            {'desc': 'Oficiales de construcción (3 x 120 días)', 'key': 'oficial', 'qty': 360},
            {'desc': 'Peones (2 x 120 días)', 'key': 'peon', 'qty': 240},
            {'desc': 'Electricista (20 días)', 'key': 'electricista', 'qty': 20},
            {'desc': 'Plomero (20 días)', 'key': 'plomero', 'qty': 20},
            {'desc': 'Carpintero (15 días)', 'key': 'carpintero', 'qty': 15},
            {'desc': 'Pintor (15 días)', 'key': 'pintor', 'qty': 15},
            {'desc': 'Instalador de pisos (12 días)', 'key': 'instalador_pisos', 'qty': 12},
        ]
    },
]

# ============================================================================================
# GENERAR CSV
# ============================================================================================
def generate_csv():
    """Genera el archivo CSV del presupuesto"""
    
    output_file = r"C:\Users\batos\OneDrive\Desktop\FELO\digital-twin-campestre\PRESUPUESTO_OBRA.csv"
    
    grand_total = 0
    
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        
        # ============================================
        # ENCABEZADO
        # ============================================
        writer.writerow(['=' * 100])
        writer.writerow(['PRESUPUESTO DE OBRA DETALLADO'])
        writer.writerow(['VIVIENDA CAMPESTRE MINIMALISTA - 120 m²'])
        writer.writerow(['=' * 100])
        writer.writerow([])
        writer.writerow(['Proyecto:', PROYECTO['nombre']])
        writer.writerow(['Código:', PROYECTO['codigo']])
        writer.writerow(['Ubicación:', PROYECTO['ubicacion']])
        writer.writerow(['Área total:', f"{PROYECTO['area_total']} m²"])
        writer.writerow(['Niveles:', str(PROYECTO['niveles'])])
        writer.writerow(['Fecha presupuesto:', datetime.now().strftime('%d/%m/%Y')])
        writer.writerow(['Moneda:', 'Pesos Colombianos (COP)'])
        writer.writerow(['Precios:', 'Homecenter Colombia 2026 (referenciales)'])
        writer.writerow([])
        writer.writerow(['=' * 100])
        writer.writerow([])
        
        # ============================================
        # TÍTULOS DE COLUMNAS
        # ============================================
        writer.writerow([
            'No.', 'PARTIDA / DESCRIPCIÓN', 'UNIDAD', 'CANTIDAD', 
            'PRECIO UNITARIO (COP)', 'PRECIO TOTAL (COP)', 'NOTAS'
        ])
        writer.writerow(['-' * 100])
        
        item_num = 0
        
        # ============================================
        # RECORRER PARTIDAS
        # ============================================
        for partida in PARTIDAS:
            writer.writerow([])
            writer.writerow([f"** {partida['partida']} **"])
            writer.writerow([])
            
            partida_total = 0
            
            for item in partida['items']:
                item_num += 1
                key = item['key']
                qty = item['qty']
                
                if key in PRECIOS:
                    precio_unit = PRECIOS[key]['price']
                    unit = PRECIOS[key]['unit']
                    desc = PRECIOS[key]['desc']
                    
                    # Calcular precio total
                    precio_total = qty * precio_unit
                    partida_total += precio_total
                    
                    # Formatear números
                    qty_str = f"{qty:,.1f}" if qty != int(qty) else f"{int(qty):,}"
                    precio_unit_str = f"${precio_unit:,.0f}"
                    precio_total_str = f"${precio_total:,.0f}"
                    
                    writer.writerow([
                        item_num,
                        item['desc'],
                        unit,
                        qty_str,
                        precio_unit_str,
                        precio_total_str,
                        desc
                    ])
            
            # Total partida
            writer.writerow(['-' * 100])
            writer.writerow(['', f"SUBTOTAL {partida['partida']}", '', '', '', f"${partida_total:,.0f}"])
            writer.writerow(['-' * 100])
            
            grand_total += partida_total
        
        # ============================================
        # TOTALES
        # ============================================
        writer.writerow([])
        writer.writerow(['=' * 100])
        writer.writerow([])
        writer.writerow(['', 'RESUMEN DEL PRESUPUESTO'])
        writer.writerow([])
        writer.writerow(['', 'SUBTOTAL MATERIALES Y MANO DE OBRA', '', '', '', f"${grand_total:,.0f}"])
        
        # Contingencia 10%
        contingencia = grand_total * 0.10
        writer.writerow(['', 'CONTINGENCIA (10%)', '', '', '', f"${contingencia:,.0f}"])
        
        # IVA 19%
        subtotal_con_contingencia = grand_total + contingencia
        iva = subtotal_con_contingencia * 0.19
        writer.writerow(['', 'IVA (19%)', '', '', '', f"${iva:,.0f}"])
        
        # TOTAL FINAL
        total_final = subtotal_con_contingencia + iva
        writer.writerow([])
        writer.writerow(['=' * 100])
        writer.writerow(['', 'TOTAL PRESUPUESTO DE OBRA', '', '', '', f"${total_final:,.0f}"])
        writer.writerow(['=' * 100])
        
        writer.writerow([])
        writer.writerow([f"Costo por m²: ${total_final / PROYECTO['area_total']:,.0f} COP/m²"])
        writer.writerow([])
        
        # ============================================
        # DESGLOSE POR CAPÍTULOS
        # ============================================
        writer.writerow([])
        writer.writerow(['=' * 100])
        writer.writerow(['DESGLOSE POR CAPÍTULOS'])
        writer.writerow(['=' * 100])
        writer.writerow([])
        writer.writerow(['CAPÍTULO', 'MONTO (COP)', '% DEL TOTAL'])
        
        # Recalcular para desglose
        chapter_totals = []
        for partida in PARTIDAS:
            ptotal = 0
            for item in partida['items']:
                key = item['key']
                if key in PRECIOS:
                    ptotal += item['qty'] * PRECIOS[key]['price']
            chapter_totals.append((partida['partida'], ptotal))
        
        for cap_name, cap_total in chapter_totals:
            pct = (cap_total / grand_total) * 100
            writer.writerow([cap_name, f"${cap_total:,.0f}", f"{pct:.1f}%"])
        
        writer.writerow(['-' * 60])
        writer.writerow(['TOTAL MATERIALES Y MANO DE OBRA', f"${grand_total:,.0f}", '100%'])
        
        writer.writerow([])
        writer.writerow(['=' * 100])
        writer.writerow(['NOTAS:'])
        writer.writerow(['1. Precios referenciales Homecenter Colombia julio 2026'])
        writer.writerow(['2. Precios pueden variar según sucursal y disponibilidad'])
        writer.writerow(['3. No incluye honorarios de arquitecto/ingeniero'])
        writer.writerow(['4. No incluye tramitología y permisos'])
        writer.writerow(['5. Contingencia cubre imprevistos y variaciones de precio'])
        writer.writerow(['6. IVA calculado sobre subtotal + contingencia'])
        writer.writerow(['7. Mano de obra referencial para Colombia central'])
        writer.writerow(['8. Se recomienda cotizar con 3 proveedores mínimo'])
        writer.writerow(['=' * 100])
    
    print("\n" + "=" * 70)
    print("PRESUPUESTO GENERADO EXITOSAMENTE")
    print("=" * 70)
    print(f"\nArchivo: {output_file}")
    print(f"\nRESUMEN:")
    print(f"  Subtotal materiales y mano de obra: ${grand_total:,.0f} COP")
    print(f"  Contingencia (10%):                 ${contingencia:,.0f} COP")
    print(f"  IVA (19%):                          ${iva:,.0f} COP")
    print(f"  TOTAL PRESUPUESTO:                  ${total_final:,.0f} COP")
    print(f"  Costo por m²:                       ${total_final / PROYECTO['area_total']:,.0f} COP/m²")
    print(f"\nPara abrir: Doble clic en el archivo CSV o abrir en Excel")
    print("=" * 70)


# ============================================================================================
# EJECUTAR
# ============================================================================================
if __name__ == '__main__':
    generate_csv()
