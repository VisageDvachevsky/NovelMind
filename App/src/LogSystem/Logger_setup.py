from .LoggerSystem import Logger

class LoggerSetup:
    def __init__(self):
        self.logger = Logger(use_json=True)
        self.log_class_instance = self.logger.log_class()
        self.log_function_instance = self.logger.log_function()
        self.debug = self.logger.debug
        self.info = self.logger.info
        self.warning = self.logger.warning
        self.error = self.logger.error
        self.critical = self.logger.critical
        self.log_block = self.logger.log_block
        self.log_system_info = self.logger.log_system_info
        self.set_trace_id = self.logger.set_trace_id
        self.profile = self.logger.profile
        self.set_log_level = self.logger.set_log_level

logger_setup = LoggerSetup()

__all__ = ['logger_setup']
