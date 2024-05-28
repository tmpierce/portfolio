from jar import Jar
import pytest


def test_init():
    jar = Jar()
    assert jar.capacity == 12
    ThinMints = Jar(4)
    assert ThinMints.capacity == 4


def test_str():
    jar = Jar()
    assert str(jar) == ""
    jar.deposit(1)
    assert str(jar) == "🍪"
    jar.deposit(11)
    assert str(jar) == "🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪"


def test_deposit():
    jar = Jar()
    jar.deposit(4)
    assert jar.size == 4
    jar.deposit(5)
    assert jar.size == 9


def test_withdraw():
    jar = Jar()
    jar.deposit(4)
    jar.withdraw(1)
    assert jar.size == 3
    jar.withdraw(2)
    assert jar.size == 1

