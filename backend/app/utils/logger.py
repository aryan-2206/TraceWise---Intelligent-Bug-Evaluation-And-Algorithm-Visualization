import logging
import sys
from typing import Optional
from datetime import datetime
import os

class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for console output"""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        # Add color to level name
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
        
        return super().format(record)

def setup_logger(name: str = "TraceWise", 
                level: str = "INFO",
                log_file: Optional[str] = None,
                console_output: bool = True,
                format_string: Optional[str] = None) -> logging.Logger:
    """Setup logger with custom configuration"""
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Default format
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, level.upper()))
        
        # Use colored formatter for console
        console_formatter = ColoredFormatter(format_string)
        console_handler.setFormatter(console_formatter)
        
        logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, level.upper()))
        
        # Use regular formatter for file
        file_formatter = logging.Formatter(format_string)
        file_handler.setFormatter(file_formatter)
        
        logger.addHandler(file_handler)
    
    return logger

def get_logger(name: str) -> logging.Logger:
    """Get logger instance"""
    return logging.getLogger(name)

def set_log_level(logger: logging.Logger, level: str):
    """Set log level for logger"""
    logger.setLevel(getattr(logging, level.upper()))

def add_file_handler(logger: logging.Logger, log_file: str, level: str = "INFO"):
    """Add file handler to logger"""
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(getattr(logging, level.upper()))
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)

def log_function_call(func):
    """Decorator to log function calls"""
    
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        
        try:
            result = func(*args, **kwargs)
            logger.debug(f"{func.__name__} returned successfully")
            return result
        except Exception as e:
            logger.error(f"{func.__name__} raised exception: {str(e)}")
            raise
    
    return wrapper

def log_performance(func):
    """Decorator to log function performance"""
    
    import time
    
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            
            execution_time = end_time - start_time
            logger.info(f"{func.__name__} executed in {execution_time:.4f} seconds")
            
            return result
        except Exception as e:
            end_time = time.time()
            execution_time = end_time - start_time
            
            logger.error(f"{func.__name__} failed after {execution_time:.4f} seconds: {str(e)}")
            raise
    
    return wrapper

class LoggerManager:
    """Manager for multiple loggers"""
    
    def __init__(self):
        self.loggers = {}
    
    def create_logger(self, name: str, **kwargs) -> logging.Logger:
        """Create and store logger"""
        logger = setup_logger(name, **kwargs)
        self.loggers[name] = logger
        return logger
    
    def get_logger(self, name: str) -> Optional[logging.Logger]:
        """Get stored logger"""
        return self.loggers.get(name)
    
    def set_all_log_levels(self, level: str):
        """Set log level for all managed loggers"""
        for logger in self.loggers.values():
            set_log_level(logger, level)
    
    def close_all(self):
        """Close all loggers"""
        for logger in self.loggers.values():
            for handler in logger.handlers:
                handler.close()
            logger.handlers.clear()

# Global logger manager instance
logger_manager = LoggerManager()

# Initialize default logger
default_logger = setup_logger(
    "TraceWise",
    level="INFO",
    log_file="logs/tracewise.log",
    console_output=True
)

logger_manager.loggers["TraceWise"] = default_logger
