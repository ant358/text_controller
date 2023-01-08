from src.input import get_pageids, get_pageids_from_graph, get_title


def test_get_pageids0():
    assert len(get_pageids()) > 0


def test_get_pageids1():
    assert "18942" in get_pageids()


def test_get_pageids_from_graph0():
    assert len(get_pageids_from_graph()) > 0


def test_get_pageids_from_graph1():
    assert "18942" in get_pageids_from_graph()


def test_get_title0():
    assert get_title("18942") == "Monty Python"
