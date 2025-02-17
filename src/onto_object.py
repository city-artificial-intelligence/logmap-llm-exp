from __future__ import annotations

import owlready2

from src.constants import LOGGER
from src.onto_access import OntologyAccess


class OntologyEntryAttr:
    def __init__(self, class_uri: str | None, onto: OntologyAccess, class_id: str | None = None) -> None:
        assert class_uri is not None or class_id is not None
        if class_uri is not None:
            self.class_id = onto.getClassByURI(class_uri)
        else:
            self.class_id = class_id
        assert self.class_id is not None
        self.annotation: dict[str : set | owlready2.ThingClass] = {"class": self.class_id}
        self.onto: OntologyAccess = onto
        self.annotate_entry(onto)

    def annotate_entry(self, onto: OntologyAccess) -> None:
        LOGGER.debug(f"Annotating {self.class_id}")
        self.annotation["children"] = onto.getDescendants(self.class_id)
        self.annotation["parents"] = onto.getAncestors(self.class_id)
        self.annotation["preffered_names"] = onto.getPrefferedLabels(self.class_id)
        self.annotation["synonyms"] = onto.getSynonymsNames(self.class_id)
        self.annotation["names"] = onto.getAnnotationNames(self.class_id)

    def get_all_entety_names(self) -> set[str]:
        return self.annotation["names"]

    def get_preffered_names(self) -> set[str]:
        return self.annotation["preffered_names"]

    def get_synonyms(self) -> set[str]:
        return self.annotation["synonyms"]

    def get_children(self, skip_itself: bool = True) -> set[owlready2.ThingClass]:
        result = self.annotation["children"]
        if skip_itself:
            result = result.difference({self.class_id})
        return result

    def get_parents(self, skip_itself: bool = True) -> set[owlready2.ThingClass]:
        result = self.annotation["parents"]
        if skip_itself:
            result = result.difference({self.class_id})
        return result

    def get_direct_parents(self) -> set:
        raise NotImplementedError

    def get_direct_children(self) -> set:
        raise NotImplementedError

    def _get_entry_names(self, name_type: str, entry: owlready2.Thing) -> set[str]:
        """Get the names of the entry.

        Args:
            name_type (str): The type of name to get.
            entry (owlready2.Thing): The entry to get the names of.


        Returns:
            set: The names of the entry.

        """
        if name_type == "preffered":
            names_func = self.onto.getPrefferedLabels
        elif name_type == "synonyms":
            names_func = self.onto.getSynonymsNames
        elif name_type == "names":
            names_func = self.onto.getAnnotationNames
        return names_func(entry)

    def get_attribute_relatives_names(
        self, attribute_name: str, name_type: str, skip_itself: bool = True
    ) -> list[set[str]]:
        """Get the names of the parents or children of the entry.

        Args:
            attribute_name (str): The attribute to get the names of.
            name_type (str): The type of name to get.
            skip_itself (bool): Whether to skip the entry itself.

        Returns:
            list: The names of the parents or children of the entry.

        """
        attribute_function = self.get_parents if attribute_name == "parents" else self.get_children
        return [
            entry_names if (entry_names := self._get_entry_names(name_type, entry)) else {entry}
            for entry in attribute_function(skip_itself=skip_itself)
        ]

    def get_parents_preferred_names(self, skip_itself: bool = True) -> list[set[str]]:
        return self.get_attribute_relatives_names("parents", "preffered", skip_itself=skip_itself)

    def get_childred_preferred_names(self, skip_itself: bool = True) -> list[set[str]]:
        return self.get_attribute_relatives_names("children", "preffered", skip_itself=skip_itself)

    def get_parents_synonyms(self, skip_itself: bool = True) -> list[set[str]]:
        return self.get_attribute_relatives_names("parents", "synonyms", skip_itself=skip_itself)

    def get_children_synonyms(self, skip_itself: bool = True) -> list[set[str]]:
        return self.get_attribute_relatives_names("children", "synonyms", skip_itself=skip_itself)

    def get_parents_names(self, skip_itself: bool = True) -> list[set[str]]:
        return self.get_attribute_relatives_names("parents", "names", skip_itself=skip_itself)

    def get_children_names(self, skip_itself: bool = True) -> list[set[str]]:
        return self.get_attribute_relatives_names("children", "names", skip_itself=skip_itself)

    def __repr__(self) -> str:
        """Return a string representation of the object.

        Returns:
            str: The string representation of the object's annotation.

        """
        return str(self.annotation)

    def __str__(self) -> str:
        """Return a string representation of the object.

        Returns:
            str: The string representation of the object's annotation.

        """
        return str(self.annotation)
