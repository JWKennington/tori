"""Parsing utilities for reading and writing PyTORI schemed files

"""
import pathlib
from typing import Union, Iterable, List

import toml
import yaml

from pytori import elements
from pytori.elements import TORI, TagGroup, Tag, Reference


class TORIParseError(ValueError):
    """TORI Parse Error"""


class TORIDictKeys:
    """Enumeration of standard TORI dict keys"""
    TagGroups = 'tag_groups'
    Tags = 'tags'
    References = 'references'


def load_dict(tori_dict: dict) -> TORI:
    """Load TORI

    Args:
        tori_dict:
            dict containing a *complete* TORI specification

    Returns:
        TORI
    """
    errors = []
    key_map = {k.lower(): k for k in tori_dict.keys()}

    # Check that the given dict is a complete TORI scheme
    for k in [TORIDictKeys.TagGroups, TORIDictKeys.Tags, TORIDictKeys.References]:
        if k not in key_map:
            raise TORIParseError('Dict missing top-level key: {}'.format(k))

    tag_group_dicts = tori_dict[key_map[TORIDictKeys.TagGroups]]
    tag_dicts = tori_dict[key_map[TORIDictKeys.Tags]]
    reference_dicts = tori_dict[key_map[TORIDictKeys.References]]

    # Check all items passed are lists
    for name, l in zip(('Tag Groups', 'Tags', 'References'), (tag_group_dicts, tag_dicts, reference_dicts)):
        if not isinstance(l, list):
            raise TORIParseError('{} must be passed as a list, not type: {}'.format(name, type(tag_group_dicts)))

        # Check all list elements are dicts
        for element in l:
            if not isinstance(element, dict):
                raise TORIParseError('{} element must be passed as a dict, not type: {}. Object given: {}'.format(name, type(element), element))

    # Build Tag Group elements first
    tag_groups = [elements.DEFAULT_TAG_GROUP]
    for tag_group_dict in tag_group_dicts:
        for key in elements.TagGroup.__slots__:
            if key not in tag_group_dict:
                raise TORIParseError('TagGroup dict missing key: {}'.format(key))
        tag_group = elements.TagGroup(**{slot: tag_group_dict[slot] for slot in elements.TagGroup.__slots__})
        tag_groups.append(tag_group)
    tag_group_map = {getattr(tag_group, elements.TagGroup.__key_attr__): tag_group for tag_group in tag_groups}

    # Build Tag elements
    tags = []
    for tag_dict in tag_dicts:
        for key in elements.Tag.__slots__:
            if key not in tag_dict:
                raise TORIParseError('Tag dict missing key: {}'.format(key))

        # Check Tag Group exists
        tag_group = tag_dict['group']
        if tag_group not in tag_group_map:
            raise TORIParseError('Tag {} has undefined group {}'.format(tag_dict['name'], tag_group))

        tag_dict = {slot: tag_dict[slot] for slot in elements.Tag.__slots__}  # Remove extra kwargs
        tag_dict.update(group=tag_group_map[tag_group])
        tag = elements.Tag(**tag_dict)
        tags.append(tag)
    tag_map = {getattr(tag, elements.Tag.__key_attr__): tag for tag in tags}

    # Build Reference elements
    references = []
    for reference_dict in reference_dicts:
        for key in elements.Reference.__required_slots__:
            if key not in reference_dict:
                raise TORIParseError('Reference dict missing required key: {}'.format(key))

        # Check Tags exists
        reference_tags = []
        raw_tags = reference_dict['tags']
        for raw_tag in raw_tags:
            if raw_tag not in tag_map:
                raise TORIParseError('Reference {} has undefined tag {}'.format(reference_dict['title'], raw_tag))
            reference_tags.append(tag_map[raw_tag])

        reference_dict = {slot: reference_dict[slot] for slot in elements.Reference.__slots__}  # Remove extra kwargs
        reference_dict.update(tags=reference_tags)
        reference = elements.Reference(**reference_dict)
        references.append(reference)

    # Construct TORI Scheme
    return elements.TORI(tag_groups=tag_groups,
                         tags=tags,
                         references=references)


def load_yaml(files: Union[Union[str, pathlib.Path], List[Union[str, pathlib.Path]]]) -> TORI:
    """Load yaml into a TORI scheme

    Args:
        files:
            Path or Paths, the file or files that contain TORI scheme data.

    Returns:
        TORI
    """
    if not isinstance(files, list):
        files = [files]

    files = [pathlib.Path(file) if not isinstance(file, pathlib.Path) else file for file in files]

    yaml_dict = {}
    for file in files:
        with open(file.as_posix(), 'r') as fid:
            file_res = yaml.safe_load(fid.read())
        yaml_dict.update(file_res)

    return load_dict(yaml_dict)


def load_toml(files: Union[Union[str, pathlib.Path], List[Union[str, pathlib.Path]]]) -> TORI:
    """Load toml into a TORI scheme

    Args:
        files:
            Path or Paths, the file or files that contain TORI scheme data.

    Returns:
        TORI
    """
    if not isinstance(files, list):
        files = [files]

    files = [pathlib.Path(file) if not isinstance(file, pathlib.Path) else file for file in files]

    toml_dict = {}
    for file in files:
        with open(file.as_posix(), 'r') as fid:
            file_res = toml.loads(fid.read())
        toml_dict.update(file_res)

    return load_dict(toml_dict)
