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
        date = date if date is not str else fixing_date(date)
        return sum(i.amount for i in self.records if date == i.date)

    def get_week_stats(self, date=dt.date.today()):
        """Declaring variables"""
        date = fixing_date(date)
        week_before = date - dt.timedelta(days=7)
        return sum(i.amount for i in self.records
                   if week_before < i.date <= date)

    def get_limit_left(self, date=dt.date.today()):
        """Declaring variables"""
        date = date if date is not str else fixing_date(date)
        return (self.limit - sum(i.amount for i in self.records
                if date == i.date))


class CaloriesCalculator(Calculator):

    def get_calories_remained(self, date=dt.date.today()):
        # Declaring variables
        date = date if date is not str else fixing_date(date)
        # Getting difference between limit and eaten calories per a day
        calories_left = self.get_limit_left(date)
        # Returning smg for client
        if calories_left > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {calories_left} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    RUB_RATE = 1.0
    USD_RATE = 60.0
    EURO_RATE = 70.0
    CURRENCIES = {'rub': (RUB_RATE, 'руб'),
                  'usd': (USD_RATE, 'USD'),
                  'eur': (EURO_RATE, 'Euro')}

    def get_today_cash_remained(self, currency='rub'):
        """Declaring variables"""
        currency = currency.lower()
        date = dt.date.today()
        rate, rate_name = self.CURRENCIES[currency]
        # Checking for correct currency input
        if currency not in self.CURRENCIES:
            return ('Введите пожалуйта одну из возможных валют: '
                    f'{", ".join(self.CURRENCIES.keys())}')
        # Getting the difference between limit and spending
        money_left = self.get_limit_left(date)
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


calc = CashCalculator(1000)
r1 = calc.add_record(Record(100, 'test'))
print(calc.get_today_cash_remained('usd'))
print(calc.get_today_cash_remained('eur'))
print(calc.get_today_cash_remained())
