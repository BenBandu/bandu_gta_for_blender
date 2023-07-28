import bpy


class Vehicle(bpy.types.PropertyGroup):
	models = []
	target_filter = lambda self, obj: obj.type != "CAMERA"

	enabled: bpy.props.BoolProperty(name="Enabled", description="Is this vehicle in the current frame?", default=False)
	index: bpy.props.IntProperty(name="Index", description="Vehicles position in the vehicle array")

	target: bpy.props.PointerProperty(
		type=bpy.types.Object,
		description="The point that the camera orbits around when playing back the replay in game (Usually the player)",
		poll=target_filter
	)

	primary_color: bpy.props.IntProperty(name="Primary Color", description="Primary color index defined in carcols")
	secondary_color: bpy.props.IntProperty(name="Secondary Color", description="Secondary color index  defined in carcols")

	model_id: bpy.props.IntProperty(name="Model Id", description="Id of the model used for this vehicle")
	model_name: bpy.props.EnumProperty(items=models, name="Model", description="The model used for this vehicle")

	@property
	def model(self):
		if self.models:
			return self.model_name

		return str(self.model_id)
