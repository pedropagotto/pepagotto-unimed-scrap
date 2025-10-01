class DateRange:
    """Classe para armazenar o intervalo de datas."""
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date   
    @staticmethod
    def get_current_month_dates() -> 'DateRange':
        """Retorna o primeiro e o último dia do mês atual."""
        import datetime

        today = datetime.date.today()
        first_day = today.replace(day=1)
        
        # Encontra o último dia do mês
        if today.month == 12:
            next_month = today.replace(year=today.year + 1, month=1, day=1)
        else:
            next_month = today.replace(month=today.month + 1, day=1)
        
        last_day = next_month - datetime.timedelta(days=1)
        return DateRange(first_day, last_day)
