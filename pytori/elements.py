"""TORI Scheme Elements and Utilities

"""
from typing import Iterable, Union, Optional

from pytori import utilities


class SchemeElementError(ValueError):
    """Scheme Element Error"""


class SchemeElement:
    """TORI scheme element base class

    """
    __key_attr__ = None
    __slots__ = ()

    def __eq__(self, other):
        """Equality is pass-thru to slots"""
        if not isinstance(other, self.__class__):
            return False
        return all(s == o for s, o in zip([getattr(self, slot) for slot in self.__slots__],
                                          [getattr(other, slot) for slot in self.__slots__]))

    def __hash__(self):
        """Hash is pass thru to slots"""
        return hash((self.__class__.__name__, tuple(getattr(self, slot) for slot in self.__slots__)))

    def __repr__(self):
        """String representation of a TORI Scheme Element"""
        return '{}({})'.format(self.__class__.__name__, getattr(self, self.__key_attr__))

    def _check_dict_keys(self, d: dict):
        """Helper function for asserting that all the slots are satisfied

        Args:
            d:
                dict,

        Raises:


        Returns:
            None
        """

    def validate(self) -> bool:
        """Base method for element validation"""
        raise NotImplementedError

    @staticmethod
    def from_dict(d: dict):
        """Base method for loading from dict"""
        raise NotImplementedError


class TagGroup(SchemeElement):
    """Tag Group Scheme Element

    """
    __key_attr__ = 'name'
    __slots__ = (
        'name',
        'description',
    )

    def __init__(self, name: str, description: str):
        """Create a Tag Group

        Args:
            name:
                str, the name of the Tag Group
            description:
                str, the description of the Tag Group
        """
        self.name = name
        self.description = description


DEFAULT_TAG_GROUP = TagGroup('Default', 'Default Tag Group')


class Tag(SchemeElement):
    """Tag Scheme Element

    """
    __key_attr__ = 'name'
    __slots__ = (
        'name',
        'description',
        'group',
    )

    def __init__(self, name: str, description: str, group: TagGroup = DEFAULT_TAG_GROUP):
        """Create a Tag

        Args:
            name:
                str, the name of the tag
            description:
                str, the description of the tag
            group:
                TagGroup, the group to which this Tag belongs
        """
        self.name = name
        self.description = description
        self.group = group


class Reference(SchemeElement):
    """Reference Scheme Element

    """
    __key_attr__ = 'title'
    __required_slots__ = (
        'title',
        'author',
        'tags',
    )
    __optional_slots__ = (
        'url',
    )
    __slots__ = __required_slots__ + __optional_slots__

    def __init__(self, title: str, author: Union[str, Iterable[str]], url: Optional[str] = None, tags: Iterable[Tag] = None):
        """Create a Reference

        Args:
            title:
                str, the title of the reference
            author:
                str or Iterable[str], the author(s) of the reference
            url:
                str, the url of the reference
            tags:
                Iterable[Tag], default None. Any Tags for the reference defined in the TORI scheme

        Returns:
            Reference
        """
        self.title = title
        self.author = (author,) if isinstance(author, str) else tuple(author)
        self.url = url
        self.tags = tuple(tags)

    def add_tag(self, tag: Tag):
        """Add a tag to a reference

        Args:
            tag:
                Tag, the tag to add to the reference

        Returns:
            None
        """
        if tag not in self.tags:
            self.tags = self.tags + (tag,)


class TORISchemeError(ValueError):
    """Error class for TORI Scheme"""


