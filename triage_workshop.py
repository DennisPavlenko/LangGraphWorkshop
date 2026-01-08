from __future__ import annotations

import uuid
from typing import Literal
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.types import Command, interrupt
from langgraph.checkpoint.memory import InMemorySaver


# ---- 1) Define state (shared data passed between nodes) ----
class State(TypedDict, total=False):
    """
    TODO:
      - define state fields 
    """


# ---- 2) Nodes ----
def classify(state: State) -> dict:
    """
    TODO:
      - read state["ticket"]
      - set "category" to one of: billing / tech / general
      - return {"category": ...}
    """
    raise NotImplementedError


def draft_reply(state: State) -> dict:
    """
    TODO:
      - use state["category"] + state["ticket"]
      - create a short deterministic "draft" string (no LLM needed)
      - return {"draft": ...}
    """
    raise NotImplementedError


def approve(state: State) -> dict:
    """
    Human-in-the-loop gate.

    We pause with interrupt(payload). When resumed, the value passed to
    Command(resume=...) becomes the return value of interrupt().
    """
    payload = {
        "draft": state["draft"],
        "prompt": "Type: approve | reject | edit:<new text>",
    }
    action = interrupt(payload)  # resume value shows up here

    # TODO:
    #  - parse action (string)
    #  - if approve -> {"decision": "approve"}
    #  - if reject  -> {"decision": "reject"}
    #  - if edit:... -> {"decision": "edit", "draft": "<new text>"}
    #  - otherwise -> treat as reject (or re-ask by setting decision="edit" and looping)
    raise NotImplementedError


def send(state: State) -> dict:
    print("\n=== SEND REPLY ===")
    print(state["draft"])
    return {}


def escalate(state: State) -> dict:
    print("\n=== ESCALATE ===")
    print("Category:", state.get("category"))
    print("Notes:", state.get("draft"))
    return {}


def route_after_approval(state: State) -> str:
    """
    TODO:
      return one of: "send", "escalate", "approve"

    Tip:
      - decision == "approve" -> "send"
      - decision == "reject"  -> "escalate"
      - decision == "edit"    -> "approve"  (loop back for another review)
    """
    raise NotImplementedError


# ---- 3) Build the graph (orchestration) ----
def build_graph():
    builder = StateGraph(State)

    # TODO: add nodes
    # builder.add_node("classify", classify)
    # builder.add_node("draft_reply", draft_reply)
    # builder.add_node("approve", approve)
    # builder.add_node("send", send)
    # builder.add_node("escalate", escalate)

    # TODO: wire the happy path sequence
    # builder.add_edge(START, "classify")
    # builder.add_edge("classify", "draft_reply")
    # builder.add_edge("draft_reply", "approve")

    # TODO: add conditional routing after approval
    # builder.add_conditional_edges(
    #     "approve",
    #     route_after_approval,
    #     {"send": "send", "escalate": "escalate", "approve": "approve"},
    # )

    # TODO: finish
    # builder.add_edge("send", END)
    # builder.add_edge("escalate", END)

    memory = InMemorySaver()  # required for interrupt/resume pattern
    return builder.compile(checkpointer=memory)


def stream_until_pause(app, input_, config) -> bool:
    paused = False
    for event in app.stream(input_, config, stream_mode="updates"):
        print(event)
        if "__interrupt__" in event:
            paused = True
    return paused


def main():
    app = build_graph()

    thread_id = input("thread_id (blank=random): ").strip() or str(uuid.uuid4())[:8]
    config = {"configurable": {"thread_id": thread_id}}

    ticket = input("Paste a ticket: ").strip() or "Refund request: double charged"

    paused = stream_until_pause(app, {"ticket": ticket}, config)
    while paused:
        action = input("\napprove | reject | edit:<text> > ").strip()
        paused = stream_until_pause(app, Command(resume=action), config)


if __name__ == "__main__":
    main()
