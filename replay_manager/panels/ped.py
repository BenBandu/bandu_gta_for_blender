import bpy


# noinspection PyPep8Naming
class RM_PT_Ped(bpy.types.Panel):
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "Replay Manager"
	bl_idname = "RM_PT_Ped"
	bl_parent_id = "RM_PT_Replay"
	bl_label = "Pedestrians"
	bl_options = {"DEFAULT_CLOSED"}

	def draw(self, context):
		manager = context.scene.replay_manager
		replay = manager.active_replay
		ped = replay.active_ped

		self.layout.template_list("RM_UL_PED_LIST", "ped_list", replay, "peds", replay, "ped_index", rows=2)

		if ped is None:
			return

		self.layout.separator()

		row = self.layout.row()
		row.scale_y = 0.5
		row.alignment = "CENTER"
		row.label(text="Ped Model: " + ped.model)

		row = self.layout.row()
		row.scale_y = 0.5
		row.alignment = "CENTER"
		row.label(text="Ped Group: " + ped.group)

		self.layout.separator()

		row = self.layout.row()
		row.prop(ped, "target", text="Location", icon="EMPTY_AXIS")

	@classmethod
	def poll(cls, context):
		manager = context.scene.replay_manager
		replay = manager.active_replay
		if replay is None:
			return False

		for ped in replay.peds:
			if ped.enabled:
				return True

		return False
