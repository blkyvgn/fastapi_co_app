from fastapi import (
	HTTPException,
	status,
)


def gate_utility(): 
	def _gate():
		pass
		
	def allow(permissions: list[str], account):
		if not account.permissions or not frozenset(account.permissions) <= frozenset(permissions):
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
			
	def deny(permissions: list[str], account): 
		if not account.permissions or not len(frozenset(account.permissions) & frozenset(permissions)) == 0:
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

	_gate.allow = allow 
	_gate.deny = deny
	return _gate

gate = gate_utility()
