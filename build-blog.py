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
- we need a url-md-map (everything is a relative url):
    {
    "url1": (date,"markdown text",tags=[])
    "url2": (date,"md text",tags[])
    }
- add `index.md` pages to `blog` and `blog/tag1`, `blog/tag2` ... `blog/tagn`
- create menu map:
    {("blog":"blog/index") : {("tag1","tag1/index")




blog/posts                                  |Blog -> index
*autogend*                                  |    tag1 -> index
*autogend*                                  |    tag2 -> index
resouces/                                   |Resources -> None
resouces/mlIntro/index                      |    ML Intro -> index
                                            |    Academic -> academic
                                            |Presentations and Code -> index
                      |    Python -> index
                      |    General -> None
                      |        Cats-> Cat

- convert the menu map to html:
    <ul>
    <li>Blog

    </ul>

- then we convert it to a url-body-map (html body)




"""

def build_blog(src='in',target='out',theme='theme'):
    '''
    :param src:
    :param target:
    :param theme:
    :return:
    '''