---
title: ftf
author: Carston Wiebe
date: AUG 19 2025
---

# NAME

ftf — Fill template files with structured data

# SYNOPSIS

**ftf** *plate_files*... *data_files*...

# DESCRIPTION

# INSTALL

# OPTIONS

-o, \--out
:   The directory in which to write all files.  Defaults to the current
    directory.

# EXAMPLES

# BUGS

1.  If a key in YAML is made up of numbers and only numbers, the YAML parser
    will store it as an integer, which won't be resolved properly when ftf
    tries to retrieve it.  To prevent this, surround such keys with double
    quotes:

    ```yaml
    # bad:
    1: this won't be resolved
    # good:
    "1": this WILL be resolved
    ```
