import pytest
from src.booking_refund import is_refundable

# flexible rate cancelled at least 48 hours before check-in -> refund
@pytest.mark.parametrize("hours", [
    72,                   # flexible, cancelled early
    48,                   # flexible, exactly 48 hours
    49,                   # flexible, just above 48
])
def test_flexible_rate_48_hours_or_more_is_refundable(hours):
    # Act
    result = is_refundable(hours, True)
    # Assert
    assert result is True


# flexible rate under 48 hours, or any non-flexible rate -> no refund
@pytest.mark.parametrize("hours, flexible", [
    (47, True),           # flexible, just below 48
    (0, True),            # flexible, same day
    (72, False),          # non-flexible, cancelled early
    (48, False),          # non-flexible, exactly 48 hours
    (24, False),          # non-flexible, cancelled late
])
def test_not_refundable_cases_return_false(hours, flexible):
    # Act
    result = is_refundable(hours, flexible)
    # Assert
    assert result is False


# correct type but outside the permitted range -> ValueError
def test_negative_hours_raises_value_error():
    with pytest.raises(ValueError):
        is_refundable(-1, True)


# wrong data type -> TypeError
@pytest.mark.parametrize("hours, flexible", [
    (48.5, True),         #  hours is a decimal
    ("72", True),         #  hours is a string
    (True, True),         #  hours is a boolean
    (None, True),         #  hours is None
    (72, 1),              #  flexible is integer 1
    (72, "True"),         #  flexible is a string
    (72, None),           #  flexible is None
])
def test_wrong_type_raises_type_error(hours, flexible):
    with pytest.raises(TypeError):
        is_refundable(hours, flexible)