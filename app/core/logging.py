"""
Logging and auditing for tool execution.
Tracks what tools are called and by whom.
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional
from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
audit_logger = logging.getLogger("audit")


class ToolExecutionAudit:
    """Audit log for tool executions"""
    
    @staticmethod
    def log_tool_call(
        tool_name: str,
        tool_args: Dict[str, Any],
        user_message: Optional[str] = None,
        metadata: Optional[Dict] = None
    ):
        """Log when a tool is called"""
        if not settings.log_tool_execution:
            return
        
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": "tool_call",
            "tool": tool_name,
            "args": tool_args,
            "user_message": user_message,
            "metadata": metadata or {}
        }
        
        audit_logger.info(json.dumps(audit_entry))
    
    @staticmethod
    def log_tool_result(
        tool_name: str,
        success: bool,
        result: Any,
        error: Optional[str] = None,
        execution_time_ms: float = 0
    ):
        """Log when a tool completes"""
        if not settings.log_tool_execution:
            return
        
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": "tool_result",
            "tool": tool_name,
            "success": success,
            "error": error,
            "execution_time_ms": execution_time_ms
        }
        
        # Don't log full result - might be sensitive
        if success:
            audit_entry["result_type"] = type(result).__name__
        
        audit_logger.info(json.dumps(audit_entry))
    
    @staticmethod
    def log_tool_rejection(
        tool_name: str,
        reason: str,
        tool_args: Dict[str, Any]
    ):
        """Log when a tool call is rejected"""
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": "tool_rejected",
            "tool": tool_name,
            "reason": reason,
            "args": tool_args
        }
        
        logger.warning(json.dumps(audit_entry))


def log_security_event(
    event_type: str,
    description: str,
    severity: str = "WARNING"
):
    """Log security-related events"""
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "description": description,
        "severity": severity
    }
    
    if severity == "ERROR":
        logger.error(json.dumps(entry))
    elif severity == "WARNING":
        logger.warning(json.dumps(entry))
    else:
        logger.info(json.dumps(entry))
