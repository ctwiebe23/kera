# NAME

kera — Fill template files with structured data

# SYNOPSIS

**kera** *plate_files*... *data_files*...

# OPTIONS

-o, \--out-dir
:   The directory in which to write all files.  Defaults to the current
    directory.

# INSTALL

kera can be installed using the pip package manager.

    pipx install kera

# DESCRIPTION

This program takes a collection of template files (.plate) and a collection of
data files (.json or .yaml) and then uses the data to fill placeholder "keys"
in the templates.  Each individual data file produces an output for each
individual template file.

To represent a simple key in a template file, surround it in double hashes:

```
!((cat par/simple_document.typ))!
```

And provide the data in your format of choice:

```
!((cat par/simple_metadata.json))!
```

This results in:

```
!((
    python3 src/kera.py \
        par/simple_document.typ par/simple_metadata.json \
        --out par
    cat par/simple_metadata_simple_document.typ
))!
```

Template files can have the extension .plate, but any file that isn't a data
file will be read as a template by default.

Supported data filetypes are:

- JSON
- YAML

If you want to use a data file as a template file, it must have the .plate
extension, e.g. .json.plate

The default filename of the filled template is the name of the data file (minus
extension), an underscore, and the name of the template file (with extension,
minus .plate if present).  These output files can be redirected to a different
directory with the \--out option.

As an example:

```
$ ls
> 123.sql 456.sql.plate abc.json def.yml
$ kera --out output 123.sql 456.sql.plate abc.json def.yml
$ ls output
> abc_123.sql abc_456.sql def_123.sql def_456.sql
```

---

kera also supports conditional keys and collection keys.  Conditional keys can
be represented as such:

```
##[ condition ]{{ if true }}{{ if false (optional) }}
```

The condition is simply a key found in the data, and it is true if the value
of the key is truthy according to Python.  If the key is not found, it is
automatically false.  The "body" of the conditional slot is treated as normal
body text, you can include other slots inside it and nest slots as much as you
wish.  For instance:

```
!((cat par/profile.html))!
```

With this, you process full profiles:

```
!((cat par/scofflaw.yml))!
```

```
!((
    python3 src/kera.py par/profile.html par/scofflaw.yml -o par
    cat par/scofflaw_profile.html
))!
```

And partial profiles:

```
!((cat par/lusaka.yml))!
```

```
!((
    python3 src/kera.py par/profile.html par/lusaka.yml -o par
    cat par/lusaka_profile.html
))!
```

---

Collection keys are represented as:

```
##collection{{ body for each collection member }}
```

In a collection body, the "scope" that contains available keys is not the
original data, but rather the keys nested insided the collection key.  This
is easier shown than explained:

```
!((cat par/table.yml))!
```

```
!((cat par/select.sql))!
```

```
!((
    python3 src/kera.py par/select.sql par/table.yml -o par
    cat par/table_select.sql
))!
```

By default each member of the collection is joined with a newline, but you
can alter this by providing a join string before the collection body:

```
!((cat par/columns.yml))!
```

```
!((cat par/select_columns.sql))!
```

```
!((
    python3 src/kera.py par/select_columns.sql par/columns.yml -o par
    cat par/columns_select_columns.sql
))!
```

# RETURN CODES

0, RETCODE_OK
:   Code execution was successful.

1, RETCODE_NOCREATE_OUTDIR
:   Unable to create or find the given output directory.

# BUGS

1.  If a key in YAML is made up of numbers and only numbers, the YAML parser
    will store it as an integer, which won't be resolved properly when kera
    tries to retrieve it as a string.  To prevent this, surround such keys with
    double quotes:

    ```
    # bad:
    1: this won't be resolved
    # good:
    "1": this WILL be resolved
    ```
