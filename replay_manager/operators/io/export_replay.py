import bpy
import mathutils
import time
from bpy_extras import io_utils
from ....bandu_gta.files.replay import Replay


# noinspection PyPep8Naming
class RM_OT_ExportReplay(bpy.types.Operator, io_utils.ExportHelper):

	bl_idname = "replay_manager.export_replay"
	bl_label = "GTA Replay (.rep)"

	filename_ext = ".rep"
	filter_glob: bpy.props.StringProperty(default="*.rep", options={"HIDDEN"})

	TIMER_STEP = 0.01

	def __init__(self):
		self.timer = None
		self.frame_current = 0
		self.frame_count = None

		self.replay_data = None
		self.replay_block = None
		self.replay_property = None

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

		tmp_frame = self.context.scene.frame_current

		manager = self.context.scene.replay_manager
		frames = self.replay_data.get_frames()
		self.frame_count = len(frames)

		start = time.time()
		while time.time() - start < self.TIMER_STEP:
			frame = frames[self.frame_current]
			self.context.scene.frame_set(self.frame_current + self.replay_property.offset)

			manager.loading_status = (self.frame_current // self.frame_count - 1) * 100 + 100
			manager.loading_message = F"Frame {self.frame_current}/{self.frame_count}"

			self.handle_general_block(self.replay_property.general, frame.get_block(self.replay_block.TYPE_GENERAL))
			self.handle_clock_block(self.replay_property.clock, frame.get_block(self.replay_block.TYPE_CLOCK))
			self.handle_weather_blocK(self.replay_property.weather, frame.get_block(self.replay_block.TYPE_WEATHER))

			if self.is_last_frame():
				self.finalize()
				return {"FINISHED"}
			else:
				self.frame_current += 1

		self.context.scene.frame_set(tmp_frame)

		return {"RUNNING_MODAL"}

	def initialize(self):
		manager = self.context.scene.replay_manager

		manager.is_exporting = True
		manager.loading_status = 0
		manager.loading_message = F"Saving replay data"

		self.replay_property = manager.active_replay
		self.replay_data = Replay.create_from_file(self.replay_property.filepath)
		self.replay_block = self.replay_data.blocks.ReplayBlock

	def finalize(self):
		self.context.scene.replay_manager.is_exporting = False
		self.replay_data.save(self.filepath)

	def handle_general_block(self, prop, data):
		matrix = self.matrix_conversion(prop.camera)
		for i in range(4):
			for j in range(4):
				data.camera[i][j] = matrix[i][j]

	def handle_clock_block(self, prop, data):
		data.hours = (prop.time_of_day // 60) % 24
		data.minutes = (prop.time_of_day % 60)

	def handle_weather_blocK(self, prop, data):
		data.new = int(prop.new)
		data.old = int(prop.old)
		data.blend = prop.blend

	def matrix_conversion(self, camera_property):
		depsgraph = self.context.evaluated_depsgraph_get()
		camera_property = camera_property.evaluated_get(depsgraph)

		convert = io_utils.axis_conversion(from_forward="Y", from_up="Z", to_forward="Z", to_up="-Y").to_4x4()
		matrix = camera_property.matrix_world @ convert
		matrix.translation = camera_property.matrix_world.to_translation()

		loc, rot, scale = matrix.decompose()
		scale *= -1
		matrix = mathutils.Matrix.LocRotScale(loc, rot, scale)
		matrix.transpose()

		return matrix

	def is_last_frame(self):
		return self.frame_current == self.frame_count - 1

	def is_first_frame(self):
		return self.frame_current == 0
