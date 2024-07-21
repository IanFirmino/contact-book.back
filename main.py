import uvicorn
from fastapi import FastAPI
from contas_pagar_receber.shared.database import engine, Base
from contas_pagar_receber.controllers import contas_pagar_rebecer_controller
from contas_pagar_receber.models import contas_pagar_receber_model

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(contas_pagar_rebecer_controller.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8081)
 