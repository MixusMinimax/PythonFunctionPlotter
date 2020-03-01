# Function Plotter

Plots functions into a pygame-surface, which can then be drawn into any pygame program.  
`app.py` shows how to do that, by making use of the plotter to draw the function that the user types into the window.

## Usage

### TL,DR

1. Initialize a Plotter instance with a size: `p = Plotter((800, 800))`
2. Set the function: `p.set_function('derivative exp(x**2 - sin(x))')`
3. Update the plotter each frame with the time-delta (for time-dependent functions): `p.update(1/60)`
4. Blit the provided surface into the window or any other surface: `display.blit(p.get_surface(), (0, 0))`

### Attributes

| Name               | Default value | Description                                 |
| ------------------ | ------------- | ------------------------------------------- |
| `RESOLUTION`       | 256           | Amount of sample points for graph           |
| `LINE_OFFSET`      | 32            | Distance of axes from the edge              |
| `X_RANGE`          | (-5, 5)       | Min and Max values for x-axis               |
| `Y_RANGE`          | (-1, 6.5)     | Min and Max values for y-axis               |
| `DRAW_POINTS`      | False         | Draw circle at every sample-point           |
| `VERBOSE`          | True          | Print parsing information                   |

### Constructor Parameters

| Name               | Default value | Description                                 |
| ------------------ | ------------- | ------------------------------------------- |
| `size`             |               | Dimensions of render target                 |
| `initial_function` | None          | Initial value of the function to render     |

All attributes are included as well, however, in lower-case (e.g. `x_range` instead of `X_RANGE`)

### Methods

| Name           | Parameters                           | Description                         |
| -------------- | ------------------------------------ | ----------------------------------- |
| `get_surface`  |                                      | returns the render image            |
| `set_function` | f(str/Function)                      | sets the function to render         |
| `update`       | dt(int/float): time-delta in seconds | calculates graph, renders to target |


### Function Syntax

The function passed into `set_function` has to be any arithmetic expression using the following functions, operations, and variables.

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

Try out `app.py` to play around with the plotter. Start typing an expression and press Enter to display the function.

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
- [x] ~~adjustable colour scheme~~ transparent background
- [x] render to image instead of window, so that the user has more control
- [ ] autocomplete for `derivative` and other things (start typing and press tab? or shortcut)
- [ ] give each function a random color, make it adjustable
- [ ] 3d? (either orthographic view or 2d image with either hue or brightness as z-axis)
- [ ] perlin noise (2d / 3d)
- [ ] perspective view and movable 3d camera? (maybe should switch to opengl for this)
