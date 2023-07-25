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

	offset_to_current_frame: bpy.props.BoolProperty(
		default=False,
		name="Offset to current frame",
		description="Sets the replay offset to the current frame",
	)

	def execute(self, context):
		scene = context.scene
		manager = scene.replay_manager
		bl_replay = manager.replays.add()
		bg_replay = Replay.create_from_file(self.filepath)

		bl_replay.name = self.filepath.split("\\")[-1]
		bl_replay.game = self.get_game_name_from_version(bg_replay.get_version())

		scene.render.fps = 30

		if self.offset_to_current_frame:
			bl_replay.offset = scene.frame_current

		if self.goto_start and not self.offset_to_current_frame:
			scene.frame_set(bl_replay.offset)

		if self.match_range:
			scene.frame_start = bl_replay.offset
			scene.frame_end = len(bl_replay.frames)

		self.create_collection(bl_replay.name)

		# TODO: Implement

		return {'FINISHED'}

	def get_game_name_from_version(self, version):
		games = {
			1: "Grand Theft Auto III",
			2: "Grand Theft Auto: Vice City",
			3: "Grand Theft Auto: San Andreas",
			4: "Grand Theft Auto: San Andreas - Steam Version"
		}

		return games[version]

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
