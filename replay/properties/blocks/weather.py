import bpy


class Weather(bpy.types.PropertyGroup):

	# TODO: Dynamic enum? Do the different games have a different set of weathers?
	TYPES = (
		("0", "Sunny", "Sunny"),
		("1", "Cloudy", "Cloudy"),
		("2", "Rainy", "Rainy"),
		("3", "Foggy", "Foggy"),
		("4", "Extra Sunny", "Extra Sunny"),
		("5", "Hurricane", "Hurricane"),
	)

	old: bpy.props.EnumProperty(
		items=TYPES,
		name="Old weather",
		description="Weather we are interpolating from"
	)

	new: bpy.props.EnumProperty(
		items=TYPES,
		name="New weather",
		description="Weather we are interpolating to"
	)

	interpolation: bpy.props.FloatProperty(
		name="Weather Interpolation",
		description="Interpolation value between weathers",
		max=1.0,
		min=0.0
	)
