import bpy
import bpy_extras


# noinspection PyPep8Naming
class REPLAY_MANAGER_OT_ExportReplay(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):

	bl_idname = "replay_list.export_item"
	bl_label = "GTA Replay (.rep)"

	filename_ext = ".rep"
	filter_glob: bpy.props.StringProperty(default="*.rep", options={"HIDDEN"})

	def execute(self, context):
		manager = context.scene.replay_manager
		bl_replay = manager.current

		# TODO: Implement

		return {'FINISHED'}
