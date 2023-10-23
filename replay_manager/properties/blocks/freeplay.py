import bpy


class Freeplay(bpy.types.PropertyGroup):
	def on_update_enabled(self, context):
		manager = context.scene.replay_manager
		replay = manager.active_replay
		if not replay.freeplay.enabled:
			replay.general.camera.data.angle = 1.0472  # 60 FOV
		else:
			replay.general.camera.data.angle = replay.freeplay.fov

	enabled: bpy.props.BoolProperty(
		name="Enable freeplay features",
		description="Enable a custom block of data that is not supported by the game, but by freeplay. Enabling this feature will make exported replays crash the game without freeplay enabled",
		default=False,
		update=on_update_enabled,
	)

	fov: bpy.props.FloatProperty(
		name="Field of View",
		description="Field of view",
		default=1.0472,
		min=0.00640536,  # Based on Camera FOV Max/Mix in Blender
		max=3.01675,
		precision=3,
		step=10.0,
		unit="ROTATION",
		subtype="ANGLE",
	)
