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
|                                           `x`| <img src="https://i.imgur.com/Z7kFGZz.png"   width="256px" /> |
|                                    `x**2 + 1`| <img src="https://i.imgur.com/HlaQSd7.png?2" width="256px" /> |
|                                    `exp(2*x)`| <img src="https://i.imgur.com/gB63azZ.png?1" width="256px" /> |
|                                    `sin(x-t)`| <img src="https://i.imgur.com/ezimZJN.gif"   width="256px" /> |
|                    `derivative sin(2*exp(x))`| <img src="https://i.imgur.com/O0kx3KR.png?1" width="256px" /> |
|`derivative derivative exp(2*x**3 + x**2 + x)`| <img src="https://i.imgur.com/RUUFUhI.png?1" width="256px" /> |

## TODOs

- [ ] `derivative g(x)**h(x)` only works if at least g or h is a constant. `derivative x**x` will return 0.
  - [ ] make it so that `t` is considered a constant, or more precicely any function not dependent on `x`
  - [ ] find an algorithm that derives any `g(x)**h(x)`
- [ ] movable camera (scale axes independently)
- [ ] side panel with multiple functions
- [ ] name functions so that they can be referred to, but make sure to prevent infinite loops (maximum depth?)
- [ ] adjustable colour scheme
- [x] maybe instead of window render to image so that it can be embedded in any pygame application?
- [ ] autocomplete for `derivative` and other things (start typing and press tab? or shortcut)
- [ ] give each function a random color, make it adjustable
- [ ] 3d? (either orthographic view or 2d image with either hue or brightness as z-axis)
- [ ] perlin noise (2d / 3d)
- [ ] perspective view and movable 3d camera? (maybe should switch to opengl for this)