class TORI:
    """TORI Specification

    """
    __slots__ = ('tag_groups', 'tags', 'references', 'keys', '_errors')

    def __init__(self, tag_groups: Iterable[TagGroup], tags: Iterable[Tag], references: Iterable[Reference]):
        """Create a TORI scheme

        Args:
            tag_groups:
                Iterable[TagGroup], a collection of TagGroups
            tags:
                Iterable[Tag], a collection of Tags
            references:
                Iterable[Reference], a collection of References

        Returns:
            TORI
        """
        self.tag_groups = tuple(tag_groups)
        self.tags = tuple(tags)
        self.references = tuple(references)
        self.keys = None
        self._errors = ()

        self._set_keys()

    def ___contains__(self, x):
        """Define contains method for use with 'in' syntax"""
        if not isinstance(x, SchemeElement):
            raise ValueError('Containment not defined for TORI and object {} of type {}'.format(str(x), type(x)))

        x_type = type(x)
        x_key = getattr(x, x_type.__key_attr__)
        return x_key in self.keys[x_type]

    def _clear_errors(self):
        """Helper method for clearing validation errors"""
        self._errors = ()

    def _raise_error(self, message: str, collect: bool = False):
        """Raise errors helper method or passively collect (for linting)

        Args:
            message:
                str, message of error to be raised or collected
            collect:
                bool, default False, if True then collect the error by appending to

        Returns:
            None
        """
        if collect:
            self._errors += (message,)
        else:
            raise TORISchemeError(message)

    def _set_keys(self):
        """Set keys"""
        self.keys = {element_type: tuple(getattr(g, element_type.__key_attr__) for g in elements)
                     for elements, element_type in zip((self.tag_groups, self.tags, self.references), (TagGroup, Tag, Reference))}

    def validate(self, collect_errors: bool = False) -> Union[bool, Iterable[TORISchemeError]]:
        """Validate the TORI scheme, run all validations

        Args:
            collect_errors:
                bool, default False, if True return a list of all the validation errors

        Returns:
            bool or Iterable[TORISchemeError]
        """
        self._clear_errors()
        valid_tag_groups = self.validate_tag_groups(collect_errors=collect_errors)
        valid_tags = self.validate_tags(collect_errors=collect_errors)
        valid_references = self.validate_references(collect_errors=collect_errors)

        valid = all([valid_tag_groups, valid_tags, valid_references])
        if collect_errors:
            return self._errors
        return valid

    def validate_tag_groups(self, collect_errors: bool = False) -> bool:
        """Validate Tag Groups according to the following criteria

        Properties:
            1. TagGroups must be unique

        Args:
            collect_errors:
                bool, default False, if True return a list of all the validation errors

        Returns:
           bool or Iterable[TORISchemeError]
        """
        # Check uniqueness
        dups = utilities.find_duplicates(self.tag_groups)
        if dups:
            self._raise_error('Tag Groups must be unique, found duplicates: {}'.format(dups), collect=collect_errors)
            return False
        return True

    def validate_tags(self, collect_errors: bool = False) -> bool:
        """Validate Tags according to the following criteria

        Attributes:
            1. Tags must have a name
            2. Tags must have a description
            3. Tags must have a TagGroup

        Properties:
            1. Tags must be unique

        Args:
            collect_errors:
                bool, default False, if True return a list of all the validation errors

        Returns:
           bool or Iterable[TORISchemeError]
        """
        valid = True
        # Check attributes
        for t in self.tags:
            if not t.name:
                self._raise_error('Tag missing name: {}'.format(t))
                valid = False

            if not t.description:
                self._raise_error('Tag missing description: {}'.format(t))
                valid = False

        # Check uniqueness
        dups = utilities.find_duplicates(self.tags)
        if dups:
            self._raise_error('Tags must be unique, found duplicates: {}'.format(dups), collect=collect_errors)
            valid = False

        return valid

    def validate_references(self, collect_errors: bool = False) -> bool:
        """Validate References according to the following criteria

        Attributes:
            1. References must have a title
            2. References must have at least one author

        Properties:
            1. References must be unique

        Args:
            collect_errors:
                bool, default False, if True return a list of all the validation errors

        Returns:
           bool or Iterable[TORISchemeError]
        """
        valid = True
        # Check attributes
        for r in self.references:
            if not r.title:
                self._raise_error('Reference missing title: {}'.format(r))
                valid = False

            if not r.author:
                self._raise_error('Reference missing author: {}'.format(r))
                valid = False

        # Check uniqueness
        dups = utilities.find_duplicates(self.references)
        if dups:
            self._raise_error('References must be unique, found duplicates: {}'.format(dups), collect=collect_errors)
            valid = False

        return valid
