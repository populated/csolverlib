class BaseExc(Exception):
    pass

class BadRequest(BaseExc):
    def __init__(self):
        super().__init__("The request could not be processed due to invalid input, or something else.")

class TaskProcessing(BaseExc):
    def __init__(self):
        super().__init__("Please wait until the task is completed.")

class TaskFailed(BaseExc):
    def __init__(self):
        super().__init__("The request could not be completed successfully.")

class TaskCompleted(BaseExc):
    def __init__(self):
        super().__init__("The request has been successfully processed.")

class NoBalance(BaseExc):
    def __init__(self):
        super().__init__("The API key has insufficient balance to process the request.")

class NoToken(BaseExc):
    def __init(self):
        super().__init__("No reCaptcha token was found in the response.")
