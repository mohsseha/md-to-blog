"""
this script moves md files in `in` to a ready-to-deploy webpage in `out` 
themes are composed from the `themes` folder by default

## SPECIFICATION:
at the end we have to have for each page 3 things:
- navigation menu (which is an html list)
    - if there is an `index.md` file in a folder it will be linked to by the title.
    - this only goes 2 levels deep. In other words:
        - `out/menu1/submenu` works but a 3rd level is ignored from the menu.
    - an index.html in the `blog` section is automatically created with:
        - Title, date, image,
    - blog menu item has as sub-items the tags:
        - each one of them returns a view that is the same as the main blog.
        - the out folder will look like:
            `out/blog/index.html` <- all blog posts
            `out/blog/tagi/index.html` <- link to blog posts that are of type tag1
- html body of the page
- section specific navigation. Specifically:
    - for blog section it next and before
    - for regular pages it's the up and down of tree of that page

## IMPLEMENTATION:
- we need a url_md_map (everything is a relative url):
    {
    "url1": (date,"markdown text",tags=[])
    "url2": (date,"md text",tags[])
    }
- add `index.md` pages to `blog` and `blog/tag1`, `blog/tag2` ... `blog/tagn`
- create menu map:
    {blog: {tag1:{},tag2:{},tag3:{}],
    About: {},
    Presentations-n-code: {},
    Resources: {Academic: {},
                Interview-Prep: {}
                ML-Papers: {}}





blog/posts                                  |Blog -> index
*autogend*                                  |    tag1 -> index
*autogend*                                  |    tag2 -> index
resouces/                                   |Resources -> None
resouces/mlIntro/index                      |    ML Intro -> index
resources/Academic/index                    |    Academic -> academic
Presentations-n-Code/index                  |Presentations and Code -> index

- convert the menu map to html:
    <li><a href="folder_i/index.html">folder_i</a></li>

    <ul>
        <li><a href="blog/index.html"> Blog</a></li>
        <ul>
            <li><a href=blog/tag1.html">Tag1</a></li>
            ....
        </ul>
        <li><a href="About/index.html">About</a></li>
        <li><a href="">Resources</a></li>
        <ul>
            ...
        </ul>
    </ul>

- then we convert it to a url-body-map (html body)

"""

from collections import namedtuple
import glob
from pathlib import Path
import markdown
MDFileData = namedtuple('MDFileData', ['date', 'raw_file', 'html', 'tags'])




def load_md_files(src:str):
    def load(filename)->MDFileData:
        date=git_date(filename)
        raw_file=Path(filename).read_text(encoding='utf8')
        md = markdown.Markdown(extensions=['meta'])
        html = md.convert(raw_file)
        tags=next((v for (k,v) in md.Meta.items() if 'tag' in k.lower()))
        return MDFileData(date=date,raw_file=raw_file,html=html,tags=tags)

    return {file_name,load(file_name) for file_name in glob.glob('in/**/*md',recursive=True) }


def add_blog_index_files(url_md_map):
    pass


def build_blog(src='in',target='out',theme='theme',debug=None)->None:
    '''
    :param src: in folder
    :param target: output
    :param theme: theme
    :param debug: folder_name to write the md intermediate values
    :return:
    '''

    url_md_map = load_md_files( src)
    url_md_map = add_blog_index_files(url_md_map)
    menu_map = find_menu_tree(url_md_map)
    nav = calc_blog_nav({k: v for (k, v) in url_md_map.items() if k.startswith("blog")}})
    nav.update(calc_non_blog_nav({k: v for (k, v) in url_md_map.items() if not k.startswith("blog")}}))
    if debug:
        write_md_map(url_md_map, menu_map, nav)
    # now that we have the menu_map, the body and the navigation we can write the output blog:
    write_html_from_maps(target,theme, url_md_map, menu_map, nav)
    write_non_md_resoures(src, target)

