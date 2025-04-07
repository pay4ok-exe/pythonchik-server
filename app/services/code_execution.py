# app/services/code_execution.py

import subprocess
import tempfile
import os
import uuid
import time
from typing import Dict, Any, Optional

class CodeExecutionService:
    """
    Service for executing Python code safely in a sandbox environment.
    """
    def __init__(self):
        self.timeout = 5  # 5 seconds timeout for code execution
        
    def execute_code(self, code: str, expected_output: Optional[str] = None) -> Dict[str, Any]:
        """
        Executes Python code and returns the result.
        
        Args:
            code: Python code to execute
            expected_output: Expected output for comparison (if any)
            
        Returns:
            Dictionary containing execution results
        """
        # Create a unique ID for this execution
        execution_id = str(uuid.uuid4())
        
        # Create a temporary file to write the code
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode="w") as temp_file:
            temp_file_path = temp_file.name
            temp_file.write(code)
        
        result = {
            "execution_id": execution_id,
            "success": False,
            "output": "",
            "error": "",
            "execution_time": 0,
            "matches_expected": False
        }
        
        try:
            # Record start time
            start_time = time.time()
            
            # Execute the code
            process = subprocess.Popen(
                ["python", temp_file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for completion with timeout
            try:
                stdout, stderr = process.communicate(timeout=self.timeout)
                result["success"] = process.returncode == 0
                result["output"] = stdout.strip()
                result["error"] = stderr.strip()
                
                # Check if the output matches expected output
                if expected_output is not None:
                    result["matches_expected"] = result["output"] == expected_output.strip()
                    
            except subprocess.TimeoutExpired:
                process.kill()
                result["error"] = "Execution timed out after {} seconds".format(self.timeout)
                result["success"] = False
                
            # Calculate execution time
            result["execution_time"] = round(time.time() - start_time, 3)
            
        except Exception as e:
            result["error"] = str(e)
            result["success"] = False
            
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
        return result