import bpy
from . import blocks


class Replay(bpy.types.PropertyGroup):

	# INFO #
	name: bpy.props.StringProperty(name="Name", description="Name of the replay", default="replay")
	version: bpy.props.IntProperty(name="Version", description="Game ID")

	# BLENDER SETTINGS #
	offset: bpy.props.IntProperty(name="Offset", description="Offset the entire replay in the timeline")

	# FRAME DATA #
	general: bpy.props.PointerProperty(type=blocks.General, name="General")
	clock: bpy.props.PointerProperty(type=blocks.Clock, name="Clock")
	weather: bpy.props.PointerProperty(type=blocks.Weather, name="Weather")

	# PEDS #
	peds: bpy.props.CollectionProperty(type=blocks.Ped, name="Ped")
	ped_index: bpy.props.IntProperty(name="Ped Index", description="Current Ped", default=-1)

	# VEHICLES #
	vehicles: bpy.props.CollectionProperty(type=blocks.Vehicle, name="Vehicle")
	vehicle_index: bpy.props.IntProperty(name="Vehicle Index", description="Current Vehicle", default=-1)

	# buffers: bpy.props.StringProperty(name="buffers", description="Contains all the replay data")

	@property
	def game(self):
		if self.version == 1:
			return "GTA III"
		elif self.version == 2:
			return "GTA: Vice City"
		elif self.version == 3:
			return "GTA: San Andreas"
		elif self.version == 4:
			return "GTA: San Andreas (Steam)"
		else:
			return "Unknown version"

	@property
	def active_ped(self):
		if len(self.peds) == 0:
			return None

		ped = self.peds[self.ped_index]
		if not ped.enabled:
			return None

		return ped

	@property
	def active_vehicle(self):
		if len(self.vehicles) == 0:
			return None

		vehicle = self.vehicles[self.vehicle_index]
		if not vehicle.enabled:
			return None

		return vehicle
