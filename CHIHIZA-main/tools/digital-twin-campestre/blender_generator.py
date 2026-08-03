"""
================================================================================
GENERADOR DE MODELO 3D - VIVIENDA CAMPESTRE PARAMÉTRICA
================================================================================
Script de Blender que genera un modelo 3D detallado a partir de un archivo
de parámetros (.json o .txt exportado desde la ficha técnica).

INSTRUCCIONES:
1. Abrir Blender (3.0 o superior)
2. Ir a Scripting workspace
3. Abrir este archivo o pegar el código
4. Cambiar la ruta del archivo de parámetros en PARAMS_FILE
5. Click en "Run Script" o presionar Alt+P

El modelo se generará automáticamente con:
- Terreno y topografía
- Edificio completo (muros, losas, cubierta)
- Ventanas y puertas
- Materiales básicos
- Vegetación básica
================================================================================
"""

import bpy
import bmesh
import json
import os
import math
from mathutils import Vector

# ============================================================================================
# CONFIGURACIÓN
# ============================================================================================
PARAMS_FILE = r"C:\Users\batos\OneDrive\Desktop\FELO\digital-twin-campestre\parametros-vivienda-campestre-minimalista.json"

# Escala: 1 unidad Blender = 1 metro
SCALE = 1.0

# Resolución de vegetación
TREE_SEGMENTS = 8
BUSH_SEGMENTS = 6

