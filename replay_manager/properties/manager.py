import bpy
from .replay import Replay


class Manager(bpy.types.PropertyGroup):

	replays: bpy.props.CollectionProperty(type=Replay)
	index: bpy.props.IntProperty(name="Replay Index", description="Current Replay", default=-1)

	@property
	def active_replay(self):
		return self.replays[self.index]