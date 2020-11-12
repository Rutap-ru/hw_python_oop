import datetime as dt

date_today = dt.datetime.now().date()
week_ago = date_today - dt.timedelta(days=7)

class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, some_record):
        self.records.append(some_record)

    def get_today_stats(self, records):
        amount_today = 0
        for record in self.records:
            if record.date == date_today:
                amount_today += record.amount
        return amount_today
 
    def get_week_stats(self):
        amount_week = 0
        for record in self.records:
            if record.date >= week_ago and record.date <= date_today:
                amount_week += record.amount
        return amount_week

class Record:

    def __init__(self, amount, comment, date=False):
        self.amount = amount
        self.comment = comment
        if date == False:
            self.date = date_today
        else:
            date_format = '%d.%m.%Y'
            self.date = dt.datetime.strptime(date, date_format).date()

class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        remained = self.limit-super().get_today_stats(self.records)
        if remained < self.limit:
            return {f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {remained} кКал'}
        else:
            return 'Хватит есть!'

class CashCalculator(Calculator):
    USD_RATE = 76.77
    EURO_RATE = 90.69   

    def exchange_rates(self, currency, money):
        list_rate = {
            'rub' : [1, 'руб'],
            'usd' : [self.USD_RATE, 'USD'],
            'eur' : [self.EURO_RATE, 'Euro']
        }
        if list_rate[currency][0]:
            money_total = round(money/list_rate[currency][0], 2)
            currency_data = [money_total, list_rate[currency][1]]
            return currency_data
        else:
            return False

    def get_today_cash_remained(self, currency):
        remained = self.limit-super().get_today_stats(self.records)
        if remained == self.limit:
            print('Денег нет, держись')
        elif remained < self.limit:
            remained_exchange = self.exchange_rates(currency, remained)
            if remained_exchange:
                return {f'На сегодня осталось {remained_exchange[0]} {remained_exchange[1]}'}
            else:
                return {f'В валюту "{currency}" пока не конвертирую'}
        else:
            remained_exchange = self.exchange_rates(currency, remained)
            if remained_exchange:
                return {f'Денег нет, держись: твой долг - {remained_exchange[0]} {remained_exchange[1]}'}
            else:
                return {f'Денег нет, держись. Но в валюту "{currency}" пока не конвертирую'}




# создадим калькулятор денег с дневным лимитом 1000
cash_calculator = CashCalculator(1000)
        
# дата в параметрах не указана, 
# так что по умолчанию к записи должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=145, comment="кофе")) 
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment="Серёге за обед"))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=3000, comment="бар в Танин др", date="08.11.2019"))
                
print(cash_calculator.get_today_cash_remained("rub"))
# должно напечататься
# На сегодня осталось 555 руб 