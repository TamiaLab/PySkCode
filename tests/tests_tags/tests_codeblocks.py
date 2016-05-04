"""
SkCode code block tag definitions test code.
"""

import unittest
from unittest import mock

from skcode.etree import RootTreeNode
from skcode.tags import (RootTagOptions,
                         CodeBlockTagOptions,
                         FixedCodeBlockTagOptions,
                         DEFAULT_RECOGNIZED_TAGS)
from skcode.utility.relative_urls import setup_relative_urls_conversion


class CodeBlockTagOptionsTestCase(unittest.TestCase):
    """ Tests suite for the code blocks tag module. """

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('code', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['code'], CodeBlockTagOptions)

    def test_tag_constant_values(self):
        """ Test tag constants. """
        opts = CodeBlockTagOptions()
        self.assertFalse(opts.newline_closes)
        self.assertFalse(opts.same_tag_closes)
        self.assertFalse(opts.standalone)
        self.assertFalse(opts.parse_embedded)
        self.assertTrue(opts.swallow_trailing_newline)
        self.assertFalse(opts.inline)
        self.assertTrue(opts.close_inlines)
        self.assertFalse(opts.make_paragraphs_here)
        self.assertEqual('code', opts.canonical_tag_name)
        self.assertEqual((), opts.alias_tag_names)
        self.assertEqual(4, opts.tab_size)
        self.assertEqual('default', opts.pygments_css_style_name)
        self.assertTrue(opts.display_line_numbers)
        self.assertEqual('text', opts.default_language_name)
        self.assertEqual('language', opts.language_attr_name)
        self.assertEqual('hl_lines', opts.hl_lines_attr_name)
        self.assertEqual('linenostart', opts.line_start_num_attr_name)
        self.assertEqual('filename', opts.filename_attr_name)
        self.assertEqual('src', opts.source_link_attr_name)
        self.assertEqual('id', opts.figure_id_attr_name)
        self.assertEqual('codetable', opts.wrapping_div_class_name)

        self.assertEqual("""<div class="{class_name}">
    {source_code}
</div>""", opts.wrapping_div_html_template)
        self.assertEqual('Source : {}', opts.source_caption_html_template)
        self.assertEqual('<a href="{src_link}"{extra_args} target="_blank">{caption} '
                         '<i class="fa fa-link" aria-hidden="true"></i></a>', opts.source_link_html_template)
        self.assertEqual("""<div class="panel panel-default" id="{figure_id}">
    <div class="panel-body">
        {source_code}
    </div>
    <div class="panel-footer">
        {caption}
    </div>
</div>""", opts.code_html_template)
        self.assertEqual('<a id="{figure_id}"></a>\n{source_code}', opts.code_only_html_template)

    def test_get_language_name_with_tagname_set(self):
        """ Test the ``get_language_name`` method with the tag name attribute set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={'code': 'test'})
        language_name = opts.get_language_name(tree_node)
        self.assertEqual('test', language_name)

    def test_get_language_name_with_language_set(self):
        """ Test the ``get_language_name`` method with the "language" attribute set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={'language': 'test'})
        language_name = opts.get_language_name(tree_node)
        self.assertEqual('test', language_name)

    def test_get_language_name_with_tagname_and_language_set(self):
        """ Test the ``get_language_name`` method with the "language" and tag name attribute set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={'code': 'test', 'language': 'test2'})
        language_name = opts.get_language_name(tree_node)
        self.assertEqual('test', language_name)

    def test_get_language_name_without_language_set(self):
        """ Test the ``get_language_name`` method with the tag name set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={})
        language_name = opts.get_language_name(tree_node)
        self.assertEqual(opts.default_language_name, language_name)

    def test_get_language_name_with_html_entities(self):
        """ Test the ``get_language_name`` method with the tag name set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={'code': '&lt;test&gt;'})
        language_name = opts.get_language_name(tree_node)
        self.assertEqual('<test>', language_name)

    def test_get_highlight_lines(self):
        """ Test the ``get_highlight_lines`` method with some valid values. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={'hl_lines': '1,2,3'})
        hl_lines = opts.get_highlight_lines(tree_node)
        self.assertEqual(hl_lines, [1, 2, 3])

    def test_get_highlight_lines_without_lines(self):
        """ Test the ``get_highlight_lines`` method without any lines set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={})
        hl_lines = opts.get_highlight_lines(tree_node)
        self.assertEqual(hl_lines, [])

    def test_get_highlight_lines_with_non_number(self):
        """ Test the ``get_highlight_lines`` method with non number value set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={'hl_lines': 'a,z,e,r,t,y'})
        hl_lines = opts.get_highlight_lines(tree_node)
        self.assertEqual(hl_lines, [])

    def test_get_highlight_lines_with_erroneous_numbers(self):
        """ Test the ``get_highlight_lines`` method with erroneous number value set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={'hl_lines': '1,z,2,r,3,y'})
        hl_lines = opts.get_highlight_lines(tree_node)
        self.assertEqual(hl_lines, [1, 2, 3])

    def test_get_highlight_lines_with_blank(self):
        """ Test the ``get_highlight_lines`` method with non number value set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={'hl_lines': '1,,2,,3,'})
        hl_lines = opts.get_highlight_lines(tree_node)
        self.assertEqual(hl_lines, [1, 2, 3])

    def test_get_highlight_lines_with_whitespaces_around_numbers(self):
        """ Test the ``get_highlight_lines`` method with non number value set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={'hl_lines': '  1 , 2  ,  3  '})
        hl_lines = opts.get_highlight_lines(tree_node)
        self.assertEqual(hl_lines, [1, 2, 3])

    def test_get_highlight_lines_with_negative_numbers(self):
        """ Test the ``get_highlight_lines`` method with negative number value set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={'hl_lines': '1,-1,2,-2,3,-3'})
        hl_lines = opts.get_highlight_lines(tree_node)
        self.assertEqual(hl_lines, [1, 2, 3])

    def test_get_start_line_number(self):
        """ Test the ``get_start_line_number`` method with some valid value. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={'linenostart': '3'})
        first_line_number = opts.get_start_line_number(tree_node)
        self.assertEqual(first_line_number, 3)

    def test_get_start_line_number_without_value(self):
        """ Test the ``get_start_line_number`` method without value set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={})
        first_line_number = opts.get_start_line_number(tree_node)
        self.assertEqual(first_line_number, 1)

    def test_get_start_line_number_with_non_number(self):
        """ Test the ``get_start_line_number`` method with some valid value. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={'linenostart': 'foobar'})
        first_line_number = opts.get_start_line_number(tree_node)
        self.assertEqual(first_line_number, 1)

    def test_get_start_line_number_with_negative_value(self):
        """ Test the ``get_start_line_number`` method with some valid value. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={'linenostart': '-3'})
        first_line_number = opts.get_start_line_number(tree_node)
        self.assertEqual(first_line_number, 1)

    def test_get_filename(self):
        """ Test the ``get_filename`` method with the "filename" attribute set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={'filename': 'test.py'})
        filename = opts.get_filename(tree_node)
        self.assertEqual('test.py', filename)

    def test_get_filename_without_value(self):
        """ Test the ``get_filename`` method with the "filename" attribute not set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={})
        filename = opts.get_filename(tree_node)
        self.assertEqual('', filename)

    def test_get_filename_with_html_entities(self):
        """ Test the ``get_filename`` method with the "filename" attribute containing HTML entities. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={'filename': '&lt;test&gt;.py'})
        filename = opts.get_filename(tree_node)
        self.assertEqual('<test>.py', filename)

    def test_get_source_link_url(self):
        """ Test the ``get_source_link_url`` method with the "src" attribute set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={'src': 'https://github.com/TamiaLab/PySkCode'})
        src_link_url = opts.get_source_link_url(tree_node)
        self.assertEqual('https://github.com/TamiaLab/PySkCode', src_link_url)

    def test_get_source_link_url_sanitize(self):
        """ Test the ``get_source_link_url`` method call the ``sanitize_url`` function. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={'src': 'https://github.com/TamiaLab/PySkCode'})
        with unittest.mock.patch('skcode.tags.codeblocks.sanitize_url') as mock_sanitize_url:
            opts.get_source_link_url(tree_node)
        mock_sanitize_url.assert_called_once_with('https://github.com/TamiaLab/PySkCode',
                                                  absolute_base_url='')

    def test_get_source_link_url_sanitize_with_relative_url_conversion(self):
        """ Test the ``get_source_link_url`` method call the ``sanitize_url`` function. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        setup_relative_urls_conversion(root_tree_node, 'http://example.com/')
        tree_node = root_tree_node.new_child('code', opts, attrs={'src': 'https://github.com/TamiaLab/PySkCode'})
        with unittest.mock.patch('skcode.tags.codeblocks.sanitize_url') as mock_sanitize_url:
            opts.get_source_link_url(tree_node)
        mock_sanitize_url.assert_called_once_with('https://github.com/TamiaLab/PySkCode',
                                                  absolute_base_url='http://example.com/')

    def test_get_source_link_url_without_value(self):
        """ Test the ``get_source_link_url`` method with the "src" attribute not set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={})
        src_link_url = opts.get_source_link_url(tree_node)
        self.assertEqual('', src_link_url)

    def test_get_figure_id(self):
        """ Test the ``get_figure_id`` method with the "id" attribute set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={'id': 'test'})
        figure_id = opts.get_figure_id(tree_node)
        self.assertEqual('test', figure_id)

    def test_get_figure_id_slugify(self):
        """ Test the ``get_figure_id`` method call the ``slugify`` function. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={'id': 'test'})
        with unittest.mock.patch('skcode.tags.codeblocks.slugify') as mock_slugify:
            opts.get_figure_id(tree_node)
        mock_slugify.assert_called_once_with('test')

    def test_get_figure_id_without_value(self):
        """ Test the ``get_figure_id`` method with the "id" attribute not set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={})
        figure_id = opts.get_figure_id(tree_node)
        self.assertEqual('', figure_id)

    def test_render_html(self):
        """ Test the ``render_html`` method. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts,
                                             attrs={'code': 'python'}, content='# Hello World!')
        output_result = opts.render_html(tree_node, '')
        expected_result = """<div class="codetable">
    <table class="highlighttable"><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%">1</pre></div></td><td class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><span style="color: #408080; font-style: italic"># Hello World!</span>
