import math
epsilon = 1e-10

def inputValues():
    quantity_x = int(input("Количество х "))
    quantity_y = int(input("Количество y "))
    XY = []
    for i in range(quantity_x * quantity_y):
        XY.append(float(input()))

    return [quantity_x, quantity_y, XY]


def findX(ansXY, quant_x, quant_y):
    X = []
    summ = 0
    curr_ind = 0
    for i in range(quant_x):

        for j in range(quant_y):
            summ = summ + ansXY[curr_ind]
            curr_ind += 1

        X.append(summ)
        summ = 0

    print("X = ", X)
    return X


def findY(ansXY, quant_x, quant_y):
    Y = []
    summ = 0
    for i in range(quant_y):
        currX = 0
        for j in range(quant_x):
            summ = summ + ansXY[i + currX]
            currX = currX + quant_y
        Y.append(summ)
        summ = 0

    print("Y = ", Y)
    return Y


def multiplication_of_probabilities_and_checkOnIndependence(X, Y, XY):
    resultList = []

    for i in range(len(X)):
        for j in range(len(Y)):
            resultList.append(X[i] * Y[j])

    are_close = all(math.isclose(x, y, rel_tol=epsilon) for x, y in zip(resultList, XY))
    if are_close:
        resultList = XY

    return [resultList, are_close]


def calc_conditional_probabilities(X, Y, XY, isIndependence):
    pXiYj = []
    pYjXi = []
    if isIndependence:
        pXiYj = X
        pYjXi = Y
    else:
        curr = 0
        for i in range(len(X)):
            for j in range(len(Y)):
                pXiYj.append(XY[i+curr + j] / Y[j])
            curr = curr + len(Y) - 1

        for i in range(len(Y)):
            currX = 0
            for j in range(len(X)):
                pYjXi.append(XY[i + currX] / X[j])
                currX = currX + len(Y)
    return [pXiYj, pYjXi]


def calc_conditional_entropy(A):
    summ = 0
    for i in range(len(A)):
        summ = summ + A[i] * math.log(A[i], 2)
    return summ * (-1)


def joint_entropy(HX, HY, isIndependence, XY):
    if isIndependence:
        return HX + HY
    else:
        summ = 0
        for i in range(len(XY)):
            summ = summ + XY[i] * math.log(XY[i], 2)
        return summ * (-1)


def calc_total_conditional_entropy(HX, HY, isIndependence, X, Y, pXiYj, pYjXi):
    if isIndependence:
        return [HX, HY]
    else:
        return [solution_TCE(X, Y, pXiYj, "Hy", "X"), solution_TCE(Y, X, pYjXi, "Hx", "Y")]


def solution_TCE(A, B, pAkBn, str1, str2):
    HbA = 0
    for i in range(len(B)):
        HbnA = 0
        curr = 0
        for j in range(len(A)):
            HbnA = HbnA + pAkBn[i + curr] * math.log(pAkBn[i + curr], 2)
            curr = curr + len(B)
        print(str1 + str(i + 1), str2, "= ", HbnA * (-1))
        HbA = HbA + B[i] * HbnA * (-1)

    return HbA


inputValuesList = inputValues()
quantity_x = inputValuesList[0]
quantity_y = inputValuesList[1]

XY = inputValuesList[2]
X = findX(XY, quantity_x, quantity_y)
Y = findY(XY, quantity_x, quantity_y)

checkIndepends = multiplication_of_probabilities_and_checkOnIndependence(X, Y, XY)
print("Произведение = ", checkIndepends[0])
print("Независим = ", checkIndepends[1])

conditional_probabilitiesXAndY = calc_conditional_probabilities(X, Y, XY, checkIndepends[1])
pXiYj = conditional_probabilitiesXAndY[0]
pYjXi = conditional_probabilitiesXAndY[1]
print("pXiYj = ", pXiYj)
print("pYjXi = ", pYjXi)

HX = calc_conditional_entropy(X)
HY = calc_conditional_entropy(Y)
print("H(X) = ", HX)
print("H(Y) = ", HY)

HyXAndHxY = calc_total_conditional_entropy(HX, HY, checkIndepends[1], X, Y, pXiYj, pYjXi)
HyX = HyXAndHxY[0]
HxY = HyXAndHxY[1]
print("HyX = ", HyX)
print("HxY = ", HxY)


print("H(XY) = ", joint_entropy(HX, HY, checkIndepends[1], XY))



