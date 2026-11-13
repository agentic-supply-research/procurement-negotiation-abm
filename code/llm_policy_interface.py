"""Integration contract for future live LLM buyer/supplier experiments.

This module only validates action schema and stores auditable memories. The
adaptive_abm.py experiments use a separate, reproducible statistical surrogate.
No LLM inference is executed in this repository.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Callable, Literal, Any
import json

Role=Literal['buyer','supplier']

@dataclass(frozen=True)
class ContractState:
    period: int
    role: Role
    self_id: int
    partner_id: int
    available_qty: float
    buyer_value: float
    seller_cost: float
    current_offer: float | None
    prior_successes: int
    prior_failures: int
    prior_delivered: float
    last_partner_outcome: str | None

@dataclass(frozen=True)
class ContractAction:
    action: Literal['propose','accept','reject','defer']
    price: float | None = None
    quantity: float | None = None
    explanation: str = ''


def validate(action: ContractAction, state: ContractState) -> ContractAction:
    """Safety layer checks legal/economically feasible action range."""
    if action.action in ('propose','accept'):
        if action.price is None or action.quantity is None:
            raise ValueError('Accepted/proposed contracts require price and quantity')
        if not(state.seller_cost <= action.price <= state.buyer_value):
            raise ValueError('Price outside bilateral reservation bounds')
        if not(0 < action.quantity <= state.available_qty):
            raise ValueError('Quantity violates remaining capacity or demand')
    return action


class ExternalLLMPolicy:
    """Dependency-injected live LLM call; caller supplies actual model client.

    The LLM is presented an *isolated* role-specific state. Caller must supply
    asynchronous-safe separate session IDs, tool logs, and model/version info.
    """
    def __init__(self, agent_id:str, role:Role, call_model:Callable[[dict],dict]):
        self.agent_id=agent_id
        self.role=role
        self.call_model=call_model
        self.audit=[]
        self.memory=[]

    def decide(self, observation:ContractState) -> ContractAction:
        if observation.role != self.role:
            raise ValueError('Role mismatch; do not share cross-party memory')
        request={'role':self.role,'self_id':self.agent_id,
                 'objective':'Negotiate feasible procurement; consider prior partner outcomes.',
                 'observation':asdict(observation),
                 'recent_memory':self.memory[-10:],
                 'action_schema':{'action':['propose','accept','reject','defer'],
                                  'price':'number or null','quantity':'number or null',
                                  'explanation':'short rationale'},
                 'constraints':'All quantities and prices must be within observation bounds.'}
        output=self.call_model(request)
        if not isinstance(output,dict):raise TypeError('Model output must be a JSON object')
        act=validate(ContractAction(**output),observation)
        self.audit.append({'observation':asdict(observation),'request':request,
                           'action':asdict(act)})
        return act

    def observe_outcome(self, outcome:dict[str,Any]):
        self.memory.append(outcome.copy())
        self.audit.append({'observed_outcome':outcome.copy()})

    def export_audit(self)->str:
        return json.dumps(self.audit,ensure_ascii=False,indent=2)


if __name__=='__main__':
    s=ContractState(period=1,role='buyer',self_id=0,partner_id=0,available_qty=10,
                    buyer_value=12,seller_cost=8,current_offer=None,
                    prior_successes=0,prior_failures=0,prior_delivered=0,last_partner_outcome=None)
    adapter=ExternalLLMPolicy('B0','buyer',lambda _: {'action':'propose','price':10.,'quantity':5.})
    assert adapter.decide(s).price==10.
    print('External LLM interface stub and constraint validation passed; no live model executed.')
