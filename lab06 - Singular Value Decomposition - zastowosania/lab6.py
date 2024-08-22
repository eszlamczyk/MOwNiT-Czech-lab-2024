from scipy import sparse
from scipy.sparse import linalg
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize

import numpy as np

from lab6_websiteHandler import *


def BOWtoVector(BOW) -> sparse.csr_matrix:
    globalBow = load_dict_from_file("Databases/globalBow.json")
    IDFs = load_dict_from_file("Databases/IDFs.json")
    SparseVector = sparse.lil_matrix((len(globalBow), 1), dtype=np.float32)
    for word, value in BOW.items():
        if word not in globalBow:
            continue
        SparseVector[globalBow[word], 0] = value*IDFs[word]
    return sparse.csr_matrix(SparseVector.tocsr())


def CreateTermByDocumentMatrix() -> sparse.csr_matrix:
    print("===============CREATING TBD MATRIX================")
    URLs = load_dict_from_file("Databases/URLs.json")
    globalBow = load_dict_from_file("Databases/globalBow.json")
    URLIndexes = load_dict_from_file("Databases/URLIndexes.json")
    IDFs = load_dict_from_file("Databases/IDFs.json")
    TermByDocumentMatrix = sparse.lil_matrix(
        (len(globalBow), len(URLs)), dtype=np.float32)
    for url, urlDict in URLs.items():
        for word, value in urlDict.items():
            TermByDocumentMatrix[globalBow[word],
                                 URLIndexes[url]] = value*IDFs[word]

    TermByDocumentMatrix_CSC = TermByDocumentMatrix.tocsc()
    column_norms = linalg.norm(TermByDocumentMatrix_CSC, axis=0)
    normalisedTermByDocumentMatrix = TermByDocumentMatrix_CSC/column_norms
    print("=======================DONE=======================")
    return normalisedTermByDocumentMatrix


def initialize_svd(search_matrix, k):

    print("SVD calculation started.")
    svd = TruncatedSVD(n_components=k)
    svd.fit(search_matrix)

    us_matrix = svd.transform(search_matrix)
    v_t_matrix = np.array(svd.components_)
    print("SVD calculation finished.")

    with open("Databases/us.npz", 'wb') as file:
        np.save(file, us_matrix)
    with open("Databases/v_t.npz", 'wb') as file:
        np.save(file, v_t_matrix)
    print("SVD matrices saved succesfully.")


def calculateCosine(Query: sparse.csr_matrix, TBDMatrix: sparse.csr_matrix, Ej: sparse.csr_matrix):
    return (Query.transpose() @ (TBDMatrix @ Ej.transpose()))/(linalg.norm(Query) * linalg.norm(TBDMatrix @ Ej.transpose()))


def PrzeglądarkaMain(TermByDocumentMatrix, InputString: str, SVD=False, OutputSize=10) -> list:
    # this slow and bad
    # def handleQuery(Query: sparse.csr_matrix):
    #     nonlocal TermByDocumentMatrix, URLs, IndexedURLs
    #     QueryResult = {}
    #     for j in range(len(URLs)):
    #         QueryResult[IndexedURLs[str(j)]] = calculateCosine(
    #             Query, TermByDocumentMatrix, TermByDocumentMatrix[j:j+1, :])
    #     return QueryResult

    def handleQuery2(Query: sparse.csr_matrix):
        nonlocal TermByDocumentMatrix, IndexedURLs
        normalisedQuery = Query/linalg.norm(Query)
        Cosines = normalisedQuery.transpose() @ TermByDocumentMatrix
        QueryResult = {}
        for j in range(Cosines.shape[1]):
            QueryResult[IndexedURLs[str(j)]] = Cosines[0, j]
        return QueryResult

    def handleQuerySVD(Query: sparse.csr_matrix):
        nonlocal TermByDocumentMatrix, IndexedURLs
        us_matrix = np.load("Databases/us.npz")
        v_t_matrix = np.load("Databases/v_t.npz")
        Query /= linalg.norm(Query)
        transposedQuery = np.transpose(Query.toarray())
        Cosines = (transposedQuery @ us_matrix) @ v_t_matrix
        QueryResult = {}
        for j in range(Cosines.shape[1]):
            QueryResult[IndexedURLs[str(j)]] = Cosines[0, j]
        return QueryResult

    IndexedURLs = load_dict_from_file("Databases/IndexedURLs.json")
    if InputString == "":
        return []

    Query = BOWtoVector(TextToBOW(InputString))

    if SVD == True:
        print("USING SVD")
        QueryResult = handleQuerySVD(Query)
    else:
        print("USING NOT SVD")
        QueryResult = handleQuery2(Query)
    sortedQueryResult = sorted(
        QueryResult.items(), key=lambda x: x[1], reverse=True)
    result_list = sortedQueryResult[:OutputSize]

    return result_list


if __name__ == '__main__':
    initialize_svd(CreateTermByDocumentMatrix(), 100)
