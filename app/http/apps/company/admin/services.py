from app.vendors.dependencies import DB, Company
from sqlalchemy.orm.exc import NoResultFound
from fastapi import (
	HTTPException,
	status,
)
from sqlalchemy import desc
from app import models as mdl
from . import schemas as sch
from app.config import cfg



def get_companies(db: DB, skip: int = 0, limit: int = cfg.items_in_list):
	select_companies = db.select(
			mdl.Company.id, mdl.Company.alias, mdl.Company.name, 
			mdl.Company.options, mdl.Company.is_valid,
		).\
		offset(skip).limit(limit).\
		order_by(desc('created_at'))
	companies = db.session.execute(select_companies).all()
	return companies


def get_company(db: DB, company_id: int):
	company = mdl.Company.get_first_item_by_filter(db, id=company_id)
	if company is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, 
			detail='Company not found'
		) from None
	return company


def create_company(db: DB, company_data: sch.CompanyInCreate):
	company = mdl.Company.get_first_item_by_filter(db, alias=company_data.alias)
	if company:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail='Company alias not unique',
		)
	new_company = mdl.Company(
		alias = company_data.alias,
		name = company_data.name,
		options = company_data.options,
		is_valid = company_data.is_valid,
	)
	db.session.add(new_company)
	db.session.commit()
	db.session.refresh(new_company)
	return new_company


def update_company(db: DB, company_id: int, company_data: sch.CompanyInUpdate):
	company = mdl.Company.get_first_item_by_filter(db, id=company_id)
	if company is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, 
			detail='Company not found'
		) from None
	for field, value in company_data:
		setattr(company, field, value)
	db.session.add(company)
	db.session.commit()
	return company


def delete_company(db: DB, company_id: int):
	company = mdl.Company.get_first_item_by_filter(db, id=company_id)
	if company is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND, 
			detail='Company not found'
		) from None
	db.session.delete(company)
	db.session.commit()