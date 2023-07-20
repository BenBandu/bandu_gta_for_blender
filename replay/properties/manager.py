import bpy
from .replay import Replay


class Manager(bpy.types.PropertyGroup):

	replays: bpy.props.CollectionProperty(type=Replay)
	index: bpy.props.IntProperty(name="Current replay index", default=-1)
