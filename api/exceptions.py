class GeminiUploadFailed(Exception):
    """Exception raised when a video upload to Gemini fails."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"GeminiUploadFailed: {self.message}"