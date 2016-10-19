"""
SkCode code block tag definitions test code.
"""

import unittest
from unittest import mock

from skcode.etree import RootTreeNode
from skcode.tags import (CodeBlockTreeNode,
                         DEFAULT_RECOGNIZED_TAGS_LIST,
                         generate_fixed_code_block_type_cls)
from skcode.utility.relative_urls import setup_relative_urls_conversion


class CodeBlockTreeNodeTestCase(unittest.TestCase):
    """ Tests suite for the code blocks tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn(CodeBlockTreeNode, DEFAULT_RECOGNIZED_TAGS_LIST)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        self.assertFalse(CodeBlockTreeNode.newline_closes)
        self.assertFalse(CodeBlockTreeNode.same_tag_closes)
        self.assertFalse(CodeBlockTreeNode.standalone)
        self.assertFalse(CodeBlockTreeNode.parse_embedded)
        self.assertFalse(CodeBlockTreeNode.inline)
        self.assertTrue(CodeBlockTreeNode.close_inlines)
        self.assertFalse(CodeBlockTreeNode.make_paragraphs_here)
        self.assertEqual('code', CodeBlockTreeNode.canonical_tag_name)
        self.assertEqual((), CodeBlockTreeNode.alias_tag_names)
        self.assertEqual(4, CodeBlockTreeNode.tab_size)
        self.assertEqual('default', CodeBlockTreeNode.pygments_css_style_name)
        self.assertTrue(CodeBlockTreeNode.display_line_numbers)
        self.assertEqual('text', CodeBlockTreeNode.default_language_name)
        self.assertEqual('language', CodeBlockTreeNode.language_attr_name)
        self.assertEqual('hl_lines', CodeBlockTreeNode.hl_lines_attr_name)
        self.assertEqual('linenostart', CodeBlockTreeNode.line_start_num_attr_name)
        self.assertEqual('filename', CodeBlockTreeNode.filename_attr_name)
        self.assertEqual('src', CodeBlockTreeNode.source_link_attr_name)
        self.assertEqual('id', CodeBlockTreeNode.figure_id_attr_name)
        self.assertEqual('codetable', CodeBlockTreeNode.wrapping_div_class_name)
        self.assertEqual("""<div class="{class_name}">
    {source_code}
</div>""", CodeBlockTreeNode.wrapping_div_html_template)
        self.assertEqual('Source : {}', CodeBlockTreeNode.source_caption_html_template)
        self.assertEqual('<a href="{src_link}"{extra_args} target="_blank">{caption} '
                         '<i class="fa fa-link" aria-hidden="true"></i></a>', CodeBlockTreeNode.source_link_html_template)
        self.assertEqual("""<div class="panel panel-default" id="{figure_id}">
    <div class="panel-body">
        {source_code}
    </div>
    <div class="panel-footer">
        {caption}
    </div>
