from pydantic import BaseModel
from pydantic_ai import Agent, RunContext


class ReturnResp(BaseModel):
    result: str


roulette_agent = Agent(
    "groq:llama-3.3-70b-versatile",
    deps_type=int,
    # result_type=bool,
    result_type=ReturnResp,
    system_prompt=(
        "Use the `roulette_wheel` function to see if the "
        "customer has won based on the number they provide."
    ),
)


@roulette_agent.tool
async def roulette_wheel(ctx: RunContext[int], square: int) -> str:
    """check if the square is a winner"""
    return "winner" if square == ctx.deps else "loser"


# Run the agent
success_number = 18
result = roulette_agent.run_sync("Put my money on square eighteen", deps=success_number)
print(result.data)
# > True

result = roulette_agent.run_sync("I bet five is the winner", deps=success_number)
print(result.data)
# > False
