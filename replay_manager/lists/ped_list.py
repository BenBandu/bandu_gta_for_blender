import bpy


# noinspection PyPep8Naming
class RM_UL_PED_LIST(bpy.types.UIList):
	bl_idname = "RM_UL_PED_LIST"

	def draw_item(self, context, layout, data, item, icon, active_data, active_property, index=0, flt_flag=0):
		custom_icon = "EMPTY_AXIS"
		ped = item
		if not ped.enabled:
			return

		if self.layout_type in {"DEFAULT", "COMPACT"}:
			layout.label(text=ped.model, icon=custom_icon)
		elif self.layout_type in {"GRID"}:
			layout.alignment = "CENTER"
			layout.label(text="", icon=custom_icon)
