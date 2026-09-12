"""Render the photoreal water-bubble source frames used by the portfolio."""

from __future__ import annotations

import math
import os
import sys
import urllib.request

import bpy
from mathutils import Vector


def cli_value(name: str, default: str) -> str:
	if "--" not in sys.argv:
		return default
	args = sys.argv[sys.argv.index("--") + 1 :]
	try:
		return args[args.index(name) + 1]
	except (ValueError, IndexError):
		return default


OUTPUT = os.path.abspath(cli_value("--output", "./static/media/water-bubble/frame_"))
START = int(cli_value("--start", "1"))
END = int(cli_value("--end", "120"))
SAMPLES = int(cli_value("--samples", "48"))
RESOLUTION = int(cli_value("--resolution", "640"))
RENDER_FRAME = int(cli_value("--render-frame", "0"))
HDRI = os.path.abspath(cli_value("--hdri", "/tmp/studio_small_09_1k.hdr"))
ENGINE = cli_value("--engine", "CYCLES").upper()
RENDER_START = int(cli_value("--render-start", str(START)))
RENDER_END = int(cli_value("--render-end", str(END)))


def look_at(obj: bpy.types.Object, target=(0.0, 0.0, 0.0)) -> None:
	direction = Vector(target) - obj.location
	obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def add_area(name: str, location, color, energy: float, shape: str, size: float, size_y: float):
	bpy.ops.object.light_add(type="AREA", location=location)
	light = bpy.context.object
	light.name = name
	light.data.color = color
	light.data.energy = energy
	light.data.shape = shape
	light.data.size = size
	light.data.size_y = size_y
	look_at(light)
	return light


def add_reflection_card(name: str, location, scale, color, strength: float, rotation=(0, 0, 0)):
	bpy.ops.mesh.primitive_plane_add(size=2, location=location, rotation=rotation)
	card = bpy.context.object
	card.name = name
	card.scale = scale
	look_at(card)
	material = bpy.data.materials.new(f"{name} Material")
	material.use_nodes = True
	nodes = material.node_tree.nodes
	nodes.clear()
	emission = nodes.new("ShaderNodeEmission")
	emission.inputs["Color"].default_value = (*color, 1)
	emission.inputs["Strength"].default_value = strength
	output = nodes.new("ShaderNodeOutputMaterial")
	material.node_tree.links.new(emission.outputs["Emission"], output.inputs["Surface"])
	card.data.materials.append(material)
	card.visible_camera = False
	card.visible_shadow = False
	return card


# Clean factory scene.
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
	for block in list(datablocks):
		if block.users == 0:
			datablocks.remove(block)

scene = bpy.context.scene
if not os.path.exists(HDRI):
	os.makedirs(os.path.dirname(HDRI), exist_ok=True)
	# Studio Small 09 by Sergej Majboroda, distributed by Poly Haven under CC0.
	urllib.request.urlretrieve(
		"https://dl.polyhaven.org/file/ph-assets/HDRIs/hdr/1k/studio_small_09_1k.hdr",
		HDRI,
	)
scene.render.engine = ENGINE
scene.render.use_persistent_data = True
if ENGINE == "CYCLES":
	scene.cycles.samples = SAMPLES
	scene.cycles.use_denoising = True
	scene.cycles.max_bounces = 8
	scene.cycles.transmission_bounces = 8
	try:
		cycles_preferences = bpy.context.preferences.addons["cycles"].preferences
		cycles_preferences.compute_device_type = "METAL"
		cycles_preferences.get_devices()
		for device in cycles_preferences.devices:
			device.use = True
		scene.cycles.device = "GPU"
	except Exception:
		scene.cycles.device = "CPU"
scene.render.resolution_x = RESOLUTION
scene.render.resolution_y = RESOLUTION
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGBA"
scene.render.image_settings.color_depth = "8"
scene.render.film_transparent = True
scene.render.filepath = OUTPUT
scene.render.fps = 24
scene.frame_start = RENDER_START
scene.frame_end = RENDER_END

