from datetime import datetime
from dateutil.relativedelta import relativedelta

# Calculating months and formatting date
class date_formatting:  
    def calculate_dates(months):
        endDate = datetime.now()
        startDate = endDate - relativedelta(months=max(months, 1))
        if months == 0:
            startDate = endDate - relativedelta(months=1)
        return endDate.strftime("%Y-%m-%d"), startDate.strftime("%Y-%m-%d")