import datetime as dt


# Transforming string date into datetime
def redo_date(date_str):
    date_full = date_str.split('.')
    day = date_full[0]
    month = date_full[1]
    year = date_full[2]
    if int(day[0]) == 0:
        day = day[1]
    if int(month[0]) == 0:
        month = month[1]
    return dt.datetime(int(year), int(month), int(day))


# Date by default
today = redo_date(dt.date.today().strftime('%d.%m.%Y'))


# Main calculator
class Calculator:
    # Declaring variables
    def __init__(self, limit):
        # Declaring attributes
        self.limit = limit
        self.records = []
    # Adding record to main variable
    def add_record(self, record):

        self.records.append(record)
    # Getting statistic fot day
    def get_today_stats(self, date=today):

        self.date = date
        amount = 0

        for added in self.records:
            if self.date == added.date:
                amount += added.amount
        return amount
    #  Getting weekly statistic
    def get_week_stats(self, date=today):

        self.date = date
        week = dt.timedelta(days=7)
        week_before = today - week
        amount = 0

        for added in self.records:
            if week_before < added.date < self.date:
                amount += added.amount
        return amount


# Calories calculator
class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        pass


# Money calculator
class CashCalculator(Calculator):
    # Getting cash amount remained for a day
    def get_today_cash_remained(self, currency='rub', date=today):
        # Declaring variables
        USD_RATE = 77
        EURO_RATE = 92
        self.currency = currency.lower()
        self.date = date
        spent_amount = 0
        # Getting amount of spending for a day
        for transfer in self.records:
            if self.date == transfer.date:
                spent_amount += transfer.amount

        difference = self.limit - spent_amount
        # Checking up on currency request
        if self.currency == 'rub':
            if difference > 0:
                return f'На сегодня осталось {"{:.2f}".format(difference)} руб'
            elif difference == 0:
                return 'Денег нет, держись'
            else:
                return f'Денег нет, держись: твой долг {"{:.2f}".format(difference)} руб'
        elif self.currency == 'usd':
            if difference > 0:
                return f'На сегодня осталось {"{:.2f}".format(difference / USD_RATE)} USD'
            elif difference == 0:
                return 'Денег нет, держись'
            else:
                return f'Денег нет, держись: твой долг - {"{:.2f}".format(difference / USD_RATE)} USD'
        elif self.currency == 'eur':
            if difference > 0:
                return f'На сегодня осталось {"{:.2f}".format(difference / EURO_RATE)} Euro'
            elif difference == 0:
                return 'Денег нет, держись'
            else:
                return f'Денег нет, держись: твой долг - {"{:.2f}".format(difference / EURO_RATE)} Euro'
        else:
            return 'Введите пожалуйта одну из возможных валют: rub, usd, eur'


class Record:

    def __init__(self, amount, comment, date=today):
        self.amount = amount
        self.comment = comment
        self.date = redo_date(date)


calc = CashCalculator(2000)
r1 = calc.add_record(Record(amount=145, comment='Безудержный шопинг', date='12.04.2021'))
r2 = calc.add_record(Record(amount=15681,
                            comment='Наполнение потребительской корзины',
                            date='12.04.2021'))
r3 = Record(amount=691, comment='Катание на такси', date='08.03.2019')

print(calc.get_week_stats())
print(calc.get_today_stats())
print(calc.get_today_cash_remained())