# AgX preserves the bright studio reflections without clipping them into white discs.
scene.view_settings.look = "AgX - Medium High Contrast"

# A dark world remains visible to glossy and transmission rays while the film stays transparent.
world = bpy.data.worlds.new("Water studio")
world.use_nodes = True
world_nodes = world.node_tree.nodes
world_links = world.node_tree.links
world_nodes.clear()
environment = world_nodes.new("ShaderNodeTexEnvironment")
environment.image = bpy.data.images.load(HDRI)
background = world_nodes.new("ShaderNodeBackground")
background.inputs["Strength"].default_value = 0.72
world_output = world_nodes.new("ShaderNodeOutputWorld")
world_links.new(environment.outputs["Color"], background.inputs["Color"])
world_links.new(background.outputs["Background"], world_output.inputs["Surface"])
scene.world = world

# Orthographic framing keeps the floating form graphic and stable while it deforms.
bpy.ops.object.camera_add(location=(0, 0, 5.7))
camera = bpy.context.object
camera.data.type = "ORTHO"
camera.data.ortho_scale = 3.25
camera.data.lens = 68
look_at(camera)
scene.camera = camera

# Dense icosphere gives the low-frequency surface motion enough resolution.
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=5, radius=1, location=(0, 0, 0))
water = bpy.context.object
water.name = "Floating water"
water.scale = (1.12, 0.98, 1.04)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
for polygon in water.data.polygons:
	polygon.use_smooth = True

# Shape keys form a seamless, restrained liquid loop. Deformations are spatially broad to
# preserve surface tension instead of looking like noisy rubber.
basis = water.shape_key_add(name="Basis")
base_positions = [vertex.co.copy() for vertex in water.data.vertices]
keys = []
for index in range(4):
	key = water.shape_key_add(name=f"Liquid wave {index + 1}")
	key.slider_min = -1
	key.slider_max = 1
	keys.append(key)

for vertex_index, base in enumerate(base_positions):
	normal = base.normalized()
	x, y, z = normal.x, normal.y, normal.z
	azimuth = math.atan2(y, x)
	polar = math.acos(max(-1.0, min(1.0, z)))
	deformations = (
		0.115 * math.sin(2 * azimuth + 0.4) * math.sin(polar) ** 2 + 0.028 * y,
		0.082 * math.cos(3 * azimuth - 0.7) * math.sin(polar) ** 3 - 0.026 * x * z,
		0.068 * math.sin(2.2 * polar + azimuth) + 0.026 * (z * z - 0.34),
		0.046 * math.cos(4 * azimuth + polar) * (1 - z * z) + 0.022 * x * y,
	)
	for key, displacement in zip(keys, deformations):
		key.data[vertex_index].co = base + normal * displacement

for index, key in enumerate(keys):
	driver = key.driver_add("value").driver
	driver.type = "SCRIPTED"
	frequency = 1 if index < 3 else 2
	phase = index * 1.37
	driver.expression = (
		f"{0.72 if index < 2 else 0.52}*sin({frequency}*2*pi*(frame-{START})/{END - START}+{phase})"
	)

