import pytest
from src.booking_cost import calculate_booking_cost


# BC01–BC08: valid inputs return the correct total
@pytest.mark.parametrize("nights, rate, expected", [
    (1, 100, 100),        # minimum valid nights
    (5, 100, 500),        # normal stay
    (30, 100, 3000),      # maximum valid nights
    (5, 0, 0),            # zero nightly rate
    (3, 12000, 36000),    # realistic rate (S$120 per night)
    (6, 100, 600),        # 6 nights, just below 7
    (7, 100, 700),        # 7 nights, no free night
    (8, 100, 800),        # 8 nights, no free night
])
def test_valid_booking_returns_correct_cost(nights, rate, expected):
    # Act
    result = calculate_booking_cost(nights, rate)
    # Assert
    assert result == expected

def test_result_is_an_integer():
    # Arrange
    nights = 3
    rate = 12000
    # Act
    result = calculate_booking_cost(nights, rate)
    # Assert
    assert type(result) is int

# correct type but out of range -> ValueError
@pytest.mark.parametrize("nights, rate", [
    (0, 100),             # BC09 nights is zero
    (31, 100),            # BC10 nights above maximum
    (-1, 100),            # BC11 negative nights
    (5, -1),              # BC12 rate one below zero
])
def test_out_of_range_raises_value_error(nights, rate):
    with pytest.raises(ValueError):
        calculate_booking_cost(nights, rate)


# wrong type -> TypeError
@pytest.mark.parametrize("nights, rate", [
    (2.5, 100),           # nights is a decimal
    ("5", 100),           # nights is a string
    (True, 100),          # nights is a boolean
    (None, 100),          # nights is None
    (5, 100.5),           # rate is a decimal
    (5, "100"),           # rate is a string
    (5, True),            # rate is a boolean
    (5, None),            # rate is None
])
def test_wrong_type_raises_type_error(nights, rate):
    with pytest.raises(TypeError):
        calculate_booking_cost(nights, rate)