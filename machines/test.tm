# Symbols
sigma = {0,1,2}
gamma = {0, 1,2,B}

# Transition function
f(q0, 0) = (q0, 1, R)
f(q0, 1) = (q0, 2, R)
f(q0, 2) = (q0, 0, R)
f(q0, B) = (q1, B, R)

# States
Q = {q0, q1}
F = {q1}

# Turing machine description
M = (sigma, gamma, Q, f, B, q0, F)

# Arrays
l = [0,1,2]

# Run machine M with input array l
!run(M, l)
