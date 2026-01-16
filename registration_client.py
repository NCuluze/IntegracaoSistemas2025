import sys
import os

# adicionar a pasta "generated" ao path
sys.path.append(os.path.join(os.path.dirname(__file__), "generated"))

import grpc
import voter_pb2
import voter_pb2_grpc

SERVER = "ken01.utad.pt:9091"

def main():
    print("=== Cliente da Entidade de Registo ===")

    citizen_card = input("Número do Cartão de Cidadão: ")

    with grpc.insecure_channel(SERVER) as channel:
        stub = voter_pb2_grpc.VoterRegistrationServiceStub(channel)

        request = voter_pb2.VoterRequest(
            citizen_card_number=citizen_card
        )

        response = stub.IssueVotingCredential(request)

        print("\n--- Resposta ---")
        print(f"Elegível: {response.is_eligible}")
        print(f"Credencial emitida: {response.voting_credential}")

if __name__ == "__main__":
    main()
