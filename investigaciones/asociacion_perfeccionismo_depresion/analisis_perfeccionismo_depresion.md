Asociación entre perfeccionismo y síntomas de depresión en estudiantes universitarios durante el aislamiento por COVID-19
================

## 1. Importamos librerías y cargamos los datos.

``` r
options(scipen=999)
library(readxl)
library(dplyr)

base_datos <- read_excel("perfeccionismo_depresion.xlsx")
```

Seleccionamos las variables de interés para el análisis y observamos la estructura de las columnas:

``` r
data <- base_datos %>%
    transmute(edad, genero, progreso,
              IF_D = IF1 + IF4 + IF6 + IF10 + IF13 + IF15,
              IF_IE = IF2 + IF5 + IF7 + IF11 + IF16,
              IF_ID = IF3 + IF9 + IF12,
              IF_L = IF8 + IF14 + IF17,
              APSR_D = APSR3 + APSR6 + APSR9 + APSR11 + APSR13 + APSR15 + APSR16 + APSR17 + APSR19 + APSR20 + APSR21 + APSR23,
              APSR_AE = APSR1 + APSR5 + APSR8 + APSR12 + APSR14 + APSR18 + APSR22,
              APSR_O = APSR2 + APSR4 + APSR7 + APSR10,
              BDI = BDI1 + BDI2 + BDI3 + BDI4 + BDI5 + BDI6 + BDI7 + BDI8 + BDI9 + BDI10 + BDI11 + BDI12 + BDI13 + BDI14 + BDI15 + BDI16 + BDI17 + BDI18 + BDI19 + BDI20 + BDI21)

str(data)
```

    ## tibble [376 x 11] (S3: tbl_df/tbl/data.frame)
    ##  $ edad    : num [1:376] 22 25 29 30 27 26 23 24 22 20 ...
    ##  $ genero  : num [1:376] 0 1 0 0 0 0 0 0 0 0 ...
    ##  $ progreso: num [1:376] 1 0 2 1 2 2 2 0 1 0 ...
    ##  $ IF_D    : num [1:376] 24 22 24 10 18 14 19 17 10 25 ...
    ##  $ IF_IE   : num [1:376] 13 17 12 7 6 13 12 13 5 24 ...
    ##  $ IF_ID   : num [1:376] 3 9 9 5 5 7 12 7 3 11 ...
    ##  $ IF_L    : num [1:376] 8 10 14 4 9 8 11 6 7 13 ...
    ##  $ APSR_D  : num [1:376] 42 52 68 34 56 49 32 51 22 54 ...
    ##  $ APSR_AE : num [1:376] 40 33 39 35 44 38 46 29 44 41 ...
    ##  $ APSR_O  : num [1:376] 25 18 23 23 24 22 21 25 23 24 ...
    ##  $ BDI     : num [1:376] 13 11 14 7 19 13 19 9 7 35 ...

Como todas las variables aparecen como númericas, cambiamos el tipo de dato de aquellas que deberían ser categóricas.

``` r
data$genero <- factor(data$genero,
                      levels = c(0, 1),
                      labels = c("female", "male"))
data$progreso <- factor(data$progreso,
                        levels = c(0, 1, 2),
                        labels = c("ingresante", "intermedio", "avanzado"))
```

## 2. Detección de Outliers

Eliminamos los outliers calculando la 'Distancia de Mahalanobis', 'Distancia de Cook' y 'Leverage'.

``` r
# Defino mi modelo lineal (incluyendo la interacción)
modelo = lm(BDI ~  edad + genero + progreso + IF_D + IF_IE + IF_ID + IF_L + APSR_D + APSR_AE + APSR_O + APSR_D * IF_IE, data)

# Creamos otro dataframe sin las variables categóricas
elimoutliers <- data %>% 
    dplyr::select(BDI, edad, IF_D, IF_IE, IF_ID, IF_L, APSR_D, APSR_AE, APSR_O)
```

``` r
### Mahalanobis
mahal = mahalanobis(elimoutliers, colMeans(elimoutliers), cov(elimoutliers))
cutoff = qchisq(1-.001, ncol(elimoutliers))
badmahal = as.numeric(mahal > cutoff)
table(badmahal)
```

    ## badmahal
    ##   0   1 
    ## 375   1

``` r
### Leverage
k= 10 # numero de variables independientes (predictoras) en el modelo
leverage = hatvalues(modelo)
cutleverage = (2*k+2) / nrow(data)
badleverage = as.numeric(leverage > cutleverage)
table(badleverage)
```

    ## badleverage
    ##   0   1 
    ## 348  28

