import datetime as dt


# Date by default
today = dt.date.today()


# Main calculator
class Calculator:

    def __init__(self, limit):
        # Declaring attributes
        self.limit = limit
        self.records = []

    def add_record(self, record):
        # Adding record to main records variable'
        self.records.append(record)

    def get_today_stats(self, date=today):
        # Declaring variables
        date = fixing_date(date)
        return sum(i.amount for i in self.records if date == i.date)

    def get_week_stats(self, date=today):
        # Declaring variables
        date = fixing_date(date)
        week = dt.timedelta(days=7)
        week_before = date - week
        amount = sum(i.amount for i in self.records
                     if week_before < i.date <= date)
        return amount


class CaloriesCalculator(Calculator):

    def get_calories_remained(self, date=today):
        # Declaring variables
        date = fixing_date(date)
        calories = sum(i.amount for i in self.records if date == i.date)
        # Getting difference between limit and eaten calories per a day
        difference = self.limit - calories
        # Returning smg for client
        if difference > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {difference} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 77.0
    EURO_RATE = 92.0

    def get_today_cash_remained(self, currency='rub'):
        # Declaring variables
        currency = currency.lower()
        date = dt.date.today()
        spent_amount = sum(i.amount for i in self.records if date == i.date)
        curs = {'rub': {'rate': 1.0, 'name': 'руб'},
                'usd': {'rate': self.USD_RATE, 'name': 'USD'},
                'eur': {'rate': self.EURO_RATE, 'name': 'Euro'}}
        # Checking for correct currency input
        if currency not in curs:
            return ('Введите пожалуйта одну из возможных валют: '
                    f'{", ".join(curs.keys())}')
        # Getting the difference between limit and spending
        money_left = self.limit - spent_amount
        if money_left > 0:
            return ('На сегодня осталось '
                    f'{"{:.2f}".format(money_left / curs[currency]["rate"])} '
                    f'{curs[currency]["name"]}')
        elif money_left < 0:
            money_left = int(str(money_left).strip('-'))
            return ('Денег нет, держись: твой долг - '
                    f'{"{:.2f}".format(money_left / curs[currency]["rate"])} '
                    f'{curs[currency]["name"]}')
        else:
            return 'Денег нет, держись'


class Record:
    def __init__(self, amount, comment, date=today):
        self.amount = amount
        self.comment = comment
        self.date = fixing_date(date)


def fixing_date(date):
    # Checking if date type is str
    if type(date) is str:
        day, month, year = date.split('.')
        date = dt.date(int(year), int(month), int(day))
    return date
