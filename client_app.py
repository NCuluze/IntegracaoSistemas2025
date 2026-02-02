import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "generated"))

import grpc

import voter_pb2
import voter_pb2_grpc
import voting_pb2
import voting_pb2_grpc


def main():
    # Fase 1 – Registo
    cc = input("Número do Cartão de Cidadão: ")
    with grpc.insecure_channel("localhost:50051") as ch:
        ar = voter_pb2_grpc.VoterRegistrationServiceStub(ch)
        resp = ar.IssueVotingCredential(
            voter_pb2.VoterRequest(citizen_card_number=cc)
        )

    if not resp.is_eligible:
        print("Eleitor não elegível.")
        return

    print("Credencial recebida:", resp.voting_credential)

    # Fase 2 – Votação
    with grpc.insecure_channel("localhost:50052") as ch:
        av = voting_pb2_grpc.VotingServiceStub(ch)
        cand = av.GetCandidates(voting_pb2.GetCandidatesRequest())

        for c in cand.candidates:
            print(c.id, "-", c.name)

        choice = int(input("Escolha o candidato: "))
        vote = av.Vote(
            voting_pb2.VoteRequest(
                voting_credential=resp.voting_credential,
                candidate_id=choice
            )
        )
        print(vote.message)

        # Fase 3 – Apuramento
        res = av.GetResults(voting_pb2.GetResultsRequest())
        print("\nResultados:")
        for r in res.results:
            print(r.name, ":", r.votes)

if __name__ == "__main__":
    main()
