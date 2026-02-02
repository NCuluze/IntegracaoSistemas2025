NSTRUÇÕES DE EXECUÇÃO DO CÓDIGO
Sistema de Votação Eletrónica (gRPC)

1. PRÉ-REQUISITOS
- Windows 10 ou 11
- Python 3.9 ou superior
- PowerShell

Verificar a versão do Python:
python --version


2. INSTALAR DEPENDÊNCIAS
Na pasta raiz do projeto, executar:
python -m pip install grpcio grpcio-tools


3. GERAR OS FICHEIROS gRPC

3.1 Criar a pasta para os ficheiros gerados (caso não exista):
mkdir generated

3.2 Gerar os ficheiros a partir dos ficheiros .proto:
python -m grpc_tools.protoc -I protos --python_out=generated --grpc_python_out=generated protos\voter.proto protos\voting.proto

Confirmar a geração:
dir generated


4. EXECUTAR O SISTEMA (ORDEM OBRIGATÓRIA)
Abrir três janelas de PowerShell.

4.1 Iniciar a Autoridade de Registo (AR):
python server_ar.py

Mensagem esperada:
AR ativa em localhost:50051


4.2 Iniciar a Autoridade de Votação (AV):
python server_av.py

Mensagem esperada:
AV ativa em localhost:50052


4.3 Executar a aplicação cliente (Eleitor):
python client_app.py


5. ENCERRAR A EXECUÇÃO
Para parar qualquer componente, usar:
CTRL + C
