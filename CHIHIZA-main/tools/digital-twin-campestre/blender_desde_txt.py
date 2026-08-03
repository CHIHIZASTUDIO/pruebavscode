"""
================================================================================
GENERADOR BLENDER 3D - DESDE FICHA TÉCNICA TXT
================================================================================
Lee directamente el archivo .txt exportado y genera el modelo 3D en Blender.

INSTRUCCIONES:
1. Abrir Blender 3.0+
2. Ir a Scripting > New
3. Pegar este código
4. Cambiar TXT_FILE_PATH abajo
5. Alt+P para ejecutar
================================================================================
"""

import bpy
import bmesh
import math
import re
import os
from mathutils import Vector

# ============================================================================================
# CONFIGURACIÓN - CAMBIAR ESTA RUTA
# ============================================================================================
TXT_FILE_PATH = r"C:\Users\batos\Downloads\ficha-completa-vivienda-campestre-minimalista.txt"

# ============================================================================================
# PARSER DEL ARCHIVO TXT
# ============================================================================================
class FichaParser:
    """Parsea el archivo TXT de la ficha técnica"""
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = {}
        self.raw_lines = []
        
    def parse(self):
        """Lee y parsea el archivo completo"""
        with open(self.filepath, 'r', encoding='utf-8') as f:
            self.raw_lines = f.readlines()
        
        self.data = {
            'project': self._parse_project(),
            'site': self._parse_site(),
            'regulations': self._parse_regulations(),
            'program': self._parse_program(),
            'design': self._parse_design(),
            'materials': self._parse_materials(),
            'sustainability': self._parse_sustainability(),
            'landscape': self._parse_landscape(),
            'budget': self._parse_budget(),
            'schedule': self._parse_schedule()
        }
        return self.data
    
    def _get_value(self, line):
        """Extrae valor después de ':'"""
        if ':' in line:
            return line.split(':', 1)[1].strip()
        return ''
    
    def _get_number(self, line, default=0):
        """Extrae número de una línea"""
        val = self._get_value(line)
        # Remover unidades y caracteres
        val = re.sub(r'[m²°%USD,h]', '', val).strip()
        val = val.replace(',', '.')
        try:
            return float(val)
        except:
            return default
    
    def _get_bool(self, line):
        """Extrae booleano SÍ/NO"""
        val = self._get_value(line).upper()
        return 'SÍ' in val or 'SI' in val or 'YES' in val
    
    def _find_line(self, text):
        """Busca una línea que contenga el texto"""
        for line in self.raw_lines:
            if text in line:
                return line
        return ''
    
    def _find_section(self, start_text, end_texts=None):
        """Extrae líneas de una sección"""
        lines = []
        capturing = False
        for line in self.raw_lines:
            if start_text in line:
                capturing = True
                continue
            if capturing:
                if end_texts:
                    for end in end_texts:
                        if end in line:
                            capturing = False
                            break
                if capturing:
                    lines.append(line.strip())
        return lines
    
    def _parse_project(self):
        return {
            'name': self._get_value(self._find_line('Nombre del proyecto')),
            'code': self._get_value(self._find_line('Código:')),
        }
    
    def _parse_site(self):
        lot_length = self._get_number(self._find_line('Largo:'))
        lot_width = self._get_number(self._find_line('Ancho:'))
        
        return {
            'lot_length': lot_length,
            'lot_width': lot_width,
            'lot_area': lot_length * lot_width,
            'topography': self._get_value(self._find_line('Pendiente:')),
            'elevation': self._get_number(self._find_line('Elevación:')),
            'climate': self._get_value(self._find_line('Tipo:')).split('\n')[0] if 'Tipo:' in str(self._find_line('Tipo:')) else 'templado',
            'temp_min': self._get_number(self._find_line('Temperaturas:')),
            'temp_max': 26,
            'wind_direction': self._get_value(self._find_line('Viento predominante')),
            'orientation': self._get_value(self._find_line('Orientación principal')),
        }
    
    def _parse_regulations(self):
        return {
            'setback_front': self._get_number(self._find_line('Frontal:')),
            'setback_back': self._get_number(self._find_line('Posterior:')),
            'setback_side': self._get_number(self._find_line('Lateral:')),
            'max_height': self._get_number(self._find_line('Altura máxima:')),
            'max_levels': int(self._get_number(self._find_line('Niveles máximos:'))),
            'max_coverage': self._get_number(self._find_line('Ocupación suelo:')),
        }
    
    def _parse_program(self):
        total_area = self._get_number(self._find_line('Área total:'))
        levels = int(self._get_number(self._find_line('Niveles:')))
        floor_height = self._get_number(self._find_line('Altura/nivel:'))
        ceiling_height = self._get_number(self._find_line('Altura libre:'))
        slab_thickness = self._get_number(self._find_line('Espesor losa:'))
        
        # Áreas por nivel
        level1_area = self._get_number(self._find_line('NIVEL 1'))
        level2_area = self._get_number(self._find_line('NIVEL 2'))
        
        return {
            'total_area': total_area,
            'levels': levels,
            'floor_height': floor_height,
            'total_height': levels * floor_height,
            'ceiling_height': ceiling_height,
            'slab_thickness': slab_thickness,
            'level1_area': level1_area if level1_area else total_area / levels,
            'level2_area': level2_area if level2_area else total_area / levels,
            'bathrooms': self._get_number(self._find_line('Baños:')),
        }
    
    def _parse_design(self):
        # Ventanas
        win_line = self._find_line('Dimensiones:')
        win_dims = re.findall(r'[\d.]+', self._get_value(win_line))
        win_width = float(win_dims[0]) if len(win_dims) > 0 else 1.2
        win_height = float(win_dims[1]) if len(win_dims) > 1 else 1.8
        
        return {
            'style': self._get_value(self._find_line('Estilo:')),
            'roof_type': self._get_value(self._find_line('Tipo:')).split('\n')[0] if 'plana' in str(self._find_line('Tipo:')).lower() else 'plana',
            'roof_pitch': self._get_number(self._find_line('Inclinación:')),
            'roof_overhang': self._get_number(self._find_line('Volado:')),
            'roof_height': self._get_number(self._find_line('Altura cubierta:')),
            'window_width': win_width,
            'window_height': win_height,
            'window_ratio': self._get_number(self._find_line('Ratio ventana/muro:')),
            'door_height': self._get_number(self._find_line('Principal:')),
        }
    
    def _parse_materials(self):
        return {
            'wall_finish': self._get_value(self._find_line('Acabado principal:')),
            'wall_thickness': self._get_number(self._find_line('Espesor:')),
            'accent_material': self._get_value(self._find_line('Material:')).split('\n')[0] if 'Material:' in str(self._find_line('Material:')) else 'madera_oscura',
            'floor_interior': self._get_value(self._find_line('Interior:')),
            'floor_exterior': self._get_value(self._find_line('Exterior:')),
            'glass_type': self._get_value(self._find_line('Tipo:')).split('\n')[0] if 'transparente' in str(self._find_line('Tipo:')).lower() else 'transparente',
            'frame_color': self._get_value(self._find_line('Color:')),
        }
    
    def _parse_sustainability(self):
        return {
            'solar_pv': self._get_bool(self._find_line('Solar fotovoltaico')),
            'rainwater': self._get_bool(self._find_line('Recolección lluvia')),
        }
    
    def _parse_landscape(self):
        return {
            'trees_large': int(self._get_number(self._find_line('Árboles grandes'))),
            'trees_small': int(self._get_number(self._find_line('Árboles pequeños'))),
            'bushes': int(self._get_number(self._find_line('Arbustos:'))),
            'grass_area': self._get_number(self._find_line('Césped:')),
            'deck': self._get_bool(self._find_line('Deck:')),
            'paths': self._get_bool(self._find_line('Senderos:')),
        }
    
    def _parse_budget(self):
        return {
            'total': self._get_number(self._find_line('Presupuesto total:')),
            'cost_m2': self._get_number(self._find_line('Costo/m²:')),
        }
    
    def _parse_schedule(self):
        return {
            'start': self._get_value(self._find_line('Inicio:')),
            'duration': self._get_number(self._find_line('Duración:')),
        }