</pre></div>
</td></tr></table>
</div>"""
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_invalid_language(self):
        """ Test the ``render_html`` method with an invalid language set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts,
                                             attrs={'code': 'somethingnotexisting'}, content='# Hello World!')
        output_result = opts.render_html(tree_node, '')
        expected_result = """<div class="codetable">
    <table class="highlighttable"><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%">1</pre></div></td><td class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"># Hello World!
</pre></div>
</td></tr></table>
</div>"""
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_default_language(self):
        """ Test the ``render_html`` method with the default language set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={}, content='# Hello World!')
        output_result = opts.render_html(tree_node, '')
        expected_result = """<div class="codetable">
    <table class="highlighttable"><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%">1</pre></div></td><td class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"># Hello World!
</pre></div>
</td></tr></table>
</div>"""
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_hl_lines(self):
        """ Test the ``render_html`` method with 'hl_lines" set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts,
                                             attrs={'code': 'python', 'hl_lines': '1'}, content='# Hello World!')
        output_result = opts.render_html(tree_node, '')
        expected_result = """<div class="codetable">
    <table class="highlighttable"><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%">1</pre></div></td><td class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><span style="background-color: #ffffcc"><span style="color: #408080; font-style: italic"># Hello World!</span>
</span></pre></div>
</td></tr></table>
</div>"""
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_linenostart(self):
        """ Test the ``render_html`` method with 'linenostart" set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts,
                                             attrs={'code': 'python', 'hl_lines': '1', 'linenostart': '5'},
                                             content='# Hello World!')
        output_result = opts.render_html(tree_node, '')
        expected_result = """<div class="codetable">
    <table class="highlighttable"><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%">5</pre></div></td><td class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><span style="background-color: #ffffcc"><span style="color: #408080; font-style: italic"># Hello World!</span>
