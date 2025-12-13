from fastapi import HTTPException, status
from sqlmodel import Session, select
from decimal import Decimal
from Models.models import Plan
from typing import Optional
from enum import Enum
from datetime import datetime

class PlanController:

    @staticmethod
    def create_plan(name: str, slug: str, description: str, price: Decimal, billing_cycle: Enum, is_active: bool, max_bus: int, max_feed:int, session: Session) -> dict:
        try:
            plan_existing = session.exec(select(Plan).where(Plan.name == name)).first()

            if plan_existing:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="plan_existing")
            
            new_plan = Plan(
                name=name,
                slug=slug,
                description=description,
                price=price,
                is_active=is_active,
                billing_cycle=billing_cycle,
                max_business=max_bus,
                max_feedbacks=max_feed
            )

            session.add(new_plan)
            session.commit()
            session.refresh()
        
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Error: {e}")
    
    @staticmethod
    def get_plan(plan_id: int, session: Session):
        try:
            plan = session.exec(select(Plan).where(Plan.id == plan_id)).first()

            if not plan:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not Found plan")

            return {
                "id": plan.id,
                "name": plan.name,
                "slug": plan.slug,
                "description": plan.description,
                "price": plan.price,
                "billing_cycle": plan.billing_cycle,
                "max_business": plan.max_business,
                "max_feedbacks": plan.max_feedbacks,
                "is_active": plan.is_active,
                "created_at": plan.created_at,
                "update_at": plan.update_at
            }
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Error: {e}")

    @staticmethod   
    def edit_plan(
        plan_id: int, 
        name: Optional[str] = None,
        slug: Optional[str] = None,
        description: Optional[str] = None,
        price: Optional[Decimal] = None,
        billing_cycle: Optional[Enum] = None,
        max_business: Optional[int] = None,
        max_feedbacks: Optional[int] = None,
        is_active: Optional[bool] = None,
        session: Session = None
        ):
        
        try:
            plan = session.get(Plan, plan_id)

            if not plan:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not Found plan")
            
            if name and name != None:
                existing_plan = session.exec(select(Plan).where(Plan.name == name)).first()

                if existing_plan:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Existing plan")
                
                plan.name = name
            
            if slug and slug != None:
                existing_plan = session.exec(select(Plan).where(Plan.slug == slug)).first()

                if existing_plan:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Existing plan")
                
            if description and description != None:
                plan.description = description
            
            if price and price != None:
                plan.price = price

            if billing_cycle and billing_cycle != None:
                plan.billing_cycle = billing_cycle
            
            if max_business and max_business != None:
                plan.max_business = max_business
            
            if max_feedbacks and max_feedbacks:
                plan.max_feedbacks = max_feedbacks
            
            if is_active and is_active != None:
                plan.is_active = is_active

            plan.update_at = datetime.utcnow

            session.commit()
            session.refresh(plan)

            return {
                "message": "Plano atualizado",
                "plan": PlanController._plan_to_dict(plan)
            }
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Error: {e}")
        
    def delete_plan():
        pass