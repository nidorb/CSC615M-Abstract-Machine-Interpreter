### 1-Way GST Machine
#### Machine Definition:
.LOGIC
A] SCAN (0,B), (1,C), (#,reject)
B] SCAN (#,reject), (0,F), (1,E)
C] SCAN (#,reject), (0,G), (1,H)
E] PRINT (Y,C)
F] PRINT (X,B)
G] PRINT (Y,B)
H] PRINT (X,C)

#### Test Cases:
Input → Output
1101101 → XY Y XY Y
000111 → XXY XX
10011 → Y XY X

---

### 1-Way 1-Stack PDA
#### Machine Definition:
.DATA
STACK S1
.LOGIC
A] WRITE(S1) (#,B)
B] SCAN (1,C), (0,E), (#,I)
C] SCAN (1,D)
D] WRITE(S1) (X,B)
E] SCAN (1,F)
F] SCAN (0,G)
G] READ(S1) (X,H)
H] SCAN (0,E), (#,I)
I] READ(S1) (#,accept)

#### Test Cases:
Accepted: λ, 11010, 1111010010
Rejected: 010010, 0, 110

---

### 2-Way 1-Stack PDA
#### Machine Definition:
.DATA
STACK S1
.LOGIC
A] WRITE(S1) (#,B)
B] SCAN RIGHT (0,C), (1,D), (X,E)
C] WRITE(S1) (Y,B)
D] WRITE(S1) (Z,B)
E] SCAN RIGHT (1,E), (0,E), (X,F)
F] SCAN RIGHT (0,G), (1,H), (#,I)
G] READ(S1) (Y,F)
H] READ(S1) (Z,F)
I] READ(S1) (#,J)
J] WRITE(S1) (#,K)
K] SCAN LEFT (0,L), (1,M), (X,N)
L] WRITE(S1) (Y,K)
M] WRITE(S1) (Z,K)
N] SCAN LEFT (0,O), (1,P), (X,Q)
O] READ(S1) (Y,N)
P] READ(S1) (Z,N)
Q] READ(S1) (#,accept)

#### Test Cases:
Accepted: 010101X010101X101010, 0010X0010X0100, 110X110X011
Rejected: 100X001X101, 1010X10100X111, 00XX0

---

### 1-Way 2-Stack PDA
#### Machine Definition:
.DATA
STACK S1
STACK S2
.LOGIC
A] WRITE(S1) (#,B), (#,O)
B] WRITE(S2) (#,C)
C] WRITE(S1) (X,D)
D] READ(S1) (X,E), (#,G)
E] WRITE(S2) (X,F)
F] SCAN (1,D)
G] SCAN (1,H), (#,accept)
H] WRITE(S1) (#,I)
I] READ(S2) (X,J), (#,L)
J] WRITE(S1) (X,I)
L] WRITE(S2) (#,M)
M] WRITE(S2) (X,N)
N] WRITE(S2) (X,F)
O] SCAN (#,P)
P] READ(S1) (#,accept)

#### Test Cases:
Accepted: λ, 1, 1111, 111111111
Rejected: 111, 11111, 11

---

### 1-Way 1-Queue PDA
#### Machine Definition:
.DATA
QUEUE Q1
STACK S1
STACK S2
.LOGIC
A] SCAN (a,B), (b,C)
B] WRITE(Q1) (X,A)
C] READ(Q1) (X,D)
D] WRITE(Q1) (Y,E)
E] SCAN (b,C), (c,F)
F] WRITE(Q1) (#,G)
G] READ(Q1) (Y,H)
H] SCAN (c,G), (#,I)
I] READ(Q1) (#,accept)

#### Test Cases:
Accepted: a^nb^nc^n