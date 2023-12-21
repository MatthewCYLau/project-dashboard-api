from api.util.util import return_dupliucated_items_in_list, is_valid_sector


def test_return_duplicated_items_in_list_one_duplicate():
    list_with_duplicated_items_foo = ["foo", "bar", "foo"]
    assert return_dupliucated_items_in_list(list_with_duplicated_items_foo) == {"foo"}


def test_return_duplicated_items_in_list_two_duplicates():
    list_with_duplicated_items_foo_bar = ["foo", "bar", "foo", "bar"]
    assert return_dupliucated_items_in_list(list_with_duplicated_items_foo_bar) == {
        "foo",
        "bar",
    }


def test_return_duplicated_items_in_list_no_duplicates():
    list_without_duplicated_items = ["bar", "foo"]
    assert return_dupliucated_items_in_list(list_without_duplicated_items) == set()


def test_is_valid_sector():
    assert is_valid_sector("Financial Services") == True
    assert is_valid_sector("Foo") == False
