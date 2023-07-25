import bpy


# noinspection PyPep8Naming
class RM_PT_Ped(bpy.types.Panel):
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "Replay Manager"
	bl_idname = "RM_PT_Ped"
	bl_parent_id = "RM_PT_Frame"
	bl_label = "Ped Data"

	def draw(self, context):
		manager = context.scene.replay_manager
		replay = manager.active_replay
		frame = replay.active_frame
		ped = frame.active_ped

	@classmethod
	def poll(cls, context):
		manager = context.scene.replay_manager
		replay = manager.active_replay
		if replay is None:
			return False

		frame = replay.active_frame

		if frame is None:
			return False

		ped = frame.active_ped
		if ped is None:
			return False

		return True