</span></pre></div>
</td></tr></table>
</div>"""
        self.assertEqual(expected_result, output_result)

    def test_render_html_with_src_filename(self):
        """ Test the ``render_html`` method with 'filename" set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts,
                                             attrs={'code': 'python', 'hl_lines': '1',
                                                    'linenostart': '5', 'filename': 'test.py'},
                                             content='# Hello World!')
        output_result = opts.render_html(tree_node, '')
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
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts,
                                             attrs={'code': 'python', 'hl_lines': '1',
                                                    'linenostart': '5', 'filename': '<test>.py'},
                                             content='# Hello World!')
        output_result = opts.render_html(tree_node, '')
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
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts,
                                             attrs={'code': 'python', 'hl_lines': '1',
                                                    'linenostart': '5', 'filename': 'test.py',
                                                    'src': 'https://github.com/TamiaLab/PySkCode'},
                                             content='# Hello World!')
        output_result = opts.render_html(tree_node, '')
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
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts,
                                             attrs={'code': 'python', 'hl_lines': '1',
                                                    'linenostart': '5',
                                                    'src': 'https://github.com/TamiaLab/PySkCode'},
                                             content='# Hello World!')
        output_result = opts.render_html(tree_node, '')
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
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts,
                                             attrs={'code': 'python', 'hl_lines': '1',
                                                    'linenostart': '5', 'filename': 'test.py',
                                                    'src': 'https://github.com/TamiaLab/PySkCode'},
                                             content='# Hello World!')
        output_result = opts.render_html(tree_node, '', force_rel_nofollow=False)
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
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts,
                                             attrs={'code': 'python', 'hl_lines': '1',
                                                    'linenostart': '5', 'filename': 'test.py',
                                                    'src': 'https://github.com/TamiaLab/PySkCode',
                                                    'id': 'helloworld'},
                                             content='# Hello World!')
        output_result = opts.render_html(tree_node, '')
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
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts,
                                             attrs={'code': 'python', 'hl_lines': '1',
                                                    'linenostart': '5',
                                                    'id': 'helloworld'},
                                             content='# Hello World!')
        output_result = opts.render_html(tree_node, '')
        expected_result = """<a id="helloworld"></a>\n<div class="codetable">
    <table class="highlighttable"><tr><td><div class="linenodiv" style="background-color: #f0f0f0; padding-right: 10px"><pre style="line-height: 125%"><a href="#helloworld-5">5</a></pre></div></td><td class="code"><div class="highlight" style="background: #f8f8f8"><pre style="line-height: 125%"><a name="helloworld-5"></a><span style="background-color: #ffffcc"><span style="color: #408080; font-style: italic"># Hello World!</span>
</span></pre></div>
</td></tr></table>
</div>"""
        self.assertEqual(expected_result, output_result)

    def test_render_text(self):
        """ Test the ``render_text`` method. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={'code': 'python'}, content='# Hello World!')
        output_result = opts.render_text(tree_node, '')
        expected_result = '1.   # Hello World!\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_trailing_blank_lines(self):
        """ Test the ``render_text`` method with trailing blank lines. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={'code': 'python'}, content='\n\n# Hello World!\n')
        output_result = opts.render_text(tree_node, '')
        expected_result = '1.   # Hello World!\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_default_language(self):
        """ Test the ``render_text`` method with the default language set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={}, content='# Hello World!')
        output_result = opts.render_text(tree_node, '')
        expected_result = '1.   # Hello World!\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_hl_lines(self):
        """ Test the ``render_text`` method with 'hl_lines" set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={'code': 'python', 'hl_lines': '1'},
                                             content='# Hello World!\n# Bonjour le monde !')
        output_result = opts.render_text(tree_node, '')
        expected_result = '1>   # Hello World!\n2.   # Bonjour le monde !\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_linenostart(self):
        """ Test the ``render_text`` method with 'linenostart" set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts,
                                             attrs={'code': 'python', 'hl_lines': '1',
                                                    'linenostart': '5'},
                                             content='# Hello World!')
        output_result = opts.render_text(tree_node, '')
        expected_result = '5.   # Hello World!\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_src_filename(self):
        """ Test the ``render_text`` method with 'filename" set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts,
                                             attrs={'code': 'python', 'hl_lines': '1',
                                                    'linenostart': '5', 'filename': 'test.py'},
                                             content='# Hello World!')
        output_result = opts.render_text(tree_node, '')
        expected_result = '5.   # Hello World!\nSource : test.py\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_src_filename_and_html_entities(self):
        """ Test the ``render_text`` method with 'filename" set containing HTML entities. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts,
                                             attrs={'code': 'python', 'hl_lines': '1',
                                                    'linenostart': '5', 'filename': '<test>.py'},
                                             content='# Hello World!')
        output_result = opts.render_text(tree_node, '')
        expected_result = '5.   # Hello World!\nSource : <test>.py\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_src_link(self):
        """ Test the ``render_text`` method with 'src" set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts,
                                             attrs={'code': 'python', 'hl_lines': '1',
                                                    'linenostart': '5', 'filename': 'test.py',
                                                    'src': 'https://github.com/TamiaLab/PySkCode'},
                                             content='# Hello World!')
        output_result = opts.render_text(tree_node, '')
        expected_result = '5.   # Hello World!\nSource : test.py (https://github.com/TamiaLab/PySkCode)\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_src_link_only(self):
        """ Test the ``render_text`` method with 'src" set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts,
                                             attrs={'code': 'python', 'hl_lines': '1',
                                                    'linenostart': '5',
                                                    'src': 'https://github.com/TamiaLab/PySkCode'},
                                             content='# Hello World!')
        output_result = opts.render_text(tree_node, '')
        expected_result = '5.   # Hello World!\nSource : https://github.com/TamiaLab/PySkCode\n'
        self.assertEqual(expected_result, output_result)

    def test_render_text_with_figure_id(self):
        """ Test the ``render_text`` method with 'src" set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts,
                                             attrs={'code': 'python', 'hl_lines': '1',
                                                    'linenostart': '5', 'filename': 'test.py',
                                                    'src': 'https://github.com/TamiaLab/PySkCode',
                                                    'id': 'helloworld'},
                                             content='# Hello World!')
        output_result = opts.render_text(tree_node, '')
        expected_result = '5.   # Hello World!\nSource : test.py (https://github.com/TamiaLab/PySkCode) [#helloworld]\n'
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_attributes(self):
        """ Test the ``get_skcode_attributes`` method. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={'code': 'python'}, content='# Hello World!')
        output_result = opts.get_skcode_attributes(tree_node, '')
        expected_result = ({
                               'language': 'python',
                               'hl_lines': '',
                               'linenostart': '',
                               'filename': '',
                               'src': '',
                               'id': '',
                           }, 'language')
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_attributes_with_default_language(self):
        """ Test the ``get_skcode_attributes`` method with the default language set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={}, content='# Hello World!')
        output_result = opts.get_skcode_attributes(tree_node, '')
        expected_result = ({
                               'language': '',
                               'hl_lines': '',
                               'linenostart': '',
                               'filename': '',
                               'src': '',
                               'id': '',
                           }, 'language')
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_attributes_with_hl_lines(self):
        """ Test the ``get_skcode_attributes`` method with 'hl_lines" set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={'code': 'python', 'hl_lines': '1'},
                                             content='# Hello World!')
        output_result = opts.get_skcode_attributes(tree_node, '')
        expected_result = ({
                               'language': 'python',
                               'hl_lines': '1',
                               'linenostart': '',
                               'filename': '',
                               'src': '',
                               'id': '',
                           }, 'language')
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_attributes_with_linenostart(self):
        """ Test the ``get_skcode_attributes`` method with 'linenostart" set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={'code': 'python', 'hl_lines': '1',
                                                                  'linenostart': '5'},
                                             content='# Hello World!')
        output_result = opts.get_skcode_attributes(tree_node, '')
        expected_result = ({
                               'language': 'python',
                               'hl_lines': '1',
                               'linenostart': '5',
                               'filename': '',
                               'src': '',
                               'id': '',
                           }, 'language')
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_attributes_with_linenostart_default(self):
        """ Test the ``get_skcode_attributes`` method with 'linenostart" set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={'code': 'python', 'hl_lines': '1',
                                                                  'linenostart': '1'},
                                             content='# Hello World!')
        output_result = opts.get_skcode_attributes(tree_node, '')
        expected_result = ({
                               'language': 'python',
                               'hl_lines': '1',
                               'linenostart': '',
                               'filename': '',
                               'src': '',
                               'id': '',
                           }, 'language')
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_attributes_with_src_filename(self):
        """ Test the ``get_skcode_attributes`` method with 'filename" set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={'code': 'python', 'hl_lines': '1',
                                                                  'linenostart': '5', 'filename': 'test.py'},
                                             content='# Hello World!')
        output_result = opts.get_skcode_attributes(tree_node, '')
        expected_result = ({
                               'language': 'python',
                               'hl_lines': '1',
                               'linenostart': '5',
                               'filename': 'test.py',
                               'src': '',
                               'id': '',
                           }, 'language')
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_attributes_with_src_filename_html_entities(self):
        """ Test the ``get_skcode_attributes`` method with 'filename" set and containing html entities. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={'code': 'python', 'hl_lines': '1',
                                                                  'linenostart': '5', 'filename': '<test>.py'},
                                             content='# Hello World!')
        output_result = opts.get_skcode_attributes(tree_node, '')
        expected_result = ({
                               'language': 'python',
                               'hl_lines': '1',
                               'linenostart': '5',
                               'filename': '<test>.py',
                               'src': '',
                               'id': '',
                           }, 'language')
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_attributes_with_src_link(self):
        """ Test the ``get_skcode_attributes`` method with 'src" set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={'code': 'python', 'hl_lines': '1',
                                                                  'linenostart': '5', 'filename': 'test.py',
                                                                  'src': 'https://github.com/TamiaLab/PySkCode'},
                                             content='# Hello World!')
        output_result = opts.get_skcode_attributes(tree_node, '')
        expected_result = ({
                               'language': 'python',
                               'hl_lines': '1',
                               'linenostart': '5',
                               'filename': 'test.py',
                               'src': 'https://github.com/TamiaLab/PySkCode',
                               'id': '',
                           }, 'language')
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_attributes_with_figure_id(self):
        """ Test the ``get_skcode_attributes`` method with 'src" set. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={'code': 'python', 'hl_lines': '1',
                                                                  'linenostart': '5', 'filename': 'test.py',
                                                                  'src': 'https://github.com/TamiaLab/PySkCode',
                                                                  'id': 'helloworld'},
                                             content='# Hello World!')
        output_result = opts.get_skcode_attributes(tree_node, '')
        expected_result = ({
                               'language': 'python',
                               'hl_lines': '1',
                               'linenostart': '5',
                               'filename': 'test.py',
                               'src': 'https://github.com/TamiaLab/PySkCode',
                               'id': 'helloworld',
                           }, 'language')
        self.assertEqual(expected_result, output_result)

    def test_get_skcode_inner_content(self):
        """ Test the ``get_skcode_inner_content`` method. """
        opts = CodeBlockTagOptions()
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('code', opts, attrs={}, content='# Hello World!')
        output_result = opts.get_skcode_inner_content(tree_node, '')
        expected_result = '# Hello World!'
        self.assertEqual(expected_result, output_result)


class FixedCodeBlocksTagTestCase(unittest.TestCase):
    """ Tests suite for the fixed code blocks tag module. """

    def test_constructor_assertions(self):
        """
        Test assertions at ``__init__``.
        """
        with self.assertRaises(AssertionError) as e:
            FixedCodeBlockTagOptions(None)
        self.assertEqual('The language name is mandatory.', str(e.exception))

    def test_tag_and_aliases_in_default_recognized_tags_dict(self):
        """ Test the presence of the tag and aliases in the dictionary of default recognized tags. """
        self.assertIn('python', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['python'], FixedCodeBlockTagOptions)
        self.assertEqual('python', DEFAULT_RECOGNIZED_TAGS['python'].language_name)
        self.assertIn('cpp', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['cpp'], FixedCodeBlockTagOptions)
        self.assertEqual('cpp', DEFAULT_RECOGNIZED_TAGS['cpp'].language_name)
        self.assertIn('java', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['java'], FixedCodeBlockTagOptions)
        self.assertEqual('java', DEFAULT_RECOGNIZED_TAGS['java'].language_name)
        self.assertIn('html', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['html'], FixedCodeBlockTagOptions)
        self.assertEqual('html', DEFAULT_RECOGNIZED_TAGS['html'].language_name)
        self.assertIn('php', DEFAULT_RECOGNIZED_TAGS)
        self.assertIsInstance(DEFAULT_RECOGNIZED_TAGS['php'], FixedCodeBlockTagOptions)
        self.assertEqual('php', DEFAULT_RECOGNIZED_TAGS['php'].language_name)

    def test_automatic_tag_name(self):
        """ Test the constructor with no custom tag name set. """
        opts = FixedCodeBlockTagOptions('customtype')
        self.assertEqual('customtype', opts.language_name)
        self.assertEqual('customtype', opts.canonical_tag_name)
        self.assertEqual((), opts.alias_tag_names)

    def test_custom_tag_name(self):
        """ Test the constructor with a custom tag name set. """
        opts = FixedCodeBlockTagOptions('customtype', canonical_tag_name='foobar')
        self.assertEqual('customtype', opts.language_name)
        self.assertEqual('foobar', opts.canonical_tag_name)
        self.assertEqual((), opts.alias_tag_names)

    def test_get_language_name_method(self):
        """ Test if the ``get_language_name`` return the value set at constructor. """
        opts = FixedCodeBlockTagOptions('foobar')
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts, attrs={}, content='# Hello World!')
        language_name = opts.get_language_name(tree_node)
        self.assertEqual('foobar', language_name)

    def test_get_skcode_attributes(self):
        """ Test the ``get_skcode_attributes`` method. """
        opts = FixedCodeBlockTagOptions('foobar')
        root_tree_node = RootTreeNode(RootTagOptions())
        tree_node = root_tree_node.new_child('test', opts, attrs={}, content='# Hello World!')
        output_result = opts.get_skcode_attributes(tree_node, '')
        expected_result = ({
                               'hl_lines': '',
                               'linenostart': '',
                               'filename': '',
                               'src': '',
                               'id': '',
                           }, None)
        self.assertEqual(expected_result, output_result)
