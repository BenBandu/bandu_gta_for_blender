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

		manager = self.context.scene.replay_manager
		frames = self.replay_data.get_frames()
		self.frame_count = len(frames)

		start = time.time()
		while time.time() - start < self.TIMER_STEP:
			frame = frames[self.frame_current]
			self.context.scene.frame_set(self.frame_current + self.replay_property.offset)

			manager.loading_status = int((self.frame_current / self.frame_count - 1) * 100 + 100)
			manager.loading_message = F"Frame {self.frame_current}/{self.frame_count}"

			self.handle_general_block(frame)

			if self.is_last_frame():
				self.finalize()
				return {"FINISHED"}
			else:
				self.frame_current += 1

		return {"RUNNING_MODAL"}

	def initialize(self):
		manager = self.context.scene.replay_manager
		self.replay_property = manager.active_replay
		self.replay_data = Replay.create_from_file(self.replay_property.filepath)
		self.replay_block = self.replay_data.blocks.ReplayBlock

	def finalize(self):
		self.replay_data.save(self.filepath)

	def handle_general_block(self, frame):
		general_property = self.replay_property.general
		general_data = frame.get_block(self.replay_block.TYPE_GENERAL)
		general_data.matrix = self.matrix_conversion(general_property.camera, general_data.camera)

	def matrix_conversion(self, camera_property, camera_data):
		depsgraph = self.context.evaluated_depsgraph_get()
		camera_property = camera_property.evaluated_get(depsgraph)

		convert = io_utils.axis_conversion(from_forward="Y", from_up="Z", to_forward="Z", to_up="-Y").to_4x4()
		matrix = camera_property.matrix_world @ convert
		matrix.translation = camera_property.matrix_world.to_translation()

		loc, rot, scale = matrix.decompose()
		scale *= -1
		matrix = mathutils.Matrix.LocRotScale(loc, rot, scale)
		matrix.transpose()


		camera_data.right.x = matrix[0][0]
		camera_data.right.y = matrix[0][1]
		camera_data.right.z = matrix[0][2]
		camera_data.right.w = matrix[0][3]

		camera_data.forward.x = matrix[1][0]
		camera_data.forward.y = matrix[1][1]
		camera_data.forward.z = matrix[1][2]
		camera_data.forward.w = matrix[1][3]

		camera_data.up.x = matrix[2][0]
		camera_data.up.y = matrix[2][1]
		camera_data.up.z = matrix[2][2]
		camera_data.up.w = matrix[2][3]

		camera_data.location.x = matrix[3][0]
		camera_data.location.y = matrix[3][1]
		camera_data.location.z = matrix[3][2]
		camera_data.location.w = matrix[3][3]

		print(matrix)

		return camera_data

	def is_last_frame(self):
		return self.frame_current == self.frame_count - 1

	def is_first_frame(self):
		return self.frame_current == 0
