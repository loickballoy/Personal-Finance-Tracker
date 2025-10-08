from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import date
from ..db import get_supabase, Client
from ..deps import get_current_user
from .. import schemas


router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("", response_model=list[schemas.TransactionOut])
def list_transactions(
    supabase: Client = Depends(get_supabase),
    user = Depends(get_current_user),
    frm: date | None = Query(None),
    to: date | None = Query(None),
    subcategory_id: str | None = Query(None),
    limit: int = Query(100, le=500),
):
    q = supabase.table("transactions").select("id,account_id,subcategory_id,description,amount,currency,date,notes,created_at,updated_at").eq("user_id", user["id"]).order("date", desc=True).order("created_at", desc=True).limit(limit)
    if frm:
        q = q.gte("date", str(frm))
    if to:
        q = q.lt("date", str(to))
    if subcategory_id:
        q = q.eq("subcategory_id", subcategory_id)
    rows = q.execute().data or []
    return [
        schemas.TransactionOut(
            id=str(r["id"]), account_id=str(r["account_id"]), subcategory_id=str(r["subcategory_id"]) if r.get("subcategory_id") else None,
            description=r.get("description"), amount=r["amount"], currency=r.get("currency","EUR"), date=date.fromisoformat(r["date"]),
            notes=r.get("notes"), created_at=r["created_at"], updated_at=r["updated_at"],
        ) for r in rows
    ]


@router.post("", response_model=schemas.TransactionOut)
def create_transaction(payload: schemas.TransactionIn, supabase: Client = Depends(get_supabase), user = Depends(get_current_user)):
# Optional: validate subcategory ownership
    if payload.subcategory_id:
        sc = supabase.table("subcategories").select("id,user_id").eq("id", payload.subcategory_id).limit(1).execute().data
    if not sc or sc[0]["user_id"] != user["id"]:
        raise HTTPException(status_code=400, detail="Invalid subcategory")
    ins = supabase.table("transactions").insert({
        "user_id": user["id"],
        "account_id": payload.account_id,
        "subcategory_id": payload.subcategory_id,
        "description": payload.description,
        "amount": str(payload.amount), # supabase/postgrest accepte str pour numeric
        "currency": payload.currency,
        "date": str(payload.date),
        "notes": payload.notes,
    }).select("id,account_id,subcategory_id,description,amount,currency,date,notes,created_at,updated_at").execute()
    r = (ins.data or [None])[0]
    if not r:
        raise HTTPException(status_code=500, detail="Insert failed")
    from datetime import date as _d
    return schemas.TransactionOut(
        id=str(r["id"]), account_id=str(r["account_id"]), subcategory_id=str(r["subcategory_id"]) if r.get("subcategory_id") else None,
        description=r.get("description"), amount=r["amount"], currency=r.get("currency","EUR"), date=_d.fromisoformat(r["date"]),
        notes=r.get("notes"), created_at=r["created_at"], updated_at=r["updated_at"],
    )

@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: str, supabase: Client = Depends(get_supabase), user = Depends(get_current_user)):
    t = supabase.table("transactions").select("id,user_id").eq("id", transaction_id).limit(1).execute().data
    if not t or t[0]["user_id"] != user["id"]:
        raise HTTPException(status_code=404, detail="Not found")
    supabase.table("transactions").delete().eq("id", transaction_id).execute()
    return {"ok": True}