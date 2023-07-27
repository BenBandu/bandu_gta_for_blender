import bpy


class Vehicle(bpy.types.PropertyGroup):
	models = []

	enabled: bpy.props.BoolProperty(name="Enabled", description="Is this vehicle in the current frame?", default=False)
	index: bpy.props.IntProperty(name="Index", description="Vehicles position in the vehicle array")

	model_id: bpy.props.IntProperty(name="Model Id", description="Id of the model used for this vehicle")
	model_name: bpy.props.EnumProperty(items=models, name="Model", description="The model used for this vehicle")

	@property
	def model(self):
		if self.models:
			return self.model_name

		return str(self.model_id)
