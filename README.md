# ServiceTree

Purpose: To be able to build (somewhat interactive) service trees, without imposing on current database structure

Example:
:::image type="content" source="data/example.png" alt-text="Example image":::

The services have different colors depending on their type. Current supported types:

* Farm - 2+ servers are delivering the service
* AAcluster - 2 servers are delivering the service in an active/active configuration
* APcluster - 2 servers are delivering the service in an active/passive configuration
* Others - undefined, usually for stand-alone services

## Table of Contents

* [How To](#how-to)
* [Install guide](#install-guide)
* [Important links](#important-links)

## How to

There are two main elements.

1. ServiceTree with other classes as data structures and logic
1. GraphBuilder for drawing the service trees including graphical logic

The last element is "scratch.py" that I use for calling and testing logic as is. It simply loads data/datastructure.json

*[Table of Contents](#table-of-contents)*

## Install guide

Make sure you install both python 3.x (preferably current version) and graphviz (preferably current version)

[Graphviz](https://graphviz.gitlab.io/_pages/Download/Download_windows.html)

And that you are having the path to the bin directory in your PATH variable. After that, you should get something
like this after typing "dot -V"

    PS C:\Users\kim> dot -v
    dot - graphviz version 2.38.0 (20140413.2041)
    libdir = "c:\program files (x86)\graphviz2.38\bin"
    Activated plugin library: gvplugin_dot_layout.dll
    Using layout: dot:dot_layout
    Activated plugin library: gvplugin_core.dll
    Using render: dot:core
    Using device: dot:dot:core
    The plugin configuration file:
            c:\program files (x86)\graphviz2.38\bin\config6
                    was successfully loaded.
        render      :  cairo dot fig gd gdiplus map pic pov ps svg tk vml vrml xdot
        layout      :  circo dot fdp neato nop nop1 nop2 osage patchwork sfdp twopi
        textlayout  :  textlayout
        device      :  bmp canon cmap cmapx cmapx_np dot emf emfplus eps fig gd gd2 gif gv imap imap_np ismap jpe jpeg jpg metafile pdf pic plain plain-ext png pov ps ps2 svg svgz tif tiff tk vml vmlz vrml wbmp xdot xdot1.2 xdot1.4
        loadimage   :  (lib) bmp eps gd gd2 gif jpe jpeg jpg png ps svg

To create and activate a virtual environment:

    python -m venv venv
    venv/Scripts/activate

And to install required packages:

    pip install -r requirements.txt

And you should now be able to run the simple scratch test

    python scratch.py

Or even better the full version

    python run.py --file=data/datastructure.json --output=output/example.gv

Enjoy!

*[Table of Contents](#table-of-contents)*

## Important links

Graphviz resources:

* Shapes - <https://www.graphviz.org/doc/info/shapes.html#html>
* Attributes - <http://www.graphviz.org/doc/info/attrs.html#d:URL>
* SO HTML record - <https://stackoverflow.com/questions/17765301/graphviz-dot-how-to-change-the-colour-of-one-record-in-multi-record-shape>
* Color schemes - <https://www.graphviz.org/doc/info/colors.html>
* Manual - <https://graphviz.readthedocs.io/en/stable/manual.html>

*[Table of Contents](#table-of-contents)*
