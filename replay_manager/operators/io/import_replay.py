import bpy
import bpy_extras
from ....bandu_gta.files.replay import Replay


# noinspection PyPep8Naming
class RM_OT_ImportReplay(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):

	bl_idname = "rm_ops.import_replay"
	bl_label = "GTA Replay (.rep)"

	filename_ext = ".rep"
	filter_glob: bpy.props.StringProperty(default="*.rep", options={"HIDDEN"})

	goto_start: bpy.props.BoolProperty(
		name="Go to start frame",
		description="Go to the start of the replay after import",
		default=True
	)

	match_range: bpy.props.BoolProperty(
		default=True,
		name="Match playback range",
		description="Match the playback frame range to the replays frame range"
	)

	match_framerate: bpy.props.BoolProperty(
		default=False,
		name="Match scene framerate",
		description="Match the scenes framerate with the playback rate of the replay in game\nGTA III/Vice City: 30fps\nSan Andreas: 25fps"
	)

	offset_to_current_frame: bpy.props.BoolProperty(
		default=False,
		name="Offset to current frame",
		description="Sets the replay offset to the current frame",
	)

	def execute(self, context):
		scene = context.scene
		manager = scene.replay_manager

		# Read file
		bg_replay = Replay.create_from_file(self.filepath)

		# Add new replay to manager
		bl_replay = manager.replays.add()
		manager.index += 1

		# Set basic replay information
		bl_replay.name = self.filepath.split("\\")[-1]
		bl_replay.game = self.get_game_name(bg_replay.get_version())

		# Handle import settings
		if self.match_framerate:
			scene.render.fps = 25 if bg_replay.get_version() >= Replay.VERSION_SAN_ANDREAS else 30

		if self.offset_to_current_frame:
			bl_replay.offset = scene.frame_current

		if self.goto_start and not self.offset_to_current_frame:
			scene.frame_set(bl_replay.offset)

		if self.match_range:
			scene.frame_start = bl_replay.offset
			scene.frame_end = len(bg_replay.get_frames())

		self.create_collection(bl_replay.name)

		# TODO: Implement

		return {'FINISHED'}

	def get_game_name(self, version):
		if version == Replay.VERSION_III:
			return "GTA III"
		elif version == Replay.VERSION_VICE_CITY:
			return "GTA: Vice City"
		elif version == Replay.VERSION_SAN_ANDREAS:
			return "GTA: San Andreas"
		elif version == Replay.VERSION_SAN_ANDREAS_STEAM:
			return "GTA: San Andreas (Steam)"
		else:
			return "Unknown version"

	def create_collection(self, name):
		collection = bpy.data.collections.new(name)
		bpy.context.scene.collection.children.link(collection)

		collection.objects.link(self.create_camera(name))
		collection.objects.link(self.create_empty(name))

	def create_camera(self, name):
		camera_data = bpy.data.cameras.new(name="camera")
		camera = bpy.data.objects.new("camera", camera_data)
		camera.name = name + ".camera"

		camera.data.lens_unit = "FOV"
		camera.data.angle = 1.22173

		return camera

	def create_empty(self, name):
		empty = bpy.data.objects.new("empty", None)
		empty.name = name + ".player"

		empty.empty_display_size = 2
		empty.empty_display_type = "PLAIN_AXES"

		return empty
