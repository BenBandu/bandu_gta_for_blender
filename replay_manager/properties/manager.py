import bpy
from .replay import Replay


class Manager(bpy.types.PropertyGroup):

	is_loading: bpy.props.BoolProperty(name="Is importing", description="")
	loading_status: bpy.props.FloatProperty(name="progress", description="", subtype="PERCENTAGE")
	loading_message: bpy.props.StringProperty(name="message", description="")

	replays: bpy.props.CollectionProperty(type=Replay)
	index: bpy.props.IntProperty(name="Replay Index", description="Current Replay", default=-1)

	@property
	def active_replay(self):
		return self.replays[self.index]
