class FKE:
	def pow(self, n, a, mod):
		if(a == 0):
			return 1
		if(a % 2 == 1):
			return (n * pow(n, a-1, mod)) % mod
		if(a % 2 == 0):
			temp = pow(n, a/2, mod)
			return (temp * temp) % mod

	def Make_Private_Code(self, N, m, p):
		P = pow(N, p, m)
		self.Private_Open_Code = (N, m, P)
		self.Private_Secret_Code = p
		return (self.Private_Open_Code, self.Private_Secret_Code)

	def Make_Communication_Code(self, N, m, P, q):
		Q = pow(N, q, m)
		K = pow(P, q, m)
		self.Communication_Open_Code = Q
		self.Communication_Secret_Code = q
		self.Key = K
		return (Q, q, K)

	def Make_Key(self, Q, m, p):
		self.Key = pow(Q, p, m)
		return self.Key