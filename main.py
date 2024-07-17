import uvicorn
from fastapi import FastAPI

from contas_pagar_receber import contas_pagar_rebecer_controller

app = FastAPI()

app.include_router(contas_pagar_rebecer_controller.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8081)
 