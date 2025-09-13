from math import ceil


def make_pagination_range(
    page_range,
    pages_qty,
    current_page,
):
    middle = ceil(pages_qty / 2)

    # início fixo
    if current_page <= middle:
        return page_range[:pages_qty]

    # final fixo
    if current_page + middle > len(page_range):
        return page_range[-pages_qty:]

    # meio dinâmico (centraliza current_page)
    start = current_page - middle
    end = start + pages_qty
    return page_range[start:end]
