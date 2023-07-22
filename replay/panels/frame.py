import bpy
import textwrap


# noinspection PyPep8Naming
class RM_PT_Frame(bpy.types.Panel):
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_category = 'Replay Manager'
	bl_idname = "RM_PT_Frame"
	bl_label = 'Frame Data'

	def draw(self, context):
		manager = context.scene.replay_manager
		replay = manager.active_replay
		frame = replay.active_frame

		if frame is None:
			self.multiline_label(context, "No frame data exists on the current frame")
			self.layout.separator()
			self.layout.operator("rm_ops.add_frame", text="Add frame(s)")
			return

		row = self.layout.split(factor=0.75)
		col = row.column()
		col.prop(frame.clock, "time_of_day")

		col = row.column()
		hours = (frame.clock.time_of_day // 60) % 24
		minutes = frame.clock.time_of_day % 60
		col.label(text="{:02d}:{:02d}".format(hours, minutes))

		self.layout.separator()

		row = self.layout.row()
		row.prop(frame.weather, "old", text='')
		row.prop(frame.weather, "new", text='')

		row = self.layout.row()
		row.prop(frame.weather, "interpolation", slider=True)

	def multiline_label(self, context, text):
		wrapper = textwrap.TextWrapper(context.region.width // 7)
		lines = wrapper.wrap(text)

		for line in lines:
			row = self.layout.row(align=True)
			row.alignment = "CENTER"
			row.scale_y = 0.5
			row.label(text=line)

	@classmethod
	def poll(cls, context):
		manager = context.scene.replay_manager
		return manager.index >= 0