</div>""", CodeBlockTreeNode.code_html_template)
        self.assertEqual('<a id="{figure_id}"></a>\n{source_code}', CodeBlockTreeNode.code_only_html_template)

    def test_get_language_name_with_tagname_set(self):
        """ Test the ``get_language_name`` method with the tag name attribute set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode, attrs={'code': 'test'})
        language_name = tree_node.get_language_name()
        self.assertEqual('test', language_name)

    def test_get_language_name_with_language_set(self):
        """ Test the ``get_language_name`` method with the "language" attribute set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode, attrs={'language': 'test'})
        language_name = tree_node.get_language_name()
        self.assertEqual('test', language_name)

    def test_get_language_name_with_tagname_and_language_set(self):
        """ Test the ``get_language_name`` method with the "language" and tag name attribute set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode, attrs={'code': 'test', 'language': 'test2'})
        language_name = tree_node.get_language_name()
        self.assertEqual('test', language_name)

    def test_get_language_name_without_language_set(self):
        """ Test the ``get_language_name`` method with the tag name set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode, attrs={})
        language_name = tree_node.get_language_name()
        self.assertEqual(tree_node.default_language_name, language_name)

    def test_get_language_name_with_html_entities(self):
        """ Test the ``get_language_name`` method with the tag name set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode, attrs={'code': '&lt;test&gt;'})
        language_name = tree_node.get_language_name()
        self.assertEqual('<test>', language_name)

    def test_get_highlight_lines(self):
        """ Test the ``get_highlight_lines`` method with some valid values. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode, attrs={'hl_lines': '1,2,3'})
        hl_lines = tree_node.get_highlight_lines()
        self.assertEqual(hl_lines, [1, 2, 3])

    def test_get_highlight_lines_without_lines(self):
        """ Test the ``get_highlight_lines`` method without any lines set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode, attrs={})
        hl_lines = tree_node.get_highlight_lines()
        self.assertEqual(hl_lines, [])

    def test_get_highlight_lines_with_non_number(self):
        """ Test the ``get_highlight_lines`` method with non number value set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode, attrs={'hl_lines': 'a,z,e,r,t,y'})
        hl_lines = tree_node.get_highlight_lines()
        self.assertEqual(hl_lines, [])

    def test_get_highlight_lines_with_erroneous_numbers(self):
        """ Test the ``get_highlight_lines`` method with erroneous number value set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode, attrs={'hl_lines': '1,z,2,r,3,y'})
        hl_lines = tree_node.get_highlight_lines()
        self.assertEqual(hl_lines, [1, 2, 3])

    def test_get_highlight_lines_with_blank(self):
        """ Test the ``get_highlight_lines`` method with non number value set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode, attrs={'hl_lines': '1,,2,,3,'})
        hl_lines = tree_node.get_highlight_lines()
        self.assertEqual(hl_lines, [1, 2, 3])

    def test_get_highlight_lines_with_whitespaces_around_numbers(self):
        """ Test the ``get_highlight_lines`` method with non number value set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode, attrs={'hl_lines': '  1 , 2  ,  3  '})
        hl_lines = tree_node.get_highlight_lines()
        self.assertEqual(hl_lines, [1, 2, 3])

    def test_get_highlight_lines_with_negative_numbers(self):
        """ Test the ``get_highlight_lines`` method with negative number value set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode, attrs={'hl_lines': '1,-1,2,-2,3,-3'})
        hl_lines = tree_node.get_highlight_lines()
        self.assertEqual(hl_lines, [1, 2, 3])

    def test_get_start_line_number(self):
        """ Test the ``get_start_line_number`` method with some valid value. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode, attrs={'linenostart': '3'})
        first_line_number = tree_node.get_start_line_number()
        self.assertEqual(first_line_number, 3)

    def test_get_start_line_number_without_value(self):
        """ Test the ``get_start_line_number`` method without value set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode, attrs={})
        first_line_number = tree_node.get_start_line_number()
        self.assertEqual(first_line_number, 1)

    def test_get_start_line_number_with_non_number(self):
        """ Test the ``get_start_line_number`` method with some valid value. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode, attrs={'linenostart': 'foobar'})
        first_line_number = tree_node.get_start_line_number()
        self.assertEqual(first_line_number, 1)

    def test_get_start_line_number_with_negative_value(self):
        """ Test the ``get_start_line_number`` method with some valid value. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode, attrs={'linenostart': '-3'})
        first_line_number = tree_node.get_start_line_number()
        self.assertEqual(first_line_number, 1)

    def test_get_filename(self):
        """ Test the ``get_filename`` method with the "filename" attribute set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode, attrs={'filename': 'test.py'})
        filename = tree_node.get_filename()
        self.assertEqual('test.py', filename)

    def test_get_filename_without_value(self):
        """ Test the ``get_filename`` method with the "filename" attribute not set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode, attrs={})
        filename = tree_node.get_filename()
        self.assertEqual('', filename)

    def test_get_filename_with_html_entities(self):
        """ Test the ``get_filename`` method with the "filename" attribute containing HTML entities. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode, attrs={'filename': '&lt;test&gt;.py'})
        filename = tree_node.get_filename()
        self.assertEqual('<test>.py', filename)

    def test_get_source_link_url(self):
        """ Test the ``get_source_link_url`` method with the "src" attribute set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode,
                                             attrs={'src': 'https://github.com/TamiaLab/PySkCode'})
        src_link_url = tree_node.get_source_link_url()
        self.assertEqual('https://github.com/TamiaLab/PySkCode', src_link_url)

    def test_get_source_link_url_sanitize(self):
        """ Test the ``get_source_link_url`` method call the ``sanitize_url`` function. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode,
                                             attrs={'src': 'https://github.com/TamiaLab/PySkCode'})
        with unittest.mock.patch('skcode.tags.codeblocks.sanitize_url') as mock_sanitize_url:
            tree_node.get_source_link_url()
        mock_sanitize_url.assert_called_once_with('https://github.com/TamiaLab/PySkCode',
                                                  absolute_base_url='')

    def test_get_source_link_url_sanitize_with_relative_url_conversion(self):
        """ Test the ``get_source_link_url`` method call the ``sanitize_url`` function. """
        root_tree_node = RootTreeNode()
        setup_relative_urls_conversion(root_tree_node, 'http://example.com/')
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode,
                                             attrs={'src': 'https://github.com/TamiaLab/PySkCode'})
        with unittest.mock.patch('skcode.tags.codeblocks.sanitize_url') as mock_sanitize_url:
            tree_node.get_source_link_url()
        mock_sanitize_url.assert_called_once_with('https://github.com/TamiaLab/PySkCode',
                                                  absolute_base_url='http://example.com/')

    def test_get_source_link_url_without_value(self):
        """ Test the ``get_source_link_url`` method with the "src" attribute not set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode, attrs={})
        src_link_url = tree_node.get_source_link_url()
        self.assertEqual('', src_link_url)

    def test_get_figure_id(self):
        """ Test the ``get_figure_id`` method with the "id" attribute set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode, attrs={'id': 'test'})
        figure_id = tree_node.get_figure_id()
        self.assertEqual('test', figure_id)

    def test_get_figure_id_slugify(self):
        """ Test the ``get_figure_id`` method call the ``slugify`` function. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode, attrs={'id': 'test'})
        with unittest.mock.patch('skcode.tags.codeblocks.slugify') as mock_slugify:
            tree_node.get_figure_id()
        mock_slugify.assert_called_once_with('test')

    def test_get_figure_id_without_value(self):
        """ Test the ``get_figure_id`` method with the "id" attribute not set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode, attrs={})
        figure_id = tree_node.get_figure_id()
        self.assertEqual('', figure_id)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode,
                                             attrs={'code': 'python'}, content='# Hello World!')
        output_result = tree_node.render_html('')
        expected_result = """<div class="codetable">
    <table class="highlighttable"><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%">1</pre></div></td><td class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><span style="color: #408080; font-style: italic"># Hello World!</span>
</pre></div>
</td></tr></table>
</div>"""
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_invalid_language(self):
        """ Test the ``render_html`` method with an invalid language set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode,
                                             attrs={'code': 'somethingnotexisting'}, content='# Hello World!')
        output_result = tree_node.render_html('')
        expected_result = """<div class="codetable">
    <table class="highlighttable"><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%">1</pre></div></td><td class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"># Hello World!
