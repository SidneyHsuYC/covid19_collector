import logging

def setup_logger(logger, level=logging.INFO, file_name='imageloader.log'):
	logger.setLevel(level)

	formatter = logging.Formatter('%(levelname)s: <%(module)s>: %(message)s')

	file_handler = logging.FileHandler(file_name, mode='w')
	file_handler.setLevel(logging.INFO)
	file_handler.setFormatter(formatter)

	stream_handler = logging.StreamHandler()
	stream_handler.setLevel(logging.WARNING)
	stream_handler.setFormatter(formatter)

	logger.addHandler(file_handler)
	logger.addHandler(stream_handler)