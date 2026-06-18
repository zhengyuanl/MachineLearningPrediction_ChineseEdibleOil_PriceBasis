from datetime import datetime, timedelta

class DateSummoner:
    def __init__(self, start_date_str: str, date_format: str = "%Y-%m-%d"):
        """
        Initializes the date tracker.
        
        :param start_date_str: The initial date string (e.g., '2025-06-15')
        :param date_format: The format blueprint for parsing and outputting
        """
        self.date_format = date_format
        # Parse the input string into a live datetime object
        self.current_date = datetime.strptime(start_date_str, self.date_format)

    def getCurrentDateString(self) -> str:
        """Returns the current date tracked by the class as a formatted string."""
        return self.current_date.strftime(self.date_format)

    def nextDate(self) -> str:
        """Steps forward by 1 day and returns the new formatted date string."""
        self.current_date += timedelta(days=1)
        return self.getCurrentDateString()
