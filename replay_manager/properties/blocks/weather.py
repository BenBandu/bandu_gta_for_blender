import bpy


class WeatherType(bpy.types.PropertyGroup):
	name: bpy.props.StringProperty(name="Name")
	value: bpy.props.StringProperty(name="Value")


class Weather(bpy.types.PropertyGroup):

	def get_weather_types(self, context):
		types = []
		for t in self.types:
			types.append((t.value, t.name, t.name))

		return tuple(types)

	def set_weather_types(self, types):
		for value, name in types.items():
			t = self.types.add()
			t.name = name
			t.value = str(value)

	types: bpy.props.CollectionProperty(type=WeatherType, name="Types", description="All weather types")

	old: bpy.props.EnumProperty(
		items=get_weather_types,
		name="Previous Weather",
		description="Weather we are interpolating from",
	)

	new: bpy.props.EnumProperty(
		items=get_weather_types,
		name="Next Weather",
		description="Weather we are interpolating to",

	)

	blend: bpy.props.FloatProperty(
		name="Blend",
		description="Weather interpolation (0 = 100% Previous Weather, 1 = 100% Next Weather)",
		max=1.0,
		min=0.0,
	)
