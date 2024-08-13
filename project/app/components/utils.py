import numpy as np

def random_value_in_range(a,b):
    return a + np.random.random() * (b-  a)

# Angulo en radianes
def Rx(psi):
    R=np.array([[1,0,0],[0,np.cos(psi),-np.sin(psi)],[0,np.sin(psi),np.cos(psi)]])
    return R

# Angulo en radianes
def Ry(theta):
    R=np.array([[np.cos(theta),0,np.sin(theta)],[0,1,0],[-np.sin(theta),0,np.cos(theta)]])
    return R

# Angulo en radianes
def Rz(phi):
    R=np.array([[np.cos(phi),-np.sin(phi),0],[np.sin(phi),np.cos(phi),0],[0,0,1]])
    return R

# Angulo en radianes
def RxRyRz(psi, theta, phi):
    R=Rx(psi=psi)@Ry(theta=theta)@Rz(phi=phi)
    return R

# Angulo en radianes
def RzRyRx(psi, theta, phi):
    R=Rz(phi=phi)@Ry(theta=theta)@Rx(psi=psi)
    return R

# R=Rz(ϕ)Ry(θ)Rx(Ψ)
def euler_angles_from_to_rotation_matrix(R):
    R11,R12,R13,R21,R22,R23,R31,R32,R33=R.flatten(order='C')
    euler_angles=np.zeros(3)
    if R31 != -1 and R31 != 1:
        theta_1=np.arcsin(-R31)
        theta_2=np.pi - theta_1
        psi_1=np.arctan2(R32 / np.cos(theta_1), R33 / np.cos(theta_1))
        psi_2=np.arctan2(R32 / np.cos(theta_2), R33 / np.cos(theta_2))
        phi_1=np.arctan2(R21 / np.cos(theta_1), R11 / np.cos(theta_1))
        phi_2=np.arctan2(R21 / np.cos(theta_2), R11 / np.cos(theta_2))
        euler_angles=np.array([psi_1, theta_1, phi_1])
    else:
        if R31 == -1:
            theta=np.pi/2
            phi=0  
            psi=np.arctan2(R12, R13) + phi
            euler_angles=np.array([psi, theta, phi])
        else:
            theta=-np.pi/2
            phi=0  
            psi=np.arctan2(-R12, -R13) - phi
            euler_angles=np.array([psi, theta, phi])
    return euler_angles