# ============================================================================================
# CLASE PRINCIPAL
# ============================================================================================
class ViviendaCampestreGenerator:
    def __init__(self, params):
        self.params = params
        self.collections = {}
        self.materials = {}
        
    def clear_scene(self):
        """Limpia la escena de Blender"""
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        
        # Limpiar materiales huérfanos
        for mat in bpy.data.materials:
            bpy.data.materials.remove(mat)
        
        # Limpiar mallas huérfanas
        for mesh in bpy.data.meshes:
            bpy.data.meshes.remove(mesh)
    
    def create_collections(self):
        """Crea las colecciones organizativas"""
        collections = {
            'Terreno': None,
            'Edificio': None,
            'Muros': None,
            'Ventanas': None,
            'Puertas': None,
            'Cubierta': None,
            'Pisos': None,
            'Acabados': None,
            'Vegetacion': None,
            'Elementos_Exteriores': None
        }
        
        for name in collections.keys():
            col = bpy.data.collections.new(name)
            bpy.context.scene.collection.children.link(col)
            collections[name] = col
        
        self.collections = collections
    
    def create_material(self, name, color, roughness=0.5, metallic=0.0):
        """Crea un material PBR básico"""
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        
        # Limpiar nodos por defecto
        for node in nodes:
            nodes.remove(node)
        
        # Crear nodos
        output = nodes.new('ShaderNodeOutputMaterial')
        bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        
        bsdf.inputs['Base Color'].default_value = (*color, 1)
        bsdf.inputs['Roughness'].default_value = roughness
        bsdf.inputs['Metallic'].default_value = metallic
        
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        self.materials[name] = mat
        return mat
    
    def setup_materials(self):
        """Configura todos los materiales del proyecto"""
        mats_config = self.params.get('materials', {})
        
        # Materiales base según selección del usuario
        wall_colors = {
            'blanco_puro': (0.95, 0.95, 0.95),
            'hormigon_visto': (0.6, 0.6, 0.6),
            'madera_clara': (0.65, 0.5, 0.35),
            'piedra_natural': (0.55, 0.55, 0.5),
            'ladrillo_vista': (0.7, 0.35, 0.2),
            'adobe': (0.7, 0.55, 0.35)
        }
        
        accent_colors = {
            'madera_oscura': (0.35, 0.22, 0.12),
            'negro_mate': (0.1, 0.1, 0.1),
            'acero_corten': (0.65, 0.32, 0.18),
            'cobre': (0.72, 0.45, 0.2),
            'cemento_pulido': (0.5, 0.5, 0.5),
            'vegetacion': (0.2, 0.5, 0.15)
        }
        
        floor_colors = {
            'porcelanato': (0.85, 0.85, 0.85),
            'madera': (0.6, 0.45, 0.3),
            'concreto_pulido': (0.55, 0.55, 0.55),
            'ceramica': (0.8, 0.75, 0.7),
            'deck_madera': (0.55, 0.4, 0.28),
            'piedra_natural': (0.5, 0.5, 0.45),
            'cesped': (0.3, 0.55, 0.2)
        }
        
        wall_finish = mats_config.get('walls', {}).get('finish', 'blanco_puro')
        accent_mat = mats_config.get('accent', {}).get('material', 'madera_oscura')
        floor_int = mats_config.get('floors', {}).get('interior', 'porcelanato')
        floor_ext = mats_config.get('floors', {}).get('exterior', 'deck_madera')
        
        # Crear materiales
        self.create_material('Muro_Principal', wall_colors.get(wall_finish, (0.9, 0.9, 0.9)), 0.85)
        self.create_material('Muro_Interno', (0.95, 0.95, 0.95), 0.9)
        self.create_material('Acento', accent_colors.get(accent_mat, (0.4, 0.25, 0.15)), 0.7)
        self.create_material('Piso_Interior', floor_colors.get(floor_int, (0.8, 0.8, 0.8)), 0.3, 0.1)
        self.create_material('Piso_Exterior', floor_colors.get(floor_ext, (0.5, 0.4, 0.3)), 0.8)
        self.create_material('Vidrio', (0.6, 0.8, 0.95), 0.05, 0.8)
        self.create_material('Vidrio_Frame', (0.1, 0.1, 0.1), 0.5, 0.7)
        self.create_material('Losa', (0.6, 0.6, 0.6), 0.9)
        self.create_material('Cubierta', (0.25, 0.25, 0.25), 0.7)
        self.create_material('Tierra', (0.4, 0.3, 0.2), 0.95)
        self.create_material('Hierba', (0.25, 0.5, 0.18), 0.9)
        self.create_material('Tronco', (0.35, 0.22, 0.12), 0.9)
        self.create_material('Hojas', (0.2, 0.45, 0.15), 0.85)
        self.create_material('Concreto', (0.5, 0.5, 0.5), 0.85)
        self.create_material('Grava', (0.55, 0.5, 0.45), 0.95)
    
    def create_box(self, name, location, dimensions, material_name='Muro_Principal'):
        """Crea un cubo con dimensiones específicas"""
        bpy.ops.mesh.primitive_cube_add(size=1, location=location)
        obj = bpy.context.active_object
        obj.name = name
        obj.scale = (dimensions[0], dimensions[1], dimensions[2])
        bpy.ops.object.transform_apply(scale=True)
        
        if material_name in self.materials:
            obj.data.materials.append(self.materials[material_name])
        
        return obj
    
    def create_terrain(self):
        """Crea el terreno"""
        site = self.params.get('site', {})
        lot = site.get('lot', {})
        
        lot_length = lot.get('length', 25) * SCALE
        lot_width = lot.get('width', 15) * SCALE
        
        # Crear plano del terreno
        bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
        terrain = bpy.context.active_object
        terrain.name = 'Terreno'
        terrain.scale = (lot_length / 2, lot_width / 2, 1)
        bpy.ops.object.transform_apply(scale=True)
        
        if 'Hierba' in self.materials:
            terrain.data.materials.append(self.materials['Hierba'])
        
        # Agregar a colección
        self.move_to_collection(terrain, 'Terreno')
        
        # Crear camino de entrada
        program = self.params.get('program', {})
        setbacks = self.params.get('regulations', {}).get('setbacks', {})
        setback_front = setbacks.get('front', 4) * SCALE
        
        self.create_box(
            'Camino_Entrada',
            (0, lot_length/4 + setback_front/2, 0.01),
            (1.2, setback_front, 0.02),
            'Concreto'
        )
        
        return terrain
    
    def create_building(self):
        """Crea el edificio completo"""
        program = self.params.get('program', {})
        design = self.params.get('design', {})
        
        general = program.get('general', {})
        total_area = general.get('totalArea', 120)
        levels = general.get('levels', 2)
        floor_height = general.get('floorHeight', 2.8)
        ceiling_height = general.get('ceilingHeight', 2.6)
        
        # Calcular dimensiones del edificio
        building_width = min(11, math.sqrt(total_area / levels) * 1.1)
        building_length = (total_area / levels) / building_width
        
        # Obtener configuración de techos
        roof_config = design.get('roof', {})
        roof_type = roof_config.get('type', 'plana')
        roof_overhang = roof_config.get('overhang', 0.6)
        
        # Crear estructura por nivel
        for level in range(levels):
            y_pos = level * floor_height
            self.create_floor_level(level, y_pos, building_width, building_length, floor_height)
        
        # Crear cubierta
        self.create_roof(building_width, building_length, roof_type, roof_overhang, levels * floor_height)
        
        # Crear base
        self.create_base(building_width, building_length)
        
        return building_width, building_length
    
    def create_floor_level(self, level, y_pos, width, length, height):
        """Crea un nivel completo"""
        level_name = f'Nivel_{level + 1}'
        
        # Muros exteriores
        self.create_walls(level_name, y_pos, width, length, height)
        
        # Losa del nivel
        self.create_slab(level_name, y_pos, width, length)
        
        # Ventanas
        self.create_windows(level_name, y_pos, width, length, height)
        
        # Puerta principal (solo nivel 0)
        if level == 0:
            self.create_main_door(y_pos, length)
        
        # Acentos
        self.create_accents(level_name, y_pos, width, length, height)
    
    def create_walls(self, level_name, y_pos, width, length, height):
        """Crea los muros del nivel"""
        wall_thickness = 0.15
        
        # Muro frontal
        self.create_box(
            f'{level_name}_Muro_Frontal',
            (0, length/2, y_pos + height/2),
            (width, wall_thickness, height),
            'Muro_Principal'
        )
        
        # Muro posterior
        self.create_box(
            f'{level_name}_Muro_Posterior',
            (0, -length/2, y_pos + height/2),
            (width, wall_thickness, height),
            'Muro_Principal'
        )
        
        # Muro izquierdo
        self.create_box(
            f'{level_name}_Muro_Izquierdo',
            (-width/2, 0, y_pos + height/2),
            (wall_thickness, length, height),
            'Muro_Principal'
        )
        
        # Muro derecho
        self.create_box(
            f'{level_name}_Muro_Derecho',
            (width/2, 0, y_pos + height/2),
            (wall_thickness, length, height),
            'Muro_Principal'
        )
    
    def create_slab(self, level_name, y_pos, width, length):
        """Crea la losa del nivel"""
        self.create_box(
            f'{level_name}_Losa',
            (0, 0, y_pos - 0.1),
            (width + 0.3, length + 0.3, 0.2),
            'Losa'
        )
    
    def create_windows(self, level_name, y_pos, width, length, height):
        """Crea las ventanas"""
        design = self.params.get('design', {})
        windows_config = design.get('windows', {})
        
        win_width = windows_config.get('width', 1.2)
        win_height = windows_config.get('height', 1.8)
        
        glass_thickness = 0.02
        frame_thickness = 0.05
        
        # Ventanas frontales (2)
        for i in [-1, 1]:
            x_pos = i * (width * 0.3)
            
            # Vidrio
            self.create_box(
                f'{level_name}_Ventana_Frontal_{i}',
                (x_pos, length/2 + 0.01, y_pos + height * 0.55),
                (win_width, glass_thickness, win_height),
                'Vidrio'
            )
            
            # Marco
            self.create_box(
                f'{level_name}_Marco_Frontal_{i}',
                (x_pos, length/2 + 0.02, y_pos + height * 0.55),
                (win_width + frame_thickness*2, frame_thickness, win_height + frame_thickness*2),
                'Vidrio_Frame'
            )
        
        # Ventanas posteriores (2)
        for i in [-1, 1]:
            x_pos = i * (width * 0.3)
            
            self.create_box(
                f'{level_name}_Ventana_Posterior_{i}',
                (x_pos, -length/2 - 0.01, y_pos + height * 0.55),
                (win_width, glass_thickness, win_height),
                'Vidrio'
            )
            
            self.create_box(
                f'{level_name}_Marco_Posterior_{i}',
                (x_pos, -length/2 - 0.02, y_pos + height * 0.55),
                (win_width + frame_thickness*2, frame_thickness, win_height + frame_thickness*2),
                'Vidrio_Frame'
            )
        
        # Ventanas laterales (1 por lado)
        for side in [-1, 1]:
            self.create_box(
                f'{level_name}_Ventana_Lateral_{side}',
                (side * width/2 - 0.01, 0, y_pos + height * 0.55),
                (glass_thickness, win_width, win_height),
                'Vidrio'
            )
    
    def create_main_door(self, y_pos, length):
        """Crea la puerta principal"""
        design = self.params.get('design', {})
        doors_config = design.get('doors', {})
        
        door_height = doors_config.get('mainHeight', 2.4)
        door_width = 1.0
        
        # Puerta
        self.create_box(
            'Puerta_Principal',
            (0, length/2 + 0.01, y_pos + door_height/2),
            (door_width, 0.08, door_height),
            'Acento'
        )
        
        # Marco
        self.create_box(
            'Marco_Puerta',
            (0, length/2 + 0.02, y_pos + door_height/2),
            (door_width + 0.1, 0.05, door_height + 0.05),
            'Vidrio_Frame'
        )
    
    def create_accents(self, level_name, y_pos, width, length, height):
        """Crea elementos de acento"""
        # Línea horizontal superior (nivel 0)
        if y_pos == 0:
            self.create_box(
                f'{level_name}_Linea_Acento',
                (0, length/2 + 0.05, y_pos + height),
                (width + 0.1, 0.12, 0.1),
                'Acento'
            )
            
            # Columnas de acento
            for side in [-1, 1]:
                self.create_box(
                    f'{level_name}_Columna_{side}',
                    (side * width/2 + side * 0.05, length/2 + 0.08, y_pos + height/2),
                    (0.1, 0.1, height),
                    'Acento'
                )
    
    def create_roof(self, width, length, roof_type, overhang, base_height):
        """Crea la cubierta"""
        roof_height = 0.2
        
        if roof_type == 'plana':
            self.create_box(
                'Cubierta',
                (0, 0, base_height + roof_height/2),
                (width + overhang*2, length + overhang*2, roof_height),
                'Cubierta'
            )
            
            # Barandilla de cubierta
            for side_x in [-1, 1]:
                self.create_box(
                    f'Barandilla_X_{side_x}',
                    (side_x * (width/2 + overhang), 0, base_height + 0.4),
                    (0.08, length + overhang*2, 0.5),
                    'Acento'
                )
            
            for side_y in [-1, 1]:
                self.create_box(
                    f'Barandilla_Y_{side_y}',
                    (0, side_y * (length/2 + overhang), base_height + 0.4),
                    (width + overhang*2, 0.08, 0.5),
                    'Acento'
                )
        
        elif roof_type in ['inclinada_baja', 'un_agua']:
            # Cubierta inclinada simplificada
            pitch = self.params.get('design', {}).get('roof', {}).get('pitch', 5)
            height_diff = math.tan(math.radians(pitch)) * length
            
            bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, base_height + height_diff/4))
            roof = bpy.context.active_object
            roof.name = 'Cubierta'
            roof.scale = ((width + overhang*2)/2, (length + overhang*2)/2, roof_height)
            roof.rotation_euler = (math.radians(pitch), 0, 0)
            bpy.ops.object.transform_apply(scale=True, rotation=True)
            
            if 'Cubierta' in self.materials:
                roof.data.materials.append(self.materials['Cubierta'])
    
    def create_base(self, width, length):
        """Crea la plataforma base"""
        self.create_box(
            'Plataforma_Base',
            (0, 0, -0.15),
            (width + 1.5, length + 1.5, 0.3),
            'Concreto'
        )
        
        # Deck exterior
        self.create_box(
            'Deck_Exterior',
            (width * 0.25, length/2 + 1.5, 0.05),
            (width * 0.5, 2, 0.1),
            'Piso_Exterior'
        )
    
    def create_vegetation(self):
        """Crea vegetación básica"""
        landscape = self.params.get('landscape', {})
        vegetation = landscape.get('vegetation', {})
        
        num_trees = vegetation.get('trees', 4)
        num_small_trees = vegetation.get('smallTrees', 8)
        num_bushes = vegetation.get('bushes', 20)
        
        # Árboles grandes
        for i in range(num_trees):
            angle = (i / num_trees) * 2 * math.pi + math.radians(30)
            radius = 12 + (i % 3) * 3
            x = math.cos(angle) * radius
            y = math.sin(angle) * radius
            self.create_tree(f'Arbol_Grande_{i}', (x, y, 0), 4, 2.5)
        
        # Árboles pequeños
        for i in range(num_small_trees):
            angle = (i / num_small_trees) * 2 * math.pi + math.radians(60)
            radius = 8 + (i % 4) * 2
            x = math.cos(angle) * radius
            y = math.sin(angle) * radius
            self.create_tree(f'Arbol_Pequeño_{i}', (x, y, 0), 2.5, 1.5)
        
        # Arbustos
        for i in range(min(num_bushes, 30)):
            angle = (i / num_bushes) * 2 * math.pi + math.radians(45)
            radius = 5 + (i % 5) * 2
            x = math.cos(angle) * radius
            y = math.sin(angle) * radius
            self.create_bush(f'Arbusto_{i}', (x, y, 0))
    
    def create_tree(self, name, location, height, crown_radius):
        """Crea un árbol"""
        # Tronco
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.15,
            depth=height * 0.6,
            location=(location[0], location[1], height * 0.3)
        )
        trunk = bpy.context.active_object
        trunk.name = f'{name}_Tronco'
        
        if 'Tronco' in self.materials:
            trunk.data.materials.append(self.materials['Tronco'])
        
        # Copa (esfera)
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=crown_radius,
            segments=TREE_SEGMENTS,
            ring_count=TREE_SEGMENTS//2,
            location=(location[0], location[1], height * 0.7)
        )
        crown = bpy.context.active_object
        crown.name = f'{name}_Copa'
        crown.scale = (1, 1, 0.8)
        bpy.ops.object.transform_apply(scale=True)
        
        if 'Hojas' in self.materials:
            crown.data.materials.append(self.materials['Hojas'])
    
    def create_bush(self, name, location):
        """Crea un arbusto"""
        # Varios esferas pequeñas agrupadas
        for j in range(3):
            offset_x = (j - 1) * 0.3
            offset_y = (j % 2) * 0.2 - 0.1
            
            bpy.ops.mesh.primitive_uv_sphere_add(
                radius=0.4 + j * 0.05,
                segments=BUSH_SEGMENTS,
                ring_count=BUSH_SEGMENTS//2,
                location=(location[0] + offset_x, location[1] + offset_y, 0.3)
            )
            bush = bpy.context.active_object
            bush.name = f'{name}_{j}'
            bush.scale = (1, 1, 0.7)
            bpy.ops.object.transform_apply(scale=True)
            
            if 'Hojas' in self.materials:
                bush.data.materials.append(self.materials['Hojas'])
    
    def move_to_collection(self, obj, collection_name):
        """Mueve un objeto a una colección"""
        if collection_name in self.collections:
            col = self.collections[collection_name]
            
            # Remover de todas las colecciones
            for c in obj.users_collection:
                c.objects.unlink(obj)
            
            col.objects.link(obj)
    
    def setup_camera(self):
        """Configura la cámara"""
        bpy.ops.object.camera_add(
            location=(15, -15, 12),
            rotation=(math.radians(55), 0, math.radians(45))
        )
        camera = bpy.context.active_object
        camera.name = 'Camera_Main'
        bpy.context.scene.camera = camera
        
        # Agregar resticción de seguimiento
        constraint = camera.constraints.new(type='TRACK_TO')
        constraint.target = bpy.data.objects.get('Plataforma_Base') or bpy.data.objects.get('Terreno')
        constraint.track_axis = 'TRACK_NEGATIVE_Z'
        constraint.up_axis = 'UP_Y'
    
    def setup_lighting(self):
        """Configura la iluminación"""
        # Sol
        bpy.ops.object.light_add(
            type='SUN',
            location=(10, -10, 20)
        )
        sun = bpy.context.active_object
        sun.name = 'Sun'
        sun.data.energy = 3
        sun.rotation_euler = (math.radians(45), math.radians(15), math.radians(-30))
        
        # Luz ambiente
        world = bpy.context.scene.world
        if not world:
            world = bpy.data.worlds.new("World")
            bpy.context.scene.world = world
        
        world.use_nodes = True
        bg = world.node_tree.nodes['Background']
        bg.inputs['Color'].default_value = (0.6, 0.75, 0.9, 1)
        bg.inputs['Strength'].default_value = 0.5
    
    def setup_render(self):
        """Configura el render"""
        scene = bpy.context.scene
        
        scene.render.engine = 'CYCLES'
        scene.cycles.samples = 128
        scene.render.resolution_x = 1920
        scene.render.resolution_y = 1080
        scene.render.film_transparent = False
        
        # Color de fondo del world
        if scene.world and scene.world.use_nodes:
            bg = scene.world.node_tree.nodes['Background']
            bg.inputs['Color'].default_value = (0.5, 0.7, 0.9, 1)
    
    def generate(self):
        """Genera el modelo completo"""
        print("="*60)
        print("GENERANDO MODELO 3D - VIVIENDA CAMPESTRE")
        print("="*60)
        
        self.clear_scene()
        self.create_collections()
        self.setup_materials()
        
        print("Creando terreno...")
        self.create_terrain()
        
        print("Creando edificio...")
        width, length = self.create_building()
        
        print("Creando vegetación...")
        self.create_vegetation()
        
        print("Configurando cámara...")
        self.setup_camera()
        
        print("Configurando iluminación...")
        self.setup_lighting()
        
        print("Configurando render...")
        self.setup_render()
        
        # Centrar vista
        bpy.ops.object.select_all(action='DESELECT')
        
        print("="*60)
        print("MODELO GENERADO EXITOSAMENTE")
        print(f"Dimensiones edificio: {width:.1f}m x {length:.1f}m")
        print("="*60)


# ============================================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================================
def load_params(filepath):
    """Carga parámetros desde archivo JSON"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    """Función principal"""
    if not os.path.exists(PARAMS_FILE):
        print(f"Error: No se encontró el archivo de parámetros: {PARAMS_FILE}")
        print("Exporta los parámetros desde la ficha técnica como .JSON")
        return
    
    print(f"Cargando parámetros desde: {PARAMS_FILE}")
    params = load_params(PARAMS_FILE)
    
    generator = ViviendaCampestreGenerator(params)
    generator.generate()


# ============================================================================================
# EJECUTAR
# ============================================================================================
if __name__ == '__main__':
    main()