</pre></div>
</td></tr></table>
</div>"""
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_default_language(self):
        """ Test the ``render_html`` method with the default language set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode, attrs={}, content='# Hello World!')
        output_result = tree_node.render_html('')
        expected_result = """<div class="codetable">
    <table class="highlighttable"><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%">1</pre></div></td><td class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"># Hello World!
</pre></div>
</td></tr></table>
</div>"""
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_hl_lines(self):
        """ Test the ``render_html`` method with 'hl_lines" set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode,
                                             attrs={'code': 'python', 'hl_lines': '1'}, content='# Hello World!')
        output_result = tree_node.render_html('')
        expected_result = """<div class="codetable">
    <table class="highlighttable"><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%">1</pre></div></td><td class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><span style="background-color: #ffffcc"><span style="color: #408080; font-style: italic"># Hello World!</span>
</span></pre></div>
</td></tr></table>
</div>"""
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_linenostart(self):
        """ Test the ``render_html`` method with 'linenostart" set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode,
                                             attrs={'code': 'python', 'hl_lines': '1', 'linenostart': '5'},
                                             content='# Hello World!')
        output_result = tree_node.render_html('')
        expected_result = """<div class="codetable">
    <table class="highlighttable"><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%">5</pre></div></td><td class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><span style="background-color: #ffffcc"><span style="color: #408080; font-style: italic"># Hello World!</span>
</span></pre></div>
</td></tr></table>
</div>"""
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_src_filename(self):
        """ Test the ``render_html`` method with 'filename" set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode,
                                             attrs={'code': 'python', 'hl_lines': '1',
                                                    'linenostart': '5', 'filename': 'test.py'},
                                             content='# Hello World!')
        output_result = tree_node.render_html('')
        expected_result = """<div class="panel panel-default" id="">
    <div class="panel-body">
        <div class="codetable">
    <table class="highlighttable"><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%">5</pre></div></td><td class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><span style="background-color: #ffffcc"><span style="color: #408080; font-style: italic"># Hello World!</span>
