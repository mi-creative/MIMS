**Note:** If you're looking to use a model scripter for mi-gen~ or Faust, we recommend using the a **newer one directly integrated into mi-gen~ using NodeJS**: head over to the mi-gen repo for more information: https://github.com/mi-creative/mi-gen.

# MIMS
PyQt application for creating mass interaction models and compiling them into [FAUST](https://faust.grame.fr) dsp code or ~gen objects (for [Max/MSP](https://cycling74.com/products/max/))

## 1. Getting Started

### Prerequisites

You will need a recent version of **Python 3**, with the **PyQt5** and **numpy** packages (the easiest way to install these is probably through *pip*).

### Installing

Clone or download the github repository.
If  you have all the necessary Python packages, you should just be able to run *MIMS_main.py*.

If you are considering development, any Python IDE (such as Pycharm) should do the trick.

Creation of one-file executable apps for Windows/Mac/Linux is ongoing (for windows, run *pyinstaller MIMS.spec --clean* from the base of the repo) 

## 2. Features

MIMS allows to describe one-dimensional mass-interaction models, and generade DSP code for the FAUST and Max/MSP environments.
Model files are made of physical elements, parameters, and input/outputs.

For more on mass-interaction models generated with MIMS in Max/MSP, see [the mi_gen~ github repo](https://github.com/mi-creative/mi-gen).

For more on mass-interaction models generated with MIMS in Faust, see [the mi_faust github repo](https://github.com/rmichon/mi_faust).

## 3. Building Models

### Structure

Below is a basic model description in MIMS

```java

# Define global parameter attributes
@m_K param 0.1
@m_Z param 0.001

@nlK param 0.05
@nlScale param 0.01

# Create material points
@m_s0 ground 0.
@m_m0 mass 1. 0. 0.
@m_m1 mass 1. 0. 0.
@m_m2 mass 1. 0. 0.

# Create and connect interaction modules
@m_r0 spring @m_s0 @m_m0 0.05 0.01
@m_r1 spring @m_m0 @m_m1 m_K m_Z
@m_r2 spring @m_m1 @m_m2 m_K m_Z
@m_r2 spring @m_m2 @m_m0 m_K m_Z

# Inputs and outputs
@in1 posInput 0.
@out1 posOutput @m_m2

# Add plucking interaction
@pick nlPluck @in1 @m_m1 nlK nlScale 

```

### Elements

| Module        | description           | Arguments  |
|:-------------:|:-------------:| :-----:|
| **param**      | labelled parameter  | *initial value* |
| **audioParam**      | audio-rate labelled parameter  | *initial value* |
| **mass**      | punctual mass  | *inertia(M), initialPos, delayedPos* |
| **massG**      | punctual mass (with gravity) | *inertia(M), gravity(G), initialPos, delayedPos* |
| **osc**      | harmonic oscillator  | *inertia(M), stiffness(K), damping(Z), initialPos, delayedPos* |
| **spring**      | linear spring     |   *stiffness(K), optional:damping(Z)* |
| **springDamper**      | linear dampened spring     |   *stiffness(K), damping(Z)* |
| **damper**      | linear damper     |   *damping(Z)* |
| **nlspring**  (or **nlSpring2**)    | non-linear dampened spring (parabolic term) |   *stiffness(K), NL stiffness(Q), damping(Z)* |
| **nlspring3**   | non-linear dampened spring (cubic term) |   *stiffness(K), NL stiffness(Q), damping(Z)* |
| **nlPluck**      | piecewise linear pluck interaction     |   *stiffness-coef(K), scale* |
| **nlBow**      | piecewise linear bowing interaction     |   *damping-coef(Z), scale* |
| **posInput**      | position input    |  *initialPos* |
| **frcInput**      | force input     |  *mass-element to apply force to* |
| **posOutput**      | position output    |  *mass-element to observe* |
| **frcOutput**      | force output     |  *mass-element to observe* |


## Built With

Library built with [PyCharm](https://www.jetbrains.com/pycharm/) and [PyQt5](https://pypi.org/project/PyQt5/).

## Contributing

We'd be happy to include more people to the development repository, so drop us a line if you would like to contribute to the development of the library.

## Authors

This project was developped by James Leonard and Jérôme Villeneuve.

For more info, see: www.mi-creative.eu

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE - see the [LICENSE](LICENSE) file for details

## Acknowledgments

This work implements mass-interaction physical modelling, a concept originally developped at ACROE - and now widely used in sound synthesis, haptic interaction and visual creation.
