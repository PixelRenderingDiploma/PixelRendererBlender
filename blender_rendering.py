import os
import argparse
import bpy

dir = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser(description="Rendering App")
parser.add_argument("--input", type=str, default=os.path.join(dir, "test.glb"), help="Path for input model to render")
parser.add_argument("--output", type=str, default=os.path.join(dir, "input/frame_####"), help="Path for rendered image directory output")
args = parser.parse_args()

# Loading add-ons
pixel_addon_file_path = os.path.join(dir, 'PixelArtAddon_v_1_1.py')

# bpy.ops.preferences.addon_install(filepath=pixel_addon_file_path)
bpy.ops.preferences.addon_enable(module='PixelArtAddon_v_1_1')

# load main blend scene
bpy.ops.wm.open_mainfile(filepath=os.path.join(dir, "Demo.blend"))

# Loding model
bpy.ops.import_scene.gltf(filepath=args.input)

# Add-on setup
bpy.ops.render.render_settings()

# Set up the rendering
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.filepath = args.output

# Add lighting if needed
bpy.ops.object.light_add(type='SUN', radius=1, align='WORLD', location=(0, 0, 10))

# Render the scene
bpy.context.scene.frame_start = 1
# bpy.context.scene.frame_end = 10
bpy.context.scene.frame_end = 360

bpy.ops.render.render(animation=True)