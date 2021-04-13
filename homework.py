import datetime as dt


# Main calculator
class Calculator:

    def __init__(self, limit):
        # Declaring attributes
        self.limit = limit
        self.records = []

    def add_record(self, record):
        # Adding record to main records variable'
        self.records.append(record)

    def get_today_stats(self, date=dt.date.today()):
        # Getting statistic for a day
        amount = 0
        date = fixing_date(date)
        # Getting the amount of spent for a day
        for added in self.records:
            if date == added.date:
                amount += added.amount
        return amount

    def get_week_stats(self, date=dt.date.today()):
        # Declaring variables
        date = fixing_date(date)
        week = dt.timedelta(days=8)
        day = dt.timedelta(days=1)
        week_before = date - week
        amount = 0
        # Counting how much did client spent for a week
        for added in self.records:
            if week_before < added.date < (date + day):
                amount += added.amount
        return amount


class CaloriesCalculator(Calculator):

    def get_calories_remained(self, date=dt.date.today()):

        # Declaring variables
        count_of_calories = 0
        date = fixing_date(date)

        # Getting amount of calories that been eaten for a day
        for record in self.records:
            if record.date == date:
                count_of_calories += record.amount

        # Getting difference between limit and eaten calories per a day
        difference = self.limit - count_of_calories

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
        spent_amount = 0
        currency = currency.lower()
        date = dt.date.today()
        currency_list = {'usd': self.USD_RATE,
                         'eur': self.EURO_RATE,
                         'rub': float(1)}
        currency_output = {'usd': 'USD',
                           'eur': 'Euro',
                           'rub': 'руб'}
        # Checking for correct currency input
        if currency not in currency_list:
            return ('Введите пожалуйта одну из возможных валют: ' 
                    f'{", ".join(currency_list.keys())}')
        # Getting amount of spending for a day
        for transfer in self.records:
            if date == transfer.date:
                spent_amount += transfer.amount
        # Getting the difference between limit and spending
        money_left = self.limit - spent_amount
        if money_left > 0:
            return ('На сегодня осталось '
                    f'{"{:.2f}".format(money_left / currency_list[currency])} '
                    f'{currency_output[currency]}')
        elif money_left < 0:
            money_left = int(str(money_left).strip('-'))
            return ('Денег нет, держись: твой долг - '
                    f'{"{:.2f}".format(money_left / currency_list[currency])} '
                    f'{currency_output[currency]}')
        else:
            return 'Денег нет, держись'


class Record:
    def __init__(self, amount, comment, date=dt.date.today()):
        self.amount = amount
        self.comment = comment
        self.date = fixing_date(date)


def fixing_date(date):
    # Checking if date type is str
    if type(date) == str:
        date = dt.date(int(date.split('.')[2]),
                       int(date.split('.')[1]),
                       int(date.split('.')[0]))
    return date
