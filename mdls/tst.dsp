import("stdfaust.lib");

k = 0.01; // raideur
z = 0.001; // viscosité
m = 1; // inertie
Fe = ma.SR;

impulsify = _ <: _,mem : - <: >(0)*_;

harmonicOsc(k,z,m,x0,x1) = equation
with{
  A = 2-(k+z)/m;
  B = z/m-1;
  C = 1/m;
  equation = x 
	letrec{
  		'x = A*(x + (x0 : impulsify)) + B*(x' + (x1 : impulsify)) + C*_;
	};
};

mass(m,x0,x1) = equation
with{
  A = 2;
  B = -1;
  C = 1/m;
  equation = x 
	letrec{
  		'x = A*(x + (x0 : impulsify)) + B*(x' + (x1 : impulsify)) + C*_;
	};
};

spring(k,z,x1,x2) = k*(x2-x1) + z*((x2-x2')-(x1-x1')) <: _,_*(-1);

modelA = (routingA : mass(10000,0,0),(_,_ :> mass(m,0,0.9) <: _,_),(_,_ :> mass(m,0,0.9) <: _,_),mass(m,0,0) : routingB : spring(k,z),spring(k,z),spring(k,z),spring(k,z))~(_,_,_,_,_,_,_,_) : *(5),!,!,!,!,!,!,!
with{
  routingA(a,b,c,d,e,f,g,h) = a,b+g,c,d,e,f+h;
  routingB(a,b,c,d,e,f) = a,b,c,d,e,f,b,f;
};

modelB = (routingA : mass(10000,0,0),mass(m,0,0.9),mass(m,0,0.9),mass(m,0,0) : routingB : spring(k,z),spring(k,z),spring(k,z),spring(k,z))~(_,_,_,_,_,_,_,_) : *(5),!,!,!,!,!,!,!
with{
  routingA(a,b,c,d,e,f,g,h) = a,b+g+c,d+e,f+h;
  routingB(a,b,c,d) = a,b,b,c,c,d,b,d;
};

modelC = (routingA : par(i,4,mass(m(i),x1(i),x2(i))) : routingB : par(i,4,spring(k(i),z(i))),par(i,2,_))~par(i,8,_) : par(i,8,!),par(i,2,_)
with{
  routingA(a,b,c,d,e,f,g,h) = a,b+g+c,d+e,f+h;
  routingB(a,b,c,d) = a,b,b,c,c,d,b,d,b,d;
  m(n) = ba.take(n+1,(100000000,1,1,1));
  x1(n) = ba.take(n+1,(0,0,0,0));
  x2(n) = ba.take(n+1,(0,0.9,0.9,0));
  k(n) = ba.take(n+1,(0.01,0.01,0.01,0.01));
  z(n) = ba.take(n+1,(0.001,0.001,0.001,0.001));
};

process = modelC : *(0.1),*(0.1);
			