</span></pre></div>
</td></tr></table>
</div>
    </div>
    <div class="panel-footer">
        Source : test.py
    </div>
</div>"""
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_src_filename_containing_html_entities(self):
        """ Test the ``render_html`` method with 'filename" set and containing HTML entities. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode,
                                             attrs={'code': 'python', 'hl_lines': '1',
                                                    'linenostart': '5', 'filename': '<test>.py'},
                                             content='# Hello World!')
        output_result = tree_node.render_html('')
        expected_result = """<div class="panel panel-default" id="">
    <div class="panel-body">
        <div class="codetable">
    <table class="highlighttable"><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%">5</pre></div></td><td class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><span style="background-color: #ffffcc"><span style="color: #408080; font-style: italic"># Hello World!</span>
</span></pre></div>
</td></tr></table>
</div>
    </div>
    <div class="panel-footer">
        Source : &lt;test&gt;.py
    </div>
</div>"""
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_src_link(self):
        """ Test the ``render_html`` method with 'src" set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode,
                                             attrs={'code': 'python', 'hl_lines': '1',
                                                    'linenostart': '5', 'filename': 'test.py',
                                                    'src': 'https://github.com/TamiaLab/PySkCode'},
                                             content='# Hello World!')
        output_result = tree_node.render_html('')
        expected_result = """<div class="panel panel-default" id="">
    <div class="panel-body">
        <div class="codetable">
    <table class="highlighttable"><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%">5</pre></div></td><td class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><span style="background-color: #ffffcc"><span style="color: #408080; font-style: italic"># Hello World!</span>
</span></pre></div>
</td></tr></table>
</div>
    </div>
    <div class="panel-footer">
        <a href="https://github.com/TamiaLab/PySkCode" rel="nofollow" target="_blank">Source : test.py <i class="fa fa-link" aria-hidden="true"></i></a>
    </div>