# Physical glass is blended through its real Fresnel response. The face-on surface remains
# transparent while the grazing angles and studio highlights stay visible over the live page.
water_material = bpy.data.materials.new("Optical water")
water_material.use_nodes = True
nodes = water_material.node_tree.nodes
links = water_material.node_tree.links
nodes.clear()
glass = nodes.new("ShaderNodeBsdfGlass")
glass.distribution = "BECKMANN"
glass.inputs["Color"].default_value = (0.82, 0.94, 1.0, 1)
glass.inputs["Roughness"].default_value = 0.026
glass.inputs["IOR"].default_value = 1.333
transparent_body = nodes.new("ShaderNodeBsdfTransparent")
transparent_body.inputs["Color"].default_value = (0.76, 0.9, 1.0, 1)
fresnel = nodes.new("ShaderNodeFresnel")
fresnel.inputs["IOR"].default_value = 1.333
fresnel_gain = nodes.new("ShaderNodeMath")
fresnel_gain.operation = "MULTIPLY_ADD"
fresnel_gain.inputs[1].default_value = 1.45
fresnel_gain.inputs[2].default_value = 0.055
fresnel_gain.use_clamp = True
water_mix = nodes.new("ShaderNodeMixShader")
output = nodes.new("ShaderNodeOutputMaterial")
links.new(fresnel.outputs["Fac"], fresnel_gain.inputs[0])
links.new(fresnel_gain.outputs[0], water_mix.inputs["Fac"])
links.new(transparent_body.outputs["BSDF"], water_mix.inputs[1])
links.new(glass.outputs["BSDF"], water_mix.inputs[2])
links.new(water_mix.outputs["Shader"], output.inputs["Surface"])
water.data.materials.append(water_material)

# A second, almost invisible skin catches broad highlights. It avoids the CG-like uniform rim
# while preserving the transparent centre of the water body.
shell = water.copy()
shell.data = water.data.copy()
shell.animation_data_clear()
shell.name = "Water surface highlights"
shell.scale = (1.008, 1.008, 1.008)
bpy.context.collection.objects.link(shell)
shell_material = bpy.data.materials.new("Surface highlight film")
shell_material.use_nodes = True
shell_nodes = shell_material.node_tree.nodes
shell_links = shell_material.node_tree.links
shell_nodes.clear()
transparent = shell_nodes.new("ShaderNodeBsdfTransparent")
glossy = shell_nodes.new("ShaderNodeBsdfGlossy")
glossy.distribution = "GGX"
glossy.inputs["Color"].default_value = (0.78, 0.86, 1.0, 1)
glossy.inputs["Roughness"].default_value = 0.08
layer = shell_nodes.new("ShaderNodeLayerWeight")
layer.inputs["Blend"].default_value = 0.28
mix = shell_nodes.new("ShaderNodeMixShader")
shell_output = shell_nodes.new("ShaderNodeOutputMaterial")
shell_links.new(layer.outputs["Fresnel"], mix.inputs["Fac"])
shell_links.new(transparent.outputs["BSDF"], mix.inputs[1])
shell_links.new(glossy.outputs["BSDF"], mix.inputs[2])
shell_links.new(mix.outputs["Shader"], shell_output.inputs["Surface"])
shell.data.materials.clear()
shell.data.materials.append(shell_material)

# The photographed HDRI supplies varied, naturally curved reflections. A single violet strip
# integrates the neutral studio light with the Delvup palette.
add_area("Violet edge", (3.6, -1.45, -0.15), (0.38, 0.08, 1.0), 820, "RECTANGLE", 0.24, 3.8)

# A slow turn changes the internal reflection pattern without suggesting a rigid object.
water.rotation_euler = (math.radians(4), math.radians(-8), math.radians(-5))
water.keyframe_insert(data_path="rotation_euler", frame=START)
water.rotation_euler = (math.radians(-4), math.radians(12), math.radians(7))
water.keyframe_insert(data_path="rotation_euler", frame=(START + END) // 2)
water.rotation_euler = (math.radians(4), math.radians(-8), math.radians(-5))
water.keyframe_insert(data_path="rotation_euler", frame=END)
shell.parent = water
shell.matrix_parent_inverse = water.matrix_world.inverted()

# Keep a reusable production source next to the generated frames.
blend_path = os.path.join(os.path.dirname(OUTPUT.rstrip("_")), "water-bubble-source.blend")
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

scene.render.filepath = OUTPUT
scene.frame_set(RENDER_FRAME or START)
if RENDER_FRAME:
	bpy.ops.render.render(write_still=True)
else:
	bpy.ops.render.render(animation=True)
