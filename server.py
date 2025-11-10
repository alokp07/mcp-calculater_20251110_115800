"""
Basic Maths MCP Server

This MCP server provides basic mathematical operations including addition, subtraction, multiplication, and division.

Environment Variables:
- None required (local computation only)

Required Permissions:
- None (local computation only)

Setup Instructions:
1. Install fastmcp: pip install fastmcp
2. Save this file as server.py
3. Run: python server.py

Authentication Method:
- None required
"""

import os
from typing import Optional
from enum import Enum
from pydantic import BaseModel, field_validator, model_validator, ValidationInfo, ConfigDict

class Config:
    '''Configuration with environment variable validation'''
    # No environment variables required for this server
    
    @classmethod
    def validate(cls) -> None:
        '''Validate required environment variables are set'''
        errors = []
        # No validations needed
        if errors:
            error_msg = "Missing required environment variables:\n"
            error_msg += "\n".join(f"  - {e}" for e in errors)
            error_msg += "\n\nSee module docstring for configuration details."
            raise ValueError(error_msg)

# Validate configuration on import
Config.validate()

class ResponseFormat(Enum):
    JSON = "json"

CHARACTER_LIMIT = 1000

class MathsInput(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    a: int
    b: int
    
    @field_validator('a', 'b')
    @classmethod
    def validate_integers(cls, v: int, info: ValidationInfo) -> int:
        """Validate that values are integers"""
        if not isinstance(v, int):
            raise ValueError(f"{info.field_name} must be an integer")
        return v

class MathsResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    result: int
    operation: str
    
    @model_validator(mode='after')
    def validate_result(self) -> 'MathsResult':
        if self.result > CHARACTER_LIMIT:
            raise ValueError("Result exceeds character limit")
        return self

class ErrorResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    error: str
    details: Optional[str] = None

class DivisionInput(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    a: int
    b: int
    
    @field_validator('b')
    @classmethod
    def validate_divisor(cls, v: int, info: ValidationInfo) -> int:
        """Validate divisor is not zero"""
        if v == 0:
            raise ValueError("Division by zero is not allowed")
        return v

def _make_api_request(operation: str, a: int, b: int) -> int:
    """Helper function to perform maths operations"""
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        return a // b  # Integer division
    else:
        raise ValueError("Unknown operation")

def _handle_api_error(error: Exception) -> ErrorResponse:
    """Helper function to handle errors"""
    return ErrorResponse(error=str(error), details="An error occurred during computation")

from fastmcp import FastMCP

mcp = FastMCP("Basic Maths Server")

@mcp.tool()
def maths_add_numbers(a: int, b: int) -> int:
    """Add two integers and return the result."""
    try:
        result = _make_api_request("add", a, b)
        return result
    except Exception as e:
        raise _handle_api_error(e)

@mcp.tool()
def maths_subtract_numbers(a: int, b: int) -> int:
    """Subtract two integers and return the result."""
    try:
        result = _make_api_request("subtract", a, b)
        return result
    except Exception as e:
        raise _handle_api_error(e)

@mcp.tool()
def maths_multiply_numbers(a: int, b: int) -> int:
    """Multiply two integers and return the result."""
    try:
        result = _make_api_request("multiply", a, b)
        return result
    except Exception as e:
        raise _handle_api_error(e)

@mcp.tool()
def maths_divide_numbers(a: int, b: int) -> int:
    """Divide two integers and return the integer result."""
    try:
        result = _make_api_request("divide", a, b)
        return result
    except Exception as e:
        raise _handle_api_error(e)

@mcp.tool()
def maths_power_numbers(a: int, b: int) -> int:
    """Raise a to the power of b and return the result."""
    try:
        result = a ** b
        if result > CHARACTER_LIMIT:
            raise ValueError("Result exceeds character limit")
        return result
    except Exception as e:
        raise _handle_api_error(e)

if __name__ == "__main__":
    mcp.run()