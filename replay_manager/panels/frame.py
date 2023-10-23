import bpy
import textwrap


# noinspection PyPep8Naming
class RM_PT_Frame(bpy.types.Panel):
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "Replay Manager"
	bl_idname = "RM_PT_Frame"
	bl_parent_id = "RM_PT_Replay"
	bl_label = "Frame"

	def draw(self, context):
		manager = context.scene.replay_manager
		replay = manager.active_replay

		row = self.layout.row()
		row.prop(replay.general, "camera", text="Camera", icon="CAMERA_DATA")

		row = self.layout.row()
		row.prop(replay.general, "target", text="Target", icon="EMPTY_AXIS")

		self.layout.separator()

		row = self.layout.split(factor=0.75)
		col = row.column()
		col.prop(replay.clock, "time_of_day")

		col = row.column()
		hours = (replay.clock.time_of_day // 60) % 24
		minutes = replay.clock.time_of_day % 60
		col.label(text="{:02d}:{:02d}".format(hours, minutes))

		self.layout.separator()

		row = self.layout.row()
		row.prop(replay.weather, "old", text='')
		row.prop(replay.weather, "new", text='')

		row = self.layout.row()
		row.prop(replay.weather, "blend", slider=True)

		self.layout.separator()

		row = self.layout.row()
		row.prop(replay.freeplay, "enabled", text="Enable Freeplay data")

		column = self.layout.column()
		column.enabled = replay.freeplay.enabled

		row = column.row()
		row.prop(replay.freeplay, "fov", text="Field of View")

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
