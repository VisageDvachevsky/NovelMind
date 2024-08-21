import logging
import functools
import time
import os
from datetime import datetime
import inspect
from typing import Any, Callable, Dict, Optional, Union, Type
import json
import contextlib
import psutil
import uuid
import cProfile
import pstats
import io
from collections import defaultdict
from logging.handlers import RotatingFileHandler

class Logger:
    def __init__(self, log_file: str = 'app.log', use_json: bool = False, 
                 max_log_size: int = 10*1024*1024, backup_count: int = 5,
                 error_threshold: int = 10, error_window: int = 3600):
        self.logger = self._setup_logger(log_file, use_json, max_log_size, backup_count)
        self.use_json = use_json
        self.trace_id = None
        self.error_counts = defaultdict(int)
        self.error_threshold = error_threshold
        self.error_window = error_window

    def _setup_logger(self, log_file: str, use_json: bool, max_log_size: int, backup_count: int) -> logging.Logger:
        logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
        os.makedirs(logs_dir, exist_ok=True)
        log_file_path = os.path.join(logs_dir, log_file)

        logger = logging.getLogger('Logger')
        logger.setLevel(logging.DEBUG)

        c_handler = logging.StreamHandler()
        f_handler = RotatingFileHandler(log_file_path, maxBytes=max_log_size, backupCount=backup_count)
        c_handler.setLevel(logging.WARNING)
        f_handler.setLevel(logging.DEBUG)

        if use_json:
            formatter = self.JsonFormatter('%(asctime)s')
        else:
            c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
            f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            c_handler.setFormatter(c_format)
            f_handler.setFormatter(f_format)

        c_handler.setFormatter(formatter)
        f_handler.setFormatter(formatter)

        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

        logger.info(f"Logging to file: {log_file_path}")
        return logger

    class JsonFormatter(logging.Formatter):
        def format(self, record):
            log_data = {
                'timestamp': self.formatTime(record, self.datefmt),
                'name': record.name,
                'level': record.levelname,
                'message': record.getMessage(),
            }
            return json.dumps(log_data)

    def _log_function(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                sig = inspect.signature(func)
                bound_args = sig.bind(*args, **kwargs)
                bound_args.apply_defaults()

                arg_str = ", ".join(f"{k}={v!r}" for k, v in bound_args.arguments.items())
                self.logger.info(f"Calling {func.__name__}({arg_str})")
            except Exception as bind_exception:
                self.logger.error(f"Error binding arguments in {func.__name__}: {bind_exception}")
                raise
            
            start_time = time.time()

            try:
                result = func(*args, **kwargs)
                self.logger.info(f"{func.__name__} completed successfully")
                
                if result is None:
                    self.logger.debug(f"{func.__name__} returned None")
                elif isinstance(result, (int, float, str, bool)):
                    self.logger.debug(f"{func.__name__} returned: {result}")
                else:
                    self.logger.debug(f"{func.__name__} returned: {type(result).__name__}")
                
                return result
            except Exception as e:
                self.logger.exception(f"Exception in {func.__name__}: {str(e)}")
                raise
            finally:
                end_time = time.time()
                self.logger.debug(f"{func.__name__} execution time: {end_time - start_time:.4f} seconds")

        return wrapper


    def log_class(self) -> Callable[[Type], Type]:
        def decorator(cls: Type) -> Type:
            for name, method in inspect.getmembers(cls, inspect.isfunction):
                if not name.startswith('__'): 
                    setattr(cls, name, self._log_function(method))
            return cls
        return decorator

    def log_function(self) -> Callable[[Callable], Callable]:
        return self._log_function

    def _log(self, level: str, message: str, extra: Dict[str, Any] = None):
        log_data = {"message": message, "trace_id": self.trace_id}
        if extra:
            log_data.update(extra)
        
        getattr(self.logger, level.lower())(json.dumps(log_data) if self.use_json else message, extra=log_data)

    def debug(self, message: str, extra: Dict[str, Any] = None):
        self._log("DEBUG", message, extra)

    def info(self, message: str, extra: Dict[str, Any] = None):
        self._log("INFO", message, extra)

    def warning(self, message: str, extra: Dict[str, Any] = None):
        self._log("WARNING", message, extra)

    def error(self, message: str, extra: Dict[str, Any] = None):
        current_time = time.time()
        error_key = (message, current_time // self.error_window)
        self.error_counts[error_key] += 1
        
        if self.error_counts[error_key] <= self.error_threshold:
            self._log("ERROR", message, extra)
        elif self.error_counts[error_key] == self.error_threshold + 1:
            self._log("ERROR", f"Suppressing similar errors for: {message}", extra)

    def critical(self, message: str, extra: Dict[str, Any] = None):
        self._log("CRITICAL", message, extra)

    @contextlib.contextmanager
    def log_block(self, block_name: str):
        self.logger.info(f"Entering block: {block_name}")
        start_time = time.time()
        try:
            yield
        finally:
            end_time = time.time()
            duration = end_time - start_time
            self.logger.info(f"Exiting block: {block_name}. Duration: {duration:.4f} seconds")

    def log_system_info(self):
        cpu_percent = psutil.cpu_percent()
        memory_info = psutil.virtual_memory()
        disk_io = psutil.disk_io_counters()
        
        self.logger.info(f"System Info - CPU: {cpu_percent}%, "
                         f"Memory: {memory_info.percent}%, "
                         f"Disk Read: {disk_io.read_bytes}, "
                         f"Disk Write: {disk_io.write_bytes}")

    def set_trace_id(self):
        self.trace_id = str(uuid.uuid4())

    def profile(self, output_file=None):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                pr = cProfile.Profile()
                pr.enable()
                result = func(*args, **kwargs)
                pr.disable()
                s = io.StringIO()
                ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
                ps.print_stats()
                self.logger.debug(f"Profile for {func.__name__}:\n{s.getvalue()}")
                if output_file:
                    ps.dump_stats(output_file)
                return result
            return wrapper
        return decorator

    def set_log_level(self, logger_name: str, level: str):
        logging.getLogger(logger_name).setLevel(getattr(logging, level.upper()))