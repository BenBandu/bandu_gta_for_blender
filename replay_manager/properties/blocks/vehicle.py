import bpy


class Vehicle(bpy.types.PropertyGroup):
	models = []

	enabled: bpy.props.BoolProperty(name="Enabled", description="Is this vehicle in the current frame?")

	model_id: bpy.props.IntProperty(name="Model Id", description="Id of the model used for this vehicle")
	model_name: bpy.props.EnumProperty(items=models, name="Model", description="The model used for this vehicle")

	@property
	def model(self):
		if self.models:
			return self.model_name

		return self.model_id
