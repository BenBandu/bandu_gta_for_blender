import bpy
from .frame import Frame


class Replay(bpy.types.PropertyGroup):

	name: bpy.props.StringProperty(name="Name", description="Name of the replay", default="replay")
	frames: bpy.props.CollectionProperty(type=Frame, name="Frame")

	buffers: bpy.props.IntVectorProperty(
		name="buffers",
		description="Contains all the replay data"
	)
