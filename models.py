#!/usr/bin/env python3


from typing import List
from pydantic import BaseModel


class WebhookData(BaseModel):
    id: str
    roomId: str
    roomType: str
    personId: str
    personEmail: str
    mentionedPeople: List[str]
    created: str


class WebhookEvent(BaseModel):
    id: str
    name: str
    targetUrl: str
    resource: str
    event: str
    filter: str
    orgId: str
    createdBy: str
    appId: str
    ownedBy: str
    status: str
    created: str
    actorId: str
    data: WebhookData


class Version(BaseModel):
    version: str


class MessageSummary(BaseModel):
    id: str
    text: str
    email: str
