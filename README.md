# Function Plotter

Plots functions.  
Type an expression and press enter.

## Features

| f(x)            | Description              |
| ---------------:| ------------------------ |
| \+, \-, \*, \/, \*\*, \% | basic arithmetic operations |
| x               | the function's input     |
| c               | real constant            |
| t               | current time in seconds  |
| sin(g(x))       |                          |
| cos(g(x))       |                          |
| tan(g(x))       |                          |
| exp(g(x))       |                          |
| ln(g(x))        |                          |
| derivative g(x) | derivative of g(x)       |
| random(g(x))    | g(x) is used as the seed |

## Examples

|                                              |     |
| --------------------------------------------:|:---:|
|                                           `x`| ![x](https://i.imgur.com/JEB9lWZ.png =100x20) |
|                                    `x**2 + 1`|image|
|                                    `exp(2*x)`|image|
|                                    `sin(x-t)`|image|
|                    `derivative sin(2*exp(x))`|image|
|`derivative derivative exp(2*x**3 + x**2 + x)`|image|

## TODOs

- `derivative g(x)**h(x)` only works if at least g or h is a constant. `derivative x**x` will return 0.
  - TODO make it so that `t` is considered a constant, or more precicely any function not dependent on `x`
  - TODO find an algorithm that derives any `g(x)**h(x)`
- TODO movable camera (scale axes independently)
- TODO side panel with multiple functions
- TODO name functions so that they can be referred to, but make sure to prevent infinite loops (maximum depth?)
- TODO adjustable colour scheme
- TODO maybe instead of window render to image so that it can be embedded in any pygame application?
- TODO autocomplete for `derivative` and other things (start typing and press tab? or shortcut)
- TODO give each function a random color, make it adjustable
- TODO 3d? (either orthographic view or 2d image with either hue or brightness as z-axis)
- TODO perlin noise (2d / 3d)
- TODO perspective view and movable 3d camera? (maybe should switch to opengl for this)
