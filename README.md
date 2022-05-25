# napari-spacemouse

[![License](https://img.shields.io/pypi/l/napari-spacemouse.svg?color=green)](https://github.com/tlambert03/napari-spacemouse/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/napari-spacemouse.svg?color=green)](https://pypi.org/project/napari-spacemouse)
[![Python Version](https://img.shields.io/pypi/pyversions/napari-spacemouse.svg?color=green)](https://python.org)
[![CI](https://github.com/tlambert03/napari-spacemouse/actions/workflows/ci.yml/badge.svg)](https://github.com/tlambert03/napari-spacemouse/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/tlambert03/napari-spacemouse/branch/main/graph/badge.svg)](https://codecov.io/gh/tlambert03/napari-spacemouse)

3DConnexion SpaceMouse support for napari

Expected to work for any product in the [SpaceMouse](https://3dconnexion.com/uk/spacemouse/) line, but only tested on a SpaceNavigator. Currently only tested on macOS.

## Usage

To install globally in napari:

```python
import napari_spacemouse

# start listening to the spacemouse
napari_spacemouse.install()

# stop listening to the spacemouse
napari_spacemouse.uninstall()
```

Alternatively, there is `SpaceMouse` widget that can be used to toggle
support for the mouse, and provide some configuration.

### Important note for macOS

Currently, this plugin requires that the `3DconnexionHelper` driver *not* be running, otherwise you will likely get an `OSError` when activating the plugin.  To fix this:

1. Open `/Applications/Utilities/Activity Monitor/`
2. Search for `3DconnexionHelper`
3. If it's running, highlight it and quit it using the X button at the top right.

When done, you can start it again anytime at `/Applications/3Dconnexion/3DconnexionHelper`.

(Eventually this could be fixed, but we need to use the actual Connexion framework API instead of direct USB reads.)
