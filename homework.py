import datetime as dt


# Main calculator
class Calculator:

    def __init__(self, limit):
        """Declaring attributes"""
        self.limit = limit
        self.records = []

    def add_record(self, record):
        """Adding record to main attribute records"""
        self.records.append(record)

    def get_today_stats(self, date=dt.date.today()):
        """Declaring variable"""
        date = fixing_date(date)
        return sum(i.amount for i in self.records if date == i.date)

    def get_week_stats(self, date=dt.date.today()):
        """Declaring variables"""
        date = fixing_date(date)
        week_before = date - dt.timedelta(days=7)
        return sum(i.amount for i in self.records
                   if week_before < i.date <= date)


class CaloriesCalculator(Calculator):

    def get_calories_remained(self, date=dt.date.today()):
        # Declaring variables
        date = fixing_date(date)
        calories = sum(i.amount for i in self.records if date == i.date)
        # Getting difference between limit and eaten calories per a day
        difference = self.limit - calories
        # Returning smg for client
        if difference > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {difference} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    RUB_RATE = 1.0
    USD_RATE = 60.0
    EURO_RATE = 70.0
    curs = {'rub': (RUB_RATE, 'руб'),
            'usd': (USD_RATE, 'USD'),
            'eur': (EURO_RATE, 'Euro')}

    def get_today_cash_remained(self, currency='rub'):
        """Declaring variables"""
        currency = currency.lower()
        date = dt.date.today()
        spent_amount = self.get_today_stats(date)
        rate, rate_name = self.curs[currency]
        # Checking for correct currency input
        if currency not in self.curs:
            return ('Введите пожалуйта одну из возможных валют: '
                    f'{", ".join(self.curs.keys())}')
        # Getting the difference between limit and spending
        money_left = self.limit - spent_amount
        if money_left > 0:
            return ('На сегодня осталось '
                    f'{"{:.2f}".format(money_left / rate)} {rate_name}')
        if money_left < 0:
            money_left = int(str(money_left).strip('-'))
            return ('Денег нет, держись: твой долг - '
                    f'{"{:.2f}".format(money_left / rate)} {rate_name}')
        return 'Денег нет, держись'


class Record:
    def __init__(self, amount, comment, date=dt.date.today()):
        self.amount = amount
        self.comment = comment
        self.date = fixing_date(date)


def fixing_date(date):
    """Checking if date type is str"""
    if type(date) is str:
        day, month, year = date.split('.')
        date = dt.date(int(year), int(month), int(day))
    return date
