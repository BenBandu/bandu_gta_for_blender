import bpy
from .frame import Frame


class Replay(bpy.types.PropertyGroup):

	name: bpy.props.StringProperty(name="Name", description="Name of the replay", default="replay")
	frames: bpy.props.CollectionProperty(type=Frame, name="Frame")
	offset: bpy.props.IntProperty(name="Offset", description="Offset the entire replay in the timeline")

	buffers: bpy.props.IntVectorProperty(
		name="buffers",
		description="Contains all the replay data"
	)

	@property
	def active_frame(self):
		if len(self.frames) == 0:
			return None

		current_frame = bpy.context.scene.frame_current
		index = current_frame - self.offset
		if index < 0 or index > len(self.frames):
			return None

		return self.frames[index]