</div>"""
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_src_link_only(self):
        """ Test the ``render_html`` method with 'src" set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode,
                                             attrs={'code': 'python', 'hl_lines': '1',
                                                    'linenostart': '5',
                                                    'src': 'https://github.com/TamiaLab/PySkCode'},
                                             content='# Hello World!')
        output_result = tree_node.render_html('')
        expected_result = """<div class="panel panel-default" id="">
    <div class="panel-body">
        <div class="codetable">
    <table class="highlighttable"><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%">5</pre></div></td><td class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><span style="background-color: #ffffcc"><span style="color: #408080; font-style: italic"># Hello World!</span>
</span></pre></div>
</td></tr></table>
</div>
    </div>
    <div class="panel-footer">
        <a href="https://github.com/TamiaLab/PySkCode" rel="nofollow" target="_blank">Source : https://github.com/TamiaLab/PySkCode <i class="fa fa-link" aria-hidden="true"></i></a>
    </div>
</div>"""
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_src_link_without_force_nofollow(self):
        """ Test the ``render_html`` method with 'src" set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode,
                                             attrs={'code': 'python', 'hl_lines': '1',
                                                    'linenostart': '5', 'filename': 'test.py',
                                                    'src': 'https://github.com/TamiaLab/PySkCode'},
                                             content='# Hello World!')
        output_result = tree_node.render_html('', force_rel_nofollow=False)
        expected_result = """<div class="panel panel-default" id="">
    <div class="panel-body">
        <div class="codetable">
    <table class="highlighttable"><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%">5</pre></div></td><td class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><span style="background-color: #ffffcc"><span style="color: #408080; font-style: italic"># Hello World!</span>
</span></pre></div>
</td></tr></table>
</div>
    </div>
    <div class="panel-footer">
        <a href="https://github.com/TamiaLab/PySkCode" target="_blank">Source : test.py <i class="fa fa-link" aria-hidden="true"></i></a>
    </div>
</div>"""
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_figure_id(self):
        """ Test the ``render_html`` method with 'src" set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode,
                                             attrs={'code': 'python', 'hl_lines': '1',
                                                    'linenostart': '5', 'filename': 'test.py',
                                                    'src': 'https://github.com/TamiaLab/PySkCode',
                                                    'id': 'helloworld'},
                                             content='# Hello World!')
        output_result = tree_node.render_html('')
        expected_result = """<div class="panel panel-default" id="helloworld">
    <div class="panel-body">
        <div class="codetable">
    <table class="highlighttable"><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%"><a href="#helloworld-5">5</a></pre></div></td><td class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><a name="helloworld-5"></a><span style="background-color: #ffffcc"><span style="color: #408080; font-style: italic"># Hello World!</span>
</span></pre></div>
</td></tr></table>
</div>
    </div>
    <div class="panel-footer">
        <a href="https://github.com/TamiaLab/PySkCode" rel="nofollow" target="_blank">Source : test.py <i class="fa fa-link" aria-hidden="true"></i></a>
    </div>
</div>"""
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_only_figure_id(self):
        """ Test the ``render_html`` method with 'src" set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode,
                                             attrs={'code': 'python', 'hl_lines': '1',
                                                    'linenostart': '5',
                                                    'id': 'helloworld'},
                                             content='# Hello World!')
        output_result = tree_node.render_html('')
        expected_result = """<a id="helloworld"></a>\n<div class="codetable">
    <table class="highlighttable"><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%"><a href="#helloworld-5">5</a></pre></div></td><td class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><a name="helloworld-5"></a><span style="background-color: #ffffcc"><span style="color: #408080; font-style: italic"># Hello World!</span>
