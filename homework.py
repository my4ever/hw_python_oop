from _datetime import datetime as dt


records = []


class Calculator:

    def __init__(self, amout, limit):
        # Declaring attributes
        self.amount = amout
        self.limit = limit

    def difference(self):
        # Getting difference
        dfr_is = self.limit - self.amount
        return dfr_is


    def add_record(self):
        Record.add_records(self)

    def get_today_stats(self):
        pass


    def get_week_stats(self):
        pass


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        pass



class CashCalculator(Calculator):

    def get_today_cash_remained(self, currency):
        pass



class Record:
    def __init__(self, amount, comment, date):
        self.amount = amount
        self.comment = comment
        self.date = date
        Record.add_records(self)


    def add_records(self):
        record = {'amount': self.amount,
                  'comment':self.comment,
                  'date': self.date}
        records.append(record)


r1 = Record(amount=145, comment='Безудержный шопинг', date='08.03.2019')
r2 = Record(amount=1568,
            comment='Наполнение потребительской корзины',
            date='09.03.2019')
r3 = Record(amount=691, comment='Катание на такси', date='08.03.2019')

print(records)
