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
        # Getting statistic for a day'
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
            if week_before < added.date and added.date < (date + day):
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
        self.currency = currency.lower()
        date = dt.date.today()
        # Checking for correct currency input
        if self.currency not in ('usd', 'eur', 'rub'):
            return 'Введите пожалуйта одну из возможных валют: rub, usd, eur'
        # Getting amount of spending for a day
        for transfer in self.records:
            if date == transfer.date:
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
                        f'{"{:.2f}".format(float(difference))} руб')
            elif difference < 0:
                # Getting rid of minus symbol
                difference = int(str(difference).strip('-'))
                return ('Денег нет, держись: твой долг - '
                        f'{"{:.2f}".format(float(difference))} руб')
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
    def __init__(self, amount, comment, date=dt.date.today()):
        self.amount = amount
        self.comment = comment
        self.date = fixing_date(date)


# Checking if date type is str
def fixing_date(date):
    if type(date) == str:
        date_info = date.split('.')
        date = dt.date(int(date_info[2]), int(date_info[1]), int(date_info[0]))
    return date
