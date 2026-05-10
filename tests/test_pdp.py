import pytest
from pages.product_page import ProductPage
from config import BASE_URL, PDP_TEST_TERMS


@pytest.mark.parametrize('term', PDP_TEST_TERMS)
def test_pdp_fields(page, term):
    plp = ProductPage(page)
    plp.maps_to(BASE_URL)
    plp.search(term)
    count = plp.get_products_count()
    if count == 0:
        pytest.skip(f'No results for "{term}" — skipping PDP test')
    plp.open_product_by_index(0)
    name = plp.get_pdp_name()
    price = float(plp.get_pdp_price())
    desc = plp.get_pdp_description()
    assert term in name.lower(), f'Expected product name to contain search term "{term}", got "{name}"'
    assert price > 0, f'Expected price to be positive, got "{price}"'
    assert len(desc) > 0, f'Expected description to be non-empty, got "{desc}"'
