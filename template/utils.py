import copy as cpy
import os
import errno
from jinja2 import Template

tab_size = 4

_utils_incl_template = Template("""\
#ifndef {{ include.basename|upper }}_H
#define {{ include.basename|upper }}_H

/* ***************
 * Include Files *
 * ***************/

{% for inc_file in include.files -%}
#include {{ inc_file }}
{%- endfor %}

/* **************
 * Declarations *
 * **************/

{% for code_snippet in include.snippets -%}
{{ code_snippet }}

{% endfor %}
#endif
""")

_utils_fcns_template = Template("""\
#define _POSIX_C_SOURCE 200809L
#include <unistd.h>

/* ***************
 * Include Files *
 * ***************/

{% for inc_file in fcns.files -%}
#include {{ inc_file }}
{%- endfor %}

/* ***********
 * Functions *
 * ***********/

{% for code_snippet in fcns.snippets -%}
{{ code_snippet }}

{% endfor %}
""")


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def getvarname(params, varname=None):
    named = False
    if varname:
        named = True
        params['name'] = varname
    return (params, named)


def mergeunorderedlist(list_one, list_two):
    list_out = copy(list_one)
    list_out.extend(list_two)
    list_out = list(set(list_out))
    return list_out


def copy(obj):
    return cpy.copy(obj)


def ccodeappend(code, code_append):

    new_code = cpy.copy(code)

    if code_append['include']['snippets']:
        new_code['include']['snippets'] \
            .extend(code_append['include']['snippets'])
    if code_append['fcns']['snippets']:
        new_code['fcns']['snippets'] \
            .extend(code_append['fcns']['snippets'])
    if code_append['init']['snippets']:
        new_code['init']['snippets'] \
            .extend(code_append['init']['snippets'])

    new_code['include']['inclfiles'] = \
        mergeunorderedlist(new_code['include']['inclfiles'],
                           code_append['include']['inclfiles'])
    new_code['fcns']['inclfiles'] = \
        mergeunorderedlist(new_code['fcns']['inclfiles'],
                           code_append['fcns']['inclfiles'])

    return new_code


def ccodeappendlist(code_list):

    new_code = cpy.copy(code_list[0])
    for i in range(1, len(code_list)):
        new_code = ccodeappend(new_code, code_list[i])

    return new_code


def ccodefiles(code, directories):

    # include
    include = {
        'name': directories['include']['filename'],
        'basename': os.path.splitext(directories['include']['filename'])[0],
        'snippets': code['include']['snippets'],
        'files': code['include']['inclfiles']
    }

    # fcns
    fcns = {
        'snippets': code['fcns']['snippets'],
        'files': code['fcns']['inclfiles']
    }
    inc_path = os.path.join(directories['subfolder'], include['name'])
    fcns['files'].extend(["\"{i}\"".format(i=inc_path)])

    include_str = _utils_incl_template.render(include=include)
    fcns_str = _utils_fcns_template.render(fcns=fcns)

    # make directories
    subfolder = os.path.join(directories['folder'], directories['subfolder'])
    mkdir_p(directories['folder'])
    mkdir_p(subfolder)

    # write include file
    f = open(os.path.join(subfolder, directories['include']['filename']), "w")
    f.write(include_str)
    f.close()

    # write c code file
    f = open(os.path.join(directories['folder'],
                          directories['fcns']['filename']), "w")
    f.write(fcns_str)
    f.close()


def ccodefilesfromclass(folder,
                        prefix,
                        code,
                        subfolder=None):

    """Create C code files"""
    if not subfolder:
        subfolder = "include"

    directories = {
        'folder': folder,
        'subfolder': subfolder,
        'include': {
            'filename': "{b}.h".format(b=prefix)
        },
        'fcns': {
            'filename': "{b}.c".format(b=prefix)
        }
    }

    ccodefiles(code, directories)

    print("Created source files.")


def ifexistscopy(keys, dest, src):
    if (isinstance(keys, list)):
        for key in keys:
            if (key in src):
                dest[key] = src[key]
    else:
        if (keys in src):
            dest[keys] = src[keys]