``` r
### Cooks
cooks = cooks.distance(modelo)
cutcooks = 4 /(nrow(elimoutliers) - k - 1)
badcooks = as.numeric(cooks > cutcooks)
table(badcooks)
```

    ## badcooks
    ##   0   1 
    ## 352  24

``` r
totalout = badmahal + badleverage + badcooks
table(totalout)
```

    ## totalout
    ##   0   1   2 
    ## 330  39   7

7 sujetos se consideraron valores atípicos por al menos dos de los indicadores, por lo tanto fueron excluidos del análisis.

## 3. Regresión Lineal Jerárquica

Se realizó un análisis de regresión lineal jerárquica para determinar cómo cada una de las variables medidas predicen los síntomas depresivos en estudiantes universitarios en condiciones de aislamiento social. El primer paso de la regresión jerárquica incluyó el progreso académico y las variables demográficas: edad y género. En el paso 2, se agregaron las subescalas de la IF y APSR.

#### Paso 1:

``` r
modelo_1 = lm(BDI ~ genero + edad + progreso,  data)
summary(modelo_1)
```

    ## 
    ## Call:
    ## lm(formula = BDI ~ genero + edad + progreso, data = data)
    ## 
    ## Residuals:
    ##      Min       1Q   Median       3Q      Max 
    ## -17.7306  -6.4076  -0.7778   4.6693  29.2991 
    ## 
    ## Coefficients:
    ##                    Estimate Std. Error t value            Pr(>|t|)    
    ## (Intercept)         26.5767     3.1851   8.344 0.00000000000000151 ***
    ## generomale          -1.8040     1.6738  -1.078              0.2818    
    ## edad                -0.2308     0.1357  -1.700              0.0899 .  
    ## progresointermedio  -5.1835     1.1240  -4.612 0.00000553689821672 ***
    ## progresoavanzado    -7.8615     1.4285  -5.503 0.00000007045975554 ***
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 8.77 on 364 degrees of freedom
    ## Multiple R-squared:  0.1166, Adjusted R-squared:  0.1069 
    ## F-statistic: 12.01 on 4 and 364 DF,  p-value: 0.000000003555

En el paso 1, el modelo explicó el 11% de la varianza (F(4, 364) = 12.01, p &lt; 0.001). El progreso académico fue el único predictor significativo del BDI. Las betas negativas indican una reducción de 5.184 puntos en la puntuación del BDI para los estudiantes intermedios y una reducción de 7.862 para los avanzados, en relación con los principiantes.

#### Paso 2:

``` r
modelo_2 = lm(BDI ~ genero + edad + progreso + IF_D + IF_IE + IF_ID + IF_L + APSR_D + APSR_AE + APSR_O, data)
summary(modelo_2)
```

    ## 
    ## Call:
    ## lm(formula = BDI ~ genero + edad + progreso + IF_D + IF_IE + 
    ##     IF_ID + IF_L + APSR_D + APSR_AE + APSR_O, data = data)
    ## 
    ## Residuals:
    ##      Min       1Q   Median       3Q      Max 
    ## -18.0190  -4.5265  -0.6477   4.0895  24.2392 
    ## 
    ## Coefficients:
    ##                    Estimate Std. Error t value             Pr(>|t|)    
    ## (Intercept)        16.26113    4.35386   3.735             0.000219 ***
    ## generomale         -2.06604    1.40926  -1.466             0.143517    
    ## edad               -0.22744    0.11460  -1.985             0.047943 *  
    ## progresointermedio -3.04357    0.94490  -3.221             0.001395 ** 
    ## progresoavanzado   -3.89210    1.24195  -3.134             0.001868 ** 
    ## IF_D               -0.19649    0.09799  -2.005             0.045695 *  
    ## IF_IE               0.40742    0.09133   4.461             0.000011 ***
    ## IF_ID               0.04070    0.17832   0.228             0.819599    
    ## IF_L                0.28897    0.17923   1.612             0.107777    
    ## APSR_D              0.25285    0.02687   9.410 < 0.0000000000000002 ***
    ## APSR_AE            -0.19725    0.07525  -2.621             0.009133 ** 
    ## APSR_O             -0.10601    0.08900  -1.191             0.234401    
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
    ## 
    ## Residual standard error: 7.208 on 357 degrees of freedom
    ## Multiple R-squared:  0.4148, Adjusted R-squared:  0.3968 
    ## F-statistic: 23.01 on 11 and 357 DF,  p-value: < 0.00000000000000022

