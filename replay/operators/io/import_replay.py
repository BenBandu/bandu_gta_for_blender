import bpy
import bpy_extras


# noinspection PyPep8Naming
class RM_OT_ImportReplay(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):

	bl_idname = "rm_ops.import_replay"
	bl_label = "GTA Replay (.rep)"

	filename_ext = ".rep"
	filter_glob: bpy.props.StringProperty(default="*.rep", options={"HIDDEN"})

	param_current_frame = bpy.props.BoolProperty(
		default=False,
		name="Current Frame",
		description="Imports the replay starting at the current frame",
		options={"ANIMATABLE"}
	)

	def execute(self, context):
		scene = context.scene
		manager = scene.replay_manager
		bl_replay = manager.replays.add()

		scene.frame_start = 0
		scene.frame_set(0)

		# TODO: Implement

		return {'FINISHED'}

	def create_collection(self):
		# TODO: Implement
		pass

	def create_camera(self, name):
		camera_data = bpy.data.cameras.new(name="camera")
		camera = bpy.data.objects.new("camera", camera_data)
		camera.name = F"{name}_camera"

		bpy.context.scene.collection.objects.link(camera)
		camera.data.lens_unit = "FOV"
		camera.data.angle = 1.22173

		return camera

	def create_empty(self, name):
		empty = bpy.data.objects.new("empty", None)
		empty.name = F"{name}_focus"

		bpy.context.scene.collection.objects.link(empty)
		empty.empty_display_size = 2
		empty.empty_display_type = "PLAIN_AXES"

		return empty
