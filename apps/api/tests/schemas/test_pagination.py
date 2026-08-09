import pytest
from pydantic import ValidationError

from app.schemas.pagination import PaginationParams
from app.schemas.pagination import PaginationResponse


def test_default_pagination():
    pagination = PaginationParams()

    assert pagination.page == 1
    assert pagination.page_size == 20
    assert pagination.offset == 0


def test_second_page_offset():
    pagination = PaginationParams(
        page=2,
        page_size=20,
    )

    assert pagination.offset == 20


def test_custom_page_size_offset():
    pagination = PaginationParams(
        page=3,
        page_size=10,
    )

    assert pagination.offset == 20


def test_page_must_be_positive():
    with pytest.raises(ValidationError):
        PaginationParams(page=0)


def test_page_size_must_be_positive():
    with pytest.raises(ValidationError):
        PaginationParams(page_size=0)


def test_page_size_cannot_exceed_100():
    with pytest.raises(ValidationError):
        PaginationParams(page_size=101)


def test_pagination_response_calculates_pages():
    response = PaginationResponse.from_total(
        page=1,
        page_size=20,
        total=45,
    )

    assert response.page == 1
    assert response.page_size == 20
    assert response.total == 45
    assert response.pages == 3


def test_pagination_response_exact_division():
    response = PaginationResponse.from_total(
        page=2,
        page_size=20,
        total=40,
    )

    assert response.pages == 2


def test_pagination_response_empty_result():
    response = PaginationResponse.from_total(
        page=1,
        page_size=20,
        total=0,
    )

    assert response.pages == 0
