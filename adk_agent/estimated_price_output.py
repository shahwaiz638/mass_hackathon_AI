from pydantic import BaseModel, Field

class EstimatedPriceOutput(BaseModel):
    estimated_price: str = Field(..., description="Estimated price for the job")