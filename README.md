# trajectory-sims

## what are these?

### basic sim

The basic sim is the most simple model which should work for low to medium powered rockets. It assumes

* uniform thrust curve
* basic atmosphere model
* mass doesn't change
* Cd doesn't change
* no parachute :(

### thrust curve

This is just the above but we can input a thrust curve

### atmosphere model

This uses the python fluids module to find rho (density of air)

### thrust model

This has a custom engine model, great if you want to model a space engine
