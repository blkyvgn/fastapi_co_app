from fastapi import (
	HTTPException,
	status,
)


def gate_utility(base_permissions=[]): 
	def _gate():
		pass
		
	def allow(permissions: list[str], account):
		''' if all permissions is in account permissions '''
		permissions = [*base_permissions, *permissions]
		if not account.permissions or not set(permissions).issubset(set(account.permissions)):
			pass
			# raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
			
	def deny(permissions: list[str], account): 
		''' if one from permissions is in account permissions '''
		permissions = [*base_permissions, *permissions]
		if not account.permissions or not len(set(permissions).intersection(set(account.permissions))) == 0:
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

	_gate.allow = allow 
	_gate.deny = deny
	return _gate

gate = gate_utility(base_permissions=['allow_admin'])
