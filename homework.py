import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is not None:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        else:
            self.date = dt.datetime.today().date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []
        print(f'доступен лимит: {limit}')

    def add_record(self, record):
        self.records.append(record)
        print('Добавлена запись.')
        print(f'количество: {record.amount}, '
              f'название: {record.comment}, '
              f'дата операции: {record.date},')

    def get_today_stats(self):
        """Расчет дневного расхода."""
        today_stats = 0
        now = dt.datetime.today().date()
        for i in self.records:
            if i.date == now:
                today_stats += i.amount
        print(f'Итог за сегодня: {today_stats}.')
        return today_stats

    def get_week_stats(self):
        """Расчет недельного расхода."""
        week_stats = 0
        now = dt.datetime.today().date()
        week_calc = now - dt.timedelta(days=6)
        for i in self.records:
            if now >= i.date >= week_calc:
                week_stats += i.amount
        print(f'Итог за неделю: {week_stats}.')
        return week_stats

    def remained(self):
        return self.limit - self.get_today_stats()


class CashCalculator(Calculator):
    """Калькулятор денег."""
    USD_RATE = float(60)
    EURO_RATE = float(70)
    RUB_RATE = float(1)

    def get_today_cash_remained(self, currency=None):
        """Остаток денежных средств на данный момент."""
        currency_dict = {'rub': (self.RUB_RATE, 'руб'),
                         'usd': (self.USD_RATE, 'USD'),
                         'eur': (self.EURO_RATE, 'Euro'),
                         }

        if currency is None:
            return 'Вы не ввели валюту!'
        elif currency not in currency_dict.keys():
            return 'Ваша валюта не поддерживается!'

        cur_rate, cur_name = currency_dict[currency]
        cash_rem = round(self.remained() / cur_rate, 2)

        if cash_rem == 0:
            return 'Денег нет, держись'
        elif cash_rem < 0:
            abs_cash = abs(cash_rem)
            return f'Денег нет, держись: твой долг - {abs_cash} {cur_name}'
        else:
            return f'На сегодня осталось {cash_rem} {cur_name}'


class CaloriesCalculator(Calculator):
    """Калькулятор калорий."""

    def get_calories_remained(self,):
        calories = self.limit - self.get_today_stats()
        if calories > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более '
                    f'{calories} кКал')
        else:
            return 'Хватит есть!'
