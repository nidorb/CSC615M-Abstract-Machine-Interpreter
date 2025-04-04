### 1-Way GST Machine
#### Machine Definition:
.LOGIC
A] SCAN (0,B), (1,C), (#,halt)
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

### 1 Tape NFA
#### Machine Definition:
.DATA
TAPE T1
.LOGIC
A] RIGHT(T1) (0/X,B), (Y/Y,D), (1/1,reject), (0/Y,B)
B] RIGHT(T1) (0/0,B), (Y/Y,B), (1/Y,C), (0/1,C)
C] LEFT(T1) (0/Y,C), (Y/Y,C), (X/X,A)
D] RIGHT(T1) (Y/Y,D), (#/#,accept), (1/1,accept)

#### Test Cases:
Accepted: 000, 00111, 0011
Reject: 1, 010, 01011

### 3 tapes
#### Machine Definition:
.DATA
TAPE T1
TAPE T2
TAPE T3
.LOGIC
A] RIGHT(T1) (a/a,B), (b/b,C)
B] RIGHT(T2) (#/X,A)
C] RIGHT(T2) (#/#,D)
D] LEFT(T2) (X/#,E)
E] RIGHT(T3) (#/X,F)
F] RIGHT(T1) (b/b,E), (c/c,G)
G] RIGHT(T3) (#/#,H)
H] LEFT(T3) (X/#,I)
I] RIGHT(T3) (c/c,H), (#/#,J)
J] LEFT(T2) (#/#,K)
K] LEFT(T3) (#/#,accept)

#### Test Cases:
Accepted: ab^nc^n


### 1 way 1 queue
#### Machine Definition:
.DATA 
QUEUE Q1

.LOGIC
A] SCAN (0,B)
B] WRITE(Q1) (0,C)
C] SCAN (0,B), (1,D)
D] WRITE(Q1) (1,E)
E] SCAN (1,D), (#,F)
F] WRITE(Q1) (#,G)
G] READ(Q1) (0,H), (X,M), (1,N), (#,AS)
H] WRITE(Q1) (X,I)
I] READ(Q1) (0,J), (1,K), (#,Q)
J] WRITE(Q1) (0,I)
K] READ(Q1) (1,L), (#,F)
L] WRITE(Q1) (1,K)
M] WRITE(Q1) (X,G)
N] WRITE(Q1) (1,O)
O] READ(Q1) (1,N), (#,Y)
Q] WRITE(Q1) (#,R)
R] READ(Q1) (X,S)
S] WRITE(Q1) (0,T)
T] READ(Q1) (X,U), (#,V), (0,X)
U] WRITE(Q1) (X,T)
V] READ(Q1) (0,Z)
Z] WRITE(Q1) (0,W) 
W] WRITE(Q1) (#,P)
X] WRITE(Q1) (0,T)
Y] WRITE(Q1) (#,P)
P] READ(Q1) (1,AB), (X,AA), (0,AH)
AA] WRITE(Q1) (X,P)
AB] READ(Q1) (#,accept), (1,AE)
AC] READ(Q1) (1,AE), (#,AD)
AE] WRITE(Q1) (1,AC)
AD] WRITE(Q1) (1,AN)
AF] WRITE(Q1) (#,AP)
AH] READ(Q1) (#,accept), (0,AI)
AI] WRITE(Q1) (0,AJ)
AJ] READ(Q1) (0,AI), (#,AK)
AK] WRITE(Q1) (0,AF)
AN] WRITE(Q1) (#,AL)
AL] READ(Q1) (1,AO), (X,AM), (#,F)
AO] WRITE(Q1) (1,AL)
AM] WRITE(Q1) (0,AL)
AP] READ(Q1) (0,AQ), (X,AR), (#,F)
AQ] WRITE(Q1) (1,AP)
AR] WRITE(Q1) (0,AP)
AS] WRITE(Q1) (#,AT)
AT] READ(Q1) (X,AU)
AU] READ(Q1) (X,reject), (#,accept)

#### Test Cases:
Accepted:  L = {ω ∈ {0, 1}∗| ω = 0n1m ∧ n, m ≥ 1 ∧ gcd(n, m) = 1}

### 1 way 2 stack PDA
.DATA
STACK S1
STACK S2
.LOGIC
A] WRITE(S1) (#,B)
B] WRITE(S2) (#,C)
C] SCAN RIGHT (0,D)
D] WRITE(S1) (X,E)
E] SCAN RIGHT (0,D), (1,F)
F] READ(S1) (X,G)
G] WRITE(S2) (X,H)
H] SCAN RIGHT (1,F), (0,I)
I] SCAN RIGHT (0,J)
J] READ(S1) (#,K)
K] WRITE(S1) (#,L)
L] READ(S2) (X,M)
M] WRITE(S1) (X,N)
N] SCAN RIGHT (1,P), (0,O)
O] SCAN RIGHT (0,L)
P] SCAN RIGHT (1,Q)
Q] READ(S2) (#,R)
R] WRITE(S2) (#,S)
S] READ(S1) (X,T)
T] SCAN RIGHT (1,U), (#,V)
U] SCAN RIGHT (1,S)
V] SCAN RIGHT (#,W)
W] READ(S1) (#,X)
X] READ(S2) (#,accept)

#### Test Cases:
{ω ∈ {0, 1}∗| ω = 0^n 1^n 0^2n 1^2n, n ≥ 1}