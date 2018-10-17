model = (RoutingLinkToMass : 
ground(0.),
ground(0.),
mass(1.0,0., 0.),
mass(1.0,0., 0.1),
mass(1.0,0., 0.),
mass(1.0,0., 0.),
mass(1.0,0., 0.),
mass(1.0,0., 0.),
mass(1.0,0., 0.),
mass(1.0,0., 0.),
mass(1.0,0., 0.),
mass(1.0,0., 0.) :
RoutingMassToLink : 
spring(0.1,0.01),
spring(0.1,0.01),
spring(0.1,0.01),
spring(0.1,0.01),
spring(0.1,0.01),
spring(0.1,0.01),
spring(0.1,0.01),
spring(0.1,0.01),
spring(0.1,0.01),
spring(0.1,0.01),
spring(0.1,0.01),         par(i, 2,_))~par(i, 22, _):         par(i, 22,!), par(i,  2, _)
with{
RoutingLinkToMass(l0_f1,l0_f2,l1_f1,l1_f2,l2_f1,l2_f2,l3_f1,l3_f2,l4_f1,l4_f2,l5_f1,l5_f2,l6_f1,l6_f2,l7_f1,l7_f2,l8_f1,l8_f2,l9_f1,l9_f2,l10_f1,l10_f2) = l0_f1, l10_f2, l0_f2+l1_f1, l1_f2+l2_f1, l2_f2+l3_f1, l3_f2+l4_f1, l4_f2+l5_f1, l5_f2+l6_f1, l6_f2+l7_f1, l7_f2+l8_f1, l8_f2+l9_f1, l9_f2+l10_f1;
RoutingMassToLink(m0,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11) = m0, m2, m2, m3, m3, m4, m4, m5, m5, m6, m6, m7, m7, m8, m8, m9, m9, m10, m10, m11, m11, m1,m5,m7;
};
process = model: *(0.5), *(0.5);