import datetime as dt


# Date by default
today = dt.datetime.strptime(dt.date.today().strftime('%d.%m.%Y'), '%d.%m.%Y')


# Main calculator
class Calculator:

    def __init__(self, limit):
        # Declaring attributes
        self.limit = limit
        self.records = []

    # Adding record to main records variable
    def add_record(self, record):
        self.records.append(record)

    # Getting statistic for a day
    def get_today_stats(self, date=today):

        amount = 0

        # Checking fot date type
        if isinstance(date, str):
            self.date = dt.datetime.strptime(date, '%d.%m.%Y')
        else:
            self.date = date
        # Getting the amount of spent for a day
        for added in self.records:
            if self.date == added.date:
                amount += added.amount
        return amount

    #  Getting weekly statistic
    def get_week_stats(self, date=today):

        # Declaring variables
        week = dt.timedelta(days=8)
        day = dt.timedelta(days=1)
        week_before = today - week
        amount = 0

        # Checking for date type
        if isinstance(date, str):
            self.date = dt.datetime.strptime(date, '%d.%m.%Y')
        else:
            self.date = date

        # Counting how much did client spent for a week
        for added in self.records:
            if week_before < added.date and added.date < (self.date + day):
                amount += added.amount
        return amount


# Calories calculator
class CaloriesCalculator(Calculator):


    def get_calories_remained(self, date=today):

        # Declaring variables
        count_of_calories = 0

        # Checking for date type
        if isinstance(date, str):
            self.date = redo_date(date)
        else:
            self.date = date

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


# Money calculator
class CashCalculator(Calculator):

    # Getting cash amount remained for a day
    def get_today_cash_remained(self, currency='rub', date=today):

        # Declaring variables
        self.USD_RATE = 77.0
        self.EURO_RATE = 92.0
        spent_amount = 0
        self.currency = currency.lower()

        # Checking for date type
        if isinstance(date, str):
            self.date = redo_date(date)
        else:
            self.date = date

        # Checking for correct currency input
        if self.currency not in ('usd', 'eur', 'rub'):
            return 'Введите пожалуйта одну из возможных валют: rub, usd, eur'

        # Getting amount of spending for a day
        for transfer in self.records:
            if self.date == transfer.date:
                spent_amount += transfer.amount

        # Getting the difference between limit and spending
        difference = self.limit - spent_amount

        # Universal answer if limit is equal to zero
        if difference == 0:
            return 'Денег нет, держись'


        # Checking up on currency request
        if self.currency == 'rub':
            if difference > 0:
                return ('На сегодня осталось '
                        f' {"{:.2f}".format(difference)} руб')
            elif difference < 0:
                # Getting rid of minus symbol
                difference = int(str(difference).strip('-'))
                return ('Денег нет, держись: твой долг - '
                        f'{"{:.2f}".format(difference)} руб')

        elif self.currency == 'usd':
            if difference > 0:
                return ('На сегодня осталось '
                        f'{"{:.2f}".format(difference / self.USD_RATE)} USD')
            elif difference < 0:
                # Getting rid of minus symbol
                difference = int(str(difference).strip('-'))
                return ('Денег нет, держись: твой долг - '
                        f'{"{:.2f}".format(difference / self.USD_RATE)} USD')

        elif self.currency == 'eur':
            if difference > 0:
                return ('На сегодня осталось '
                        f'{"{:.2f}".format(difference / self.EURO_RATE)} Euro')

            elif difference < 0:
                # Getting rid of minus symbol
                difference = int(str(difference).strip('-'))
                return ('Денег нет, держись: твой долг - '
                        f'{"{:.2f}".format(difference / self.EURO_RATE)} Euro')


class Record:

    def __init__(self, amount, comment, date=today):
        self.amount = amount
        self.comment = comment
        self.date = dt.datetime.strptime(date, '%d.%m.%Y')

calc = CashCalculator(1000)
r1 = calc.add_record(Record(amount=145, comment='Безудержный шопинг', date='06.04.2021'))
r2 = calc.add_record(Record(amount=145, comment='Безудержный шопинг', date='10.04.2021'))
r3 = calc.add_record(Record(amount=145, comment='Безудержный шопинг', date='13.04.2021'))

print(calc.get_week_stats())
print(calc.get_today_cash_remained('usd'))
