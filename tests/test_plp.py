import pytest
from pages.product_page import ProductPage
from config import USE_CSV_DATA, SINGLE_SEARCH_TERM, BASE_URL
from utils.data_reader import load_search_terms


def _get_terms():
    if USE_CSV_DATA:
        terms = load_search_terms()
        return terms or [SINGLE_SEARCH_TERM]
    return [SINGLE_SEARCH_TERM]


@pytest.mark.parametrize('term', _get_terms())
def test_plp_search_filter(page, term):
    plp = ProductPage(page)
    plp.maps_to(BASE_URL)
    plp.search(term)
    count = plp.get_products_count()
    if count == 0:
        no_results = plp.get_no_results_text()
        assert len(no_results) > 0, f'Expected a no-results message for "{term}" but found none'
        pytest.skip(f'PASS (0 results): search "{term}" returned no products — no-results message confirmed: "{no_results}"')
    else:
        names = plp.get_product_names()
        assert all(term.lower() in n.lower() for n in names), (
            f"Not all product names contain '{term}': {names}"
        )
        print(f'PASS ({count} results): search "{term}" returned {count} matching products')


@pytest.mark.parametrize('min_price,max_price', [(10, 150)])
def test_plp_price_filter(page, min_price, max_price):
    plp = ProductPage(page)
    plp.maps_to(BASE_URL)
    effective = plp.apply_price_filter(min_price=min_price, max_price=max_price)

    effective_min = effective['min']
    effective_max = effective['max']


    prices = plp.get_product_prices()
    assert len(prices) > 0, 'No product prices found after applying filter'
    out_of_range = [p for p in prices if p < effective_min or p > effective_max]
    assert out_of_range == [], (
        f'Products outside [{effective_min}, {effective_max}] range: {out_of_range}'
    )
