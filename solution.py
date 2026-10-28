# 도서관 대출 시스템 — 아래 클래스를 완성하세요. (클래스·메서드 이름은 바꾸지 마세요)

BOOKS = ("B001", "B002", "B003", "B004", "B005")
LOAN_DAYS = 14
MAX_LOANS = 3


def _valid_day(day):
    # bool은 int의 하위 타입이라 따로 걸러야 함. 2.0 같은 float도 거절.
    return isinstance(day, int) and not isinstance(day, bool) and day >= 1


class LibraryLoan:
    def __init__(self):
        self._loans = {}      # book_id -> (name, 빌린 날)
        self._ban_until = {}  # name -> 대출 정지의 마지막 날(포함)

    def borrow(self, book_id, name, day):
        if not isinstance(book_id, str) or book_id not in BOOKS:
            return False
        if not isinstance(name, str) or not _valid_day(day):
            return False
        if book_id in self._loans:
            return False
        mine = [(b, d) for b, (n, d) in self._loans.items() if n == name]
        if len(mine) >= MAX_LOANS:
            return False
        if any(day > d + LOAN_DAYS for _, d in mine):
            return False
        if day <= self._ban_until.get(name, 0):
            return False
        self._loans[book_id] = (name, day)
        return True

    def return_book(self, book_id, name, day):
        if not isinstance(book_id, str) or not isinstance(name, str):
            return -1
        if not _valid_day(day):
            return -1
        loan = self._loans.get(book_id)
        if loan is None or loan[0] != name:
            return -1
        borrowed = loan[1]
        if day < borrowed:
            return -1
        late = max(0, day - (borrowed + LOAN_DAYS))
        del self._loans[book_id]
        if late > 0:
            end = day + late - 1
            if end > self._ban_until.get(name, 0):
                self._ban_until[name] = end
        return late

    def get_loans(self, name):
        if not isinstance(name, str):
            return []
        result = [(b, d + LOAN_DAYS) for b, (n, d) in self._loans.items() if n == name]
        result.sort(key=lambda t: (t[1], t[0]))
        return result
