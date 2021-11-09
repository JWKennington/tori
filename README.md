# TOpic Reference Index (TORI)

TORI is a general scheme for tracking references and metadata. Implemented as an abstract specification, the TORI scheme
allows for the underlying data to be stored in human-readable formats such as TOML, YAML, and JSON. The python utilities
in the `pytori` package provide both an object-relational mapping for TORI scheme elements as well as a set of tools for
validation of scheme elements.

## TORI Scheme

The TORI scheme consists of two principle elements: `Reference` and `Tag`. Each element has both *attributes*, which are 
pieces of metadata associated to a particular instance, as well as *properties*, which apply to collecitons of elements. 
For example, a particular `Tag` must have name and description attributes, while it must have the property of uniqueness
with respect to a collection of `Tag` elements.

### The `Reference` Element

The `Reference` element is the primary data element in the TORI scheme. It represents a source of information, such as a
journal article, book, presentation, or other document. A `Reference` has the following features.

#### Attributes

The `Reference` element has the following attributes:

- **title** [required] (string)

### The `Tag` Element

The `Tag` element is the primary metadata element in the TORI scheme

### The `TagGroup` Element

The `TagGroup` element

## Python Implementation

The included `pytori` python package contains utilities for reading, writing, validating, and interacting with data in 
the TORI scheme. 

