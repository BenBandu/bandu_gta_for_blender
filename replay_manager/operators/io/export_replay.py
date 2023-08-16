import bpy
import mathutils
from bpy_extras import io_utils
from ....bandu_gta.files.replay import Replay


# noinspection PyPep8Naming
class RM_OT_ExportReplay(bpy.types.Operator, io_utils.ExportHelper):

	bl_idname = "replay_manager.export_replay"
	bl_label = "GTA Replay (.rep)"

	filename_ext = ".rep"
	filter_glob: bpy.props.StringProperty(default="*.rep", options={"HIDDEN"})

	def __init__(self):
		self.timer = None
		self.frame_current = 0
		self.frame_count = None

		self.replay_data = None
		self.replay_property = None

		self.context = None

	def execute(self, context):
		self.context = context
		self.initialize()
		self.finalize()

		return {'FINISHED'}

	def initialize(self):
		manager = self.context.scene.replay_manager
		self.replay_property = manager.active_replay

		buffers = []
		size = Replay.BUFFER_SIZE
		for i in range(0, len(self.replay_property.buffers), size):
			offset = i + size
			buffer = bytearray(self.replay_property.buffers[i:offset])
			buffers.append(buffer)

		self.replay_data = Replay.create_from_buffers(buffers, self.replay_property.version)

	def finalize(self):
		self.replay_data.save(self.filepath)

	def matrix_bl_to_bg(self, camera):
		matrix = mathutils.Matrix(camera.transposed().as_list())
		convert = io_utils.axis_conversion(from_forward="Y", from_up="Z", to_forward="Z", to_up="-Y").to_4x4()
		final = matrix @ convert
		final.translation = matrix.to_translation()
		return final