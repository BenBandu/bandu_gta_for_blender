import bpy
import bpy_extras
import math
import mathutils
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
		frames = bg_replay.get_frames()
		frame_count = len(frames)

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
			scene.frame_end = frame_count

		collection = self.create_collection(bl_replay.name)
		bl_replay.general.camera = collection.objects[0]
		bl_replay.general.target = collection.objects[1]

		bpy.context.view_layer.objects.active = bl_replay.general.target
		bpy.ops.view3d.localview(frame_selected=True)

		# Max Vehicles in SA (I think)
		for i in range(110):
			bl_replay.vehicles.add()

		# Max Peds in SA (I think)
		for i in range(140):
			bl_replay.peds.add()

		frameblock = bg_replay.blocks.ReplayBlock
		for frame_index, frame in enumerate(frames):
			bl_frame_index = bl_replay.offset + frame_index

			# General
			general = frame.get_block(frameblock.TYPE_GENERAL)
			bl_replay.general.camera.matrix_world = self.matrix_bg_to_bl(general.camera)
			bl_replay.general.camera.scale *= -1
			bl_replay.general.camera.keyframe_insert(data_path="location",       frame=frame_index)
			bl_replay.general.camera.keyframe_insert(data_path="rotation_euler", frame=frame_index)
			bl_replay.general.camera.keyframe_insert(data_path="scale",          frame=frame_index)

			bl_replay.general.target.location = general.player.as_list()
			bl_replay.general.target.keyframe_insert(data_path="location", frame=frame_index)

			# Clock
			clock = frame.get_block(frameblock.TYPE_CLOCK)
			bl_replay.clock.time_of_day = clock.hours * 60 + clock.minutes
			bl_replay.clock.keyframe_insert(data_path="time_of_day", frame=bl_frame_index)

			# Weather
			# TODO: Figure out the possible weather for each game

			for vehicle_block in frameblock.get_vehicles_types():
				vehicle_blocks = frame.get_block(vehicle_block)
				if vehicle_blocks is None:
					continue

				for bg_vehicle in vehicle_blocks:
					bl_vehicle = bl_replay.vehicles[bg_vehicle.index]
					if bl_vehicle is None:
						continue

					bl_vehicle.index = bg_vehicle.index
					bl_vehicle.keyframe_insert(data_path="index", frame=bl_frame_index)

					bl_vehicle.model_id = bg_vehicle.model_id
					bl_vehicle.keyframe_insert(data_path="model_id", frame=bl_frame_index)

					bl_vehicle.primary_color = bg_vehicle.colors.primary
					bl_vehicle.keyframe_insert(data_path="primary_color", frame=bl_frame_index)

					bl_vehicle.secondary_color = bg_vehicle.colors.secondary
					bl_vehicle.keyframe_insert(data_path="secondary_color", frame=bl_frame_index)

					if not bl_vehicle.target:
						empty = self.create_empty(F"{bl_replay.name}.vehicle.{bl_vehicle.index}")
						collection.objects.link(empty)
						bl_vehicle.target = empty

					matrix = bg_vehicle.matrix.decompress()
					bl_vehicle.target.matrix_world = self.matrix_bg_to_bl(matrix)
					bl_vehicle.target.scale *= -1
					bl_vehicle.target.keyframe_insert(data_path="location",       frame=frame_index)
					bl_vehicle.target.keyframe_insert(data_path="rotation_euler", frame=frame_index)
					bl_vehicle.target.keyframe_insert(data_path="scale",          frame=frame_index)

					if frame_count > bl_frame_index:
						bl_vehicle.enabled = False
						bl_vehicle.keyframe_insert(data_path="enabled", frame=bl_frame_index + 1)

					bl_vehicle.enabled = True
					bl_vehicle.keyframe_insert(data_path="enabled", frame=bl_frame_index)

		for bl_vehicle in bl_replay.vehicles:
			if bl_vehicle.target:
				driver = bl_vehicle.target.driver_add("hide_viewport").driver

				variable = driver.variables.new()
				variable.type = "SINGLE_PROP"
				variable.name = "enabled"

				target = variable.targets[0]
				target.id_type = "SCENE"
				target.id = scene
				target.data_path = bl_vehicle.path_from_id("enabled")

				driver.expression = "not enabled"

		return {'FINISHED'}

	def matrix_bg_to_bl(self, camera):
		matrix = mathutils.Matrix(camera.as_list(True))
		convert = bpy_extras.io_utils.axis_conversion(from_forward="Z", from_up="-Y", to_forward="Y", to_up="Z").to_4x4()
		final = matrix @ convert
		final.translation = matrix.to_translation()
		return final

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
		collection.objects.link(self.create_empty(F"{name}.target"))

		return collection

	def create_camera(self, name):
		camera_data = bpy.data.cameras.new(name="camera")
		camera = bpy.data.objects.new("camera", camera_data)
		camera.name = name + ".camera"

		camera.data.lens_unit = "FOV"
		camera.data.angle = 1.22173

		return camera

	def create_empty(self, name):
		empty = bpy.data.objects.new("empty", None)
		empty.name = name

		empty.empty_display_size = 2
		empty.empty_display_type = "PLAIN_AXES"

		return empty
