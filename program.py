import datetime as dt


class Record:
    def __init__(self, ammount, comment, date=None):
        date_format = '%d.%m.%Y'
        self.ammount = ammount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now()
        else:
            self.date = dt.datetime.strptime(date, date_format)


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []
        self.today = dt.datetime.now()
        self.week = self.today - dt.timedelta(7)

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_count = 0
        for r in self.records:
            if r.date == self.today:
                today_count += r.ammount
        return today_count

    def get_week_stats(self):
        week_count = 0
        for r in self.records:
            if self.week <= r.date <= self.today:
                week_count += r.ammount
        return week_count

    def get_remained(self):
        return self.limit - self.get_today_stats()


class CashCalculator(Calculator):
    RUB_RATE = 1
    USD_RATE = 70.26
    EUR_RATE = 82.09

    def get_today_cash_remained(self, currency='rub'):
        CURRENCIES = {
            'rub': ('rub', CashCalculator.RUB_RATE),
            'usd': ('usd', CashCalculator.USD_RATE),
            'eur': ('eur', CashCalculator.EUR_RATE)
        }

        cash_remained = self.get_remained()
        name = CURRENCIES[currency][0]
        rate = CURRENCIES[currency][1]
        if 0 < cash_remained <= self.limit:
            if name != 'rub':
                cash_remained = round(cash_remained/rate, 2)
            return f'На сегодня осталось {cash_remained} {name}'
        if cash_remained == 0:
            return f'Денег нет, держись.'
        if cash_remained < 0:
            if name != 'rub':
                cash_remained = round(abs(cash_remained)/rate, 2)
            return f'Ваш долг {abs(cash_remained)} {name}'


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        calories = self.get_today_stats()
        calories_remained = self.get_remained()
        if calories >= self.limit:
            return 'Хватит есть'
        else:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {calories_remained}'


if __name__ == '__main__':
    cash_calculator = CashCalculator(1000)
    cash_calculator.add_record(Record(ammount=145, comment="кофе"))
    cash_calculator.add_record(Record(ammount=300, comment="Серёге за обед"))
    cash_calculator.add_record(Record(ammount=1000, comment="Серёге за обед"))
    cash_calculator.add_record(Record(ammount=3000, comment="бар в Танин др", date="08.11.2019"))
    print(cash_calculator.get_today_cash_remained("rub")) # На сегодня осталось 555 руб
    calories_calculator = CaloriesCalculator(1000)
    calories_calculator.add_record(Record(ammount=100, comment='cyka'))
    print(calories_calculator.get_calories_remained())