# Nome do arquivo de saída único
arquivo_saida = "BLOCAO_APDL.txt"

# Código ANSYS com placeholders
codigo_base = """
! ----------------------------
! INICIO DA VARIACAO
! Localizacao do Defeito = {Localizacao_do_defeito}%
! Profundidade Do Defeito = {Profundidade_do_defeito}%
! Modo de Vibracao = {MODO_DE_VIBRACAO}
! Espessura do defeito = {Espessura_do_defeito}
! ----------------------------

/CLEAR,START
/PREP7

*SET, L, 0.81
*SET, B, 0.0254
*SET, H, B/2

ET, 1, SOLID185

*SET,RHO,7851
*SET,E,193E9
*SET,U,0.3
MP,DENS,1,RHO
MP,EX,1,E
MP,PRXY,1,U

BLOCK, 0, L*{X}, 0, H, 0, B
BLOCK, L*{X}, L*{X}+{Espessura_do_defeito}, 0, H*{Y}, 0, B
BLOCK, L*{X}+{Espessura_do_defeito}, L, 0, H, 0, B

VGLUE,ALL

VSEL, ALL
LESIZE, ALL, 0.004
VSWEEP, ALL

FLST,2,1,4,ORDE,1
FITEM,2,34
!*
/GO
DL,P51X, ,UY,
FLST,2,1,4,ORDE,1
FITEM,2,34
!*
/GO
DL,P51X, ,UZ,
FLST,2,1,4,ORDE,1
FITEM,2,9
!*
/GO
DL,P51X, ,ALL,

ALLSEL,ALL
NSEL,S,LOC,Y,0
NSEL,R,LOC,Z,B
D,ALL,UZ,0
ALLSEL,ALL

/SOL
ANTYPE,2
MODOPT,LANB,6
EQSLV,SPAR
MXPAND,0, , ,0
LUMPM,0
PSTRES,0
MODOPT,LANB,6,0,1000, ,OFF
SOLVE

/POST1
SET, 1, {MODO_DE_VIBRACAO}

PATH, MYPATH, 2, , 100
PPATH, 1, , 0, 0, 0
PPATH, 2, , L, 0, 0

PDEF, UY_ON_PATH, U, Y, AVG

*DIM,DESL_NODE_PATH_{i},ARRAY,100,1,1
PAGET,DESL_NODE_PATH,TABL

*CREATE,MACRO_GRAVA_PATH,txt
*CFOPEN,'{pasta}{nome_arquivo_saida}',txt
*CFWRITE,UY_PATH
*VWRITE,DESL_NODE_PATH(1,5)
(1F11.9)
*CFCLOS
*END
/INPUT,MACRO_GRAVA_PATH,txt

! ----------------------------
! FIM DA VARIACAO
! Localizacao do Defeito = {Localizacao_do_defeito}%
! Profundidade Do Defeito = {Profundidade_do_defeito}%
! Modo de Vibracao = {MODO_DE_VIBRACAO}
! Espessura do defeito = {Espessura_do_defeito}
! ----------------------------
"""

# Abre o arquivo de saída final
with open(arquivo_saida, 'w') as f:

    MODO_DE_VIBRACAO = 1
    pasta = '\\Users\\GVA\\Desktop\\dico\\'

    # ===== Caso sem defeito =====
    X = 1.0
    Y = 1.0
    Espessura_do_defeito = 0
    Localizacao_do_defeito = 0
    Profundidade_do_defeito = 0
    i = 0
    j = 0
    nome_arquivo_saida = f"sem_defeito"

    codigo_sem_defeito = codigo_base.format(
        i=i, X=X, Y=Y, j=j,
        MODO_DE_VIBRACAO=MODO_DE_VIBRACAO,
        Localizacao_do_defeito=Localizacao_do_defeito,
        Profundidade_do_defeito=Profundidade_do_defeito,
        Espessura_do_defeito=Espessura_do_defeito,
        pasta = pasta,
        nome_arquivo_saida=nome_arquivo_saida
    )
    f.write(codigo_sem_defeito)

    # ===== Casos com defeito =====
    for k in range(1, 5):
        Espessura_do_defeito = 0.001 * k
        for i in range(10, 100):
            X = 0.01 * i
            Localizacao_do_defeito = round(X * 100, 1)
            for j in range(50, 99):
                Y = 0.01 * j
                Profundidade_do_defeito = round((1 - Y) * 100, 1)

                nome_arquivo_saida = f"VETOR_MODAL_{MODO_DE_VIBRACAO}_{Localizacao_do_defeito}_{Profundidade_do_defeito}_{Espessura_do_defeito}"
                codigo_var = codigo_base.format(
                    i=i, X=round(X, 2), Y=round(Y, 2), j=j,
                    MODO_DE_VIBRACAO=MODO_DE_VIBRACAO,
                    Localizacao_do_defeito=Localizacao_do_defeito,
                    Profundidade_do_defeito=Profundidade_do_defeito,
                    Espessura_do_defeito=Espessura_do_defeito,
                    pasta = pasta,
                    nome_arquivo_saida=nome_arquivo_saida
                )
                f.write(codigo_var)

print(f"Arquivo com todos os casos salvo em: {arquivo_saida}")
