"""
SkCode tag dictionary builder test code.
"""

import unittest

from skcode.etree import TreeNode
from skcode.tags import build_recognized_tags_dict


class UnamedTreeNode(TreeNode):
    """ Tree node class without canonical name """

    canonical_tag_name = ''


class DummyTreeNode(TreeNode):
    """ Dummy tree node class """

    canonical_tag_name = 'test'
    alias_tag_names = ('debug', )


class DummyNameTreeNode(TreeNode):
    """ Dummy tree node class """

    canonical_tag_name = 'test'
    alias_tag_names = ('debug2', )


class DummyAliasTreeNode(TreeNode):
    """ Dummy tree node class """

    canonical_tag_name = 'test2'
    alias_tag_names = ('debug', )


class TagsDictionaryBuilderTestCase(unittest.TestCase):
    """ Tests suite for the tag dictionary builder helper. """

    def test_build_recognized_tags_dict(self):
        """ Test if the ``build_recognized_tags_dict`` helper do it's job """
        known_tags = (
            DummyTreeNode,
        )
        known_tags = build_recognized_tags_dict(known_tags)
        self.assertEqual({
            'test': DummyTreeNode,
            'debug': DummyTreeNode,
        }, known_tags)

    def test_build_recognized_tags_dict_check_type(self):
        """ Test if the ``build_recognized_tags_dict`` check the type of the class """
        known_tags = (
            1,
        )
        with self.assertRaises(ValueError) as e:
            build_recognized_tags_dict(known_tags)
        self.assertEqual('int is an instance, not a class type', str(e.exception))

    def test_build_recognized_tags_dict_check_canonical_name_exist(self):
        """ Test if the ``build_recognized_tags_dict`` check the canonical name of the class """
        known_tags = (
            UnamedTreeNode,
        )
        with self.assertRaises(ValueError) as e:
            build_recognized_tags_dict(known_tags)
        self.assertEqual('UnamedTreeNode does not have a canonical name',  str(e.exception))

    def test_build_recognized_tags_dict_check_canonical_name_duplicate(self):
        """ Test if the ``build_recognized_tags_dict`` check the canonical name of the class """
        known_tags = (
            DummyTreeNode,
            DummyNameTreeNode,
        )
        with self.assertRaises(KeyError) as e:
            build_recognized_tags_dict(known_tags)
        self.assertEqual('\'Tag name "test" is already registered\'', str(e.exception))

    def test_build_recognized_tags_dict_check_alias_name_duplicate(self):
        """ Test if the ``build_recognized_tags_dict`` check the alias names of the class """
        known_tags = (
            DummyTreeNode,
            DummyAliasTreeNode,
        )
        with self.assertRaises(KeyError) as e:
            build_recognized_tags_dict(known_tags)
        self.assertEqual('\'Alias name "debug" is already registered\'', str(e.exception))
