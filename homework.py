import datetime as dt


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, some_record):
        self.records.append(some_record)

    def get_today_stats(self):
        date_today = dt.datetime.now().date()
        amount_today = sum(i.amount for i in self.records
                           if i.date == date_today)
        return amount_today

    def get_week_stats(self):
        today = dt.datetime.now().date()
        week = today - dt.timedelta(days=7)
        records = self.records
        return sum(i.amount for i in records if i.date >= week and
                   i.date <= today)

    def count_remainder(self):
        return self.limit - self.get_today_stats()


class Record:

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment

        if date is None:
            date_today = dt.datetime.now().date()
            self.date = date_today
        else:
            date_format = '%d.%m.%Y'
            self.date = dt.datetime.strptime(date, date_format).date()


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        remained = self.count_remainder()

        if remained > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {remained} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0
    currencies = {
        'rub': [1, 'руб'],
        'usd': [USD_RATE, 'USD'],
        'eur': [EURO_RATE, 'Euro']
    }

    def exchange_rates(self, currency, money):
        exchange, rate = self.currencies[currency]
        money = round(money / exchange, 2)
        return [money, rate]

    def get_today_cash_remained(self, currency):

        if currency not in self.currencies:
            return 'Конвертация в данную валюту не поддерживается'

        remained = self.count_remainder()

        if remained == 0:
            return 'Денег нет, держись'

        money, rate = self.exchange_rates(currency, remained)

        if remained > 0:
            return f'На сегодня осталось {money} {rate}'

        money = abs(money)
        return f'Денег нет, держись: твой долг - {money} {rate}'
