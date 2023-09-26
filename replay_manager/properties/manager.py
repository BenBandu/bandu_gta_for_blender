import bpy
from .replay import Replay


class Manager(bpy.types.PropertyGroup):

	is_importing: bpy.props.BoolProperty(name="Importing", description="")
	is_exporting: bpy.props.BoolProperty(name="Exporting", description="")
	loading_status: bpy.props.IntProperty(name="progress", description="", subtype="PERCENTAGE", min=0, max=100)
	loading_message: bpy.props.StringProperty(name="message", description="")

	replays: bpy.props.CollectionProperty(type=Replay)
	index: bpy.props.IntProperty(name="Replay Index", description="Current Replay", default=-1)

	@property
	def active_replay(self):
		return self.replays[self.index]
