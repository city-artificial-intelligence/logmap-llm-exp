from __future__ import annotations

import owlready2

from src.constants import LOGGER
from src.onto_access import OntologyAccess


class OntologyEntryAttr:
    def __init__(
        self, class_uri: str | None, onto: OntologyAccess, onto_entry: owlready2.ThingClass | None = None
    ) -> None:
        assert class_uri is not None or onto_entry is not None
        if class_uri is not None:
            self.thing_class = onto.getClassByURI(class_uri)
        else:
            self.thing_class = onto_entry
        assert self.thing_class is not None
        self.annotation: dict[str : set | owlready2.ThingClass] = {"class": self.thing_class}
        self.onto: OntologyAccess = onto
        self.annotate_entry(onto)

    def annotate_entry(self, onto: OntologyAccess) -> None:
        LOGGER.debug(f"Annotating {self.thing_class}")
        self.annotation["uri"] = self.thing_class.iri
        self.annotation["preffered_names"] = onto.getPrefferedLabels(self.thing_class)
        self.annotation["synonyms"] = onto.getSynonymsNames(self.thing_class)
        self.annotation["all_names"] = onto.getAnnotationNames(self.thing_class)
        self.annotation["parents"] = onto.getAncestors(self.thing_class, include_self=False)
        self.annotation["children"] = onto.getDescendants(self.thing_class, include_self=False)

    def _get_entry_names(self, name_type: str) -> set[str]:
        """Get the names of the entry.

        Args:
            name_type (str): The type of name to get, either "preffered", "synonyms", or "all_names".
            entry (OntologyEntryAttr): The entry to get the names of.


        Returns:
            set[str]: The names of the entry.

        """
        return self.annotation[name_type]

    def get_all_entity_names(self) -> set[str]:
        return self.annotation["all_names"]

    def get_preffered_names(self) -> set[str]:
        return self.annotation["preffered_names"]

    def get_synonyms(self) -> set[str]:
        return self.annotation["synonyms"]

    def __wrap_owlready2_objects(self, owlready2_class: owlready2.ThingClass) -> OntologyEntryAttr:
        return OntologyEntryAttr(class_uri=None, onto_entry=owlready2_class, onto=self.onto)

    def __owlready_set2_objects_set(self, owlready2_set: set[owlready2.ThingClass]) -> set[OntologyEntryAttr]:
        return {self.__wrap_owlready2_objects(owlready2_class) for owlready2_class in owlready2_set}

    def get_children(self) -> set[OntologyEntryAttr]:
        return self.__owlready_set2_objects_set(self.annotation["children"])

    def get_parents(self) -> set[OntologyEntryAttr]:
        return self.__owlready_set2_objects_set(self.annotation["parents"])

    def get_direct_relations(self, relation: str, relatives_getter: callable) -> set[OntologyEntryAttr]:
        related_set: set = self.annotation[relation]
        indirect_related = {rel for item in related_set for rel in relatives_getter(item, include_self=False)}

        related_set.difference_update(indirect_related)
        return {self.__wrap_owlready2_objects(entry_thing) for entry_thing in related_set}

    def get_direct_parents(self) -> set[OntologyEntryAttr]:
        return self.get_direct_relations("parents", self.onto.getAncestors)

    def get_direct_children(self) -> set[OntologyEntryAttr]:
        return self.get_direct_relations("children", self.onto.getDescendants)

    def get_attribute_relatives_names(self, attribute_name: str, name_type: str) -> list[set[str]]:
        """Get the names of the parents or children of the entry.

        Args:
            attribute_name (str): The attribute to get the names of.
            name_type (str): The type of name to get.

        Returns:
            list: The names of the parents or children of the entry.

        """
        attribute_function = self.get_parents if attribute_name == "parents" else self.get_children
        return [
            entry_names if (entry_names := entry._get_entry_names(name_type)) else {entry}
            for entry in attribute_function()
        ]

    def get_parents_preferred_names(self) -> list[set[str]]:
        return self.get_attribute_relatives_names("parents", "preffered_names")

    def get_children_preferred_names(self) -> list[set[str]]:
        return self.get_attribute_relatives_names("children", "preffered_names")

    def get_parents_synonyms(self) -> list[set[str]]:
        return self.get_attribute_relatives_names("parents", "synonyms")

    def get_children_synonyms(self) -> list[set[str]]:
        return self.get_attribute_relatives_names("children", "synonyms")

    def get_parents_names(self) -> list[set[str]]:
        return self.get_attribute_relatives_names("parents", "all_names")

    def get_children_names(self) -> list[set[str]]:
        return self.get_attribute_relatives_names("children", "all_names")

    def __repr__(self) -> str:
        """Return a string representation of the object."""
        return str(self.thing_class)

    def __str__(self) -> str:
        """Return a string representation of the object."""
        return str(self.annotation)

    def __eq__(self, other: OntologyEntryAttr) -> bool:
        """Check if this OntologyEntryAttr is equal to another OntologyEntryAttr."""
        return self.thing_class == other.thing_class

    def __hash__(self) -> int:
        """Return the hash value of the object."""
        return hash(self.thing_class)
