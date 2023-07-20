import bpy
from . import blocks


class Frame(bpy.types.PropertyGroup):

	general: bpy.props.PointerProperty(type=blocks.General, name="Camera")
	clock:   bpy.props.PointerProperty(type=blocks.Clock,   name="Clock")
	weather: bpy.props.PointerProperty(type=blocks.Weather, name="Weather")

