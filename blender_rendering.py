import os
import argparse
import bpy

dir = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser(description="Rendering App")
parser.add_argument("--input", type=str, default=os.path.join(dir, "test.glb"), help="Path for input model to render")
parser.add_argument("--output", type=str, default=os.path.join(dir, "output.png"), help="Path for rendered image file output")
args = parser.parse_args()

# Loading add-ons
pixel_addon_file_path = os.path.join(dir, 'PixelArtAddon_v_1_1.py')

# bpy.ops.preferences.addon_install(filepath=pixel_addon_file_path)
bpy.ops.preferences.addon_enable(module='PixelArtAddon_v_1_1')

# Loding model
glb_file = args.input

if "Cube" in bpy.data.objects:
    bpy.data.objects['Cube'].select_set(True)
    bpy.ops.object.delete()

before_import = set(obj.name for obj in bpy.context.scene.objects)
bpy.ops.import_scene.gltf(filepath=glb_file)
after_import = set(obj.name for obj in bpy.context.scene.objects)
imported_objects = [bpy.context.scene.objects[name] for name in after_import - before_import]

# Add-on setup
bpy.ops.render.render_settings()

# Set up the rendering
bpy.context.scene.render.engine = 'CYCLES'  # or 'BLENDER_EEVEE'
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.filepath = args.output

# Add lighting if needed
bpy.ops.object.light_add(type='SUN', radius=1, align='WORLD', location=(0, 0, 10))

# Render the scene
bpy.ops.render.render(write_still=True)