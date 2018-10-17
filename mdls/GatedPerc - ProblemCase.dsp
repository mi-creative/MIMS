import("stdfaust.lib");

Fe = ma.SR;

impulsify = _ <: _,mem : - <: >(0)*_;

// integrated oscillator (mass-spring-ground system)
// m, k, z: mass, stiffness, damping (algorithmic values)
// x0, x1: initial position and delayed position
osc(m,k,z,x0,x1) = equation
with{
  A = 2-(k+z)/m;
  B = z/m-1;
  C = 1/m;
  equation = x 
	letrec{
  		'x = A*(x + (x0 : impulsify)) + B*(x' + (x1 : impulsify)) + C*_;
	};
};

// punctual mass module
// m: mass (algorithmic value)
// x0, x1: initial position and delayed position
mass(m,x0,x1) = equation
with{
  A = 2;
  B = -1;
  C = 1/m;
  equation = x 
	letrec{
  		'x = A*(x + (x0 : impulsify)) + B*(x' + (x1 : impulsify) + (x0 : impulsify)') + C*_;
	};
};

// punctual ground module
// x0: initial position
ground(x0) = equation
with{
  // could this term be removed or simlified? Need "unused" input force signal for routing scheme
  C = 0;
  equation = x 
	letrec{
		'x = x + (x0 : impulsify) + C*_;
	};
};

// spring
// k,z: stiffness and daming (algorithmic values)
spring(k,z,x1,x2) = k*(x2-x1) + z*((x2-x2')-(x1-x1')) <: _,_*(-1);

// collision
// k,z: stiffness and daming (algorithmic values)
// thres: position threshold for the collision to be active
collision(k,z,thres,x1,x2) = spring(k,z,x1,x2) : (select2(comp,0,_),select2(comp,0,_))
with{
  comp = (x2-x1)<thres;
};

gateT = button("gate"):ba.impulsify;
gateR = gateT * 1.1;

gain = hslider("gain",1,0,1,0.01);

str_M = 1.0;
str_K = hslider("stiffness",0.01,0.001,0.3,0.0001);
str_Z = hslider("damping",0.0001,0.001,0.1,0.0001);

model = (RoutingLinkToMass : 
ground(0.),
ground(0.),
mass(str_M,0., 0.),
mass(str_M,0., 0.),
mass(str_M,0., 0.),
mass(str_M,0., 0.),
mass(str_M,0., 0.),
mass(str_M,0., 0.),
mass(str_M,0., 0.),
mass(str_M,0., 0.),
mass(str_M,0., 0.),
mass(str_M,0., 0.),
mass(str_M,0., 0.),
mass(str_M,0., 0.),
mass(str_M,0., 0.),
mass(str_M,0., 0.),
mass(str_M,0., 0.),
mass(str_M,0., 0.),
mass(str_M,0., 0.),
mass(str_M,0., 0.),
mass(str_M,0., 0.),
mass(str_M,0., 0.),

// Issue: setting position and delayed position of the mass !
// Currently adds to the x and x' positions instead of forcing them to a given state
// is this possible using this approach, or do we need to add a "set positions" entry to the mass function ?
mass(10, 1 + gateT, 1. + gateR ) : 

RoutingMassToLink : 
spring(str_K,str_Z),
spring(str_K,str_Z),
spring(str_K,str_Z),
spring(str_K,str_Z),
spring(str_K,str_Z),
spring(str_K,str_Z),
spring(str_K,str_Z),
spring(str_K,str_Z),
spring(str_K,str_Z),
spring(str_K,str_Z),
spring(str_K,str_Z),
spring(str_K,str_Z),
spring(str_K,str_Z),
spring(str_K,str_Z),
spring(str_K,str_Z),
spring(str_K,str_Z),
spring(str_K,str_Z),
spring(str_K,str_Z),
spring(str_K,str_Z),
spring(str_K,str_Z),
spring(str_K,str_Z),
collision(0.1,0,0),         par(i, 2,_))~par(i, 44, _):         par(i, 44,!), par(i,  2, _)
with{
RoutingLinkToMass(l0_f1,l0_f2,l1_f1,l1_f2,l2_f1,l2_f2,l3_f1,l3_f2,l4_f1,l4_f2,l5_f1,l5_f2,l6_f1,l6_f2,l7_f1,l7_f2,l8_f1,l8_f2,l9_f1,l9_f2,l10_f1,l10_f2,l11_f1,l11_f2,l12_f1,l12_f2,l13_f1,l13_f2,l14_f1,l14_f2,l15_f1,l15_f2,l16_f1,l16_f2,l17_f1,l17_f2,l18_f1,l18_f2,l19_f1,l19_f2,l20_f1,l20_f2,l21_f1,l21_f2) = l0_f1, l20_f2, l0_f2+l1_f1, l1_f2+l2_f1, l2_f2+l3_f1, l3_f2+l4_f1, l4_f2+l5_f1, l5_f2+l6_f1, l6_f2+l7_f1, l7_f2+l8_f1, l8_f2+l9_f1, l9_f2+l10_f1, l10_f2+l11_f1+l21_f1, l11_f2+l12_f1, l12_f2+l13_f1, l13_f2+l14_f1, l14_f2+l15_f1, l15_f2+l16_f1, l16_f2+l17_f1, l17_f2+l18_f1, l18_f2+l19_f1, l19_f2+l20_f1, l21_f2;
RoutingMassToLink(m0,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16,m17,m18,m19,m20,m21,m22) = m0, m2, m2, m3, m3, m4, m4, m5, m5, m6, m6, m7, m7, m8, m8, m9, m9, m10, m10, m11, m11, m12, m12, m13, m13, m14, m14, m15, m15, m16, m16, m17, m17, m18, m18, m19, m19, m20, m20, m21, m21, m1, m12, m22,m5,m7;
};
process = model: *(0.5), *(0.5);