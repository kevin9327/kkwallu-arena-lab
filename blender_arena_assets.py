import bpy
import math
import os

OUT_DIR = "/Users/kevin/contest_submissions/68_extriver_creator_hackathon/models"
os.makedirs(OUT_DIR, exist_ok=True)

def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def make_mat(name, base_color, metallic=0.5, roughness=0.35, emission=None, emission_strength=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*base_color, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    if emission is not None and emission_strength > 0:
        bsdf.inputs["Emission Color"].default_value = (*emission, 1.0)
        bsdf.inputs["Emission Strength"].default_value = emission_strength
    return mat

def export_glb(filename):
    path = os.path.join(OUT_DIR, filename)
    bpy.ops.export_scene.gltf(
        filepath=path,
        export_format='GLB',
        export_apply=True,
    )
    print("Exported:", path, os.path.getsize(path))

# 1. Cyber-Brawler Hero ("brawler_striker.glb")
def build_brawler_striker():
    reset_scene()
    m_armor = make_mat("StrikerArmor", (0.12, 0.45, 0.95), metallic=0.75, roughness=0.25)
    m_dark = make_mat("StrikerDark", (0.08, 0.10, 0.15), metallic=0.85, roughness=0.30)
    m_visor = make_mat("StrikerVisor", (0.10, 0.95, 1.0), metallic=0.2, roughness=0.1, emission=(0.1, 0.92, 1.0), emission_strength=4.5)
    m_gold = make_mat("StrikerGold", (1.0, 0.72, 0.15), metallic=0.9, roughness=0.2, emission=(1.0, 0.6, 0.1), emission_strength=1.2)

    # Torso
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=16, radius=0.52, location=(0, 0, 0.95))
    torso = bpy.context.active_object
    torso.scale = (1.05, 0.82, 1.15)
    torso.data.materials.append(m_armor)

    # Head + Helmet
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=16, radius=0.46, location=(0, 0, 1.72))
    head = bpy.context.active_object
    head.scale = (1.08, 1.0, 0.95)
    head.data.materials.append(m_armor)

    # Glowing Cyber Visor (facing +Y -> exported as -Z/forward in glTF, let's place on +Y and +Z visible from top-3/4)
    bpy.ops.mesh.primitive_cube_add(size=0.55, location=(0, 0.34, 1.74))
    visor = bpy.context.active_object
    visor.scale = (1.25, 0.32, 0.38)
    bpy.ops.object.modifier_add(type='SUBSURF')
    visor.modifiers["Subdivision"].levels = 2
    visor.data.materials.append(m_visor)

    # Twin Pulse Blasters on left/right hands
    for sx in (-0.72, 0.72):
        bpy.ops.mesh.primitive_cylinder_add(vertices=18, radius=0.16, depth=0.82, location=(sx, 0.35, 1.02), rotation=(math.radians(90), 0, 0))
        gun = bpy.context.active_object
        gun.data.materials.append(m_dark)

        bpy.ops.mesh.primitive_torus_add(major_radius=0.17, minor_radius=0.045, location=(sx, 0.72, 1.02), rotation=(math.radians(90), 0, 0))
        muzzle = bpy.context.active_object
        muzzle.data.materials.append(m_visor)

        # Shoulder pauldrons
        bpy.ops.mesh.primitive_uv_sphere_add(segments=18, ring_count=12, radius=0.28, location=(sx * 0.88, 0, 1.28))
        pad = bpy.context.active_object
        pad.scale = (1.1, 0.9, 0.75)
        pad.data.materials.append(m_gold)

    # Jetpack + thruster glow
    bpy.ops.mesh.primitive_cube_add(size=0.48, location=(0, -0.44, 1.05))
    pack = bpy.context.active_object
    pack.scale = (1.1, 0.55, 1.15)
    pack.data.materials.append(m_dark)

    for sx in (-0.18, 0.18):
        bpy.ops.mesh.primitive_cone_add(vertices=16, radius1=0.13, radius2=0.06, depth=0.28, location=(sx, -0.52, 0.68))
        thr = bpy.context.active_object
        thr.data.materials.append(m_visor)

    # Hover base ring
    bpy.ops.mesh.primitive_torus_add(major_radius=0.58, minor_radius=0.05, location=(0, 0, 0.12))
    ring = bpy.context.active_object
    ring.data.materials.append(m_visor)

    export_glb("brawler_striker.glb")

