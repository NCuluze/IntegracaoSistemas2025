import sys
import os

# adicionar a pasta "generated" ao path
sys.path.append(os.path.join(os.path.dirname(__file__), "generated"))

import grpc
import voting_pb2
import voting_pb2_grpc

SERVER = "ken01.utad.pt:9091"

def show_candidates(stub):
    response = stub.GetCandidates(voting_pb2.GetCandidatesRequest())
    print("\n=== Candidatos ===")
    for c in response.candidates:
        print(f"{c.id} - {c.name}")

def vote(stub):
    credential = input("Credencial de voto: ")
    candidate_id = int(input("ID do candidato: "))

    request = voting_pb2.VoteRequest(
        voting_credential=credential,
        candidate_id=candidate_id
    )

    response = stub.Vote(request)
    print("\nResultado:", response.message)

def show_results(stub):
    response = stub.GetResults(voting_pb2.GetResultsRequest())
    print("\n=== Resultados ===")
    for r in response.results:
        print(f"{r.name}: {r.votes} votos")

def main():
    print("=== Cliente da Entidade de Votação ===")

    with grpc.insecure_channel(SERVER) as channel:
        stub = voting_pb2_grpc.VotingServiceStub(channel)

        while True:
            print("\n1 - Ver candidatos")
            print("2 - Votar")
            print("3 - Ver resultados")
            print("0 - Sair")

            option = input("Opção: ")

            if option == "1":
                show_candidates(stub)
            elif option == "2":
                vote(stub)
            elif option == "3":
                show_results(stub)
            elif option == "0":
                break
            else:
                print("Opção inválida")

if __name__ == "__main__":
    main()
