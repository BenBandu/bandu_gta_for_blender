import bpy


# noinspection PyPep8Naming
class RM_PT_Manager(bpy.types.Panel):
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = "Replay Manager"
	bl_idname = "RM_PT_Manager"
	bl_label = "Replay Manager"

	def draw(self, context):
		manager = context.scene.replay_manager

		row = self.layout.row()
		row.scale_y = 2.0
		if manager.is_importing:
			row.prop(manager, "loading_status", text=F"{manager.loading_message}", slider=True)
		else:
			row.operator("replay_manager.import_replay", text="Import Replay")

		self.layout.separator()

		row = self.layout.row()
		row.template_list("RM_UL_REPLAY_LIST", "replay_list", manager, "replays", manager, "index")
