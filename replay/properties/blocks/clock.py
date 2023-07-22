import bpy


class Clock(bpy.types.PropertyGroup):

	time_of_day: bpy.props.IntProperty(name="Time of Day", description="Time of day",            default=0, min=0)
	hours:       bpy.props.IntProperty(name="Hours",       description="In game hour counter",   default=0, min=0)
	minutes:     bpy.props.IntProperty(name="Minutes",     description="In game minute counter", default=0, min=0)

