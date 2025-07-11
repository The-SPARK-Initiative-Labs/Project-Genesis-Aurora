# aura_engine/schemas.py
#
# This file defines the Pydantic data models that enforce a strict,
# predictable structure for data flowing through the A.U.R.A. Engine.
# Using these schemas with the lmstudio-python SDK's `response_format`
# feature guarantees that the LLM's output is always machine-readable,
# preventing errors from creative or malformed responses.

from pydantic import BaseModel, Field
from typing import List

class VerifiedFact(BaseModel):
    """
    Represents a single, verbatim fact extracted directly from a source text.
    This schema is used to ensure that each extracted fact is a simple string.
    """
    fact_text: str = Field(
        ..., 
        description="A single, complete, and verbatim sentence extracted from the source text that represents a key fact."
    )

class FactList(BaseModel):
    """
    A container for a list of VerifiedFact objects. This schema is used by the
    Extractor Agent to ensure its output is always a well-formed list of facts,
    even if it finds no facts to extract.
    """
    facts: List[VerifiedFact] = Field(
        ..., 
        description="A list of all verbatim facts extracted from the source text."
    )

class ValidationResponse(BaseModel):
    """
    A schema to guarantee the Validator Agent's output is a simple boolean.
    This prevents conversational responses and ensures a clear, binary
    judgement on whether a fact is verbatim.
    """
    is_verbatim: bool = Field(
        ...,
        description="True if the fact is a verbatim quote from the source text, otherwise False."
    )

class NarrativeSummary(BaseModel):
    """
    A schema for the output of the Narrative Weaver Agent. This ensures the
    agent's summary is returned as a single, coherent string.
    """
    summary_text: str = Field(
        ...,
        description="A concise, third-person narrative summary of the key events and facts from the conversation."
    )
