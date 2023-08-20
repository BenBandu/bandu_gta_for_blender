import bpy


class Ped(bpy.types.PropertyGroup):
	groups = []
	models = []

	target_filter = lambda self, obj: obj.type != "CAMERA"

	enabled: bpy.props.BoolProperty(name="Enabled", description="Is this ped in the current frame?")
	index: bpy.props.IntProperty(name="Index", description="Ped pool array index")

	target: bpy.props.PointerProperty(
		type=bpy.types.Object,
		description="The point that the camera orbits around when playing back the replay in game (Usually the player)",
		poll=target_filter
	)

	model_id: bpy.props.IntProperty(name="Model Id", description="Id of the model used for this ped")
	model_name: bpy.props.EnumProperty(items=models, name="Model", description="The model used for this ped")

	group_id: bpy.props.IntProperty(name="Group Id", description="Id of the group used for this ped")
	group_name: bpy.props.EnumProperty(items=groups, name="Group", description="The group type used for this ped")

	@property
	def model(self):
		if self.models:
			return self.model_name

		return str(self.model_id)

	@property
	def group(self):
		if self.groups:
			return self.group_name

		return str(self.group_id)
