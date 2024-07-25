import uvicorn
from fastapi import FastAPI
from shared.database import engine, Base
from contas_pagar_receber.controllers import contas_pagar_rebecer_controller
from contas_pagar_receber.controllers import fornecedor_cliente_controller 
from contas_pagar_receber.models import contas_pagar_receber_model
from shared.exceptions import NotFound
from shared.exceptions_handler import not_found_exception_handler

#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(contas_pagar_rebecer_controller.router)
app.include_router(fornecedor_cliente_controller.router)
app.add_exception_handler(NotFound, not_found_exception_handler)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8081)
 