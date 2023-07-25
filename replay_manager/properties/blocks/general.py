import bpy


class General(bpy.types.PropertyGroup):
	camera_filter = lambda self, obj: obj.type == "CAMERA"
	target_filter = lambda self, obj: obj.type != "CAMERA"

	camera: bpy.props.PointerProperty(
		type=bpy.types.Object,
		description="The camera that is exported to the replay",
		poll=camera_filter
	)

	target: bpy.props.PointerProperty(
		type=bpy.types.Object,
		description="The point that the camera orbits around when playing back the replay in game (Usually the player)",
		poll=target_filter
	)
