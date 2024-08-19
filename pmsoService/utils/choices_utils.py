from .json_reader import read_file

def get_all_tier_choices():
	"""
		Get all Tiers of Customer
	"""
	choices_config_file = "config/choices_config.json"
	tier = read_file(choices_config_file)
	return  tier["CUSTOMER"]["TIER_CHOICES"]

def get_all_category_choices():
	"""
		Get all Category of Product
	"""
	choices_config_file = "config/choices_config.json"
	category = read_file(choices_config_file)
	return  category["PRODUCT"]["CATEGORY_CHOICES"]

def get_all_status_choices():
	"""
		Get all Status of Product Order
	"""
	choices_config_file = "config/choices_config.json"
	status = read_file(choices_config_file)
	return  status["PRODUCT_ORDER"]["STATUS_CHOICES"]