Cuando se agregan las variables restantes, el progreso académico siguió siendo significativo y la edad también se volvió significativa. El paso 2 agregó un 29,8% adicional de varianza explicada. Dos subescalas de la IF y dos subescalas de la APS-R resultaron predictores significativos del BDI. Como se esperaba, APSR-D e IF-IE predijeron un aumento de los síntomas de depresión. Según las correlaciones parciales, APSR-D (pR<sup>2</sup> = 0.20) fue el predictor más importante de la depresión. IF-IE (pR<sup>2</sup> = 0.05) y el progreso académico (pR<sup>2</sup>s = 0.03) también fueron predictores relevantes. La edad, APSR-AE e IF-D hicieron contribuciones menores a la varianza explicada (pR<sup>2</sup>s &lt; 0.02).

*La correlaciones parciales se calcularon siguiendo la fórmula:* <br> *t-value<sup>2</sup> / t-value<sup>2</sup> + DFresidual*

Un ANOVA para comparar el modelo 1 y el modelo 2 determinó que el aumento en R<sup>2</sup> es estadísticamente significativo (F(7, 357) = 25.993, p &lt; 0.001).

``` r
anova(modelo_1, modelo_2)
```

    ## Analysis of Variance Table
    ## 
    ## Model 1: BDI ~ genero + edad + progreso
    ## Model 2: BDI ~ genero + edad + progreso + IF_D + IF_IE + IF_ID + IF_L + 
    ##     APSR_D + APSR_AE + APSR_O
    ##   Res.Df   RSS Df Sum of Sq      F                Pr(>F)    
    ## 1    364 27998                                              
    ## 2    357 18546  7    9452.1 25.993 < 0.00000000000000022 ***
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

El modelo que incluyó la interacción entre APSR-D e IF-IE mostró una pequeña mejora significativa en la varianza explicada del BDI (pR<sup>2</sup> = 0.422, ΔpR<sup>2</sup> = 0.007, F(1, 356) = 4.417, p &lt; 0.04)

## 4. Análisis de Correlación Canónica

Este análisis se utiliza para estudiar la correlación entre dos conjuntos de variables. En este caso, el primer conjunto de variables lo conformaron todos los predictores significativos identificados en el análisis de regresión: APSR-D, APSR-AE, IF-IE, IF-D, Edad y Progreso Académico. El segundo conjunto de variables estuvo compuesto por los 21 ítems del BDI por separado.

``` r
library(CCA)
library(CCP)

# Definimos otro dataframe con las variables del primer y segundo conjunto
data_cca <- base_datos %>%
    transmute(edad, genero, progreso,
              IF_D = IF1 + IF4 + IF6 + IF10 + IF13 + IF15,
              IF_IE = IF2 + IF5 + IF7 + IF11 + IF16,
              IF_ID = IF3 + IF9 + IF12,
              IF_L = IF8 + IF14 + IF17,
              APSR_D = APSR3 + APSR6 + APSR9 + APSR11 + APSR13 + APSR15 + APSR16 + APSR17 + APSR19 + APSR20 + APSR21 + APSR23,
              APSR_AE = APSR1 + APSR5 + APSR8 + APSR12 + APSR14 + APSR18 + APSR22,
              APSR_O = APSR2 + APSR4 + APSR7 + APSR10,
              BDI1, BDI2, BDI3, BDI4, BDI5, BDI6, BDI7, BDI8, BDI9, BDI10, BDI11, BDI12, BDI13,
              BDI14, BDI15, BDI16, BDI17, BDI18, BDI19, BDI20, BDI21)

data_cca <- subset(data_cca, totalout < 2)
```

``` r
#Definimos los conjuntos de variables
VIs <- data_cca %>%
    transmute(edad, progreso, IF_IE, IF_D, APSR_D, APSR_AE)

VDs <- data_cca[, 11:31]
```

``` r
#Correlación Canónica
cc1 <- cc(VIs, VDs)
cc1$cor
```

    ## [1] 0.7205864 0.4181353 0.3303552 0.3079222 0.2555320 0.2191021

