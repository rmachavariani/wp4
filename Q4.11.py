def lug_thermalstress(alphaA, alphaB, Eb, phi):  # phi to be imported from Q4.10
    sigmamax = 5.44 * (alphaA - alphaB) * Eb * phi
    sigmamin = -46.63 * (alphaA - alphaB) * Eb * phi
    return sigmamax, sigmamin
