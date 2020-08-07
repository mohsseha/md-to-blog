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
- create menu map with format:
{"blog": {"tag1":{},
            "tag2:{}...},
"Resouces": {"academic":...
...
}


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
from pathlib import Path
import markdown
import shlex
import datetime
import re
from pprint import pprint
import glob, os


MDFileData = namedtuple('MDFileData', ['date', 'raw_file', 'html', 'tags'])


def git_date(filename: str):
    from subprocess import Popen, PIPE
    result = datetime.datetime.now()  # default value
    try:
        cmd = f"""git log -1 --pretty="format:%ct" {filename}"""
        process = Popen(shlex.split(cmd), stdout=PIPE)
        res = process.communicate()
        # print(f"ran '{cmd}' and got={res}")
        unix_time = int(res[0])
        process.wait()
        result = datetime.datetime.fromtimestamp(unix_time)
    finally:
        return result


from typing import Tuple, Dict, Iterable


def md_to_html_converter(raw_file: str) -> Tuple[str, Dict]:
    '''
    :param raw_file: markdown
    :return: valid html
    '''
    md = markdown.Markdown(extensions=['meta'])
    return (md.convert(raw_file), md.Meta)


def load_file(filename) -> MDFileData:
    date = git_date(filename)
    raw_file = Path(filename).read_text(encoding='utf8')
    html, meta = md_to_html_converter(raw_file)
    tags = next((v for (k, v) in meta.items() if 'tag' in k.lower()), [])
    return MDFileData(date=date, raw_file=raw_file, html=html, tags=tags)


def load_md_files(src: str):
    return {file_name[len(src) + 1:]: load_file(file_name) for file_name in glob.glob(f"{src}/**/*md", recursive=True)}


title_pattern = re.compile(".*^\# *(.*)$.*", re.MULTILINE)
img_pattern = re.compile(".*^\!\[.*\]\((.*)\)$.*", re.MULTILINE)


def summarize_post(filename: str, post: MDFileData) -> str:
    '''
    takes a MD file and takes out the Title (pre-fixed with #) and the first image and return as md
    :param raw_file: markdown body of post
    :return: markdown snippet of that blog post
    '''
    date = post.date
    try:
        title = title_pattern.findall(post.raw_file)[0]
    except:
        title = "😢NO TITLE😢"
    try:
        img_url = img_pattern.findall(post.raw_file)[0]
    except:
        img_url = None
    assert date and title and filename, f"something is wrong with {filename} or {post}"
    return f"""{date}\n### {title}""" \
           + (f"""\n!(preview)[{img_url}]""" if img_url else "") \
           + f"""\n(Read More][{filename}]\n\n"""


def make_MD_index(blog_items) -> MDFileData:
    '''
    :param blog_items: that you need to create an index document for
    :return: index document sorted by dates
    '''
    sorted_posts = {k: v for (k, v) in sorted(blog_items.items(), key=lambda kv: kv[1].date, reverse=True)}
    raw_file = ""
    for post in (summarize_post(k, v) for (k, v) in sorted_posts.items()):
        raw_file = raw_file + post
    html, _ = md_to_html_converter(raw_file)
    return MDFileData(date=datetime.datetime.now(), raw_file=raw_file, html=html, tags=[])


def add_blog_index_files(url_md_map):
    '''
    method only cares about creating `blog/index.md` and 'blog/tagi/index.m'
    :param url_md_map: {"full_file_path: MDFileData(tags=[],...)
    :return: append to url_md_map the new files
    '''
    pattern = re.compile("^blog/.*")
    blog_items = {k: v for (k, v) in url_md_map.items() if pattern.match(k)}
    all_tags = {tag for i in blog_items.values() for tag in i.tags}

    url_md_map["blog/index.md"] = make_MD_index(blog_items)
    for tag in all_tags:
        tag_items = {k: v for (k, v) in blog_items.items() if tag in v.tags}
        url_md_map[f"blog/{tag}/index.md"] = make_MD_index(tag_items)
    return url_md_map



def find_menu_tree(url_md_map):
    '''
    find navigation menu data structure based on webpage
    :param url_md_map: map of all posts and pages index by url
    :return:
    {"blog": {"tag1":{},
            "tag2:{}...},
    "Resouces": {"academic":...
    ...
    }
    '''
    result = {}
    for url in url_md_map.keys():
        folder_li=url.split('/')[:-1]
        # now we insert into tree dict:
        pt=result # point to the current level of the map
        for l in folder_li:
            #going left to right inserting elements
            if l not in pt:
                pt[l]={}
            pt=pt[l]
    return result

def calc_blog_nav(blog_md_map:Dict[str,MDFileData])->Dict[str,str]:
    '''
    for blog pages *only* point to the next or previous blog post in time.
    returns aa dict from url to MD snippet of links
    '''

    nav_keys=[k for k in blog_md_map if re.findall(r"blog/[^/]+.md",k) and ("index.md" not in k)]
    nav_keys.sort(key=lambda k:blog_md_map[k].date)


def calc_non_blog_nav(other_md_map):
    pass




def _create_non_blog_index_docs(dir: str) -> Dict[str, MDFileData]:
    result = {}
    if 'blog' in dir:
        return result
    rel_sub_dirs = [x[len(dir) + 1:-1] for x in glob.glob(f"{dir}/**/")]
    if not os.path.exists(f"{dir}/index.md"):
        # need to create index file for this folder
        raw_file = ""
        for sub_dir in rel_sub_dirs:
            raw_file += f"# [{sub_dir}]({sub_dir})\n"
        for file in glob.glob(f"{dir}/*.md"):
            f=file[len(dir)+1:]
            raw_file += f"### [{f}]({f})"
        new_index = MDFileData(date=datetime.datetime.now(),
                               raw_file=raw_file,
                               html=md_to_html_converter(raw_file)[0],
                               tags=[])
        result.update({dir + "/index.md": new_index})
    for sub_dir in rel_sub_dirs:
        result.update(_create_non_blog_index_docs(dir + "/" + sub_dir))
    return result


def create_non_blog_index_docs(dir: str) -> Dict[str, MDFileData]:
    return {k[len(dir) + 1:]: v for (k, v) in _create_non_blog_index_docs(dir).items()}


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
    url_md_map.update(create_non_blog_index_docs(src))
    # at this stage there are no folders without index files

    menu_map = find_menu_tree(url_md_map)
    page_nav_links = calc_blog_nav({k: v for (k, v) in url_md_map.items() if k.startswith("blog")})
    page_nav_links.update(calc_non_blog_nav({k: v for (k, v) in url_md_map.items() if not k.startswith("blog")}))
    if debug:
        write_md_map(url_md_map, menu_map, page_nav_links)
    # now that we have the menu_map, the body and the navigation we can write the output blog:
    write_html_from_maps(target, theme, url_md_map, menu_map, page_nav_links)
    write_non_md_resoures(src, target)


def write_md_map(url_md_map, menu_map, nav) -> None:
    pass


def write_html_from_maps(target, theme, url_md_map, menu_map, nav) -> None:
    pass


def write_non_md_resoures(src, target) -> None:
    pass

# build_blog()
