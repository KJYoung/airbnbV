from django.utils import timezone
import calendar


class Day:
    def __init__(self, num, past, month, year):
        self.year = year
        self.month = month
        self.num = num
        self.past = past

    def __str__(self):
        return str(self.num)


class Calendar(calendar.Calendar):
    def __init__(self, year, month):
        super().__init__(firstweekday=6)  # Starts with Sunday.
        self.year = year
        self.month = month
        self.day_names = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")
        self.month_names = (
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        )

    def get_days(self):
        weeks = self.monthdays2calendar(self.year, self.month)
        now = timezone.now()
        year, month, today = now.year, now.month, now.day
        days = []
        for week in weeks:
            for day, _ in week:
                if month == self.month:
                    past = day <= today  # current month
                else:
                    past = False  # next month : past must false.
                new_day = Day(num=day, past=past, month=self.month, year=self.year)
                days.append(new_day)
        return days

    def get_month(self):
        return self.month_names[self.month - 1]
