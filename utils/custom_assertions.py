from typing import Any

from hamcrest.core.base_matcher import BaseMatcher, T
from hamcrest.core.description import Description


def dataclass_equals(expected: T) -> 'IsDataclassEqualTo':
    return IsDataclassEqualTo(expected)


class IsDataclassEqualTo(BaseMatcher):
    class MismatchEntry:
        def __init__(self, attribute: str, expected: Any, actual: Any):
            self.attribute = attribute
            self.expected = expected
            self.actual = actual

        def __str__(self):
            return f"\t'{self.attribute}' to be '{self.expected}' but was '{self.actual}'"

        def __repr__(self):
            return self.__str__()

    def __init__(self, dataclass_instance: T):
        self.dataclass_instance = dataclass_instance
        self.mismatches = []

    def describe_to(self, description: Description) -> None:
        description.append_text("Dataclasses to be equal")

    def describe_mismatch(self, item: T, mismatch_description: Description) -> None:
        formatted_messages = [str(entry) for entry in self.mismatches]
        mismatch_description.append_text("Following fields are incorrect:\n")
        mismatch_description.append_text("\n".join(formatted_messages))

    def _matches(self, item: T) -> bool:
        return self.__compare(self.dataclass_instance, item)

    def __compare(self, expected_item: T, actual_item: T, path="") -> bool:
        if not hasattr(actual_item, '__annotations__'):
            return False
        if expected_item.__annotations__.keys() != actual_item.__annotations__.keys():
            return False

        for attribute, attribute_type in expected_item.__annotations__.items():
            expected = getattr(expected_item, attribute, None)
            actual = getattr(actual_item, attribute, None)
            if expected is None:
                continue

            if attribute_type in (int, float, str, list, tuple, dict):
                if expected != actual:
                    self.mismatches.append(self.MismatchEntry(path + attribute, expected, actual))
            else:
                new_path = path + attribute + "."
                self.__compare(expected, actual, new_path)
        return len(self.mismatches) == 0
