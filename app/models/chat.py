from app.vendors.base.database import BaseModel
from sqlalchemy.orm import (
	relationship,
	backref,
)
from app.vendors.mixins.model import (
	TimestampsMixin, 
	ValidMixin,
	HelpersMixin,
)
from sqlalchemy import (
	Column, 
	ForeignKey, 
	Integer, 
	String,
	Text,
	JSON,
)


class Room(ValidMixin, TimestampsMixin, HelpersMixin, BaseModel):
	__tablename__ = 'rooms'

	alias = Column(
		String(30), 
		unique=True,
	)
	messages = relationship(
		'Message', 
		back_populates='room'
	)
	account_id = Column(
		Integer, 
		ForeignKey('accounts.id')
	)
	account = relationship(
		'Account', 
		back_populates='chat_rooms'
	)
	company_id = Column(
		Integer, 
		ForeignKey('companies.id')
	)
	company = relationship(
		'Company', 
		back_populates='chat_rooms'
	)


class Message(TimestampsMixin, BaseModel):
	__tablename__ = 'messages'

	message = Column(
		String(500),
		nullable=False,
	) 
	room_id = Column(
		Integer, 
		ForeignKey('rooms.id')
	)
	room = relationship(
		'Room', 
		back_populates='messages'
	)
	sender_id = Column(
		Integer, 
		nullable=True,
	)