import bpy


class Clock(bpy.types.PropertyGroup):

	clock:   bpy.props.IntProperty(name="Clock",   description="In game clock",          default=0, min=0)
	hours:   bpy.props.IntProperty(name="Hours",   description="In game hour counter",   default=0, min=0)
	minutes: bpy.props.IntProperty(name="Minutes", description="In game minute counter", default=0, min=0)

