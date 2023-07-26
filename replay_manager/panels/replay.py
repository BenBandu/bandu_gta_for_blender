import bpy
from ..operators import replay


# noinspection PyPep8Naming
class RM_PT_Replay(bpy.types.Panel):
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_category = 'Replay Manager'
	bl_idname = "RM_PT_Replay"
	bl_label = 'Replay Data'

	def draw(self, context):
		replay = context.scene.replay_manager.active_replay

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
		row.prop(replay, "offset")

		self.layout.separator()

		row = self.layout.row()
		row.operator('rm_ops.export_replay', text='Export Replay')

	@classmethod
	def poll(cls, context):
		manager = context.scene.replay_manager
		return manager.index >= 0
