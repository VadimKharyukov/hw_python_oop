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

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        """Расчет дневного расхода."""
        now = dt.datetime.today().date()
        return sum(i.amount for i in self.records if i.date == now)

    def get_week_stats(self):
        """Расчет недельного расхода."""
        now = dt.datetime.today().date()
        week_sum = now - dt.timedelta(days=6)
        return sum(i.amount for i in self.records if now >= i.date >= week_sum)

    def remained(self):
        return self.limit - self.get_today_stats()


class CashCalculator(Calculator):
    """Калькулятор денег."""
    USD_RATE = float(60)
    EURO_RATE = float(70)
    RUB_RATE = float(1)

    def get_today_cash_remained(self, currency=None):
        """Остаток денежных средств на данный момент."""
        currency_dict = {
            'rub': (self.RUB_RATE, 'руб'),
            'usd': (self.USD_RATE, 'USD'),
            'eur': (self.EURO_RATE, 'Euro'),
        }
        if self.remained() == 0:
            return 'Денег нет, держись'
        elif currency is None:
            return 'Вы не ввели валюту!'
        elif currency not in currency_dict.keys():
            return 'Ваша валюта не поддерживается!'
        cur_rate, cur_name = currency_dict[currency]
        cash_rem = round(self.remained() / cur_rate, 2)
        if cash_rem < 0:
            abs_cash = abs(cash_rem)
            return f'Денег нет, держись: твой долг - {abs_cash} {cur_name}'
        else:
            return f'На сегодня осталось {cash_rem} {cur_name}'


class CaloriesCalculator(Calculator):
    """Калькулятор калорий."""

    def get_calories_remained(self):
        calories = self.limit - self.get_today_stats()
        if calories > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более '
                    f'{calories} кКал')
        else:
            return 'Хватит есть!'