``` r
# tests of canonical dimensions
rho <- cc1$cor

n <- dim(VIs)[1]
p <- length(VIs)
q <- length(VDs)

p.asym(rho, n, p, q, tstat = "Wilks")
```

    ## Wilks' Lambda, using F-approximation (Rao's F):
    ##               stat   approx df1      df2         p.value
    ## 1 to 6:  0.2846563 3.822666 126 1990.807 0.0000000000000
    ## 2 to 6:  0.5921023 1.902974 100 1677.998 0.0000004518261
    ## 3 to 6:  0.7175581 1.570162  76 1357.424 0.0016133183422
    ## 4 to 6:  0.8054618 1.434721  54 1028.780 0.0233802364194
    ## 5 to 6:  0.8898322 1.223167  34  692.000 0.1815133219252
    ## 6 to 6:  0.9519943 1.093625  16  347.000 0.3593949024659

Se utilizó la prueba Lambda de Wilks para explorar la significancia de las correlaciones canónicas. La combinación de las seis soluciones canónicas resultó significativa (F(126, 1990) = 3.82; p &lt; 0.001), incluso cuando se excluyeron tres correlaciones (F(54, 1028) = 1.434721; p &lt; 0.03). Las últimas dos combinaciones no fueron significativas (ps &gt; 0.18).
La primer (RC = 0.72) y segunda (RC = 0.41) correlación canónica explicaron el 68% de la varianza. Las restantes están por debajo de 0.35 y, por lo tanto, no fueron interpretadas.

``` r
# Cargas de VIs para la primer correlación canónica
cc2 <- comput(VIs, VDs, cc1)
sort(cc2$corr.X.xscores[,1])
```

    ##     APSR_D      IF_IE       IF_D    APSR_AE       edad   progreso 
    ## -0.9128762 -0.5079531 -0.2521423  0.1410888  0.1737083  0.4379993

``` r
# Cargas de VIs para la segunda correlación canónica
sort(cc2$corr.X.xscores[,2])
```

    ##      IF_IE       IF_D    APSR_AE     APSR_D   progreso       edad 
    ## -0.6560822 -0.4919132 -0.2254783  0.1964183  0.4369227  0.5753022

APSR-D fue la carga principal para la primer correlación (-0.91) pero mostró una contribución muy pequeña en la segunda correlación canónica (0.19). La carga de IF-IE en la primera correlación también fue relevante (-0.51), e incluso fue más importante para la segunda (-0.65). IF-D también cargó más fuerte en la segunda (-0.49) que en la primer correlación (-0.25). El progreso académico mostró una carga similar para ambas correlaciones (0.43). APSR-AE no fue relevante en ningna de las correlaciones, y la Edad solo fue relevante en la segunda correlación (0.57), cargando en dirección opuesta a las subescalas de la IF.

``` r
# Cargas de VDs para la primer correlación canónica
sort(cc2$corr.Y.yscores[,1])
```

    ##       BDI3       BDI5      BDI14       BDI7       BDI8       BDI1      BDI19 
    ## -0.8240179 -0.6991292 -0.6397206 -0.6381171 -0.5528265 -0.5428419 -0.5361756 
    ##      BDI13       BDI9       BDI2       BDI6      BDI15      BDI10      BDI20 
    ## -0.5188485 -0.5117504 -0.4887134 -0.4794259 -0.4342020 -0.4220883 -0.4146866 
    ##      BDI12      BDI18       BDI4      BDI16      BDI17      BDI11      BDI21 
    ## -0.4056969 -0.3693004 -0.3477587 -0.2716799 -0.2578925 -0.2318397 -0.1615048

``` r
# Cargas de VDs para la segunda correlación canónica
sort(cc2$corr.Y.yscores[,2])
```

    ##       BDI12       BDI10       BDI17        BDI1        BDI6        BDI9 
    ## -0.43613472 -0.40034206 -0.37122382 -0.35227709 -0.33572677 -0.31179173 
    ##       BDI11        BDI8        BDI7       BDI20        BDI4       BDI19 
    ## -0.28661680 -0.26002448 -0.20547308 -0.20337537 -0.20199021 -0.13668709 
    ##       BDI14       BDI15        BDI5       BDI16       BDI13       BDI21 
    ## -0.13614795 -0.04896191 -0.03907128 -0.01214681 -0.01032184  0.01195220 
    ##       BDI18        BDI2        BDI3 
    ##  0.03321331  0.06554743  0.35499818

Con respecto al BDI, los ítems 3 (Fracaso), 5 (Sentimientos de culpa), 14 (Desvalorización), 7 (Disconformidad a uno mismo) y 8 (Autocrítica) fueron las principales cargas de la primera correlación canónica. Los ítems 12 (Pérdida de interés), 10 (Llanto), 17 (Irritabilidad) y 1 (Tristeza) fueron las principales cargas para la segunda.