</span></pre></div>
</td></tr></table>
</div>"""
        self.assertEqual(expected_result, output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode, attrs={'code': 'python'}, content='# Hello World!')
        output_result = tree_node.render_text('')
        expected_result = '1.   # Hello World!\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_trailing_blank_lines(self):
        """ Test the ``render_text`` method with trailing blank lines. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode, attrs={'code': 'python'}, content='\n\n# Hello World!\n')
        output_result = tree_node.render_text('')
        expected_result = '1.   # Hello World!\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_default_language(self):
        """ Test the ``render_text`` method with the default language set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode, attrs={}, content='# Hello World!')
        output_result = tree_node.render_text('')
        expected_result = '1.   # Hello World!\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_hl_lines(self):
        """ Test the ``render_text`` method with 'hl_lines" set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode, attrs={'code': 'python', 'hl_lines': '1'},
                                             content='# Hello World!\n# Bonjour le monde !')
        output_result = tree_node.render_text('')
        expected_result = '1>   # Hello World!\n2.   # Bonjour le monde !\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_linenostart(self):
        """ Test the ``render_text`` method with 'linenostart" set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode,
                                             attrs={'code': 'python', 'hl_lines': '1',
                                                    'linenostart': '5'},
                                             content='# Hello World!')
        output_result = tree_node.render_text('')
        expected_result = '5.   # Hello World!\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_src_filename(self):
        """ Test the ``render_text`` method with 'filename" set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode,
                                             attrs={'code': 'python', 'hl_lines': '1',
                                                    'linenostart': '5', 'filename': 'test.py'},
                                             content='# Hello World!')
        output_result = tree_node.render_text('')
        expected_result = '5.   # Hello World!\nSource : test.py\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_src_filename_and_html_entities(self):
        """ Test the ``render_text`` method with 'filename" set containing HTML entities. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode,
                                             attrs={'code': 'python', 'hl_lines': '1',
                                                    'linenostart': '5', 'filename': '<test>.py'},
                                             content='# Hello World!')
        output_result = tree_node.render_text('')
        expected_result = '5.   # Hello World!\nSource : <test>.py\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_src_link(self):
        """ Test the ``render_text`` method with 'src" set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode,
                                             attrs={'code': 'python', 'hl_lines': '1',
                                                    'linenostart': '5', 'filename': 'test.py',
                                                    'src': 'https://github.com/TamiaLab/PySkCode'},
                                             content='# Hello World!')
        output_result = tree_node.render_text('')
        expected_result = '5.   # Hello World!\nSource : test.py (https://github.com/TamiaLab/PySkCode)\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_src_link_only(self):
        """ Test the ``render_text`` method with 'src" set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode,
                                             attrs={'code': 'python', 'hl_lines': '1',
                                                    'linenostart': '5',
                                                    'src': 'https://github.com/TamiaLab/PySkCode'},
                                             content='# Hello World!')
        output_result = tree_node.render_text('')
        expected_result = '5.   # Hello World!\nSource : https://github.com/TamiaLab/PySkCode\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_figure_id(self):
        """ Test the ``render_text`` method with 'src" set. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('code', CodeBlockTreeNode,
                                             attrs={'code': 'python', 'hl_lines': '1',
                                                    'linenostart': '5', 'filename': 'test.py',
                                                    'src': 'https://github.com/TamiaLab/PySkCode',
                                                    'id': 'helloworld'},
                                             content='# Hello World!')
        output_result = tree_node.render_text('')
        expected_result = '5.   # Hello World!\nSource : test.py (https://github.com/TamiaLab/PySkCode) [#helloworld]\n'
        self.assertEqual(expected_result, output_result)


class FixedCodeBlocksTagTestCase(unittest.TestCase):
    """ Tests suite for the fixed code blocks tag module. """

    def test_automatic_tag_name(self):
        """ Test the constructor with no custom tag name set. """
        opts = generate_fixed_code_block_type_cls('customtype')
        self.assertEqual('customtype', opts.language_name)
        self.assertEqual('customtype', opts.canonical_tag_name)
        self.assertEqual((), opts.alias_tag_names)

    def test_custom_tag_name(self):
        """ Test the constructor with a custom tag name set. """
        opts = generate_fixed_code_block_type_cls('customtype', canonical_tag_name='foobar')
        self.assertEqual('customtype', opts.language_name)
        self.assertEqual('foobar', opts.canonical_tag_name)
        self.assertEqual((), opts.alias_tag_names)

    def test_get_language_name_method(self):
        """ Test if the ``get_language_name`` return the value set at constructor. """
        root_tree_node = RootTreeNode()
        tree_node = root_tree_node.new_child('test', generate_fixed_code_block_type_cls('foobar'),
                                             attrs={}, content='# Hello World!')
        language_name = tree_node.get_language_name()
        self.assertEqual('foobar', language_name)