# ============================================================================================
# GENERADOR 3D
# ============================================================================================
class Vivienda3DGenerator:
    """Genera el modelo 3D en Blender"""
    
    def __init__(self, params):
        self.p = params
        self.materials = {}
        
    def clear_scene(self):
        """Limpia escena"""
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        
        for mat in bpy.data.materials:
            bpy.data.materials.remove(mat)
        for mesh in bpy.data.meshes:
            bpy.data.meshes.remove(mesh)
    
    def create_mat(self, name, color, roughness=0.5, metallic=0.0, alpha=1.0):
        """Crea material"""
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        
        for node in nodes:
            nodes.remove(node)
        
        output = nodes.new('ShaderNodeOutputMaterial')
        bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        
        bsdf.inputs['Base Color'].default_value = (*color, 1)
        bsdf.inputs['Roughness'].default_value = roughness
        bsdf.inputs['Metallic'].default_value = metallic
        
        if alpha < 1.0:
            bsdf.inputs['Alpha'].default_value = alpha
            mat.blend_method = 'BLEND' if hasattr(mat, 'blend_method') else None
        
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        self.materials[name] = mat
        return mat
    
    def setup_materials(self):
        """Configura materiales según TXT"""
        mat_data = self.p.get('materials', {})
        
        # Colores según selección
        wall_colors = {
            'blanco_puro': (0.95, 0.95, 0.93),
            'hormigon_visto': (0.6, 0.6, 0.58),
            'madera_clara': (0.7, 0.55, 0.4),
            'piedra_natural': (0.55, 0.52, 0.48),
            'ladrillo_vista': (0.72, 0.38, 0.22),
        }
        
        accent_colors = {
            'madera_oscura': (0.32, 0.2, 0.1),
            'negro_mate': (0.08, 0.08, 0.08),
            'acero_corten': (0.62, 0.3, 0.15),
            'cobre': (0.72, 0.45, 0.2),
        }
        
        floor_colors = {
            'porcelanato': (0.88, 0.86, 0.84),
            'madera': (0.58, 0.42, 0.28),
            'concreto_pulido': (0.55, 0.55, 0.55),
            'deck_madera': (0.52, 0.38, 0.25),
            'piedra_natural': (0.5, 0.48, 0.45),
        }
        
        wall_key = mat_data.get('wall_finish', 'blanco_puro')
        accent_key = mat_data.get('accent_material', 'madera_oscura')
        floor_int_key = mat_data.get('floor_interior', 'porcelanato')
        floor_ext_key = mat_data.get('floor_exterior', 'deck_madera')
        
        self.create_mat('Muro', wall_colors.get(wall_key, (0.92, 0.92, 0.9)), 0.88)
        self.create_mat('Muro_Int', (0.95, 0.95, 0.93), 0.9)
        self.create_mat('Acento', accent_colors.get(accent_key, (0.35, 0.22, 0.12)), 0.65)
        self.create_mat('Piso_Int', floor_colors.get(floor_int_key, (0.85, 0.85, 0.83)), 0.25, 0.15)
        self.create_mat('Piso_Ext', floor_colors.get(floor_ext_key, (0.5, 0.38, 0.25)), 0.82)
        self.create_mat('Vidrio', (0.65, 0.82, 0.95), 0.02, 0.85)
        self.create_mat('Marco', (0.1, 0.1, 0.1), 0.45, 0.75)
        self.create_mat('Losa', (0.62, 0.62, 0.6), 0.88)
        self.create_mat('Cubierta', (0.22, 0.22, 0.22), 0.72)
        self.create_mat('Concreto', (0.52, 0.52, 0.5), 0.85)
        self.create_mat('Hierba', (0.28, 0.52, 0.2), 0.92)
        self.create_mat('Tronco', (0.35, 0.22, 0.12), 0.92)
        self.create_mat('Hojas', (0.22, 0.48, 0.18), 0.88)
        self.create_mat('Grava', (0.55, 0.52, 0.48), 0.95)
        self.create_mat('Tierra', (0.42, 0.32, 0.22), 0.95)
    
    def box(self, name, loc, size, mat='Muro'):
        """Crea caja"""
        bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
        obj = bpy.context.active_object
        obj.name = name
        obj.scale = (size[0]/2, size[1]/2, size[2]/2)
        bpy.ops.object.transform_apply(scale=True)
        if mat in self.materials:
            obj.data.materials.append(self.materials[mat])
        return obj
    
    def cylinder(self, name, loc, radius, depth, mat='Tronco'):
        """Crea cilindro"""
        bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=loc)
        obj = bpy.context.active_object
        obj.name = name
        if mat in self.materials:
            obj.data.materials.append(self.materials[mat])
        return obj
    
    def sphere(self, name, loc, radius, mat='Hojas', scale_z=1.0):
        """Crea esfera"""
        bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, segments=12, ring_count=8, location=loc)
        obj = bpy.context.active_object
        obj.name = name
        obj.scale = (1, 1, scale_z)
        bpy.ops.object.transform_apply(scale=True)
        if mat in self.materials:
            obj.data.materials.append(self.materials[mat])
        return obj
    
    def generate(self):
        """Genera modelo completo"""
        print("\n" + "="*60)
        print("GENERANDO MODELO 3D DESDE FICHA TÉCNICA")
        print("="*60)
        
        self.clear_scene()
        self.setup_materials()
        
        # Obtener parámetros
        site = self.p.get('site', {})
        program = self.p.get('program', {})
        design = self.p.get('design', {})
        landscape = self.p.get('landscape', {})
        regulations = self.p.get('regulations', {})
        
        lot_l = site.get('lot_length', 25)
        lot_w = site.get('lot_width', 15)
        total_area = program.get('total_area', 120)
        levels = program.get('levels', 2)
        floor_h = program.get('floor_height', 2.8)
        total_h = program.get('total_height', 5.6)
        ceiling_h = program.get('ceiling_height', 2.6)
        slab_t = program.get('slab_thickness', 0.2)
        
        # Calcular dimensiones del edificio
        bldg_w = min(lot_w - 4, math.sqrt(total_area / levels) * 1.15)
        bldg_l = (total_area / levels) / bldg_w
        bldg_w = min(bldg_w, 11)
        bldg_l = min(bldg_l, 13)
        
        roof_type = design.get('roof_type', 'plana')
        roof_overhang = design.get('roof_overhang', 0.6)
        roof_height = design.get('roof_height', 0.3)
        win_w = design.get('window_width', 1.2)
        win_h = design.get('window_height', 1.8)
        door_h = design.get('door_height', 2.4)
        
        setback_front = regulations.get('setback_front', 4)
        
        print(f"Terreno: {lot_l}m x {lot_w}m")
        print(f"Edificio: {bldg_w:.1f}m x {bldg_l:.1f}m")
        print(f"Niveles: {levels}, Altura: {total_h}m")
        
        # ============================================
        # TERRENO
        # ============================================
        print("Creando terreno...")
        
        bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
        terrain = bpy.context.active_object
        terrain.name = 'Terreno'
        terrain.scale = (lot_l, lot_w, 1)
        bpy.ops.object.transform_apply(scale=True)
        if 'Hierba' in self.materials:
            terrain.data.materials.append(self.materials['Hierba'])
        
        # Borde del terreno
        self.box('Borde_N', (0, lot_w/2, 0.01), (lot_l, 0.15, 0.03), 'Concreto')
        self.box('Borde_S', (0, -lot_w/2, 0.01), (lot_l, 0.15, 0.03), 'Concreto')
        self.box('Borde_E', (lot_l/2, 0, 0.01), (0.15, lot_w, 0.03), 'Concreto')
        self.box('Borde_O', (-lot_l/2, 0, 0.01), (0.15, lot_w, 0.03), 'Concreto')
        
        # Camino de entrada
        self.box('Camino', (0, lot_l/4 + 1, 0.01), (1.5, lot_l/2, 0.02), 'Concreto')
        
        # ============================================
        # PLATAFORMA BASE
        # ============================================
        print("Creando plataforma...")
        
        self.box('Plataforma', (0, 0, -0.2), (bldg_w + 2, bldg_l + 2, 0.4), 'Concreto')
        
        # ============================================
        # EDIFICIO - POR NIVEL
        # ============================================
        print("Creando edificio...")
        
        wall_t = 0.15  # Espesor muro
        
        for lvl in range(levels):
            y = lvl * floor_h
            lvl_name = f'Nivel{lvl+1}'
            
            # --- Muros exteriores ---
            # Frontal
            self.box(f'{lvl}_Muro_F', (0, bldg_l/2, y + floor_h/2), 
                     (bldg_w, wall_t, floor_h), 'Muro')
            # Posterior
            self.box(f'{lvl}_Muro_B', (0, -bldg_l/2, y + floor_h/2), 
                     (bldg_w, wall_t, floor_h), 'Muro')
            # Izquierdo
            self.box(f'{lvl}_Muro_L', (-bldg_w/2, 0, y + floor_h/2), 
                     (wall_t, bldg_l, floor_h), 'Muro')
            # Derecho
            self.box(f'{lvl}_Muro_R', (bldg_w/2, 0, y + floor_h/2), 
                     (wall_t, bldg_l, floor_h), 'Muro')
            
            # --- Losa ---
            self.box(f'{lvl}_Losa', (0, 0, y - slab_t/2), 
                     (bldg_w + 0.3, bldg_l + 0.3, slab_t), 'Losa')
            
            # --- Ventanas Frontales (2) ---
            for i, xoff in enumerate([-0.35, 0.35]):
                x = xoff * bldg_w
                self.box(f'{lvl}_Win_F{i}', 
                         (x, bldg_l/2 + 0.02, y + floor_h * 0.55),
                         (win_w, 0.02, win_h), 'Vidrio')
                self.box(f'{lvl}_Frame_F{i}', 
                         (x, bldg_l/2 + 0.03, y + floor_h * 0.55),
                         (win_w + 0.08, 0.04, win_h + 0.08), 'Marco')
            
            # --- Ventanas Posteriores (2) ---
            for i, xoff in enumerate([-0.35, 0.35]):
                x = xoff * bldg_w
                self.box(f'{lvl}_Win_B{i}', 
                         (x, -bldg_l/2 - 0.02, y + floor_h * 0.55),
                         (win_w, 0.02, win_h), 'Vidrio')
                self.box(f'{lvl}_Frame_B{i}', 
                         (x, -bldg_l/2 - 0.03, y + floor_h * 0.55),
                         (win_w + 0.08, 0.04, win_h + 0.08), 'Marco')
            
            # --- Ventanas Laterales (1 por lado) ---
            for side in [-1, 1]:
                self.box(f'{lvl}_Win_S{side}', 
                         (side * bldg_w/2 - 0.02 * side, 0, y + floor_h * 0.55),
                         (0.02, win_w * 0.8, win_h), 'Vidrio')
                self.box(f'{lvl}_Frame_S{side}', 
                         (side * bldg_w/2 - 0.03 * side, 0, y + floor_h * 0.55),
                         (0.04, win_w * 0.8 + 0.08, win_h + 0.08), 'Marco')
            
            # --- Puerta principal (solo nivel 0) ---
            if lvl == 0:
                self.box('Puerta', 
                         (0, bldg_l/2 + 0.02, door_h/2),
                         (1.0, 0.08, door_h), 'Acento')
                self.box('Marco_Puerta', 
                         (0, bldg_l/2 + 0.03, door_h/2),
                         (1.1, 0.05, door_h + 0.06), 'Marco')
            
            # --- Acentos nivel 0 ---
            if lvl == 0:
                # Línea horizontal superior
                self.box('Linea_Acento', 
                         (0, bldg_l/2 + 0.06, y + floor_h),
                         (bldg_w + 0.12, 0.12, 0.1), 'Acento')
                # Columnas
                for side in [-1, 1]:
                    self.box(f'Columna_{side}', 
                             (side * bldg_w/2 + side * 0.05, bldg_l/2 + 0.08, y + floor_h/2),
                             (0.12, 0.12, floor_h), 'Acento')
        
        # ============================================
        # CUBIERTA
        # ============================================
        print("Creando cubierta...")
        
        top_y = levels * floor_h
        
        if roof_type == 'plana':
            self.box('Cubierta', (0, 0, top_y + roof_height/2), 
                     (bldg_w + roof_overhang*2, bldg_l + roof_overhang*2, roof_height), 'Cubierta')
            
            # Barandilla
            bar_h = 0.5
            bar_t = 0.06
            for sx in [-1, 1]:
                self.box(f'Bar_X{sx}', 
                         (sx * (bldg_w/2 + roof_overhang), 0, top_y + bar_h/2 + roof_height),
                         (bar_t, bldg_l + roof_overhang*2, bar_h), 'Acento')
            for sy in [-1, 1]:
                self.box(f'Bar_Y{sy}', 
                         (0, sy * (bldg_l/2 + roof_overhang), top_y + bar_h/2 + roof_height),
                         (bldg_w + roof_overhang*2, bar_t, bar_h), 'Acento')
        
        # ============================================
        # TERRAZA / DECK
        # ============================================
        print("Creando terraza...")
        
        if landscape.get('deck', True):
            deck_w = bldg_w * 0.6
            deck_l = 2.5
            self.box('Deck', (bldg_w * 0.2, bldg_l/2 + deck_l/2 + 0.5, 0.05), 
                     (deck_w, deck_l, 0.1), 'Piso_Ext')
            
            # Escalón
            self.box('Escalon', (0, bldg_l/2 + deck_l + 0.8, -0.1), 
                     (deck_w + 1, 0.4, 0.2), 'Concreto')
        
        # ============================================
        # ESTACIONAMIENTO
        # ============================================
        print("Creando estacionamiento...")
        
        park_w = 5.5
        park_l = 5
        self.box('Estacionamiento', (-bldg_w/2 + park_w/2 - 1, -bldg_l/2 - park_l/2 - 1, 0.01), 
                 (park_w, park_l, 0.02), 'Concreto')
        # Líneas
        for i in range(2):
            x = -bldg_w/2 + park_w/2 - 1 + (i - 0.5) * 2.8
            self.box(f'Linea_Park{i}', (x, -bldg_l/2 - 1, 0.025), 
                     (0.1, park_l - 0.5, 0.01), 'Marco')
        
        # ============================================
        # VEGETACIÓN
        # ============================================
        print("Creando vegetación...")
        
        num_trees_lg = landscape.get('trees_large', 4)
        num_trees_sm = landscape.get('trees_small', 8)
        num_bushes = landscape.get('bushes', 20)
        
        # Árboles grandes
        for i in range(num_trees_lg):
            angle = (i / num_trees_lg) * 2 * math.pi + 0.5
            radius = 10 + (i % 3) * 3
            x = math.cos(angle) * radius
            y = math.sin(angle) * radius
            
            # Limitar al terreno
            x = max(-lot_l/2 + 2, min(lot_l/2 - 2, x))
            y = max(-lot_w/2 + 2, min(lot_w/2 - 2, y))
            
            h = 4 + (i % 2) * 0.5
            self.cylinder(f'Arbol_Lg_{i}_Trunk', (x, y, h*0.35), 0.18, h*0.7, 'Tronco')
            self.sphere(f'Arbol_Lg_{i}_Crown', (x, y, h*0.75), 2.2 + (i%2)*0.3, 'Hojas', 0.8)
        
        # Árboles pequeños
        for i in range(num_trees_sm):
            angle = (i / num_trees_sm) * 2 * math.pi + 1.2
            radius = 7 + (i % 4) * 2
            x = math.cos(angle) * radius
            y = math.sin(angle) * radius
            
            x = max(-lot_l/2 + 1.5, min(lot_l/2 - 1.5, x))
            y = max(-lot_w/2 + 1.5, min(lot_w/2 - 1.5, y))
            
            h = 2.5 + (i % 3) * 0.3
            self.cylinder(f'Arbol_Sm_{i}_Trunk', (x, y, h*0.35), 0.1, h*0.7, 'Tronco')
            self.sphere(f'Arbol_Sm_{i}_Crown', (x, y, h*0.7), 1.3 + (i%2)*0.2, 'Hojas', 0.75)
        
        # Arbustos
        for i in range(min(num_bushes, 25)):
            angle = (i / num_bushes) * 2 * math.pi + 2.0
            radius = 4 + (i % 6) * 1.5
            x = math.cos(angle) * radius
            y = math.sin(angle) * radius
            
            x = max(-lot_l/2 + 1, min(lot_l/2 - 1, x))
            y = max(-lot_w/2 + 1, min(lot_w/2 - 1, y))
            
            self.sphere(f'Bush_{i}', (x, y, 0.35), 0.45 + (i%3)*0.08, 'Hojas', 0.65)
        
        # ============================================
        # ILUMINACIÓN
        # ============================================
        print("Configurando iluminación...")
        
        # Sol
        bpy.ops.object.light_add(type='SUN', location=(15, -10, 25))
        sun = bpy.context.active_object
        sun.name = 'Sun'
        sun.data.energy = 4
        sun.rotation_euler = (math.radians(50), math.radians(15), math.radians(-35))
        
        # Cielo
        world = bpy.context.scene.world
        if not world:
            world = bpy.data.worlds.new("World")
            bpy.context.scene.world = world
        world.use_nodes = True
        bg = world.node_tree.nodes['Background']
        bg.inputs['Color'].default_value = (0.55, 0.72, 0.92, 1)
        bg.inputs['Strength'].default_value = 0.6
        
        # ============================================
        # CÁMARA
        # ============================================
        print("Configurando cámara...")
        
        cam_x = lot_l * 0.6
        cam_y = -lot_w * 0.6
        cam_z = total_h * 2.2
        
        bpy.ops.object.camera_add(
            location=(cam_x, cam_y, cam_z),
            rotation=(math.radians(58), 0, math.radians(42))
        )
        cam = bpy.context.active_object
        cam.name = 'Camera_Main'
        bpy.context.scene.camera = cam
        
        # ============================================
        # RENDER
        # ============================================
        print("Configurando render...")
        
        scene = bpy.context.scene
        scene.render.engine = 'CYCLES'
        scene.cycles.samples = 64
        scene.render.resolution_x = 1920
        scene.render.resolution_y = 1080
        
        # ============================================
        # FIN
        # ============================================
        bpy.ops.object.select_all(action='DESELECT')
        
        print("\n" + "="*60)
        print("MODELO GENERADO EXITOSAMENTE")
        print(f"Terreno: {lot_l}m x {lot_w}m")
        print(f"Edificio: {bldg_w:.1f}m x {bldg_l:.1f}m x {total_h}m")
        print(f"Niveles: {levels}")
        print(f"Vegetación: {num_trees_lg} árboles grandes, {num_trees_sm} pequeños, {num_bushes} arbustos")
        print("="*60)
        print("\nPara render: Ctrl+F12 o Render > Render Image")
        print("Para guardar: Image > Save As")
        print("="*60 + "\n")


# ============================================================================================
# EJECUTAR
# ============================================================================================
def main():
    if not os.path.exists(TXT_FILE_PATH):
        print(f"\nERROR: No se encontró el archivo:")
        print(f"  {TXT_FILE_PATH}")
        print("\nVerifica la ruta en TXT_FILE_PATH")
        return
    
    print(f"Leyendo ficha técnica: {TXT_FILE_PATH}")
    
    parser = FichaParser(TXT_FILE_PATH)
    params = parser.parse()
    
    generator = Vivienda3DGenerator(params)
    generator.generate()


if __name__ == '__main__':
    main()
