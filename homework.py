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

    def get_today_stats(self, date=None):
        """Declaring variable"""
        date = (date if date is not None and type(date) is not str
                else fixing_date(date))
        return sum(i.amount for i in self.records if date == i.date)

    def get_week_stats(self, date=None):
        """Declaring variables"""
        date = (date if date is not None
                and type(date) is not str else fixing_date(date))
        week_before = date - dt.timedelta(days=7)
        return sum(i.amount for i in self.records
                   if week_before < i.date <= date)

    def get_limit_left(self, date=None):
        """Declaring variable"""
        date = (date if date is not None and type(date) is not str
                else fixing_date(date))
        return (self.limit - sum(i.amount for i in self.records
                if date == i.date))


class CaloriesCalculator(Calculator):

    def get_calories_remained(self, date=None):
        """Declaring variable"""
        date = (date if date is not None and type(date) is not str
                else fixing_date(date))
        # Getting difference between limit and eaten calories per a day
        calories_left = self.get_limit_left(date)
        # Returning smg for client
        if calories_left > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {calories_left} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    RUB_RATE = float(1)
    USD_RATE = float(60)
    EURO_RATE = float(70)
    CURRENCIES = {'rub': (RUB_RATE, 'руб'),
                  'usd': (USD_RATE, 'USD'),
                  'eur': (EURO_RATE, 'Euro')}

    def get_today_cash_remained(self, currency='rub'):
        """Declaring variables"""
        date = dt.date.today()
        currency = currency.lower()
        # Checking for correct currency input
        if currency not in self.CURRENCIES:
            return ('Введите пожалуйта одну из возможных валют: '
                    f'{", ".join(self.CURRENCIES.keys())}')
        rate, rate_name = self.CURRENCIES[currency]
        # Getting the difference between limit and spending
        money_left = self.get_limit_left(date) / rate
        if money_left == 0:
            return 'Денег нет, держись'
        if money_left < 0:
            return ('Денег нет, держись: твой долг - '
                    f'{money_left * -1:.2f} {rate_name}')
        return ('На сегодня осталось '
                f'{money_left:.2f} {rate_name}')


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        self.date = (date if date is not None and type(date) is not str
                     else fixing_date(date))


def fixing_date(date):
    """Checking if date type is str"""
    if type(date) is str:
        day, month, year = date.split('.')
        return dt.date(int(year), int(month), int(day))
    return dt.date.today()
