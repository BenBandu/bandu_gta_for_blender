import bpy
from bpy_extras import io_utils
import time
import mathutils
from ....bandu_gta.files.replay import Replay


# noinspection PyPep8Naming
class RM_OT_ImportReplay(bpy.types.Operator, io_utils.ImportHelper):

	bl_idname = "replay_manager.import_replay"
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

	TIMER_STEP = 0.01

	def __init__(self):
		self.timer = None
		self.frame_current = 0
		self.frame_count = None

		self.replay_data = None
		self.replay_block = None
		self.replay_property = None
		self.replay_collection = None

		self.context = None

	def execute(self, context):
		self.context = context
		self.initialize()

		wm = context.window_manager
		self.timer = wm.event_timer_add(self.TIMER_STEP, window=context.window)
		wm.modal_handler_add(self)

		return {"RUNNING_MODAL"}

	def modal(self, context, event):
		if event.type != "TIMER":
			return {"RUNNING_MODAL"}

		manager = self.context.scene.replay_manager

		start = time.time()
		while time.time() - start < self.TIMER_STEP:
			frame = self.replay_data.get_frames()[self.frame_current]
			bl_index = self.frame_current + self.replay_property.offset

			manager.loading_status = int((self.frame_current / self.frame_count - 1) * 100 + 100)
			manager.loading_message = F"Frame {self.frame_current}/{self.frame_count}"

			self.handle_general_block(frame, bl_index)
			self.handle_clock_block(frame, bl_index)
			self.handle_weather_block(frame, bl_index)
			self.handle_vehicle_blocks(frame, bl_index)

			if self.is_last_frame():
				self.finalize()
				return {"FINISHED"}
			else:
				self.frame_current += 1

		return {"RUNNING_MODAL"}

	def initialize(self):
		manager = self.context.scene.replay_manager
		manager.is_loading = True
		manager.loading_status = 0
		manager.loading_message = F"Loading replay data"

		scene = self.context.scene
		manager = scene.replay_manager

		# Read file
		self.replay_data = Replay.create_from_file(self.filepath)
		self.replay_block = self.replay_data.blocks.ReplayBlock
		self.frame_count = len(self.replay_data.get_frames())

		self.replay_property = manager.replays.add()
		manager.index += 1

		self.handle_replay_data()
		self.handle_import_settings()

	def finalize(self):
		self.context.scene.replay_manager.is_loading = False
		self.context.area.tag_redraw()

	def handle_replay_data(self):
		self.replay_property.name = self.filepath.split("\\")[-1]
		self.replay_property.version = self.replay_data.get_version()
		# self.replay_property.buffers = b''.join(self.replay_data.get_buffers())
		self.create_collection(self.replay_property.name)

		# Max Vehicles in SA (I think), maybe adjust this based on replay version?
		for i in range(110):
			self.replay_property.vehicles.add()

		# Max Peds in SA (I think), do we even care about peds?
		for i in range(140):
			self.replay_property.peds.add()

	def handle_import_settings(self):
		scene = self.context.scene
		if self.match_framerate:
			scene.render.fps = 25 if self.replay_data.get_version() >= Replay.VERSION_SAN_ANDREAS else 30

		if self.offset_to_current_frame:
			self.replay_property.offset = scene.frame_current

		if self.goto_start and not self.offset_to_current_frame:
			scene.frame_set(self.replay_property.offset)

		if self.match_range:
			scene.frame_start = self.replay_property.offset
			scene.frame_end = self.frame_count
			# TODO: Focus on this range, make its own operator perhaps, so we can have a button that does the same?

	def handle_general_block(self, frame, frame_index):
		general_data = frame.get_block(self.replay_block.TYPE_GENERAL)
		general_property = self.replay_property.general

		# Camera
		if not general_property.camera:
			camera = self.create_camera(F"{self.replay_property.name}.camera")
			self.replay_collection.objects.link(camera)
			general_property.camera = camera

		general_property.camera.matrix_world = self.matrix_conversion(general_data.camera.transposed())
		general_property.camera.scale *= -1
		general_property.camera.keyframe_insert(data_path="location", frame=frame_index)
		general_property.camera.keyframe_insert(data_path="rotation_euler", frame=frame_index)
		general_property.camera.keyframe_insert(data_path="scale", frame=frame_index)

		# Camera Target
		if not general_property.target:
			target = self.create_empty(F"{self.replay_property.name}.target")
			self.replay_collection.objects.link(target)
			general_property.target = target

		general_property.target.location = general_data.player.as_list()
		general_property.target.keyframe_insert(data_path="location", frame=frame_index)

	def handle_clock_block(self, frame, frame_index):
		clock_data = frame.get_block(self.replay_block.TYPE_CLOCK)
		clock_property = self.replay_property.clock

		clock_property.time_of_day = clock_data.hours * 60 + clock_data.minutes
		clock_property.keyframe_insert(data_path="time_of_day", frame=frame_index)

	def handle_weather_block(self, frame, frame_index):
		weather_data = frame.get_block(self.replay_block.TYPE_WEATHER)
		weather_property = self.replay_property.weather
		if len(weather_property.types) <= 0:
			weather_property.set_weather_types(weather_data.get_weather_types())

		weather_property.old = str(weather_data.old)
		weather_property.new = str(weather_data.new)
		weather_property.blend = weather_data.blend

		weather_property.keyframe_insert(data_path="old", frame=frame_index)
		weather_property.keyframe_insert(data_path="new", frame=frame_index)
		weather_property.keyframe_insert(data_path="blend", frame=frame_index)

	def handle_vehicle_blocks(self, frame, frame_index):
		for vehicle_block in self.replay_block.get_vehicles_types():
			vehicle_blocks = frame.get_block(vehicle_block)
			if vehicle_blocks is None:
				continue

			for vehicle_data in vehicle_blocks:
				vehicle_property = self.replay_property.vehicles[vehicle_data.index]
				if vehicle_property is None:
					continue

				vehicle_property.index = vehicle_data.index
				vehicle_property.model_id = vehicle_data.model_id
				vehicle_property.primary_color = vehicle_data.colors.primary
				vehicle_property.secondary_color = vehicle_data.colors.secondary

				vehicle_property.keyframe_insert(data_path="index", frame=frame_index)
				vehicle_property.keyframe_insert(data_path="model_id", frame=frame_index)
				vehicle_property.keyframe_insert(data_path="primary_color", frame=frame_index)
				vehicle_property.keyframe_insert(data_path="secondary_color", frame=frame_index)

				if not vehicle_property.target:
					empty = self.create_empty(F"{self.replay_property.name}.vehicle.{vehicle_property.index}")
					self.replay_collection.objects.link(empty)
					vehicle_property.target = empty

				matrix = vehicle_data.matrix.decompress().transposed()
				vehicle_property.target.matrix_world = self.matrix_conversion(matrix)
				vehicle_property.target.scale *= -1
				vehicle_property.target.keyframe_insert(data_path="location",       frame=frame_index)
				vehicle_property.target.keyframe_insert(data_path="rotation_euler", frame=frame_index)
				vehicle_property.target.keyframe_insert(data_path="scale",          frame=frame_index)

				if self.frame_count > frame_index:
					vehicle_property.enabled = False
					vehicle_property.keyframe_insert(data_path="enabled", frame=frame_index + 1)

				vehicle_property.enabled = True
				vehicle_property.keyframe_insert(data_path="enabled", frame=frame_index)

		if self.is_last_frame():
			# Once we're at the last frame, go through all vehicles with a target and create a
			# driver that connects the vehicles enabled property to the targets visibility
			for bl_vehicle in self.replay_property.vehicles:
				if bl_vehicle.target:
					driver = bl_vehicle.target.driver_add("hide_viewport").driver

					variable = driver.variables.new()
					variable.type = "SINGLE_PROP"
					variable.name = "enabled"

					target = variable.targets[0]
					target.id_type = "SCENE"
					target.id = self.context.scene
					target.data_path = bl_vehicle.path_from_id("enabled")

					driver.expression = "not enabled"

	def is_last_frame(self):
		return self.frame_current == self.frame_count - 1

	def is_first_frame(self):
		return self.frame_current == 0

	def matrix_conversion(self, matrix):
		matrix = mathutils.Matrix(matrix.as_list())
		convert = io_utils.axis_conversion(from_forward="Z", from_up="-Y", to_forward="Y", to_up="Z").to_4x4()
		final = matrix @ convert
		final.translation = matrix.to_translation()
		return final

	def create_collection(self, name):
		collection = bpy.data.collections.new(name)
		bpy.context.scene.collection.children.link(collection)
		self.replay_collection = collection

	def create_camera(self, name):
		camera_data = bpy.data.cameras.new(name=name)
		camera = bpy.data.objects.new(name, camera_data)
		camera.name = name

		camera.data.lens_unit = "FOV"
		camera.data.angle = 1.22173

		return camera

	def create_empty(self, name):
		empty = bpy.data.objects.new("empty", None)
		empty.name = name

		empty.empty_display_size = 2
		empty.empty_display_type = "PLAIN_AXES"

		return empty
