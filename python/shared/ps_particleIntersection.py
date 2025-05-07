import math
import numpy as np 
def particlesIntersection(self,F,T):
    
    
    A = np.array([F.PosLoc[0], F.PosLoc[1]])
    B = np.array([T.PosLoc[0], T.PosLoc[1]])
	
    a = F.PosLoc[3]
    b = T.PosLoc[3]
    c = np.linalg.norm(A-B)
    cosAlpha = (b**2+c**2-a**2)/(2*b*c)
    
    # Unit vector pointing to centers
    u_AB = (B - A)/c
    # Normal vector
    pu_AB = np.array([u_AB[1], -u_AB[0]])
    # Calc points of intersection 
    self.ups_i1 = A + u_AB * (b*cosAlpha) + pu_AB * (b*math.sqrt(1-cosAlpha**2))
    self.ups_i2 = A + u_AB * (b*cosAlpha) - pu_AB * (b*math.sqrt(1-cosAlpha**2))
    if self.rptIntersectionPoints == True:
        print("Pt1:{},Pt2:{}".format(self.ups_i1, self.ups_i2))