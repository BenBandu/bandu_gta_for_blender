from . import replay_manager


def register():
	replay_manager.register()


def unregister():
	replay_manager.unregister()


if __name__ == '__main__':
	register()
	# unregister()
