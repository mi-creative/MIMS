

mass_modules = ["mass", "massG","osc","ground", "string", "stiffString", "posInput"]

link_modules = ["damper", "spring", "nlSpring", "nlSpring2", "nlSpring3","nlPluck", "nlBow","contact", "springDamper"]

macro_modules = ["string", "stiffString", "chain", "mesh", "closedMesh", "cornerMesh"]

in_out_modules = ["frcInput","posOutput","frcOutput"]

other_modules = ["none", "param", "audioParam"]

all_modules = mass_modules + link_modules + macro_modules + in_out_modules + other_modules
