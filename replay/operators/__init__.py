from .io_export import REPLAY_MANAGER_OT_ExportReplay
from .io_import import REPLAY_MANAGER_OT_ImportReplay

classes = [
	REPLAY_MANAGER_OT_ExportReplay,
	REPLAY_MANAGER_OT_ImportReplay,
]


def menu_import(self, context):
	self.layout.operator(REPLAY_MANAGER_OT_ImportReplay.bl_idname, text=REPLAY_MANAGER_OT_ImportReplay.bl_label)


def menu_export(self, context):
	self.layout.operator(REPLAY_MANAGER_OT_ExportReplay.bl_idname, text=REPLAY_MANAGER_OT_ExportReplay.bl_label)