# 2. Mecha Boss ("boss_mecha_titan.glb")
def build_boss_mecha_titan():
    reset_scene()
    m_crimson = make_mat("BossCrimson", (0.78, 0.08, 0.14), metallic=0.82, roughness=0.24)
    m_obsidian = make_mat("BossObsidian", (0.07, 0.07, 0.10), metallic=0.90, roughness=0.28)
    m_core = make_mat("BossCore", (1.0, 0.18, 0.32), metallic=0.2, roughness=0.1, emission=(1.0, 0.15, 0.28), emission_strength=5.5)
    m_warn = make_mat("BossGold", (1.0, 0.55, 0.08), metallic=0.85, roughness=0.22, emission=(1.0, 0.45, 0.05), emission_strength=2.0)

    # Heavy Armored Chassis
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=1.05, depth=1.35, location=(0, 0, 1.25))
    body = bpy.context.active_object
    body.data.materials.append(m_obsidian)

    # Crimson Armor Plates
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=1.18, depth=0.68, location=(0, 0, 1.42))
    chest = bpy.context.active_object
    chest.data.materials.append(m_crimson)

    # Glowing Reactor Core in Chest + Crown
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.42, location=(0, 0.88, 1.38))
    core = bpy.context.active_object
    core.data.materials.append(m_core)

    # Horned Command Head
    bpy.ops.mesh.primitive_cube_add(size=0.78, location=(0, 0.1, 2.22))
    head = bpy.context.active_object
    head.scale = (1.15, 0.95, 0.72)
    head.data.materials.append(m_obsidian)

    bpy.ops.mesh.primitive_cube_add(size=0.52, location=(0, 0.48, 2.22))
    eye = bpy.context.active_object
    eye.scale = (1.35, 0.22, 0.28)
    eye.data.materials.append(m_core)

    for sx in (-0.55, 0.55):
        bpy.ops.mesh.primitive_cone_add(vertices=12, radius1=0.14, radius2=0.02, depth=0.75, location=(sx, 0.15, 2.65), rotation=(0, math.radians(sx * -28), 0))
        horn = bpy.context.active_object
        horn.data.materials.append(m_warn)

    # Shoulder Missile Pods & Rotary Cannons
    for sx in (-1.42, 1.42):
        bpy.ops.mesh.primitive_cube_add(size=0.68, location=(sx, 0, 1.85))
        pod = bpy.context.active_object
        pod.scale = (0.85, 1.15, 0.92)
        pod.data.materials.append(m_crimson)

        bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.24, depth=1.25, location=(sx, 0.55, 1.18), rotation=(math.radians(90), 0, 0))
        cannon = bpy.context.active_object
        cannon.data.materials.append(m_obsidian)

        bpy.ops.mesh.primitive_torus_add(major_radius=0.25, minor_radius=0.055, location=(sx, 1.12, 1.18), rotation=(math.radians(90), 0, 0))
        ring = bpy.context.active_object
        ring.data.materials.append(m_core)

    # Threat shockwave ring at base
    bpy.ops.mesh.primitive_torus_add(major_radius=1.35, minor_radius=0.07, location=(0, 0, 0.14))
    b_ring = bpy.context.active_object
    b_ring.data.materials.append(m_core)

    export_glb("boss_mecha_titan.glb")

# 3. Tactical Cover Bunker ("arena_pillar.glb")
def build_arena_pillar():
    reset_scene()
    m_wall = make_mat("BunkerWall", (0.14, 0.18, 0.28), metallic=0.78, roughness=0.32)
    m_neon = make_mat("BunkerNeon", (0.18, 0.85, 1.0), metallic=0.3, roughness=0.15, emission=(0.15, 0.82, 1.0), emission_strength=3.2)

    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=1.0, depth=1.6, location=(0, 0, 0.8))
    p = bpy.context.active_object
    p.data.materials.append(m_wall)

    for z in (0.18, 1.48):
        bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=1.05, depth=0.10, location=(0, 0, z))
        r = bpy.context.active_object
        r.data.materials.append(m_neon)

    export_glb("arena_pillar.glb")

# 4. Power Cube Gem ("power_gem.glb")
def build_power_gem():
    reset_scene()
    m_gem = make_mat("PowerGem", (0.2, 1.0, 0.55), metallic=0.15, roughness=0.08, emission=(0.15, 0.95, 0.48), emission_strength=4.2)
    m_frame = make_mat("GemFrame", (0.95, 0.82, 0.25), metallic=0.92, roughness=0.18)

    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.45, location=(0, 0, 0.65))
    g = bpy.context.active_object
    g.scale = (0.9, 0.9, 1.28)
    g.data.materials.append(m_gem)

    bpy.ops.mesh.primitive_torus_add(major_radius=0.52, minor_radius=0.04, location=(0, 0, 0.65), rotation=(math.radians(35), math.radians(25), 0))
    fr = bpy.context.active_object
    fr.data.materials.append(m_frame)

    export_glb("power_gem.glb")

build_brawler_striker()
build_boss_mecha_titan()
build_arena_pillar()
build_power_gem()
print("ALL ARENA PBR GLB MODELS EXPORTED SUCCESSFULLY.")
