import bpy


# noinspection PyPep8Naming
class RM_OT_AddFrame(bpy.types.Operator):
	bl_idname = 'replay_manager.add_frame'
	bl_label = "Add frame"

	def execute(self, context):
		scene = context.scene
		replay = scene.replay_manager.active_replay
		frame = replay.frames.add()

		# Maybe add some settings for creating a new frame?

		return {'FINISHED'}
