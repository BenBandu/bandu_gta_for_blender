import bpy


# noinspection PyPep8Naming
class REPLAY_UL_LIST(bpy.types.UIList):

	def draw_item(self, context, layout, data, item, icon, active_data, active_property, index=0, flt_flag=0):
		custom_icon = "EMPTY_AXIS"

		if self.layout_type in {"DEFAULT", "COMPACT"}:
			layout.label(text=item.name, icon=custom_icon)
		elif self.layout_type in {"GRID"}:
			layout.alignment = "CENTER"
			layout.label(text="", icon=custom_icon)