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

		self.layout.prop(replay, "name")

		self.layout.separator()

		self.layout.prop(replay, "offset")

		row = self.layout.row()
		row.scale_y = 2.0
		self.layout.operator('rm_ops.export_replay', text='Export Replay')

	@classmethod
	def poll(cls, context):
		manager = context.scene.replay_manager
		return manager.index >= 0