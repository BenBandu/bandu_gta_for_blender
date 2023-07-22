from .io.export_replay import RM_OT_ExportReplay
from .io.import_replay import RM_OT_ImportReplay
from .replay.add_frame import RM_OT_AddFrame
from .debug.refresh_addon import RM_OT_RefreshAddon

classes = [
	RM_OT_ExportReplay,
	RM_OT_ImportReplay,
	RM_OT_AddFrame,
	RM_OT_RefreshAddon,
]


def menu_import(self, context):
	self.layout.operator(RM_OT_ImportReplay.bl_idname, text=RM_OT_ImportReplay.bl_label)


def menu_export(self, context):
	self.layout.operator(RM_OT_ExportReplay.bl_idname, text=RM_OT_ExportReplay.bl_label)
