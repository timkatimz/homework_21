from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def __init__(self, capacity):
        self._items = {}
        self._capacity = capacity

    @abstractmethod
    def add(self, title, count):
        pass

    @abstractmethod
    def remove(self, title, count):
        pass

    @property
    @abstractmethod
    def get_free_space(self):
        pass

    @property
    @abstractmethod
    def get_items(self):
        pass

    @property
    @abstractmethod
    def get_unique_items_count(self):
        pass


class Store(Storage):
    def __init__(self):
        self._items = {}
        self._capacity = 100

    def add(self, title, count):
        if title in self.items:
            self._items[title] += count
        else:
            self._items[title] = count
        self._capacity -= count

    def remove(self, title, count):
        resp = self._items[title] - count
        if resp > 0:
            self._items[title] = resp
        else:
            del self._items[title]
        self._capacity += count

    @property
    def get_free_space(self):
        return self._capacity

    @property
    def get_items(self):
        return self._items

    @property
    def get_unique_items_count(self):
        return len(self._items.keys())

    @property
    def items(self):
        return self._items

    @get_items.setter
    def get_items(self, new_items):
        self._items = new_items


class Shop(Store):
    def __init__(self):
        super().__init__()
        self._capacity = 20


class Request:
    def __init__(self, message):
        self.message = self._split_message(message)
        self.from_ = self.message[4]
        self.to = self.message[6]
        self.ammount = int(self.message[1])
        self.product = self.message[2]

    @staticmethod
    def _split_message(message):
        return message.split(" ")

    def __repr__(self):
        return f"Доставить {self.ammount} {self.product} из {self.from_} в {self.to}"


def main():
    while (True):
        user_input = input("Введите запрос: ")
        if user_input == "стоп":
            break

        request = Request(user_input)



        from_ = store if request.from_ == "склад" else shop
        to = store if request.to == "склад" else shop

        if request.product in store.items:
            print(f"Нужный товар есть  в пункте {request.from_}")
        else:
            print(f"Нужного товара нет в пункте {request.from_}")

        if from_.items[request.product] >= request.ammount:
            print(f"Нужное количество есть  в пункте {request.from_}")
        else:
            print(f"В пункте {request.from_} не хватает {request.ammount - from_.items[request.product]}")

        if to.get_free_space <= request.ammount:
            print(f"В пункте {request.to} не достаточно свободного места")
            continue

        store.remove(request.product, request.ammount)

        shop.add(request.product, request.ammount)

        print(f"Курьер забрал {request.ammount} {request.product} co {request.from_}")
        print(f"Курьер везет {request.ammount} {request.product} co {request.from_} в {request.to}")
        print(f"Курьер привез {request.ammount} {request.product} в {request.to}\n")

        print(f"В {request.from_} хранится:")
        for item, count in store.get_items.items():
            print(f"{count}  {item}")
        print("\n")

        print(f"В {request.to} хранится:")
        for item, count in shop.get_items.items():
            print(f"{count}  {item}")
        print("\n")


if __name__ == "__main__":
    store = Store()
    shop = Shop()

    store_items = {
        "молоко": 20,
        "сахар": 15,
        "сливки": 7,
        "печеньки": 9,
    }

    for item, count in store_items.items():
        store.add(item, count)
    main()
