from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional, Literal, Any


app = FastAPI(
    title="ExamPrep API (GCSE & HKDSE)",
    version="0.1.0",
    description="Minimal API skeleton for math exam preparation with simple sample endpoints."
)


# Minimal in-memory content skeleton to demonstrate topics and examples
TOPICS: Dict[str, Dict[str, Any]] = {
    "probability": {
        "description": "Basics: equally likely outcomes, simple probabilities, complementary events.",
        "samples": [
            {
                "id": "prob-1",
                "question": "A bag contains 3 red and 2 blue balls. What is P(red)?",
                "data": {"red": 3, "blue": 2},
                "expected": "3/5"
            }
        ]
    },
    "coordinate-geometry": {
        "description": "Distance, midpoint, gradients, equation of a line.",
        "samples": [
            {
                "id": "coord-1",
                "question": "Find the distance between (1,2) and (4,6).",
                "data": {"x1": 1, "y1": 2, "x2": 4, "y2": 6},
                "expected": "5"
            }
        ]
    },
    "calculus": {
        "description": "Derivatives and basic integrals.",
        "samples": [
            {
                "id": "calc-1",
                "question": "Differentiate f(x) = 2x^2 + 3x + 1.",
                "data": {"a": 2, "b": 3, "c": 1},
                "expected": "f'(x) = 4x + 3"
            }
        ]
    },
    "matrices": {
        "description": "2x2 addition and multiplication.",
        "samples": [
            {
                "id": "mat-1",
                "question": "Compute A·B where A=[[1,2],[3,4]], B=[[2,0],[1,2]].",
                "data": {"A": [[1, 2], [3, 4]], "B": [[2, 0], [1, 2]]},
                "expected": "[[4, 4], [10, 8]]"
            }
        ]
    }
}


class SolveRequest(BaseModel):
    topic: Literal["probability", "coordinate-geometry", "calculus", "matrices"]
    sample_id: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Welcome to ExamPrep API for GCSE & HKDSE (minimal demo)."}


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/topics")
async def list_topics() -> Dict[str, List[str]]:
    return {"topics": list(TOPICS.keys())}


@app.get("/samples/{topic}")
async def get_samples(topic: str) -> Dict[str, Any]:
    if topic not in TOPICS:
        raise HTTPException(status_code=404, detail="Unknown topic")
    bucket = TOPICS[topic]
    return {"topic": topic, "description": bucket["description"], "samples": bucket["samples"]}


@app.post("/solve")
async def solve(req: SolveRequest) -> Dict[str, Any]:
    topic = req.topic
    data = req.data or {}

    if topic == "probability":
        red = int(data.get("red", 0))
        blue = int(data.get("blue", 0))
        total = red + blue
        if total == 0:
            raise HTTPException(status_code=400, detail="Total number of balls must be > 0")
        prob_red = red / total
        steps = [
            "Identify total outcomes: total = red + blue",
            f"Compute total = {red} + {blue} = {total}",
            "Probability of red = red / total",
            f"P(red) = {red}/{total} = {prob_red:.3f}",
        ]
        return {"topic": topic, "result": prob_red, "steps": steps}

    if topic == "coordinate-geometry":
        x1 = float(data.get("x1", 0))
        y1 = float(data.get("y1", 0))
        x2 = float(data.get("x2", 0))
        y2 = float(data.get("y2", 0))
        dx = x2 - x1
        dy = y2 - y1
        distance = (dx ** 2 + dy ** 2) ** 0.5
        steps = [
            "Use distance formula: d = sqrt((x2-x1)^2 + (y2-y1)^2)",
            f"dx = {x2} - {x1} = {dx}",
            f"dy = {y2} - {y1} = {dy}",
            f"d = sqrt({dx**2:.3f} + {dy**2:.3f}) = {distance:.3f}",
        ]
        return {"topic": topic, "result": distance, "steps": steps}

    if topic == "calculus":
        # Differentiate ax^2 + bx + c -> 2ax + b
        a = float(data.get("a", 0))
        b = float(data.get("b", 0))
        derivative = f"f'(x) = {2*a}x + {b}"
        steps = [
            "Differentiate ax^2 -> 2ax",
            "Differentiate bx -> b",
            "Sum results",
            derivative,
        ]
        return {"topic": topic, "result": derivative, "steps": steps}

    if topic == "matrices":
        A = data.get("A")
        B = data.get("B")
        if not (isinstance(A, list) and isinstance(B, list)):
            raise HTTPException(status_code=400, detail="A and B must be 2x2 lists")
        if not (len(A) == len(B) == 2 and all(len(row) == 2 for row in A) and all(len(row) == 2 for row in B)):
            raise HTTPException(status_code=400, detail="Only 2x2 matrices are supported in this demo")
        c11 = A[0][0]*B[0][0] + A[0][1]*B[1][0]
        c12 = A[0][0]*B[0][1] + A[0][1]*B[1][1]
        c21 = A[1][0]*B[0][0] + A[1][1]*B[1][0]
        c22 = A[1][0]*B[0][1] + A[1][1]*B[1][1]
        C = [[c11, c12], [c21, c22]]
        steps = [
            "Compute C = A·B for 2x2 matrices",
            f"c11 = {A[0][0]}*{B[0][0]} + {A[0][1]}*{B[1][0]} = {c11}",
            f"c12 = {A[0][0]}*{B[0][1]} + {A[0][1]}*{B[1][1]} = {c12}",
            f"c21 = {A[1][0]}*{B[0][0]} + {A[1][1]}*{B[1][0]} = {c21}",
            f"c22 = {A[1][0]}*{B[0][1]} + {A[1][1]}*{B[1][1]} = {c22}",
        ]
        return {"topic": topic, "result": C, "steps": steps}

    raise HTTPException(status_code=400, detail="Unsupported topic")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

