# Symbols
bin = {0,1}
binGamma = {0, 1, B}

# Transition function
sum(q0, 0) = (q0, 1, R)
sum(q0, 1) = (q0, 1, R)
sum(q0, B) = (q2, B, L)
sum(q2, 1) = (q1, B, R)

# States
Q = {q0, q1, q2}
F = {q1}

# Turing machine description
M = (bin, binGamma, Q, sum, B, q0, F)

# Arrays
input = [1,1,1,0,1,1]

# Run machine M with input array l
!run(M, input)