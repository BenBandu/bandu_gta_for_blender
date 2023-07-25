import bpy


class Ped(bpy.types.PropertyGroup):
	groups = []
	models = []

	enabled: bpy.props.BoolProperty(name="Enabled", description="Is this ped in the current frame?")

	model_id: bpy.props.IntProperty(name="Model Id", description="Id of the model used for this ped")
	model_name: bpy.props.EnumProperty(items=models, name="Model", description="The model used for this ped")

	group_id: bpy.props.IntProperty(name="Group Id", description="Id of the group used for this ped")
	group_name: bpy.props.EnumProperty(items=groups, name="Group", description="The group type used for this ped")

	@property
	def model(self):
		if self.models:
			return self.model_name

		return self.model_id

	@property
	def group(self):
		if self.groups:
			return self.group_name

		return self.group_id
