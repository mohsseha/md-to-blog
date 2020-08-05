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
import shlex
import datetime
import re

MDFileData = namedtuple('MDFileData', ['date', 'raw_file', 'html', 'tags'])


def git_date(filename: str):
    from subprocess import Popen, PIPE

    cmd = f"""git log -1 --pretty="format:%ct" {filename}"""
    process = Popen(shlex.split(cmd), stdout=PIPE)
    unix_time = int(process.communicate()[0])
    exit_code = process.wait()
    assert not exit_code, "git command failed"
    return datetime.datetime.fromtimestamp(unix_time)


def md_to_html_converter(raw_file:str)->str:
    '''
    :param raw_file: markdown
    :return: valid html
    '''
    md = markdown.Markdown(extensions=['meta'])
    return md.convert(raw_file)


def load_file(filename) -> MDFileData:
    date = git_date(filename)
    raw_file = Path(filename).read_text(encoding='utf8')
    html = md_to_html_converter(raw_file)
    tags = next((v for (k, v) in md.Meta.items() if 'tag' in k.lower()), [])
    return MDFileData(date=date, raw_file=raw_file, html=html, tags=tags)


def load_md_files(src: str):
    return {file_name[len(src) + 1:]: load_file(file_name) for file_name in glob.glob(f"{src}/**/*md", recursive=True)}


title_pattern = re.compile(".*^\# *(.*)$.*", re.MULTILINE)
img_pattern = re.compile(".*^\!\[.*\]\((.*)\)$.*", re.MULTILINE)


def summarize_post(filename: str, file: MDFileData) -> str:
    '''
    takes a MD file and takes out the Title (pre-fixed with #) and the first image and return as md
    :param raw_file: markdown body of post
    :return: markdown snippet of that blog post
    '''
    date = file.date
    try:
        title = title_pattern.findall(file.raw_file)[0]
    except:
        title = None
    try:
        img_url = img_pattern.findall(file.raw_file)[0]
    except:
        img_url = None
    assert date and title and filename, f"something is wrong with {filename} or {file}"
    return f"""{date}\n### {title}""" \
           + (f"""\n!(preview)[{img_url}]""" if img_url else "") \
           + f"""\n(Read More][{filename}]\n\n"""


def make_MD_index(blog_items) -> MDFileData:
    '''
    :param blog_items: that you need to create an index document for
    :return: index document sorted by dates
    '''
    sorted_itmes = {k: v for (k, v) in sorted(blog_items.items(), key=lambda kv: kv[1].date, reverse=True)}
    raw_file = ""
    for post in (summarize_post(k,v) for (k,v) in sorted_itmes):
        raw_file=raw_file+post
    html = md_to_html_converter(raw_file)
    return MDFileData(date=datetime.datetime.now(),raw_file=raw_file,html=html,tags=[])


def add_blog_index_files(url_md_map):
    '''
    method only cares about creating `blog/index.md` and 'blog/tagi/index.m'
    :param url_md_map: {"full_file_path: MDFileData(tags=[],...)
    :return: append to url_md_map the new files
    '''
    pattern = re.compile("^blog/.*")
    blog_items = {k: v for (k, v) in url_md_map.items() if pattern.match(k)}
    all_tags = {tag for i in blog_items.values() for tag in i.tags}

    url_md_map["blog/index.md"]=make_MD_index(blog_items)
    for tag in all_tags:
        tag_items={k:v for (k,v) in blog_items.items() if tag in v.tags}
        url_md_map[f"blog/{tag}/index.md"]=make_MD_index(tag_items)
    return url_md_map


def find_menu_tree(url_md_map):
    pass


def calc_blog_nav(map):
    pass


def calc_non_blog_nav(param):
    pass


def build_blog(src='in', target='out', theme='theme', debug=None) -> None:
    '''
    :param src: in folder
    :param target: output
    :param theme: theme
    :param debug: folder_name to write the md intermediate values
    :return:
    '''

    url_md_map = load_md_files(src)
    url_md_map = add_blog_index_files(url_md_map)
    menu_map = find_menu_tree(url_md_map)
    nav = calc_blog_nav({k: v for (k, v) in url_md_map.items() if k.startswith("blog")})
    nav.update(calc_non_blog_nav({k: v for (k, v) in url_md_map.items() if not k.startswith("blog")}))
    if debug:
        write_md_map(url_md_map, menu_map, nav)
    # now that we have the menu_map, the body and the navigation we can write the output blog:
    write_html_from_maps(target, theme, url_md_map, menu_map, nav)
    write_non_md_resoures(src, target)


def write_md_map(url_md_map, menu_map, nav) -> None:
    pass


def write_html_from_maps(target, theme, url_md_map, menu_map, nav) -> None:
    pass


def write_non_md_resoures(src, target) -> None:
    pass
