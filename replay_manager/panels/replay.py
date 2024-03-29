import bpy
from ..operators import replay


# noinspection PyPep8Naming
class RM_PT_Replay(bpy.types.Panel):
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_category = 'Replay Manager'
	bl_idname = "RM_PT_Replay"
	bl_label = 'Replay'

	def draw(self, context):
		manager = context.scene.replay_manager
		replay = manager.active_replay

		row = self.layout.row()
		row.scale_y = 0.5
		row.alignment = "CENTER"
		row.label(text=replay.name)

		row = self.layout.row()
		row.scale_y = 0.5
		row.alignment = "CENTER"
		row.label(text=replay.game)

		self.layout.separator()

		row = self.layout.row()
		row.operator('replay_manager.merge_replay', text="Merge Replay")

		row = self.layout.row()
		row.prop(replay, "offset")

		self.layout.separator()

		row = self.layout.row()
		row.scale_y = 2.0
		if manager.is_exporting:
			row.prop(manager, "loading_status", text=F"{manager.loading_message}", slider=True)
		else:
			row.operator('replay_manager.export_replay', text='Export Replay')

	@classmethod
	def poll(cls, context):
		manager = context.scene.replay_manager
		return manager.index >= 0
