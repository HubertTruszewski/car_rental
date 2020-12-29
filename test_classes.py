from classes import Car
from errors import (NegativeFuelConsumptionError, NegativeSeatsError,
                    WrongDbIdTypeError, NegativeDbIdError,
                    WrongSeatsTypeError,
                    WrongFuelConsumptionTypeError,
                    WrongDoorsTypeError, NegativeDoorsError,
                    WrongPriceType, NegativePriceError)
from pytest import raises


def test_create_car_without_values():
    auto = Car()
    assert auto.type_id() == 0
    assert auto.mark() is None
    assert auto.model() is None
    assert auto.registration_number() is None
    assert auto.seats() is None
    assert auto.fuel_consumption() is None
    assert auto.doors() is None
    assert auto.color() is None
    assert auto.price() is None


def test_create_car_with_values():
    auto = Car('Skoda', 'Superb', 'WM7529E', 5, 8.9, 5, 'biały', 200)
    assert auto.type_id() == 0
    assert auto.mark() == 'Skoda'
    assert auto.model() == 'Superb'
    assert auto.registration_number() == 'WM7529E'
    assert auto.seats() == 5
    assert auto.fuel_consumption() == 8.9
    assert auto.doors() == 5
    assert auto.color() == 'biały'
    assert auto.price() == 200


def test_car_set_db_id():
    auto = Car()
    auto.set_db_id(1)
    assert auto.db_id() == 1


def test_car_set_db_id_str():
    auto = Car()
    auto.set_db_id('12')
    assert auto.db_id() == 12


def test_car_set_db_id_not_number():
    auto = Car()
    with raises(WrongDbIdTypeError):
        auto.set_db_id('abc')


def test_car_set_db_id_negative_number():
    auto = Car()
    with raises(NegativeDbIdError):
        auto.set_db_id('-7')


def test_car_set_seats():
    auto = Car()
    auto.set_seats(4)
    assert auto.seats() == 4


def test_car_set_seats_str():
    auto = Car()
    auto.set_seats('5')
    assert auto.seats() == 5


def test_car_set_seats_not_number():
    auto = Car()
    with raises(WrongSeatsTypeError):
        auto.set_seats('abc')


def test_car_set_seats_negative_value():
    auto = Car()
    with raises(NegativeSeatsError):
        auto.set_seats('-9')


def test_car_set_fuel_consumption():
    auto = Car()
    auto.set_fuel_consumption(8.8)
    assert auto.fuel_consumption() == 8.8


def test_car_set_fuel_consumption_str():
    auto = Car()
    auto.set_fuel_consumption('3.9')
    assert auto.fuel_consumption() == 3.9


def test_car_set_fuel_consumption_not_number():
    auto = Car()
    with raises(WrongFuelConsumptionTypeError):
        auto.set_fuel_consumption('abc')


def test_car_set_fuel_consumption_negative():
    auto = Car()
    with raises(NegativeFuelConsumptionError):
        auto.set_fuel_consumption('-4.3')


def test_car_set_doors():
    auto = Car()
    auto.set_doors(5)
    assert auto.doors() == 5


def test_car_set_doors_str():
    auto = Car()
    auto.set_doors(3)
    assert auto.doors() == 3


def test_car_set_doors_not_number():
    auto = Car()
    with raises(WrongDoorsTypeError):
        auto.set_doors('abc')


def test_car_set_doors_negative():
    auto = Car()
    with raises(NegativeDoorsError):
        auto.set_doors('-6')


def test_car_set_price():
    auto = Car()
    auto.set_price(120)
    assert auto.price() == 120.0


def test_car_set_price_str():
    auto = Car()
    auto.set_price('123.98')
    assert auto.price() == 123.98


def test_car_set_price_not_number():
    auto = Car()
    with raises(WrongPriceType):
        auto.set_price('abc')


def test_car_set_price_negative():
    auto = Car()
    with raises(NegativePriceError):
        auto.set_price('-150.98')
