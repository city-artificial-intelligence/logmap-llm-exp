from __future__ import annotations

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
        self.annotation: dict[str:set] = {"class": self.class_id}
        self.onto: OntologyAccess = onto
        self.annotate_entry(onto)

    def annotate_entry(self, onto: OntologyAccess) -> None:
        LOGGER.debug(f"Annotating {self.class_id}")
        self.annotation["children"] = onto.getDescendants(self.class_id)
        self.annotation["parents"] = onto.getAncestors(self.class_id)
        self.annotation["synonyms"] = onto.getSynonymsNames(self.class_id)
        self.annotation["names"] = onto.getAnnotationNames(self.class_id)

    def get_all_entety_names(self) -> list:
        return self.annotation["names"]

    def get_synonyms(self) -> list:
        return self.annotation["synonyms"]

    def get_children(self, skip_itself: bool = True) -> set:
        result = self.annotation["children"]
        if skip_itself:
            result = result.difference({self.class_id})
        return result

    def get_parents(self, skip_itself: bool = True) -> set:
        result = self.annotation["parents"]
        if skip_itself:
            result = result.difference({self.class_id})
        return result

    def get_parents_preferred_names(self, skip_itself: bool = True) -> set:
        labels = []
        for parent in self.get_parents(skip_itself=skip_itself):
            preffered = self.onto.getPrefferedLabels(parent)
            if preffered:
                labels.append(preffered)
            else:
                labels.append({parent})
        return labels

    def get_childred_preferred_names(self, skip_itself: bool = True) -> list:
        return [
            preffered if (preffered := self.onto.getPrefferedLabels(child)) else {child}
            for child in self.get_children(skip_itself=skip_itself)
        ]

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
