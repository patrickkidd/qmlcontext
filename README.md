# qmlcontext - Architectural POC for Python + QQuickWidget

This is to demonstrate a clean architecture for embedding Qml views in a
QtWidgets application using PyQt. The main focus is to show a proper python
object, python model, qml view approach.

## Problem/Context

- Combining python and qml is difficult because you can't debug the qml code.
    - It is difficult to understand how/why qml properties are set the way they
      are without qml stack traces.
    - Trying to make a clean reactive QtQuick UI with python data causes difficult
      to debug circular bindings in qml.
- Portable PyQt applications need to use QtQuick to ensure performant OpenGL
rendering across all platforms, e.g. Windows, macOS, iOS, iPadOS. Such an
application needs to use QtWidgets if QMainWindow is going to manage menus.
    - It can be difficult to understand how and where to link qml items and
      signals to their python counterparts.

## Architecture

### Application Type

The demo application is a document editor based on QMainWindow. One document can
be opened at a time by the QMainWindow. Opening a new document file replaces the
document object on the main window.

### Object Model

The main, UI-agnostic document object is `Document`. A single `DocumentModel`
wraps the current `Document` object and it's properties for it's qml property
sheet `DocumentProperties`. 

This demo only demonstrates the architecture for python models to be edited by a
persistent qml view. It only does this with `Document` and `DocumentProperties`,
but the same principles can be applied to any other model / property sheet
combo.

### Property Flow

Properties in the `Document` object can be edited progrmatically directly from
python, or through user interaction via `DocumentProperties`. Everything is
automatically kept in sync.
